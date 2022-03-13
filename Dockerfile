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

# TODO gunicorn
CMD ["python", "main.py"]