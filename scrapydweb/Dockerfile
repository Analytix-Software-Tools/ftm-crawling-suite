FROM python:3.6-slim

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt install git -y

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
COPY scrapydweb_settings_v10.py .
RUN python3 -m pip install --upgrade git+https://github.com/my8100/scrapydweb.git
RUN python3 -m pip install -r requirements.txt



ENTRYPOINT ["scrapydweb"]
