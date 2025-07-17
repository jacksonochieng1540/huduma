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

# Copy project
COPY . /app/

# Collect static (optional)
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "huduma.wsgi:application", "--bind", "0.0.0.0:8000"]
