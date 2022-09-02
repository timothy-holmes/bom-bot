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

# CMD curl http://192.168.1.103:8000/ping/9ca9609e-474c-4b02-a24c-e3e1ba88ee35/start && python /bom-bot/bom-bot.py && curl http://192.168.1.103:8000/ping/9ca9609e-474c-4b02-a24c-e3e1ba88ee35

CMD tail -f
