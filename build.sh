#!/usr/bin/env bash
set -o errexit

curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="/tmp/.uv" sh
export PATH="/tmp/.uv/bin:$PATH"
uv sync
uv run python manage.py collectstatic --noinput
uv run python manage.py migrate --noinput && uv run python manage.py collectstatic --noinput
