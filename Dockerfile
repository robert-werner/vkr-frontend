FROM python:3.12-slim

ADD . /opt/vkr-frontend

RUN cd /opt/vkr-frontend && pip install --no-cache-dir -e .

CMD ["fastapi", "run", "--port", "8080", "/opt/vkr-frontend/frontend/main.py"]
