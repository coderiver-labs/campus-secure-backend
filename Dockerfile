FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

# Django log directory
RUN mkdir -p /var/log/campus-secure/logs

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --locked

# Copy Django project
COPY . .

EXPOSE 8000

CMD ["uv","run","gunicorn","CampusSecure.wsgi:application","--bind", "0.0.0.0:8000","--workers", "3"]
