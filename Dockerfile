FROM python:latest

RUN apt-get update
RUN apt-get -y install cron

ENV INSTALL_PATH /bom-bot
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY bom_bot.py bom_bot.py
COPY src src/

# Testing cron
COPY bom.bot.cronjob*.test /etc/cron.d/
COPY cron_test.py cron_test.py

# Production cron
COPY bom.bot.cronjob /etc/cron.d/

# Setup container to run continuously
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log
