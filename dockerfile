# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in docker
WORKDIR /-------2025

# Copy the current directory contents into the container at /app
COPY . /-------2025

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]