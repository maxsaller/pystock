import os
import bs4
import requests as rq
import multiprocessing as mp


class Stock():

    def __init__(self, code=None, name=None, market=None):
        # Stock data
        self.dat = {}

        if code is None:
            raise ValueError("Stock requires code to initialize!")
        else:
            self.dat["code"] = code

        # Get ingredients
        r = rq.get(f"https://finance.yahoo.com/quote/{self.dat['code']}").text

        # Start cooking
        self.soup = bs4.BeautifulSoup(r, features="html5lib")

        # Stock name
        if name is None:
            n = self.soup.find("h1", {"data-reactid": "7"}).get_text()
            self.dat["name"] = n.split("-")[-1].lstrip()
        else:
            self.dat["name"] = name

        # Stock market
        if market is None:
            sub = self.soup.find("div", {"data-reactid": "18", "class": None})
            market = sub.find("span", {"data-reactid": "9"}).get_text()
            self.dat["market"] = market.split("-")[0].rstrip()
        else:
            self.dat["market"] = market

        # Stock forward dividend and yield
        filtr = "DIVIDEND_AND_YIELD-value"
        dividend = self.soup.find("td", {"data-test": filtr}).get_text()
        self.dat["dividend"] = float(dividend.split()[0])

    def get_price(self):
        price = self.soup.find("span", {"data-reactid": "14"})
        self.dat["price"] = float(price.get_text())

    def output_html(self):
        os.remove(f"{self.code.lower()}.html")
        with open(f"{self.code.lower()}.html", "w") as f:
            for line in self.soup.prettify().splitlines():
                f.write(f"{line}\n")


if __name__ == "__main__":

    stocks = ["MMM", "GILD", "PG", "MSFT", "DIS", "WFC"]

    def stock_test(sn):
        s = Stock(code=sn)
        s.get_price()
        for k in s.dat.keys():
            print("{:15}".format(k), s.dat[k])
        print()

    with mp.Pool(len(stocks)) as p:
        p.map(stock_test, stocks)
