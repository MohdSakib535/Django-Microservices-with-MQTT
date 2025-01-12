FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements.txt to the working directory
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install -r requirements.txt

# Upgrade paho-mqtt
RUN pip install --upgrade paho-mqtt

# Copy the rest of the application files
COPY . .

# Command to run the MQTT subscriber
CMD ["python", "mqtt_subscriber.py"]
