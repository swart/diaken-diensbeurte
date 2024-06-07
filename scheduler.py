import os
import csv
import random
from pdf import Pdf
from datetime import datetime, timedelta
from helpers import (
    Format,
    Strategy,
    # SundaySchedule, # not implemented
    format_date_file_name,
    INPUT_FILE,
    OUTPUT_FILE_PREFIX,
    OUTPUT_DIRECTORY,
    SHIFT_SIZE,
)
from dateutil.relativedelta import relativedelta, SU
import math


class Scheduler:
    def __init__(self, months=4, strategy=Strategy.RANDOM, include_current_month=False):
        self.names = []
        self.available_names = []
        self.months = months
        self.strategy = strategy
        self.include_current_month = include_current_month

    def read_names(self):
        with open(INPUT_FILE, "r") as file:
            self.names = file.read().splitlines()

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

    def reserve_for_duty(self):
        """
        Return the names to be assigned to next shift and
        remove them from the to-be-assigned list of names.

        Returns:
            on_duty_list : list of strings
        """
        # Make sure theres enough names to assign (available_names)
        if len(self.available_names) < SHIFT_SIZE:
            names = self.names.copy()

            if self.strategy != Strategy.ORDERED:
                random.shuffle(names)

            self.available_names.extend(names)

        # Assign four names to the next shift
        on_duty_list = []
        for i in range(SHIFT_SIZE):
            item = self.available_names.pop(0)

            # Groups of names that should be assigned together
            on_duty_list.extend(item.split(","))

            if len(on_duty_list) == SHIFT_SIZE:
                break

        for name in on_duty_list:
            name = name.rstrip()

        return on_duty_list

    def generate(self):
        self.read_names()

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
            sunday_shift = self.reserve_for_duty()

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
