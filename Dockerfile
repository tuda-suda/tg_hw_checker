FROM python:3.9.14-alpine
RUN apk update && apk add gcc libc-dev libffi-dev py-cryptography
WORKDIR /usr/app
COPY . /usr/app
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "main.py"]