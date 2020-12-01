# -*- coding: utf-8 -*-

"""Database Experiments."""


import sqlite3

from . import xml


def sqlite(text):
    "Create/Append an sqlite db with the output of the xml.words()."
    # sqlite3 is built-in so it makes a good first test.
    conn = sqlite3.connect("words.db")
    cur = conn.cursor()
    cur.execute(
        """SELECT name FROM sqlite_master WHERE type='table' AND name='words';"""
    )
    result = cur.fetchone()
    if not result:
        print("Creating words table.")
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
