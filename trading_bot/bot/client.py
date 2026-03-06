from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

def get_client():
    client = Client(API_KEY, API_SECRET)

    client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    return client