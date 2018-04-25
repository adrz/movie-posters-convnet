FROM alpine:latest

# Copy python requirements file
COPY requirements.txt /tmp/requirements.txt

RUN apk add --no-cache \
    python3 \
    python3-dev \
    py-virtualenv \
    py-pip \
    git \
    bash \
    nginx \
    uwsgi \
    pcre \
    pcre-dev \
    uwsgi-python3 \
    gcc \
    libc-dev \
    linux-headers \
    supervisor && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r /tmp/requirements.txt && \
    rm /etc/nginx/conf.d/default.conf && \
    rm -r /root/.cache && \
    rm -rf /etc/nginx/sites-available/default && \\
    rm -rf /etc/nginx/sites-available/default


# Copy the Flask Nginx site conf
COPY flask-site-nginx.conf /etc/nginx/sites-available/movieposters
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY uwsgi.ini /etc/uwsgi/
# Custom Supervisord config
COPY supervisord.conf /etc/supervisord.conf

# Add demo app
COPY ./ /app
WORKDIR /app

CMD ["/usr/bin/supervisord"]