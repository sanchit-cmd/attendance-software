# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
RUN mkdir /app
WORKDIR /app

# Install system dependencies (e.g. for psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

# Copy the entire project
COPY . /app/

# Install dependencies using uv
# --frozen ensures uv.lock is not updated during build
RUN uv sync --frozen --no-dev

# Collect static files
# This will use the environment variables from your .env file
RUN /app/.venv/bin/python backend/manage.py collectstatic --noinput

# Expose port 
EXPOSE 8000

# Set the working directory to where manage.py and wsgi.py live
WORKDIR /app/backend

# Run gunicorn, binding to the PORT environment variable if it exists, otherwise 8000
CMD ["sh", "-c", "/app/.venv/bin/gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
