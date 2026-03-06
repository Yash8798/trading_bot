import logging
from decimal import Decimal, InvalidOperation
from bot.client import get_client

client = get_client()


def _get_symbol_info(symbol):
    exchange_info = client.futures_exchange_info()
    for item in exchange_info.get("symbols", []):
        if item.get("symbol") == symbol:
            return item
    raise ValueError(f"Symbol not found on futures exchange: {symbol}")


def _extract_filter(symbol_info, filter_type):
    for f in symbol_info.get("filters", []):
        if f.get("filterType") == filter_type:
            return f
    return {}


def _validate_limit_price(symbol, price):
    symbol_info = _get_symbol_info(symbol)
    percent_filter = _extract_filter(symbol_info, "PERCENT_PRICE")
    price_filter = _extract_filter(symbol_info, "PRICE_FILTER")

    try:
        price_decimal = Decimal(str(price))
    except (InvalidOperation, TypeError):
        raise ValueError("Price must be a valid number for LIMIT orders.")

    mark_price = Decimal(client.futures_mark_price(symbol=symbol)["markPrice"])

    min_allowed = None
    max_allowed = None

    if percent_filter:
        min_allowed = mark_price * Decimal(percent_filter["multiplierDown"])
        max_allowed = mark_price * Decimal(percent_filter["multiplierUp"])

    if price_filter:
        absolute_min = Decimal(price_filter["minPrice"])
        absolute_max = Decimal(price_filter["maxPrice"])
        min_allowed = absolute_min if min_allowed is None else max(min_allowed, absolute_min)
        max_allowed = absolute_max if max_allowed is None else min(max_allowed, absolute_max)

    if min_allowed is not None and price_decimal < min_allowed:
        raise ValueError(
            f"Limit price too low for {symbol}. Minimum allowed right now is {min_allowed:.2f} "
            f"(mark price: {mark_price:.2f})."
        )

    if max_allowed is not None and price_decimal > max_allowed:
        raise ValueError(
            f"Limit price too high for {symbol}. Maximum allowed right now is {max_allowed:.2f} "
            f"(mark price: {mark_price:.2f})."
        )

    return str(price_decimal)

def place_market_order(symbol, side, quantity):

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )

        logging.info(order)
        return order

    except Exception as e:
        logging.error(str(e))
        return {"error": str(e)}


def place_limit_order(symbol, side, quantity, price):

    try:
        validated_price = _validate_limit_price(symbol, price)

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=validated_price,
            timeInForce="GTC"
        )

        logging.info(order)
        return order

    except Exception as e:
        logging.error(str(e))
        return {"error": str(e)}
