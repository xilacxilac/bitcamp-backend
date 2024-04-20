# Use the official Python 3.10.6 image from Docker Hub
FROM python:3.10.6

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port on which your Flask app will run
EXPOSE 5000

# Set environment variables if necessary
# ENV VARIABLE_NAME=value

# Command to run the Flask application
CMD ["python", "app.py"]
