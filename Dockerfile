# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the entire project directory into the container
COPY . .


# Install dependencies
RUN pip install -r requirements.txt

# Run the Celery worker
CMD ["celery", "-A", "celery_app", "worker", "--loglevel=INFO", "-B"]
