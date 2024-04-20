# Use the official Python 3.10.6 image from Docker Hub
FROM python:3.10.6

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables if necessary
ENV MONGO_URI='mongodb+srv://xilacxilac:zKJETi5FrIQ0fyUH@bitcamp2024.ayaslsf.mongodb.net/?retryWrites=true&w=majority&appName=bitcamp2024'

# Command to run the Flask application
CMD ["python", "app.py"]
