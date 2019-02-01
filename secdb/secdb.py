#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import argparse
import json

from datetime import datetime
from aggregator import Aggregator
from vendors.factory import VendorFactory
from vendors.iex import IEX


def build_database(vendors):
    currencies = []
    exchanges = []
    symbols = []
    prices = []
    agg = Aggregator()

    # Using 4 loops, one for each dataset to be built.
    # Ensures that each dataset is fully built before building the next.
    for vendor in vendors:
        currencies.append(vendor.build_currency())
    agg.import_currencies(currencies)

    for vendor in vendors:
        exchanges.append(vendor.build_exchanges())
    agg.import_exchanges(exchanges)

    for vendor in vendors:
        symbols.append(vendor.build_symbols(agg.currencies, agg.exchanges))
    agg.import_symbols(symbols)

    # print(agg.symbols)

    for vendor in vendors:
        print(type(vendor))
        if (type(vendor) == IEX):
            prices.append(vendor.build_prices(agg.symbols))

    # agg.import_prices(prices)


def update_database(vendors):
    for vendor in vendors:
        vendor.update_currency()
        vendor.update_exchange()
        vendor.update_symbol()
        vendor.update_price()

    exit()


def help():
    print("Usage:")
    print("secdb --build")
    print("secdb --update")


def import_vendors():
    vendors = []
    config_filename = "vendors.conf"

    # Load Configuration File
    with open(config_filename) as json_data_file:
        config = json.load(json_data_file)

    # Read Configuration Contents and create class object
    for vendor in config:
        factory = VendorFactory()
        vendor = factory(vendor, config)
        if vendor is not None:
            vendors.append(vendor)

    return vendors


def main(build=None, update=None):

    logging.basicConfig(filename="../log/secdb.log", level=logging.DEBUG)
    now = datetime.utcnow()

    vendors = import_vendors()
    if (build):
        logging.info(str(now) + " Build option selected. Building database.")
        build_database(vendors)

    elif (update):
        logging.info(str(now) + " Update option selected. Updating database.")
        # update_database(vendors)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Build and update a securities \
        master database"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--build", action="store_true", help="Build the database from scratch"
    )

    group.add_argument(
        "--update", action="store_true", help="Update the database with daily \
         values"
    )
    args = parser.parse_args()
    main(build=args.build, update=args.update)
