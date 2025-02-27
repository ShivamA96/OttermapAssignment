FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /data
VOLUME /data

ENV DATABASE_FILE=/data/database.db
ENV PYTHONPATH=/app/app/src
ENV JWT_SECRET_KEY="" \
    JWT_ALGORITHM="HS256" \
    JWT_TOKEN_EXPIRY_MINUTES="30" \
    DB_TYPE="sqlite" \
    DB_FILE="/data/database.db" \
    DB_ECHO="True" \
    API_PREFIX="/api/v1"
EXPOSE 8000

CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "8000"]