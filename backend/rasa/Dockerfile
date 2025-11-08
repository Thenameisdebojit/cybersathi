# backend/rasa/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y build-essential gcc git && rm -rf /var/lib/apt/lists/*

# copy action server code
COPY actions/ /app/actions/
COPY app/ /app/backend_app/ 

WORKDIR /app/actions

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/backend_app

EXPOSE 5055
CMD ["rasa-sdk", "run", "--actions", "actions"]
