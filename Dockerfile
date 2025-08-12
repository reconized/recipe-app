# Use a slim, stable Python image as the base
FROM python:3.11-slim

# Set environment variables for uv and Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV UV_VIRTUALENV_PROMPT "recipe-app"

# Set the working directory inside the container
WORKDIR /usr/src/app


COPY pyproject.toml .
COPY uv.lock .

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="/tmp/.uv" sh
RUN export PATH="/tmp/.uv/bin:$PATH"
RUN uv sync
RUN uv run python manage.py collectstatic --noinput
RUN uv run python manage.py migrate --noinput && uv run python manage.py collectstatic --noinput


COPY . .

WORKDIR /usr/src/app/recipe-app

RUN python manage.py collectstatic --noinput

# Expose the port the app will run on
EXPOSE 8000

CMD ["gunicorn", "recipe-app.wsgi:application", "--bind", "0.0.0.0:8000"]
