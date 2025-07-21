# Use a Python base image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

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
