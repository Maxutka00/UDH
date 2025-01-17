FROM python:3
LABEL authors="bezumnui"

COPY requirements.txt requirements.txt
RUN pip install -r ./requirements.txt


EXPOSE 8000
#WORKDIR /app


CMD ["python", "udh_backend/manage.py", "migrate"]
CMD ["python", "udh_backend/manage.py", "runserver", "0.0.0.0:8000"]
