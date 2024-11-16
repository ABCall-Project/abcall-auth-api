FROM python:alpine3.16 AS python-base

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev \
    nginx \
    openssl-dev \
    make

RUN apk add --no-cache cargo

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

COPY ./docker/nginx.conf /etc/nginx/nginx.conf

EXPOSE 3004

COPY ./docker/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]