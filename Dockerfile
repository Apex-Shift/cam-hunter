# Use a lightweight official Python image based on Alpine Linux
FROM python:3.12-alpine

# Set system environment variables to optimize Python inside Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (readline support for interactive terminal navigation)
RUN apk add --no-cache libedit-dev build-base

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python packages (httpx and readline utilities)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Ensure the execution reports directory exists
RUN mkdir -p reports

# Set the entrypoint command to launch the framework interactively
ENTRYPOINT ["python", "main.py"]
