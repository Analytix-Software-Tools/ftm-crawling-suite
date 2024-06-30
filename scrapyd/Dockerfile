FROM vimagick/scrapyd

COPY ./scrapyd.conf /etc/scrapyd/
COPY requirements.txt .
COPY run.sh .

RUN python3 -m pip install -r requirements.txt

EXPOSE 6800

ENTRYPOINT ["./run.sh"]