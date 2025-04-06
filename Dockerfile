# Dockerfile
FROM python:3.11-slim

# Allow breaking system packages for psycopg2-binary
ENV PIP_BREAK_SYSTEM_PACKAGES=1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]