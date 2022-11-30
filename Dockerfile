FROM python:3

WORKDIR /code

COPY requirements.txt .

# RUN /bin/sh -c pip install -r requirements.txt
RUN python -m pip install -r requirements.txt


