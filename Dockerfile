FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY gpu_webhook_validator.py /app

EXPOSE 8443

CMD ["gunicorn", "-b", "0.0.0.0:8443", "--certfile=/etc/certs/tls.crt", "--keyfile=/etc/certs/tls.key", "gpu_webhook_validator:app"]
