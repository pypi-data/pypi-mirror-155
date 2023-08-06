from pybit import HTTP  # supports inverse perp & futures, usdt perp, spot.
from pybit import usdc_options  # <-- import HTTP & WSS for inverse perp
from pybit import spot  # <-- import HTTP & WSS for spot
from pybit import inverse_futures, usdt_perpetual, account_asset
import logging

logging.basicConfig(filename="my_http_example.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

api_key = "RdHxmhZAaqqFn3aI19"
api_secret = "XCgnXkuRGwrk6NdWIGt0SNmC1nr671UsZfaS"


## Authenticated
session = account_asset.HTTP(
    endpoint="https://api-testnet.bybit.com",
    api_key=api_key,
    api_secret=api_secret,
    referral_id="dextertest"
)
from time import time

from uuid import uuid4
#print(session.enable_universal_transfer(transferable_sub_ids="246824"))
print(session.create_universal_transfer(
    transfer_id=str(uuid4()),
    coin="BTC",
    amount="0.00000001",
    from_member_id=246824,
    to_member_id=106958,
    from_account_type="SPOT",
    to_account_type="CONTRACT",

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
