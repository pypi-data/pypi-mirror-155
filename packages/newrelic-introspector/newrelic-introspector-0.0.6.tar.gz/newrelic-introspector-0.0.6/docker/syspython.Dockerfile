FROM python:3.7

RUN mkdir -p /app/

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./tests /app/

WORKDIR /app/

CMD ["/app/start.sh"]
