
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY approval_demo ./approval_demo

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

CMD ["sh", "-c", "exec uvicorn approval_demo.web_app:app --host 0.0.0.0 --port ${PORT}"]
