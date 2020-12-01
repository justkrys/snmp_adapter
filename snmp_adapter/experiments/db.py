# -*- coding: utf-8 -*-

"""Database Experiments."""


import sqlite3
import sqlalchemy as sa

from . import xml


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
