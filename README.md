## Overview

This project is a Python-based implementation of a Language Model using OpenAI's GPT-3.5, designed to be used by a Telegram bot. The project consists of three main files and an environment variable configuration file (.env).

## Introduction

The Project is developed for HealthServe as part of AI in Humanity Module by Group 6 to assist in onboarding process and enhance employee's quality of service when serving customers 

Use Cases:
- ☑️ Chat with your documents using OpenAI's LLM Chatbot
- ☑️ CD to AWS BeanStalk
- ☑️ Telegram Bot integration
- ☐ (In progress) WhatsApp integration using Twillio
 - ☐ (In progress) Talk via voice notes to your documents using OpenAI's Voice to Text AI

## Files

1. **.env.template**
   Create a file named `.env` by copying this template and filling in the necessary values for the environment variables.

   * `OPENAI_API_KEY`: Your OpenAI API key for accessing the language model.
   * `TELEGRAM_BOT_TOKEN`: Your Telegram bot's API token.
   * `LANGCHAIN_API_KEY`: Your LangChain API key if applicable.
2. **model.py**

   * Main file for training the Language Model using OpenAI.
   * Used to interact with the trained model.

   To use this file, make sure to configure your environment variables as specified in the `.env` file.
3. **train.py**

   * Training script that can be executed using the command `python train.py`.
   * Used for training your specific Language Model with OpenAI's GPT-3.5.
4. **telegram_bot.py**

   * Main file to activate the Telegram bot connected to the trained Language Model.
   * Run the Telegram bot using the command `python telegram_bot.py`.

## Getting Started

1. Clone this repository to your local machine:
   ```
   git clone https://github.com/absolutelynoot/ready-serve-chatbot.git
   ```
2. Create an `.env` file based on the provided `.env.template` and populate it with the necessary API keys and tokens.
3. Install the required Python dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Train the Language Model using `train.py`. 
5. Run the Telegram bot using `telegram_bot.py` to interact with the trained Language Model via Telegram.

Note: The system will run on localhost machine

### Starting on Docker on Localhost

Run the following code:
```
   docker compose -p ready-serve-chatbot up 
```

## Deployment to the cloud

This project has automated CD pipeline to deploy your LLM chatbot to AWS Elastic Beanstalk using GitHub Actions and GitHub Secrets

To setup CD to AWS Elastic Beanstalk please follow the steps below:
1. Create AWS Infrastructure
   - Register for an AWS Account
   - Register an AWS account and enter `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
   - Create an AWS Beanstalk environment in AWS and create GitHub secret `AWS_EBS_APPLICATION_NAME` and `AWS_EBS_ENVIRONMENT_NAME` with newly created AWS Elastic Beanstalk Application/Environment

2. Register for a Docker Hub Account and enter you `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` into Github secrets

## Usage

1. Ensure that the environment variables are correctly configured in the `.env` file.
2. Train the custom Language Model using `train.py` if needed after storing into `./docs` folder.
3. Run the Telegram bot using `telegram_bot.py` to start interacting with the Language Model through Telegram.

