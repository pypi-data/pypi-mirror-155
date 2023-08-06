FROM centos/python-38-centos7:latest

USER 0

RUN mkdir -p /app/

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./tests /app/

WORKDIR /app/

CMD ["/app/start.sh"]
