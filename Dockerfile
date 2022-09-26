FROM python:latest

ENV INSTALL_PATH /bom-bot
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY bom_bot.py bom_bot.py
COPY src src/
COPY scripts scripts/

# start up run
RUN ./scripts/run.sh
