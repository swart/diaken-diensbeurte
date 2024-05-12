import random
from datetime import datetime, timedelta
from helper import output_csv, output_pdf, read_diakens


def generate_schedule(months=6):
    """
    Generate a shuffled schedule for diakens for a specified number of months. Outputs the schedule to a CSV file.

    Args:
        months (int): The number of months for which to generate the schedule. Default is 6.
    """

    names = read_diakens()
    random.shuffle(names)
    # print(names)

    current_month = datetime.now().month
    current_year = datetime.now().year
    first_day = datetime(current_year, current_month, 1)
    first_sunday = first_day + timedelta(days=(6 - first_day.weekday() + 7) % 7)

    sundays = []
    for week in range(months * 4):
        sunday = first_sunday + timedelta(weeks=week)

        names_starting_index = week * 4

        sunday_diakens = []
        for i in range(4):
            diaken_index = (names_starting_index + i) % len(names)
            diaken = names[diaken_index].strip()
            sunday_diakens.append(diaken)

        random.shuffle(sunday_diakens)

        sunday_dict = {
            "sondag_datum": sunday.date(),
            "diaken_1": sunday_diakens[0],
            "diaken_2": sunday_diakens[1],
            "diaken_3": sunday_diakens[2],
            "diaken_4": sunday_diakens[3],
        }

        sundays.append(sunday_dict)

    # Save the list of dicts to a CSV file
    last_sunday = first_sunday + timedelta(weeks=months * 4)

    output_csv_file_name = f"diakens_diensbeurte_{first_sunday.strftime('%Y-%m-%d')}_{last_sunday.strftime('%Y-%m-%d')}.csv"
    output_csv(sundays, output_csv_file_name)

    output_pdf_file_name = f"diakens_diensbeurte_{first_sunday.strftime('%Y-%m-%d')}_{last_sunday.strftime('%Y-%m-%d')}.pdf"
    output_pdf(sundays, output_pdf_file_name)


def main():
    while True:
        print(
            "Welkom! Hierdie is 'n hulpmiddel om diaken diensbeurte uit te werk. Kies asseblief 'n opsie (1-3)"
        )
        print(
            "1. (default) Die diakenlys word geshuffel en ingedeel per sondag. Ingedeelde diakens word weer geshuffel."
        )
        print(
            "2. Dieselfde as opsie 1, maar die hele diakenlys word elke silklus geshuffel."
        )
        print("3. Gaan uit.")
        first_input = input()
        strategy = 1

        if first_input == "1" or first_input == "":
            strategy = 1
        elif first_input == "2":
            strategy = 2
        elif first_input == "3":
            break
        else:
            print("Ongeldige opsie.")
            break

        print("Hoeveelheid maande? (default: 6)")
        second_input = input()

        if second_input == "":
            months = 6
        elif second_input.isdigit():
            months = int(second_input)
        else:
            print("Ongeldige opsie.")
            break

        if strategy == 1:
            generate_schedule(months)
            break
        if strategy == 2:
            generate_schedule(months, True)
            break
        else:
            print("Ongeldige opsie.")
            break


# Call the main function to start the program
main()
