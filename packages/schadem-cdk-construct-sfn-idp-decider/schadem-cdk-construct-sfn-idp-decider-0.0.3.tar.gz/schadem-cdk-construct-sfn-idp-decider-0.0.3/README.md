# Context

Construct as part of the IDP processing suite, usually ran at the beginning.
Gets number of pages, validates that the mime type of the file is supported.
Will serialize to a manifest and therefore requires that format.

https://pypi.org/project/schadem-tidp-manifest/

# Input

A manifest file as event source for a Lambda function.

# Output

adds:

mime
numberOfPages

```javascript
{
  "manifest": {
    "S3Path": "s3://my-stack-dev-documentbucket04c71448-19ew04s4uhy8t/uploads"
  },
  "mime": "application/pdf",
  "numberOfPages": 12
}
```
