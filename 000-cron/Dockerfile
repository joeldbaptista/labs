FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY script.py script.py
COPY crontab /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

CMD crond -f
#CMD [ "tail", "-f", "/dev/null" ]
