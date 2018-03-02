FROM alpine:3.5

# Base install
RUN apk update && apk add --no-cache \
    # bash \
    python \
    py-pip \
    supervisor

# Setup Flask application
RUN mkdir -p /deploy/
COPY app /deploy/app
COPY requirements.txt manage.py config.py /deploy/
RUN pip install -r /deploy/requirements.txt

# Set up Prometheus multiprocess registry
RUN mkdir -p /deploy/metrics

# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY docker/supervisord.conf /etc/supervisord.conf

# Start processes
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
