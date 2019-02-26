from secdb.currency import Currency
from secdb.symbol import Symbol
from secdb.exchange import Exchange
from secdb.price import Price
from secdb.vendors.vendor import Vendor
from secdb.database import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

'''
    Initialisation variables
'''
db_host = "localhost"
db_user = "postgres"
db_pass = ""
db_name = "securities_master"

db_string = "postgresql://"+db_user+":"+db_pass+"@"+db_host+"/"+db_name
db = create_engine(db_string)

Session = sessionmaker(db)
session = Session()
Base.metadata.create_all(db)

aud = Currency(
        code='AUD',
        num=36,
        minor_unit=2,
        name='Australian Dollar'
    )


def test_create_currency():
    # Create
    session.add(aud)
    session.commit()


def test_read_currency():
    # Read
    currencies = session.query(Currency)
    for currency in currencies:
        print(currency)


def test_update_currency():
    # Update
    aud.name = "Non-Australian Dollar"
    session.commit()
    test_read_currency()


def test_delete_currency():
    # Delete
    session.delete(aud)
    session.commit()


def test_currency_equality():
    test_code = 'AUD'
    assert test_code == aud
