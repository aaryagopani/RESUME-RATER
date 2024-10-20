# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to /app
COPY . /app

# Set environment variables, e.g., Flask-specific ones
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port 5000 for Flask
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
