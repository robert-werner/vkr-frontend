FROM python:3.12-slim

EXPOSE 8080

ADD . /opt/vkr-frontend

RUN cd /opt/vkr-frontend && pip install --no-cache-dir -e .

ENTRYPOINT /opt/vkr-frontend/scripts/exec_service.sh
