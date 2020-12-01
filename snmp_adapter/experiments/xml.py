# -*- coding: utf-8 -*-

"""XML Experiments."""

from datetime import datetime, timezone

import yattag


def _words(words):
    """Returns an XML document of all the words in the given text."""
    words = words.split() if isinstance(words, str) else words
    timestamp = datetime.now(timezone.utc)
    doc, tag, text, line = yattag.Doc().ttl()
    doc.asis("<!DOCTYPE xml>")
    with tag("root"):
        line("timestamp", timestamp.isoformat())
        with tag("words", myattribute="So many pretty words!"):
            for word in words:
                line("word", word)
    return doc.getvalue()


def words(words):
    """Prints an XML document of all the words in the given text."""
    raw_output = _words(words)
    pretty_output = yattag.indent(raw_output)
    print(raw_output)
    print("-" * 79)
    print(pretty_output)
