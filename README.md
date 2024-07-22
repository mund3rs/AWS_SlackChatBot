# AWS Slack Chatbot

A Slack chatbot that interacts with AWS services using Python. This bot can list EC2 instances and restart specified instances.

## Features

- List all EC2 instances
- Restart a specified EC2 instance

## Prerequisites

- Python 3.6+
- AWS account with EC2 instances
- Slack workspace with a created bot

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/aws-slack-chatbot.git
    cd aws-slack-chatbot
    ```

2. Install the required packages:
    ```sh
    pip install slack_sdk boto3 flask
    ```

3. Set up environment variables:
    ```sh
    export SLACK_BOT_TOKEN='your-slack-bot-token'
    export AWS_ACCESS_KEY='your-aws-access-key'
    export AWS_SECRET_KEY='your-aws
