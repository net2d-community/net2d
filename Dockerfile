# pull official base image
FROM python:3

# set work directory
WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# # copy entrypoint.sh
COPY ./api-entrypoint.sh .
RUN chmod +x /app/api-entrypoint.sh

COPY . /app/

ENTRYPOINT ["/app/api-entrypoint.sh"]

