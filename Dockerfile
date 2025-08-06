# Use Python 3.10 slim base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir Jinja2

# Expose port for the service
EXPOSE 8001

# Command to run the microservice
CMD ["python", "risk_service.py"]
