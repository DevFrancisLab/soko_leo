# syntax=docker/dockerfile:1

FROM python:3.12-slim

# Ensure stdout/stderr are not buffered
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Cloud Run provides PORT via env
    PORT=8080

WORKDIR /app

# Install build dependencies (for any packages requiring compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Collect static assets at build time (ensures they are available in the image)
ENV DJANGO_SETTINGS_MODULE=backend.settings
RUN python backend/manage.py collectstatic --noinput

# Ensure entrypoint is executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
