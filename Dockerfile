FROM --platform=$BUILDPLATFORM python:3.9-alpine AS builder
EXPOSE 8000
WORKDIR /find_work
COPY requirements.txt /find_work
RUN pip3 install -r requirements.txt --no-cache-dir
COPY ./find_work /find_work
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]