# Binance Futures Trading Bot

Simple Python CLI trading bot for Binance Futures Testnet.

## Setup

Install dependencies

pip install -r requirements.txt

Create .env

BINANCE_API_KEY=your_key
BINANCE_SECRET_KEY=your_secret

## Run Market Order

python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

## Run Limit Order

python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 60000