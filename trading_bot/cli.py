import argparse
from bot.orders import place_market_order, place_limit_order
from bot.validators import validate_side, validate_order_type
from bot.logging_config import setup_logging

setup_logging()

parser = argparse.ArgumentParser()

parser.add_argument("--symbol", required=True)
parser.add_argument("--side", required=True)
parser.add_argument("--type", required=True)
parser.add_argument("--quantity", required=True)
parser.add_argument("--price")

args = parser.parse_args()

symbol = args.symbol.upper()
side = args.side.upper()
order_type = args.type.upper()
quantity = float(args.quantity)
price = args.price

validate_side(side)
validate_order_type(order_type)

print("Order Request Summary")
print("---------------------")
print(f"Symbol: {symbol}")
print(f"Side: {side}")
print(f"Type: {order_type}")
print(f"Quantity: {quantity}")

if order_type == "LIMIT":
    if price is None:
        raise ValueError("LIMIT orders require --price")
    price = float(price)
    print(f"Price: {price}")
    response = place_limit_order(symbol, side, quantity, price)
else:
    response = place_market_order(symbol, side, quantity)

print("\nOrder Response")
print(response)
