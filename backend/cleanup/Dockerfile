FROM python:3.11-slim

WORKDIR /app

# Install only the necessary system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary application code
COPY main.py .

# Run the cleanup service
CMD ["python", "main.py"] 