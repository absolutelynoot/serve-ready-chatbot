# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Update and install a compatible SQLite version
RUN apt-get update && apt-get install -y sqlite3

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Train chatbot
RUN python /app/train.py

# Run python.telegram_bot.py when the container launches
CMD ["python", "telegram_bot.py"]
