FROM python:3.12

WORKDIR /app

COPY wheels ./wheels
COPY requirements.txt .

RUN pip install --no-index --find-links=./wheels -r requirements.txt

COPY app ./app
COPY .env .env

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
