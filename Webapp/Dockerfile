# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only necessary files
COPY requirements.txt requirements.txt

COPY . .  

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8050

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Command to run the app
CMD ["waitress-serve", "--host=0.0.0.0", "--port=8050", "--threads=8", "app:app.server"]