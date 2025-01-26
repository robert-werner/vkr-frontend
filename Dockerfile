FROM python:3.12-slim

COPY . /opt/vkr_frontend
WORKDIR /opt/vkr_frontend

RUN mkdir /tmp_downloads
RUN pip install --no-cache-dir -r requirements.txt

