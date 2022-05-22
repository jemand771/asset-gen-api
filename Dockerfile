FROM python:3

WORKDIR /tmp
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY assets assets
COPY generators generators
COPY outputs outputs
COPY util util
COPY __init__.py .
COPY main.py .

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:80", "--workers", "1", "--threads", "4"]
