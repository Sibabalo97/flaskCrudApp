# Use the official Python image as a base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install Flask
RUN pip install Flask Flask-PyMongo

# Expose port 5003 to the outside world
EXPOSE 5003

# Run the Flask application
CMD ["python", "app.py"]
