FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-traditional && apt-get clean

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["gunicorn", "foodgram_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
