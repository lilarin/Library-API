FROM python:3.12.2-alpine3.19

ENV PYTHONUNBUFFERED 1

RUN addgroup -S mygroup && adduser -S my_user -G mygroup

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN chown -R my_user:mygroup /app

USER my_user
