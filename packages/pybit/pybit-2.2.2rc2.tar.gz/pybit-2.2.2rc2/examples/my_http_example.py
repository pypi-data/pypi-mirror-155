from pybit import HTTP  # supports inverse perp & futures, usdt perp, spot.
from pybit import usdc_options  # <-- import HTTP & WSS for inverse perp
from pybit import spot  # <-- import HTTP & WSS for spot
from pybit import inverse_futures, usdt_perpetual
import logging

logging.basicConfig(filename="my_http_example.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

api_key = "RdHxmhZAaqqFn3aI19"
api_secret = "XCgnXkuRGwrk6NdWIGt0SNmC1nr671UsZfaS"


## Authenticated
session = spot.HTTP(
    endpoint="https://api-testnet.bybit.com",
    api_key=api_key,
    api_secret=api_secret,
    referral_id="dextertest"
)
from time import time


print(session.query_symbol())
print(session.get_wallet_balance())
print(session.place_active_order(
    symbol="BTCUSDT",
    qty=10,
    side="Buy",
    type="LIMIT",
    price=18000
))

exit()


# We can fetch our wallet balance using an auth'd session.
session_auth.get_wallet_balance(coin="BTC")


"""
Spot & other APIs.
from pybit import HTTP  <-- supports inverse perp & futures, usdt perp, spot.
from pybit.spot import HTTP   <-- exclusively supports spot.
"""

# Reassign session_auth to exclusively use spot.
session_auth = spot.HTTP(
    endpoint="https://api.bybit.com",
    api_key="...",
    api_secret="..."
)


# Prefer spot endpoint via the `spot` arg
session_unauth = HTTP(endpoint="https://api.bybit.com", spot=True)

# Require spot endpoint (`spot` arg unnecessary)
session_auth.get_wallet_balance(coin="BTC")
