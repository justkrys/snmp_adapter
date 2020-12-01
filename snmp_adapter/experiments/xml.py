# -*- coding: utf-8 -*-

"""XML Experiments."""

from datetime import datetime, timezone

import yattag


def words(words):
    """Prints an XML document of all the words in the given text."""
    words = words.split() if isinstance(words, str) else words
    timestamp = datetime.now(timezone.utc)
    doc, tag, text, line = yattag.Doc().ttl()
    doc.asis("<!DOCTYPE xml>")
    with tag("root"):
        line("timestamp", timestamp.isoformat())
        with tag("words", myattribute="So many pretty words!"):
            for word in words:
                line("word", word)
    raw_output = doc.getvalue()
    pretty_output = yattag.indent(raw_output)
    print(raw_output)
    print("-" * 79)
    print(pretty_output)
