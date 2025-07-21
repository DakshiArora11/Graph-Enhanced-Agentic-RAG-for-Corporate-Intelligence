# Use a Python base image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy only the requirements first (for layer caching)
COPY requirements.txt .

# Install system dependencies (uncomment if needed)
# RUN apt-get update && apt-get install -y build-essential

# Upgrade pip and install Python libraries
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy rest of the app
COPY . .

# Expose port used by Streamlit
EXPOSE 8501

# Start the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
