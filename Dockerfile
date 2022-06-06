FROM python:3.10-slim-bullseye

EXPOSE 8000
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering 
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN apt update && apt install postgresql-client -y

RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -u 5678 --disabled-password --gecos "" user && chown -R user /app
# RUN adduser -D user
USER user

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi"]
