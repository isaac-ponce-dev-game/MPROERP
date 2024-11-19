FROM alpine:3.7
MAINTAINER isaac.ponce@duponce.com.br
RUN mkdir -p /opt/erp_mpro/
WORKDIR /opt/erp_mpro/
COPY requirements.txt /opt/erp_mpro/
RUN apk add --no-cache python3 python3-dev \
    py3-cffi zlib-dev gcc jpeg-dev \
    linux-headers libressl-dev \
    libxml2-dev libxslt-dev \
    musl-dev postgresql-dev \
    && pip3 install -r requirements.txt \
    && pip3 install gunicorn psycopg2
