FROM python:3

WORKDIR /sky_school

COPY ./requirements.txt /sky_school/

RUN pip install -r requirements.txt

COPY . .