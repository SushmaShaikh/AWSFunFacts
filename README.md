# Fun Fact Generator

A serverless app that pulls a random cloud-computing fact from DynamoDB and
rewrites it in a witty voice using **Amazon Bedrock (Nova Micro)** served
through API Gateway to a frontend hosted on AWS Amplify.

## Architecture

 <img width="1983" height="2412" alt="funfact_architecture" src="https://github.com/user-attachments/assets/4d63def2-4264-4f62-8a2f-f26e7bb20e42" />

## Tech stack

- **AWS Amplify** — static frontend hosting
- **Amazon API Gateway** (HTTP API) — `GET /funfact`
- **AWS Lambda** — `backend/lambda_function.py`
- **Amazon DynamoDB** — `CloudFacts` table (schema in `infra/dynamodb-schema.md`)
- **Amazon Bedrock** — `amazon.nova-micro-v1:0` (Nova Micro)
- **IAM** — least-privilege execution role (`infra/iam-policy.json`)

## Repo structure

```
fun-fact-generator/
├── README.md
├── article.md
├── architecture-diagram.md
├── backend/
│   └── lambda_function.py
├── frontend/
├── infra/
│   ├── iam-policy.json
│   └── dynamodb-schema.md
└── screenshots/
```

## Setup

1. Create a DynamoDB table named `CloudFacts` (see `infra/dynamodb-schema.md`)
   and seed it with some facts.
2. Deploy `backend/lambda_function.py` as a Lambda function.
3. Attach the policy in `infra/iam-policy.json` to the Lambda's execution role
   (update the region/account if you scope it further).
4. Enable Amazon Nova Micro access in Bedrock for your region and deploy the
   Lambda behind an API Gateway HTTP API with a `GET /funfact` route.
5. Configure CORS on the API to allow your frontend's exact origin (no
   trailing slash).
6. Deploy the frontend to AWS Amplify, pointed at your API endpoint.

## Cost

Realistically **$0/month** for portfolio-level traffic — Nova Micro,
Lambda, DynamoDB, and Amplify all fall within AWS free-tier limits at this
scale. See `article.md` for the full breakdown.
