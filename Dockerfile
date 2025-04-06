# Use the official Python image as a base image
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
