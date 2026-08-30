# DynamoDB table: CloudFacts

| Attribute  | Type   | Notes                          |
|------------|--------|---------------------------------|
| `FactId`   | String | Partition key                  |
| `FactText` | String | The raw cloud-computing fact   |

Billing mode: on-demand.

Example item:

```json
{
  "FactId": { "S": "001" },
  "FactText": { "S": "S3 stores objects, not files — there's no real folder structure, just key prefixes." }
}
