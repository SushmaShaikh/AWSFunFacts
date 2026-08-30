import boto3
import random
import json


# DynamoDB connection
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("CloudFacts")


# Bedrock client
bedrock = boto3.client("bedrock-runtime")

# Amazon Nova Micro — cheapest, text-only Nova model, good fit for short witty rewrites
NOVA_MODEL_ID = "amazon.nova-micro-v1:0"


def lambda_handler(event, context):
    # Fetch all facts from DynamoDB
    response = table.scan()
    items = response.get("Items", [])
    if not items:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"fact": "No facts available in DynamoDB."})
        }

    fact = random.choice(items)["FactText"]

    prompt = (
        f"Take this cloud computing fact and make it fun and engaging in 1-2 "
        f"sentences maximum. Keep it short and witty: {fact}"
    )

    # Nova uses the same "messages" shape as Claude, but each content block
    # is a list of {"text": ...} objects instead of a raw string.
    messages = [
        {
            "role": "user",
            "content": [{"text": prompt}]
        }
    ]

    # Nova's request body: no "anthropic_version"/top-level max_tokens — those
    # live under "inferenceConfig" instead. "schemaVersion" is required.
    body = {
        "schemaVersion": "messages-v1",
        "messages": messages,
        "inferenceConfig": {
            "maxTokens": 100,
            "temperature": 0.7,
            "topP": 0.9
        }
    }

    try:
        # Call Amazon Nova Micro on Bedrock
        resp = bedrock.invoke_model(
            modelId=NOVA_MODEL_ID,
            body=json.dumps(body),
            accept="application/json",
            contentType="application/json"
        )

        # Parse response
        result = json.loads(resp["body"].read())
        witty_fact = ""

        # Nova response shape: result["output"]["message"]["content"] is a
        # list of {"text": ...} blocks (mirrors the request format).
        content_blocks = (
            result.get("output", {})
            .get("message", {})
            .get("content", [])
        )
        for block in content_blocks:
            if "text" in block:
                witty_fact = block["text"].strip()
                break

        # Fallback if empty or too long
        if not witty_fact or len(witty_fact) > 300:
            witty_fact = fact

    except Exception as e:
        print(f"Bedrock error: {e}")
        witty_fact = fact

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps({"fact": witty_fact})
    }
