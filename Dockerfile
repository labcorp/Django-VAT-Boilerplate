# Stage 1: build the front-end assets with the same toolchain used in development
FROM node:24.7-slim AS front

WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/.npm \
    set -ex && npm install -g npm@latest && npm install

COPY _front ./_front
COPY vite.config.mjs ./

RUN npm run build

###

# Stage 2: build the Python application image
FROM python:3.13.7-slim AS base

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gettext tzdata locales ca-certificates \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Configure timezone and locale
RUN echo "America/Sao_Paulo" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    echo 'LANG="pt_BR.UTF-8"'>/etc/default/locale && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=pt_BR.UTF-8

# Set python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set production environment
ENV LANG="pt_BR.UTF-8" \
    LC_ALL="pt_BR.UTF-8" \
    DJANGO_SETTINGS_MODULE="conf.settings.production" \
    DOCKERIZED=True \
    DEBUG=False

# Other variables
ENV DATABASE_URL="sqlite:///app.db" \
    SENTRY_DSN="https://0000000000000000000000000000000@000000000000000000.ingest.us.sentry.io/0000000000000000" \
    SECRET_KEY="change-me" \
    PORT=80 \
    UV_LINK_MODE="copy"

# Set production environment
ENV LANG="pt_BR.UTF-8" \
    LC_ALL="pt_BR.UTF-8" \
    DJANGO_SETTINGS_MODULE="conf.settings.production" \
    DOCKERIZED=True \
    DEBUG=False

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

ENV PATH="/app/.venv/bin:$PATH"

COPY . .
COPY --from=front /app/_static /app/_static

RUN mkdir -p _logs _media _static_collected

RUN SECRET_KEY=s uv run manage.py collectstatic --clear --noinput
RUN SECRET_KEY=s uv run manage.py compilemessages

RUN useradd -ms /bin/bash app
USER app:app

EXPOSE 80

CMD ["gunicorn", \
     "--access-logfile", "/app/_logs/gunicorn_access.log", \
     "--log-level", "error", \
     "--workers", "3", \
     "--timeout", "60", \
     "--bind", "0.0.0.0:$PORT", \
     "--forwarded-allow-ips", "*", \
     "conf.wsgi:application"]
