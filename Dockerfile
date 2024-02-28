FROM python:latest
WORKDIR /app

COPY helpers.py /app/helpers.py
COPY loggerManager.py /app/loggerManager.py
COPY mediacenterManager.py /app/mediacenterManager.py
COPY overseerrAPI.py /app/overseerrAPI.py
COPY radarrAPI.py /app/radarrAPI.py
COPY sonarrAPI.py /app/sonarrAPI.py
COPY tautulliAPI.py /app/tautulliAPI.py
COPY webhookCaller.py /app/webhookCaller.py
COPY constants.py /app/constants.py


COPY config.json /app/config.json
COPY requirements.txt /app/requirements.txt
COPY crontab /app/crontab
COPY crontab /etc/cron.d/crontab

RUN apt-get update && apt-get -y install cron && \
    pip3 install -r /app/requirements.txt && \
    chmod 0644 /etc/cron.d/crontab && \
    /usr/bin/crontab /etc/cron.d/crontab

#uncoment this line if you want it to do an update on start
#RUN /usr/local/bin/python3 /app/mediacenterManager.py

CMD ["cron", "-f"]