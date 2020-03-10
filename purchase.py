import os
import bs4
import json as js
import requests as rq
from stock import Stock


class Purchase(Stock):

    def __init__(self, code=None, name=None, market=None,
                 price=None, units=None):
        super().__init__(code=code, name=name, market=market)
        if price is None or units is None:
            raise ValueError("Need to specify both units bought and " +
                             "purchase price!")

        print("Acquired!")


if __name__ == "__main__":
    for sn in ["MMM", "GILD", "PG", "MSFT", "DIS", "WFC"]:
        p = Purchase(code=sn, units=1, price=100.0)
