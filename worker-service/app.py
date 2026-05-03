import json
import boto3
import requests
from bs4 import BeautifulSoup
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'jobs-table')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # EventBridge sends data inside "detail"
        detail = event.get("detail", {})
        job_id = detail.get("job_id")
        url = detail.get("url")

        if not job_id or not url:
            print("Invalid event")
            return

        print(f"Processing job: {job_id}")

        #fetch webpage
        response = requests.get(url, timeout=5)
        html = response.text

        #parse HTML
        soup = BeautifulSoup(html, "html.parser")

        #extract title
        title = soup.title.string if soup.title else "No Title"

        #Count words
        text = soup.get_text()
        word_count = len(text.split())

        #Update the DynamoDB
        table.update_item(
            Key={"job_id": job_id},
            UpdateExpression="SET #s = :s, #r = :r",
            ExpressionAttributeNames={
                "#s": "status",
                "#r": "result"
            },
            ExpressionAttributeValues={
                ":s": "COMPLETED",
                ":r": {
                    "title": title,
                    "word_count": word_count
                }
            }
        )

        print(f"Job {job_id} completed")

    except Exception as e:
        print(f"Error: {str(e)}")

        #mark job as failed
        if job_id:
            table.update_item(
                Key={"job_id": job_id},
                UpdateExpression="SET #s = :s",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={
                    ":s": "FAILED"
                }
            )