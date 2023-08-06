FROM conda/miniconda3:latest

RUN mkdir -p /app/

RUN conda init bash && \
    conda create -y --name app_env flask gunicorn

COPY ./tests /app/

WORKDIR /app/

CMD ["/app/start.sh"]
