# Use a lightweight Python image
FROM python:3.11-slim

# Install curl (needed for Jenkins integration testing)
RUN apt-get update && apt-get install -y curl && apt-get clean

# Set work directory
WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Start the application
CMD ["python", "app.py"]
