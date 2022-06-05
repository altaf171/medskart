FROM python:3.10-alpine

EXPOSE 8000
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN adduser -D user
USER user

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi"]
