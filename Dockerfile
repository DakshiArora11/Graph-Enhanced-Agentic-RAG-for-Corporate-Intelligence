# Use a Python 3.11 slim base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (optional but improves build reliability)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port required by Render
EXPOSE 10000

# Start the Streamlit app correctly for Render
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0", "--server.enableCORS=false"]
