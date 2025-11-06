# syntax=docker/dockerfile:1
# check=skip=SecretsUsedInArgOrEnv

# Stage 1: build the front-end assets with the same toolchain used in development
FROM node:24.7-slim AS front

WORKDIR /app
# copy only lockfiles first for reproducible, cached installs
COPY package.json package-lock.json ./

# try npm ci for reproducible installs; fall back to npm install on Node versions
# where `npm ci` isn't available (some Node 24/npm combos). Keep cache mount.
RUN --mount=type=cache,target=/root/.npm \
    set -ex && (npm ci || npm install)

# copy templates needed by tailwind and frontend source, then build
# copying `templates/` after `npm ci` preserves the dependency cache
COPY templates ./templates
COPY _front ./_front
COPY vite.config.mjs ./

RUN npm run build

###

# Stage 2: build the Python application image
FROM python:3.14-slim AS base

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tzdata \
        locales \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Set build envs
ENV LANG="pt_BR.UTF-8" \
    LC_ALL="pt_BR.UTF-8" \
    TZ="America/Sao_Paulo"

# Configure timezone and locale without reconfiguring the entire system
RUN ln -snf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone && \
    localedef -i en_US -f UTF-8 en_US.UTF-8 && \
    localedef -i pt_BR -f UTF-8 pt_BR.UTF-8

# Copy the 'uv' tool from the upstream image (requires BuildKit and support for
# --mount and --from referencing images). Keep this as-is but be aware BuildKit is
# required when building this Dockerfile.
COPY --from=ghcr.io/astral-sh/uv:0.4.22 /uv /uvx /bin/

###

FROM base AS build

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gettext \
        build-essential \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Django required envs, they're fake!
ENV DJANGO_SETTINGS_MODULE="conf.settings.production" \
    DOCKERIZED=True \
    DEBUG=False \
    DATABASE_URL="sqlite:///app.db" \
    SENTRY_DSN="https://0000000000000000000000000000000@000000000000000000.ingest.us.sentry.io/0000000000000000" \
    SECRET_KEY="FAKE"

# Set python/runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE="copy"

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked \
    uv sync --frozen --no-install-project --no-dev

# copy application source and the built frontend static files
COPY . .
COPY --from=front /app/_static /app/_static

# collectstatic and compilemessages in a single layer
RUN SECRET_KEY=FAKE \
    && uv run manage.py collectstatic --clear --noinput \
    && uv run manage.py compilemessages --ignore=cache --ignore=.venv

###

FROM base

# create unprivileged user and copy app as root (chown during copy)
RUN useradd -ms /bin/bash app
COPY --from=build --chown=app:app /app /app

# ensure entrypoint is executable
RUN chmod +x /app/docker-entrypoint.sh

# ensure virtualenv bin is on PATH
ENV PATH="/app/.venv/bin:$PATH"

# run migrations on startup
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# switch to non-root user for runtime
USER app:app

EXPOSE 80

# assumes the server is running behind a reverse proxy (Nginx, AWS ALB, etc.)
# set the `WEB_CONCURRENCY` environment variable to the number of workers you'd like to run
CMD ["gunicorn","conf.wsgi:application","--bind","0.0.0.0:80","--worker-class","gthread","--workers","4","--threads","4","--timeout","60","--graceful-timeout","30","--max-requests","2000","--max-requests-jitter","200","--access-logfile","-","--error-logfile","-","--log-level","info","--forwarded-allow-ips","*","--worker-tmp-dir","/dev/shm"]
