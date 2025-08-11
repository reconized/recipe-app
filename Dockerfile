# Use a slim, stable Python image as the base
FROM python:3.11-slim

# Set environment variables for uv and Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV UV_VIRTUALENV_PROMPT "recipe-app"

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the uv-related files first to leverage Docker's caching
# This assumes your pyproject.toml is in the django-app directory
COPY apps/recipe-app/pyproject.toml .
COPY apps/recipe-app/uv.lock .

# Install dependencies using uv sync
# This is a key step where uv reads the lock file and installs packages
RUN pip install uv && uv sync --no-default-python

# Copy the rest of the application code
COPY . .

# Change to the django-app directory for all future commands
WORKDIR /usr/src/app/apps/recipe-app

# Collect static files
# Use `python manage.py collectstatic --noinput` to avoid interactive prompts
RUN python manage.py collectstatic --noinput

# Expose the port the app will run on
EXPOSE 8000

# The command to run the application using Gunicorn
# This will be the main process of the container
# Use `CMD` instead of `ENTRYPOINT` so it can be overridden
CMD ["gunicorn", "recipe-app.wsgi:application", "--bind", "0.0.0.0:8000"]
