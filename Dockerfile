FROM --platform=$BUILDPLATFORM python:3.9-alpine AS builder
EXPOSE 8000
WORKDIR /find_work
COPY requirements.txt /find_work
RUN  pip install --requirement /find_work/requirements.txt
COPY ./find_work /find_work
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
