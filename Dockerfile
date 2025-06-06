# Use official Python image (closest to 3.13 is 3.12 as of June 2025)
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install system dependencies (if needed, e.g., for pandas, dateutil)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Default command (can be changed as needed)
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
