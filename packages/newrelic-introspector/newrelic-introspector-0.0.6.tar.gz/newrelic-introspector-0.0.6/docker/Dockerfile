FROM python:3.7

RUN mkdir -p /app/

COPY requirements.txt /
RUN /bin/bash -c "\
        pip install virtualenv && \
        virtualenv /venv && \
        source /venv/bin/activate && \
        pip install -r /requirements.txt\
    "

COPY ./tests /app/

WORKDIR /app/

RUN chown -R 1000:0 /app/ && \
    chown -R 1000:0 /venv/ && \
    useradd 1000

CMD ["/app/start.sh"]
