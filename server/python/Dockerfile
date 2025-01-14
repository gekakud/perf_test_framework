# Use the latest stable Python image (change 3.11-slim to your desired version)
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for psycopg2 and PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy all the application files into the container
COPY . /app

EXPOSE 8000

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# # Command to run the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
