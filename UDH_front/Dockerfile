FROM python:3.10-slim
# Install system dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc


WORKDIR /simple_web
COPY . /simple_web

RUN pip install -r requirements.txt
EXPOSE 5009
CMD python ./main.py
