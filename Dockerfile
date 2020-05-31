FROM python:3.6-alpine

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

RUN mkdir -p /app
COPY storj_exporter.py /app
WORKDIR /app
ENV STORJ_HOST_ADDRESS=storagenode STORJ_API_PORT=14002 STORJ_EXPORTER_PORT=9651
CMD [ "python", "./storj_exporter.py" ]
