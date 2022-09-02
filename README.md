# BOM scraper

Usage:

1. Clone

2. Build and name: docker build -t bom-bot .

3. Run/test: docker run -it bom-bot

4. Schedule with Ofelia by adding to config.ini in Ofelia container:

```ini
[job-run "job-executed-on-new-container"]
schedule = @daily
image = bom-bot:latest
command = curl http://192.168.1.103:8000/ping/9ca9609e-474c-4b02-a24c-e3e1ba88ee35/start && python /bom-bot/bom-bot.py && curl http://192.168.1.103:8000/ping/9ca9609e-474c-4b02-a24c-e3e1ba88ee35
```
