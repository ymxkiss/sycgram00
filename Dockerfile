FROM python:3.9-alpine
LABEL maintainer=ymxkiss

WORKDIR /sycgrambot
COPY . /sycgrambot

# The libc6-compat dependency is required to use the host's docker commands
RUN apk add --no-cache libjpeg libwebp libpng py3-lxml bc neofetch libc6-compat \
    && apk add --no-cache --virtual build-deps gcc g++ zlib-dev jpeg-dev libxml2-dev libxslt-dev libwebp-dev libpng-dev \
    && pip install -r requirements.txt --no-cache-dir \
    && apk del build-deps \
    && mkdir -p /sycgrambot/data \
    && rm -rf .git .github .gitignore Dockerfile install.sh LICENSE README.md requirements.txt

VOLUME /sycgrambot/data

ENTRYPOINT ["/usr/local/bin/python3", "-u", "main.py"]
