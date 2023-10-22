# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip
RUN python -m pip install --upgrade pip

# Update and install a compatible SQLite version
RUN apt-get update && apt-get install -y sqlite3

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Set environment variables
ARG OPENAI_API_KEY
ARG TELEGRAM_BOT_TOKEN
ARG LANGCHAIN_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
ENV LANGCHAIN_API_KEY=$LANGCHAIN_API_KEY

# Train chatbot
RUN python train.py

# Run python.telegram_bot.py when the container launches
CMD ["python", "telegram_bot.py"]
