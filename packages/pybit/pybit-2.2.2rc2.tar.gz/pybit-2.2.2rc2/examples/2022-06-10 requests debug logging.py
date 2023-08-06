import requests
import logging

logging.basicConfig(filename="2022-06-10 requests debug logging.py.log",
                    level=logging.DEBUG)

print(requests.get("https://api.bybit.com/v2/public/symbols"))

