FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./prompts ./prompts

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"] 