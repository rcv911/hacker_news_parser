FROM python:3.7-alpine

RUN apk update && apk add --virtual build-deps \
    autoconf \
    automake \
    libxslt-dev \
    g++ \
    libstdc++ \
    make \
    build-deps \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev

RUN pip install --no-cache-dir \
    pytoml \
    requests \
    aiohttp \
    aiohttp-rest-api \
    beautifulsoup4 \
    psycopg2 \
    sqlalchemy \
    pytest \
    pytest-aiohttp

COPY . /app

VOLUME ["/config/config.toml"]

WORKDIR /app

ENTRYPOINT ["python", "api.py", "-c", "/config/config.toml"]
