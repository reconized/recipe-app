# Use Python base image
FROM python:3.11-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev curl

# Set working directory
WORKDIR /app

# Install Pipenv
RUN pip install pipenv

# Copy project files
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --ignore-pipfile

COPY . .

# Collect static files (optional, if using whitenoise)
RUN pipenv run python manage.py collectstatic --noinput

# Run Gunicorn
CMD ["pipenv", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
