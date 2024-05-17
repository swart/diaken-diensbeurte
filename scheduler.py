import random
import csv
from datetime import datetime, timedelta
from helpers import (
    Format,
    Strategy,
    SundaySchedule,
    format_date_file_name,
)
from datetime import datetime
from pdf import Pdf


class Scheduler:
    def __init__(self, months=6, strategy=Strategy.RANDOM, names_file="diakens.txt"):
        self.months = months
        self.strategy = strategy
        self.names_file = names_file

    def read_names(self):
        with open(self.names_file, "r") as file:
            lines = file.readlines()

        return lines

    def output_csv(self, sundays, file_name):
        with open(f"data/{file_name}", "w", newline="") as file:
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
        return f"diaken_diensbeurte_{format_date_file_name(first_sunday)}_tot_{format_date_file_name(last_sunday)}.{format.value}"

    def generate(self):
        names = self.read_names()

        if self.strategy != Strategy.ORDERED:
            random.shuffle(names)

        current_month = datetime.now().month
        current_year = datetime.now().year

        first_day = datetime(current_year, current_month, 1)
        first_sunday = first_day + timedelta(days=(6 - first_day.weekday() + 7) % 7)
        last_sunday = first_sunday + timedelta(weeks=self.months * 4)

        sundays = []
        for week in range(self.months * 4):
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

        self.output_csv(
            sundays, self.output_file_name(first_sunday, last_sunday, Format.CSV)
        )
        self.output_pdf(
            sundays, self.output_file_name(first_sunday, last_sunday, Format.PDF)
        )
