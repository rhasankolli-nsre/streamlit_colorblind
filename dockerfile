# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the Docker container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
