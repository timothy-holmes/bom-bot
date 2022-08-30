from python:latest

ENV INSTALL_PATH /bom-bot
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY bom_bot.py bom_bot.py
COPY src src/

# testing cron
COPY bom.bot.cronjob.test /etc/cron.d/
COPY cron_test.py cron_test.py

# production cron
COPY bom.bot.cronjob /etc/cron.d/

ENTRYPOINT ["bash"]
