FROM alpine

# Copy python requirements file
COPY requirements-api.txt /tmp/requirements.txt
# Add demo app
COPY ./ /app

RUN apk add --no-cache \
    python3 \
    python3-dev \
    py-virtualenv \
    py-pip \
    git \
    bash \
    nginx \
    postgresql-libs \
    postgresql-dev \
    musl-dev \
    pcre \
    pcre-dev \
    uwsgi-python3 \
    gcc \
    libc-dev \
    linux-headers \
    supervisor && \
    python3 -m ensurepip && \
    rm /etc/nginx/conf.d/default.conf && \
    rm -rf /etc/nginx/sites-available/default && \
    rm -rf /etc/nginx/sites-available/default


# Copy the Flask Nginx site conf
COPY flask-site-nginx.conf /etc/nginx/sites-available/movieposters
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY uwsgi.ini /etc/uwsgi/
# Custom Supervisord config
COPY supervisord.conf /etc/supervisord.conf

WORKDIR /app
RUN rm -r /usr/lib/python*/ensurepip && \
    rm -rf env && \
    virtualenv -p python3 env && \
    source env/bin/activate && \
    pip install -r /tmp/requirements.txt


CMD ["/usr/bin/supervisord"]