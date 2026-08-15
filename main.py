name: KuzineSportBot Scheduled Run

on:
  schedule:
    # TSİ 16:00, 18:00, 20:00 (UTC 13:00, 15:00, 17:00)
    - cron: '0 13,15,17 * * *'
  workflow_dispatch:

jobs:
  run-sport-bot:
    runs-on: ubuntu-latest
    steps:
      - name: Code Checkout
        uses: actions/checkout@v3

      - name: Python Setup
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: pip install requests pytz

      - name: Run Sport Bot
        env:
          FOOTBALL_API_KEY: ${{ secrets.FOOTBALL_API_KEY }}
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
        run: python main.py
