from enum import Enum
from datetime import datetime
from dataclasses import dataclass
import random


INPUT_FILE = "diakens.txt"
CONTEXT_FILE = "konteks.txt"
CONTEXT_SIZE = 13
OUTPUT_FILE_PREFIX = "diaken_diensbeurte"
OUTPUT_DIRECTORY = "data"
PAGE_HEADING = "DIENSBEURTE VIR DIAKENS"
SHIFT_SIZE = 4
MONTHS = [
    "Januarie",
    "Februarie",
    "Maart",
    "April",
    "Mei",
    "Junie",
    "Julie",
    "Augustus",
    "September",
    "Oktober",
    "November",
    "Desember",
]


class Strategy(Enum):
    RANDOM = 1
    ORDERED = 2


class Format(Enum):
    CSV = "csv"
    PDF = "pdf"


def format_date_file_name(date):
    """
    Args:
        date (datetime.date):

    Returns:
        str: e.g. "mei_2020" or "jan_2020"
    """
    month = MONTHS[date.month - 1].lower()

    if len(month) > 5:
        format_month = month[0:3]
    else:
        format_month = month

    return f"{format_month}_{date.year}"


def format_date_month_year(date):
    """
    Args:
        date (datetime.date):

    Returns:
        str: e.g. "Mei 2020"
    """
    return f"{MONTHS[date.month - 1]} {date.year}"


def format_date_day_month(date):
    """
    Args:
        date (datetime.date):

    Returns:
        str: e.g. "14 Mei"
    """
    return f"{date.day} {MONTHS[date.month - 1]}"


def format_datetime_day_month_year_hour_minute():
    """
    Current date and time

    Returns:
        str: e.g. "14 Mei 2020 15:00"
    """
    dt = datetime.now()
    return f"{dt.day} {MONTHS[dt.month - 1]} {dt.year} {dt.hour}:{dt.minute}"


def months_difference(start_date, end_date):
    """
    Args:
        start_date (datetime):
        end_date (datetime):

    Returns:
        int: number of months
    """
    years = end_date.year - start_date.year
    months = end_date.month - start_date.month
    total_months = years * 12 + months
    return total_months


def insert_randomly(lst, item):
    index = random.randint(0, len(lst))
    lst.insert(index, item)
