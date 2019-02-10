import logging
from datetime import datetime
from secdb.vendors.asx import ASX
from secdb.vendors.asxh import ASXHistorical
from secdb.vendors.currencyiso import CurrencyISO
from secdb.vendors.marketindex import MarketIndex
from secdb.vendors.worldtradingdata import WorldTradingData
from secdb.vendors.alphavantage import AlphaVantage
from secdb.vendors.barchart import Barchart
from secdb.vendors.iex import IEX
from secdb.vendors.stooq import Stooq
from secdb.vendors.quandl import Quandl


class VendorFactory:
    def __init__(self):
        self.factory = {
            "asx": ASX,
            "alphavantage": AlphaVantage,
            "quandl": Quandl,
            "worldtradingdata": WorldTradingData,
            "barchart": Barchart,
            "stooq": Stooq,
            "iex": IEX,
            "asxhistoricaldata": ASXHistorical,
            "marketindex": MarketIndex,
            "currencyiso": CurrencyISO,
        }

    def __call__(self, vendor_name, config):

        api = config[vendor_name].get('api', None)
        name = config[vendor_name].get('name', None)
        website_url = config[vendor_name].get('website_url', None)
        support_email = config[vendor_name].get('support_email', None)
        now = datetime.utcnow()

        try:
            obj = self.factory[vendor_name.lower()](
                name, website_url, support_email, api
            )
            return obj

        except Exception:
            out = "%s: Vendor '%s' not currently supported. Skipping" % (
                str(now),
                name
                )
            logging.info(out)