FROM python:3.11.0b5-alpine3.16

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install mysql-connector-python

COPY app.py .

CMD ["python", "app.py"]