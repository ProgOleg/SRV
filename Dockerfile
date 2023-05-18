FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN apt-get install tzdata

RUN python manage.py collectstatic --noinput

EXPOSE 8001

ENV NUM_WORKERS 2

CMD ["sh", "-c", "gunicorn --workers=$NUM_WORKERS --bind 0.0.0.0:8001 --log-level=debug mysite.wsgi"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["sh", "-c", "uvicorn srv_site.asgi:application --host 0.0.0.0 --port 8000 --workers $NUM_WORKERS"]