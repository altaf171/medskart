FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering 
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt
#db
RUN apk add --update --no-cache postgresql-client 

RUN mkdir /app
WORKDIR /app
COPY ./app /app
#User
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER $appuser

COPY ./entrypoint.sh /

ENTRYPOINT [ "sh","/entrypoint.sh" ]
