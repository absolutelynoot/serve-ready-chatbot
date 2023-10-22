# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set environment variables
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
ENV LANGCHAIN_API_KEY=$LANGCHAIN_API_KEY

# Upgrade pip
RUN pip install --upgrade pip

# Update and install a compatible SQLite version
RUN apt-get update && apt-get install -y sqlite3

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set environment variables
ENV TELEGRAM_TOKEN=$TELEGRAM_TOKEN 
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV LANGCHAIN_API_KEY=$LANGCHAIN_API_KEY

# Train chatbot
RUN python train.py

# Run python.telegram_bot.py when the container launches
CMD ["python", "telegram_bot.py"]
