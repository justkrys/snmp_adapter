# -*- coding: utf-8 -*-

"""Database Experiments."""


import sqlite3
import sqlalchemy as sa
from sqlalchemy.ext import declarative as dcl
from sqlalchemy import orm
from sqlalchemy import inspect

from . import xml


# Added type hint to make mypy happy.
# https://github.com/python/mypy/issues/2477
Base: dcl.DeclarativeMeta = dcl.declarative_base()


class MyMixin:
    """Mixin class to give ORM objects a nicer default presentation."""

    def _asdict(self):
        """Returns a dictionary containing all column names and values."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def keys(self):
        """Return the column names as dictionary keys.

        Implements the Mapping protocol.

        """
        return self._asdict().keys()

    def __getitem__(self, key):
        """Returns the value for the given key (column name).

        Implements the Mapping protocol.

        """
        # This way is less efficient, but ensures we can only use columns as keys and not any attribute.
        return self._asdict()[key]

    def __str__(self):
        """Represent object as a string."""
        # Based on https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
        return str(dict(self))


class Words(Base, MyMixin):
    __tablename__ = "words"

    id = sa.Column(sa.Integer, primary_key=True)  # Implicit autoincrement.
    xml = sa.Column(sa.Unicode, nullable=False)

    def __init__(self, xml=None):
        """Init that allows positional argument for xml and deferred setting of xml attribute."""
        self.xml = xml

    @classmethod
    def from_text(cls, text):
        """Returns an instance of this class with the text converted into the xml attribute/column."""
        return cls(xml._words(text))


def sqlite(text):
    """Create/Append an sqlite db with the output of the xml.words().

    Uses sqlite3 directly.

    """
    # sqlite3 is built-in so it makes a good first test.
    conn = sqlite3.connect("words.db")
    cur = conn.cursor()
    cur.execute(
        """SELECT name FROM sqlite_master WHERE type='table' AND name='words';"""
    )
    result = cur.fetchone()
    if not result:
        cur.execute(
            """CREATE TABLE words (id INTEGER PRIMARY KEY AUTOINCREMENT, xml TEXT NOT NULL);"""
        )
        conn.commit()
    xml_doc = xml._words(text)
    cur.execute("""INSERT INTO words (xml) VALUES (?);""", (xml_doc,))
    conn.commit()
    print("-" * 79)
    for row in cur.execute("""SELECT * from words;"""):
        print(row)


def litealchemy(text):
    """Create/Append an sqlite db with the output of the xml.words().

    Uses sqlalchemy expression language with sqlite3.

    """
    engine = sa.create_engine("sqlite:///words2.db")
    meta = sa.MetaData()
    words = sa.Table(
        "words",
        meta,
        sa.Column("id", sa.Integer, primary_key=True),  # Implicit autoincrement.
        sa.Column("xml", sa.Unicode, nullable=False),
    )
    meta.create_all(engine)  # Automatically checks for existing tables before create.
    xml_doc = xml._words(text)
    conn = engine.connect()
    conn.execute(words.insert().values(xml=xml_doc))
    result = conn.execute(words.select())
    for row in result:
        print(row)


def ormlite(text):
    """Create/Append an sqlite db with the output of the xml.words().

    Uses sqlalchemy ORM language with sqlite3.

    """
    # I started getting quite fancy with this example.
    # The classes include lots of unnecessary, but nice, extras.
    engine = sa.create_engine("sqlite:///words3.db")
    # Automatically checks for existing tables before create.
    Base.metadata.create_all(engine)
    Session = orm.sessionmaker(bind=engine)
    session = Session()
    words = Words.from_text(text)
    session.add(words)
    session.commit()
    results = session.query(Words).all()
    for row in results:
        print(row)
