# Step 1: Front
FROM node:20-alpine AS build-front

WORKDIR /app
COPY package.json webpack.config.js ./
RUN yarn install
COPY _front/ ./_front/
RUN yarn build --mode production

###

# Step 2: Build App
FROM python:3.13-slim AS build-app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYDEVD_DISABLE_FILE_VALIDATION=1
ENV PYTHONUNBUFFERED=1

RUN apt update && \
    apt install -y \
    python3-dev

RUN pip install --upgrade pip
COPY requirements.txt ./
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

ENV DATABASE_URL="sqlite:///app.db" \
    SECRET_KEY="unset" \
    DJANGO_SETTINGS_MODULE="conf.settings.development" \
    DEBUG=True \
    PORT=8000

COPY . ./

RUN mkdir -p /app/_static/dist
RUN mkdir -p _logs
RUN mkdir -p _media

COPY --from=build-front /app/_static/dist /app/_static/dist

RUN python manage.py collectstatic --clear --noinput

ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8000
CMD ["gunicorn", \
     "--access-logfile", "/app/_logs/gunicorn_access.log", \
     "--log-level", "error", \
     "--workers", "3", \
     "--timeout", "10", \
     "--bind", "0.0.0.0:$PORT", \
     "--forwarded-allow-ips", "*", \
     "conf.wsgi:application"]
#CMD python manage.py runserver 0.0.0.0:$PORT
