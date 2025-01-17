FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc


WORKDIR /udh_backend
COPY . /udh_backend

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD python udh_backend/manage.py runserver