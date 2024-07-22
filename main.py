import os
import json
import boto3
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, jsonify

# Initialize the Slack client
slack_token = os.getenv('SLACK_BOT_TOKEN')
client = WebClient(token=slack_token)

# Initialize the AWS client
aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
region_name = os.getenv('AWS_REGION', 'us-west-2')

ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region_name
)

# Function to list EC2 instances
def list_ec2_instances():
    response = ec2_client.describe_instances()
    instances = response['Reservations']
    instance_info = []
    for reservation in instances:
        for instance in reservation['Instances']:
            instance_info.append({
                'InstanceId': instance['InstanceId'],
                'InstanceType': instance['InstanceType'],
                'State': instance['State']['Name'],
                'PublicIpAddress': instance.get('PublicIpAddress', 'N/A')
            })
    return instance_info

# Function to restart a specified EC2 instance
def restart_ec2_instance(instance_id):
    try:
        ec2_client.reboot_instances(InstanceIds=[instance_id])
        return f"Instance {instance_id} is being restarted."
    except Exception as e:
        return f"Error restarting instance {instance_id}: {str(e)}"

# Function to handle Slack events
def handle_slack_event(event_data):
    event = event_data['event']
    if 'bot_id' not in event:
        text = event.get('text')
        channel = event['channel']

        if text and 'list ec2 instances' in text.lower():
            instances = list_ec2_instances()
            message = "EC2 Instances:\n"
            for instance in instances:
                message += f"ID: {instance['InstanceId']}, Type: {instance['InstanceType']}, State: {instance['State']}, IP: {instance['PublicIpAddress']}\n"
            try:
                response = client.chat_postMessage(channel=channel, text=message)
            except SlackApiError as e:
                print(f"Error posting message: {e.response['error']}")

        elif text and text.lower().startswith('restart ec2 instance'):
            instance_id = text.split()[-1]
            message = restart_ec2_instance(instance_id)
            try:
                response = client.chat_postMessage(channel=channel, text=message)
            except SlackApiError as e:
                print(f"Error posting message: {e.response['error']}")

# Lambda function handler (for deployment in AWS Lambda)
def lambda_handler(event, context):
    event_data = json.loads(event['body'])
    if 'event' in event_data:
        handle_slack_event(event_data)
    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }

if __name__ == "__main__":
    # This is for local testing. When running locally, set up a way to receive and handle events.
    # For example, using Flask to create a local server to receive events from Slack.
    app = Flask(__name__)

    @app.route('/slack/events', methods=['POST'])
    def slack_events():
        event_data = request.get_json()
        handle_slack_event(event_data)
        return jsonify({'status': 'OK'})

    app.run(port=3000)
