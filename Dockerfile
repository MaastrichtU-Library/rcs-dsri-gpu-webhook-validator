FROM python:3.12-slim

WORKDIR /app

COPY gpu_webhook_validator.py /app

RUN pip install flask

CMD ["python", "gpu_webhook_validator.py"]
