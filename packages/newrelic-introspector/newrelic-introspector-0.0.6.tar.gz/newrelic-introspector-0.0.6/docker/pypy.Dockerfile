FROM pypy:3-buster

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

CMD ["/app/start.sh"]
