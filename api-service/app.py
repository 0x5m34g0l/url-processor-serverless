import json
import boto3
import uuid
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'jobs-table')
table = dynamodb.Table(table_name)

eventbridge = boto3.client('events')

def lambda_handler(event, context):
    try:
        http_method = event.get("httpMethod")

        
        # POST url
        
        if http_method == "POST":
            body = json.loads(event.get("body", "{}"))
            url = body.get("url")

            if not url:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "URL is required"})
                }

            job_id = str(uuid.uuid4())

            # Save job in DynamoDB
            table.put_item(
                Item={
                    "job_id": job_id,
                    "url": url,
                    "status": "PENDING"
                }
            )

            # Send event to EventBridge
            eventbridge.put_events(
                Entries=[
                    {
                        "Source": "url.processor",
                        "DetailType": "ProcessURL",
                        "Detail": json.dumps({
                            "job_id": job_id,
                            "url": url
                        }),
                        "EventBusName": os.environ.get("EVENT_BUS_NAME", "default")
                    }
                ]
            )

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Job submitted",
                    "job_id": job_id
                })
            }

        
        # GET posted Job Result
        
        elif http_method == "GET":
            job_id = event.get("pathParameters", {}).get("id")

            if not job_id:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Job ID is required"})
                }

            response = table.get_item(Key={"job_id": job_id})
            item = response.get("Item")

            if not item:
                return {
                    "statusCode": 404,
                    "body": json.dumps({"error": "Job not found"})
                }

            return {
                "statusCode": 200,
                "body": json.dumps(item)
            }

        
        # Invalid Method message
        
        else:
            return {
                "statusCode": 405,
                "body": json.dumps({"error": "Method not allowed"})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
#i test the  CI/CD pipeline to see the workflow
