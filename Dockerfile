FROM python:3.10
EXPOSE 8000

ADD ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app /app
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
