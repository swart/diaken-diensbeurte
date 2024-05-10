import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def read_diakens():
    """
    Reads the lines from the 'diakens.txt' file and returns them as a list.

    Returns:
        list: A list of lines from the 'diakens.txt' file.
    """
    with open("diakens.txt", "r") as file:
        lines = file.readlines()
    return lines


def output_csv(sundays, file_name):
    with open(file_name, "w", newline="") as file:
        fieldnames = ["sondag_datum", "diaken_1", "diaken_2", "diaken_3", "diaken_4"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sundays)


def output_pdf(sundays, file_name):
    """
    Args:
        sundays (list): list of dicts { sondag_datum: str, diaken_1: str, diaken_2: str, diaken_3: str, diaken_4: str }
        file_name (str): file name for the pdf file
    """
    doc = SimpleDocTemplate(file_name, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    # styleN = styles['Normal']
    styleH1 = styles["Heading1"]
    styleH2 = styles["Heading2"]
    elements.append(Paragraph("DIENSBEURTE VIR DIAKENS", styleH1))

    table_header = [["Datum", "Punt 1", "Punt 2", "Punt 3", "Punt 4"]]

    # Create table style
    styleT = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.white),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    sundays_groups = [sundays[i : i + 4] for i in range(0, len(sundays), 4)]

    print(sundays_groups)

    for group in sundays_groups:
        table_data = []
        table_data.append(table_header)

        for item in group:
            table_data.append(
                [
                    item["sondag_datum"],
                    item["diaken_1"],
                    item["diaken_2"],
                    item["diaken_3"],
                    item["diaken_4"],
                ]
            )

        table = Table(table_data)
        table.setStyle(styleT)

        elements.append(Paragraph("Maart 2024", styleH2))
        elements.append(table)

    # Build the PDF document
    doc.build(elements)
