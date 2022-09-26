#!/bin/sh

# Start ping
curl -m 10 http://health.hh.home/ping/9ca9609e-474c-4b02-a24c-e3e1ba88ee35/start

# Payload here:
python /bom-bot/bom_bot.py

# Finished ping
curl -m 10 --retry 5 http://health.hh.home/ping/9ca9609e-474c-4b02-a24c-e3e1ba88ee35/$?
