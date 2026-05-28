ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

WORKDIR /code

# Install uv for fast dependency resolution
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

# Copy dependency files
COPY pyproject.toml uv.lock /code/

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy the entire project
COPY . /code/

# Fly might build without secrets, so we provide a dummy SECRET_KEY just for collectstatic
ENV SECRET_KEY "dummy-secret-for-build"
# Run collectstatic using the python from uv's virtual environment
RUN /code/.venv/bin/python backend/manage.py collectstatic --noinput

EXPOSE 8000

# Set working directory to where wsgi.py lives
WORKDIR /code/backend

# Use gunicorn from uv's virtual environment
CMD ["/code/.venv/bin/gunicorn","--bind","0.0.0.0:8000","--workers","2","core.wsgi"]
