# Base image
FROM python:3.10-slim

# Set env
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work dir
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . /app/

# Set permissions
RUN chmod +x /app/entrypoint.sh

# Run using Gunicorn + entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
