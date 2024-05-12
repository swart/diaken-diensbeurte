import csv
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
)
from reportlab.platypus.flowables import BalancedColumns
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors


def read_diakens():
    """
    Reads the lines from the 'diakens.txt' file and returns them as a list.

    Returns:
        list: A list of lines from the 'diakens.txt' file.
    """
    with open("diakens.txt", "r") as file:
        lines = file.readlines()
    return lines


months = [
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


def format_date_month_year(date):
    """
    Args:
        date (datetime.date): The date to be formatted.

    Returns:
        str: e.g. "Mei 2020"
    """
    return f"{months[date.month - 1]} {date.year}"


def format_date_day_month(date):
    """
    Args:
        date (datetime.date): The date to be formatted.

    Returns:
        str: e.g. "14 Mei"
    """
    return f"{date.day} {months[date.month - 1]}"


def format_datetime_day_month_year_hour_minute():
    """
    Current date and time

    Returns:
        str: e.g. "14 Mei 2020 15:00"
    """
    dt = datetime.now()
    return f"{dt.day} {months[dt.month - 1]} {dt.year} {dt.hour}:{dt.minute}"


def output_csv(sundays, file_name):
    """
    Write a list of dictionaries to a CSV file.

    Args:
        sundays (list): A list of dictionaries representing the data to be written to the CSV file.
        file_name (str): The name of the CSV file to be created.

    Returns:
        None
    """
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


def output_pdf(sundays, file_name):
    """
    Write a list of dictionaries to a PDF file.

    Args:
        sundays (list): list of dicts { sondag_datum: date, diaken_1: str, diaken_2: str, diaken_3: str, diaken_4: str }
        file_name (str): file name for the pdf file
    """

    # table_data = [
    #     ["MAART 2024", "", ""],
    #     ["3 Maart", "1", "Nicol van Wijk"],
    #     ["", "2", "Pierre du Toit"],
    #     ["", "3", "Mannes Nijeboer"],
    #     ["", "4", "Ludwig Venter"],
    #     ["10 Maart", "1", "Nicol van Wijk"],
    #     ["", "2", "Pierre du Toit"],
    #     ["", "3", "Mannes Nijeboer"],
    #     ["", "4", "Ludwig Venter"],
    #     ["17 Maart", "1", "Nicol van Wijk"],
    #     ["", "2", "Pierre du Toit"],
    #     ["", "3", "Mannes Nijeboer"],
    #     ["", "4", "Ludwig Venter"],
    #     ["24 Maart", "1", "Nicol van Wijk"],
    #     ["", "2", "Pierre du Toit"],
    #     ["", "3", "Mannes Nijeboer"],
    #     ["", "4", "Ludwig Venter"],
    # ]
    table_data = []
    first_sunday = sundays[0]["sondag_datum"]

    for index, sunday in enumerate(sundays):
        table_data_index = sunday["sondag_datum"].month - first_sunday.month

        is_new_month = True
        if index > 0:
            is_new_month = (
                sunday["sondag_datum"].month != sundays[index - 1]["sondag_datum"].month
            )

        if is_new_month:
            table_data.append([])
            table_data[table_data_index].append(
                [format_date_month_year(sunday["sondag_datum"]), "", ""]
            )

        table_data[table_data_index].append(
            [format_date_day_month(sunday["sondag_datum"]), "1", sunday["diaken_1"]]
        )
        table_data[table_data_index].append(["", "2", sunday["diaken_2"]])
        table_data[table_data_index].append(["", "3", sunday["diaken_3"]])
        table_data[table_data_index].append(["", "4", sunday["diaken_4"]])

    # Create a PDF document
    doc = SimpleDocTemplate(
        f"data/{file_name}",
        pagesize=A4,
        leftMargin=10,
        rightMargin=10,
        topMargin=10,
        bottomMargin=0,
        title="Diaken Diensbeurte",
        pageCompression=None,
        lang="af",
    )

    # Define styles
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="Heading1_center",
            parent=styles["Heading1"],
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Normal_center",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            spaceBefore=20,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Info_center",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=6,
            textColor=colors.lightgrey,
            spaceBefore=20,
        )
    )

    table_style = TableStyle(
        [
            ("SPAN", (0, 0), (-1, 0)),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("LINEBELOW", (0, 0), (-1, 0), 1, colors.black),
            ("LINEABOVE", (0, 5), (-1, 5), 1, colors.black),
            ("LINEABOVE", (0, 9), (-1, 9), 1, colors.black),
            ("LINEABOVE", (0, 13), (-1, 13), 1, colors.black),
            ("LINEABOVE", (0, 17), (-1, 17), 1, colors.black),
            ("LINEBEFORE", (1, 1), (1, -1), 1, colors.black),
            ("LINEBEFORE", (2, 1), (2, -1), 1, colors.black),
        ]
    )

    # Build the PDF document
    elements = []

    elements.append(Paragraph("DIENSBEURTE VIR DIAKENS", styles["Heading1_center"]))

    tables = []
    for data in table_data:
        table = Table(
            data=data,
            spaceAfter=20,
            style=table_style,
            repeatRows=1,
            rowSplitRange=1,
            colWidths=[80, 20, 150],
        )
        tables.append(table)

    elements.append(
        BalancedColumns(
            F=tables,  # the flowables we are balancing
            nCols=2,  # the number of columns
            needed=72,  # the minimum space needed by the flowable
            spaceBefore=0,
            spaceAfter=0,
            showBoundary=None,  # optional boundary showing
            leftPadding=20,  # these override the created frame
            rightPadding=None,  # paddings if specified else the 50
            topPadding=None,  # default frame paddings
            bottomPadding=None,  # are used
            innerPadding=None,  # the gap between frames if specified else
            # endSlack=0.1,  # height disparity allowance ie 10% of available height
        )
    )

    elements.append(
        Paragraph(
            "Punt 1 : Ouderlinge, Punt 2 : Middel, Punt 3 : Diakens, Punt 4 : Moederskamer",
            styles["Normal_center"],
        )
    )
    elements.append(Paragraph("Gemaak op 12 Mei 2024 15:10", styles["Info_center"]))

    # start the construction of the pdf
    doc.build(elements)
