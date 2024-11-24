FROM python:alpine3.16

COPY . /app/

WORKDIR /app

RUN apk update && apk upgrade
RUN apk add --no-cache build-base
RUN apk add --no-cache g++ jpeg-dev zlib-dev libjpeg make gcc nginx
RUN apk add --no-cache python3-dev  py-pip
RUN apk add --no-cache py-pip py-virtualenv musl-dev linux-headers libffi-dev openssl-dev
RUN apk add --no-cache cargo
RUN pip install --upgrade pip setuptools
RUN pip install --upgrade pip
RUN pip install wheel
RUN make activate
RUN make install

EXPOSE 3004

ENTRYPOINT ["sh", "./docker/entrypoint.sh"]