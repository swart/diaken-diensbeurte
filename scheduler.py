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
    SHIFT_SIZE
)
from dateutil.relativedelta import relativedelta, SU
import math

class Scheduler:
    def __init__(self, months=4, strategy=Strategy.RANDOM, include_current_month=False):
        self.months = months
        self.strategy = strategy
        self.include_current_month = include_current_month

    def read_names(self):
        with open(INPUT_FILE, "r") as file:
            lines = file.readlines()

        return lines

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

    def reserve_for_duty(self, to_be_assigned_list):
        """
        Return the names to be assigned to next shift and
        remove them from the to-be-assigned list of names.

        Args:
            to_be_assigned_list : list of strings

        Raises:
            NotEnoughForShiftError

        Returns:
            on_duty_list : list of strings
        """
        on_duty_list = []
        temp = {}

        for i in range(SHIFT_SIZE):
            # Split to also catch grouped names
            entry = to_be_assigned_list[i].split(",")
            # First add grouped names
            for name in entry:
                if len(entry) > 1:
                    temp[name.rstrip()] = to_be_assigned_list[i]
            # Now add individuals
            for name in entry:
                if len(entry) == 1:
                    temp[name.rstrip()] = to_be_assigned_list[i]

        # Raise exception if not enough for a shift
        if len(temp) < SHIFT_SIZE:
            raise NotEnoughForShiftError

        # Set on duty list, constrain to shift size
        on_duty_list = list(temp.keys())[0:SHIFT_SIZE]

        # Remove from to be assigned list entries that we
        # have names for in the on duty list. Constrain to
        # Shift size. Expect duplicate values so convert it
        # to a set.
        entries_to_remove = set(list(temp.values())[0:SHIFT_SIZE])
        for entry in set(temp.values()):
            to_be_assigned_list.remove(entry)

        return on_duty_list

    def get_names(self):
        """
        Return read names in order determined by strategy

        Return:
            names: list of strings
        """
        names = self.read_names()

        if self.strategy != Strategy.ORDERED:
            random.shuffle(names)

        return names

    def generate(self):
        names = []

        current_month = datetime.now().month if self.include_current_month else datetime.now().month + 1
        current_year = datetime.now().year

        first_day = datetime(current_year, current_month, 1)
        first_sunday = first_day + timedelta(days=(6 - first_day.weekday() + 7) % 7)
        last_sunday = first_day + relativedelta(months=self.months, weekday=SU(-1))
        end_date = first_day + relativedelta(months=self.months)
        weeks = math.ceil((end_date - first_sunday).days / 7)

        sundays = []
        for week in range(weeks):
            sunday_datetime = first_sunday + timedelta(weeks=week)

            # If not enough unassigned names add some
            if len(names) < SHIFT_SIZE:
                names = names + self.get_names()

            sunday_shift = self.reserve_for_duty(names)

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
