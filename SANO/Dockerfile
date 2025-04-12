# Use the official Python image as a base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libssl-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get remove --purge -y gcc libffi-dev libssl-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Create a directory for logs
RUN mkdir -p logs

# Expose the necessary ports (if applicable)
# EXPOSE 8000  # Uncomment and set the appropriate port if your app runs a web server

# Define the entry point for the application
CMD ["python", "scripts/sync_partners.py"]  # Change this to your main script
