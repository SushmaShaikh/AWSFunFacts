# Fun Fact Generator — Architecture

```mermaid
flowchart TD
    Browser["🖥️ Browser<br/>funfacts app"]
    Amplify["AWS Amplify<br/>Static Hosting"]
    APIGW["Amazon API Gateway<br/>HTTP API · GET /funfact"]
    Lambda["AWS Lambda<br/>fun-fact-generator"]
    DynamoDB[("Amazon DynamoDB<br/>CloudFacts table")]
    Bedrock["Amazon Bedrock<br/>Nova Micro"]

    Amplify -- "serves static site (once)" --> Browser
    Browser -- "GET /funfact (CORS)" --> APIGW
    APIGW -- "invoke" --> Lambda
    Lambda -- "JSON response" --> APIGW
    APIGW -- "200 OK { fact }" --> Browser
    Lambda -- "Scan(CloudFacts)" --> DynamoDB
    DynamoDB -- "random fact" --> Lambda
    Lambda -- "InvokeModel: amazon.nova-micro-v1:0" --> Bedrock
    Bedrock -- "witty rewrite" --> Lambda

    subgraph IAM["IAM execution role — dynamodb:Scan · bedrock:InvokeModel"]
        Lambda
        DynamoDB
        Bedrock
    end
```

**How it works:** the browser loads the app once from Amplify, then on each request calls API Gateway, which invokes Lambda. Lambda scans DynamoDB for a random fact, sends it to Amazon Bedrock's Nova Micro model to be rewritten, and returns the result — all outbound calls from Lambda authorized by its IAM execution role.

This renders natively on GitHub — drop this file into your repo, or paste the ` ```mermaid ` block directly into your README.md.
