FROM python:3.9-slim-buster

RUN mkdir -p /app

WORKDIR /app

COPY run.sh /app
COPY dist/* /app/

RUN chown -R 1001:0 /app && \
    chmod -R g=u /app && \
    chmod +x /app/run.sh

WORKDIR /app

RUN pip install --upgrade pip && pip install -r requirements.txt; \
    pip check

USER 1001

CMD ["./run.sh"]