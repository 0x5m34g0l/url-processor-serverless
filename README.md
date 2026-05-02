# Cloud-Based URL Processing System

## Overview

This project is a serverless cloud application that processes user-submitted URLs asynchronously. Users submit a URL, which is stored and processed in the background. The system extracts useful information such as page title and word count and stores the result.

---

## Architecture

Client → API Gateway → API Lambda
→ DynamoDB → EventBridge → Worker Lambda → DynamoDB

---

## Services

### API Service (Lambda)

* Accepts user requests
* Generates job ID
* Stores job in DynamoDB
* Sends event to EventBridge

### Worker Service (Lambda)

* Triggered by EventBridge
* Fetches webpage
* Extracts title and word count
* Updates job result in DynamoDB

---

## API Endpoints

### POST /process-url

Request:

```json
{
  "url": "https://example.com"
}
```

Response:

```json
{
  "job_id": "generated-id"
}
```

---

### GET /job/{id}

Response:

```json
{
  "job_id": "...",
  "url": "...",
  "status": "COMPLETED",
  "result": {
    "title": "...",
    "word_count": 123
  }
}
```

---

## Technologies Used

* AWS Lambda
* API Gateway
* EventBridge
* DynamoDB
* Docker
* Terraform (infrastructure)
* GitHub Actions (CI/CD)

---

## Notes

* The system follows an event-driven serverless architecture
* Job processing is asynchronous
* Infrastructure is provisioned using Terraform
