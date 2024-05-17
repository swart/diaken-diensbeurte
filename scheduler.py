import os
import csv
import random
from pdf import Pdf
from datetime import datetime, timedelta
from helpers import (
    Format,
    Strategy,
    SundaySchedule, # not implemented
    format_date_file_name,
    INPUT_FILE,
    OUTPUT_FILE_PREFIX,
    OUTPUT_DIRECTORY
)
from dateutil.relativedelta import relativedelta, SU
import math

class Scheduler:
    def __init__(self, months=6, strategy=Strategy.RANDOM):
        self.months = months
        self.strategy = strategy

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

    def generate(self):
        names = self.read_names()

        if self.strategy != Strategy.ORDERED:
            random.shuffle(names)

        current_month = datetime.now().month
        current_year = datetime.now().year

        first_day = datetime(current_year, current_month, 1)
        first_sunday = first_day + timedelta(days=(6 - first_day.weekday() + 7) % 7)
        last_sunday = first_day + relativedelta(months=self.months, weekday=SU(-1))
        end_date = first_day + relativedelta(months=self.months)
        weeks = math.ceil((end_date - first_sunday).days / 7)
        
        sundays = []
        for week in range(weeks):
            sunday_datetime = first_sunday + timedelta(weeks=week)
            names_starting_index = week * 4

            sunday_diakens = []
            for i in range(4):
                diaken_index = (names_starting_index + i) % len(names)
                diaken_name = names[diaken_index].strip()
                sunday_diakens.append(diaken_name)

            random.shuffle(sunday_diakens)
            sunday_schedule = {
                "sondag_datum": sunday_datetime.date(),
                "diaken_1": sunday_diakens[0],
                "diaken_2": sunday_diakens[1],
                "diaken_3": sunday_diakens[2],
                "diaken_4": sunday_diakens[3],
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
