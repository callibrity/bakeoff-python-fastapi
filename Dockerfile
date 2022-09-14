FROM python:3.9.14-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install libpq-dev

RUN mkdir /src

WORKDIR /src

RUN pip install --upgrade pip

COPY requirements.txt /src/

RUN pip install -r requirements.txt

COPY . /src/

CMD ["python", "./src/main.py"]