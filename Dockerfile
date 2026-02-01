# Use Python 3.11 slim as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy SDK files
COPY . /app/

# Install the SDK in editable mode plus all intelligence providers
RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir google-generativeai openai anthropic python-dotenv

# Default command: Launch the Sovereign Agent runtime
CMD ["python", "examples/example_agent.py"]
