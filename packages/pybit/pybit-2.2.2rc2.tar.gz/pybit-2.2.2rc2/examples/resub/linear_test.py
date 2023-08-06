"""
To see which endpoints and topics are available, check the Bybit API
documentation: https://bybit-exchange.github.io/docs/inverse/#t-websocket

There are several WSS URLs offered by Bybit, which pybit manages for you.
However, you can set a custom `domain` as shown below.
"""

from time import sleep

# Import your desired markets from pybit
from pybit import usdc_perpetual, usdt_perpetual, inverse_perpetual, spot

"""
An alternative way to import:
from pybit.inverse_perpetual import WebSocket, HTTP
"""

# Set up logging (optional)
import logging
logging.basicConfig(filename="pybit.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

api_key = "19NqMAULbxl1jK8vXr"
api_secret = "grThnUcO7S5JgEt5Nfxx6gkogsffMOKKKeSe"

# Connect with authentication!
ws = usdt_perpetual.WebSocket(
    test=True,
    api_key=api_key,
    api_secret=api_secret,
    # to pass a custom domain in case of connectivity problems, you can use:
    domain="bybit",  # the default is "bybit"
    trace_logging=True,
    ping_interval=5,
    ping_timeout=3
)


def handle_message(message):
    #print(message)
    pass


ws.trade_stream(handle_message, "BTCUSDT")
#ws.orderbook_25_stream(handle_message, "BTCUSDT")

#ws.position_stream(handle_message)
#ws.order_stream(handle_message)

while True:
    # This while loop is required for the program to run. You may execute
    # additional code for your trading logic here.
    print("connected", ws.is_connected())
    print("subscriptions", ws.subscriptions)
    sleep(1)
