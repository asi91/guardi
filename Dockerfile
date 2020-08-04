FROM python:3.7-alpine
WORKDIR /app/src/guardi
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "dummy_server.py"]