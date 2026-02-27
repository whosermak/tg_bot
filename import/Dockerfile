FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install psycopg[binary]
CMD ["python", "import.py"]