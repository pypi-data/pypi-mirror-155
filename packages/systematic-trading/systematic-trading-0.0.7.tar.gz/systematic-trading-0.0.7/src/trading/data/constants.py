"""
Definition of the constants of the module
"""
from datetime import date
import json
import os


EMPTY = "empty"

script_path = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(script_path, "database-futures.json")
with open(file_path, "r", encoding="utf-8") as handler:
    FUTURES = json.load(handler)

FUTURE_TYPE = "Future"

LAST_MODIFIED = "last-modified"

LETTERS = ["F", "G", "H", "J", "K", "M", "N", "Q", "U", "V", "X", "Z"]

LIBOR_BEFORE_2001 = 6.65125

START_DATE = date(2000, 1, 1)
