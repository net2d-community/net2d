# pull official base image
FROM python:3

# set work directory
WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

ENTRYPOINT ["/app/api-entrypoint.sh"]

