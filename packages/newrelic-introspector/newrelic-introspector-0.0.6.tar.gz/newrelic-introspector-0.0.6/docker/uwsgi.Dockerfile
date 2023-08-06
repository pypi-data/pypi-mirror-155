FROM tiangolo/uwsgi-nginx-flask:latest

RUN mkdir -p /app/

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"]