FROM python:3.7-stretch

WORKDIR /usr/src/app

COPY src/requirements.txt ./
RUN apt-get update && apt-get install -y busybox sysstat && pip install --no-cache-dir -r requirements.txt

COPY src ./

CMD [ "python", "./main.py" ]