import os
import csv
import math
import random
from pdf import Pdf
from collections import deque
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, SU

from helpers import (
    INPUT_FILE,
    CONTEXT_FILE,
    OUTPUT_FILE_PREFIX,
    OUTPUT_DIRECTORY,
    SHIFT_SIZE,
    CONTEXT_SIZE,
    Format,
    Strategy,
    format_date_file_name,
    insert_randomly,
)


class Scheduler:
    def __init__(self, months=4, strategy=Strategy.RANDOM, include_current_month=False):
        self.context = deque(
            self._load_names_from_file(CONTEXT_FILE), maxlen=CONTEXT_SIZE
        )
        self.names = self._load_names_from_file(INPUT_FILE)
        self.available_names = []
        self.months = months
        self.strategy = strategy
        self.include_current_month = include_current_month

    def _load_names_from_file(self, file_path):
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as file:
            return file.read().splitlines()

    def output_csv(self, sundays, file_name):
        with open(f"{OUTPUT_DIRECTORY}/{file_name}", "w", newline="") as file:
            fieldnames = [
                "sondag_datum",
                "diaken_1",
                "diaken_2",
                "diaken_3",
                "diaken_4",
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sundays)

    def output_pdf(self, sundays, file_name):
        pdf = Pdf(filename=file_name, sundays=sundays)
        pdf.build()

    @staticmethod
    def output_file_name(first_sunday, last_sunday, format):
        return f"{OUTPUT_FILE_PREFIX}_{format_date_file_name(first_sunday)}_tot_{format_date_file_name(last_sunday)}.{format.value}"

    def _assign_names_to_shift(self):
        """
        Return the names to be assigned to the next shift and
        remove them from the list of available names.

        Returns:
            swift_list : list of strings
        """
        # Make sure there are enough names to assign (available_names)
        if len(self.available_names) < SHIFT_SIZE:
            names = self.names.copy()

            if self.strategy != Strategy.ORDERED:
                random.shuffle(names)

            self.available_names.extend(names)

        # Assign four names to the next shift
        swift_list = []
        while len(swift_list) < SHIFT_SIZE:
            item = self.available_names.pop(0)
            names = [name.rstrip() for name in item.split(",")]

            # Check if names are in context
            if any(name in self.context for name in names):
                self.available_names.append(item)
                # insert_randomly(self.available_names, item)
            else:
                swift_list.extend(names)
                self.context.extend(names)

        return swift_list

    def generate(self):
        current_month = (
            datetime.now().month
            if self.include_current_month
            else datetime.now().month + 1
        )
        current_year = datetime.now().year

        first_day = datetime(current_year, current_month, 1)
        first_sunday = first_day + timedelta(days=(6 - first_day.weekday() + 7) % 7)
        last_sunday = first_day + relativedelta(months=self.months, weekday=SU(-1))
        end_date = first_day + relativedelta(months=self.months)
        weeks = math.ceil((end_date - first_sunday).days / 7)

        sundays = []
        for week in range(weeks):
            sunday_datetime = first_sunday + timedelta(weeks=week)
            sunday_shift = self._assign_names_to_shift()

            random.shuffle(sunday_shift)

            sunday_schedule = {
                "sondag_datum": sunday_datetime.date(),
                "diaken_1": sunday_shift[0],
                "diaken_2": sunday_shift[1],
                "diaken_3": sunday_shift[2],
                "diaken_4": sunday_shift[3],
            }
            sundays.append(sunday_schedule)

        if not os.path.exists(OUTPUT_DIRECTORY):
            os.makedirs(OUTPUT_DIRECTORY)

        self.output_csv(
            sundays, self.output_file_name(first_sunday, last_sunday, Format.CSV)
        )
        self.output_pdf(
            sundays, self.output_file_name(first_sunday, last_sunday, Format.PDF)
        )
