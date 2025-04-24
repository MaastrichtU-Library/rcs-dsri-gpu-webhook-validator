FROM python:3.12-slim

COPY gpu_webhook_validator.py /app

WORKDIR /app

RUN pip install flask

CMD ["python", "gpu_webhook_validator.py"]