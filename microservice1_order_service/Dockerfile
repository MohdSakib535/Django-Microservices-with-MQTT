FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install --upgrade paho-mqtt

COPY . .

RUN mkdir -p /app/data && \
    chmod 777 /app/data

# Run migrations before starting the server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
