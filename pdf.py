from reportlab.platypus import SimpleDocTemplate
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

from helpers import (
    format_date_day_month,
    format_date_month_year,
    format_datetime_day_month_year_hour_minute,
)


PAGE_HEADING = "DIENSBEURTE VIR DIAKENS"


class Pdf(SimpleDocTemplate):
    """
    See https://docs.reportlab.com/reportlab/userguide/ch7_tables/ for more information
    """

    def __init__(self, filename, sundays):
        super().__init__(
            f"data/{filename}",
            pagesize=A4,
            leftMargin=10,
            rightMargin=10,
            topMargin=10,
            bottomMargin=0,
            title=PAGE_HEADING,
            pageCompression=None,
            lang="af",
        )
        self.sundays = sundays
        self.elements = []
        self.styles = getSampleStyleSheet()
        self.set_styles()

    def set_styles(self):
        self.styles.add(
            ParagraphStyle(
                name="Heading1_center",
                parent=self.styles["Heading1"],
                alignment=TA_CENTER,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="Normal_center",
                parent=self.styles["Normal"],
                alignment=TA_CENTER,
                spaceBefore=20,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="Info_center",
                parent=self.styles["Normal"],
                alignment=TA_CENTER,
                fontSize=6,
                textColor=colors.lightgrey,
                spaceBefore=20,
            )
        )
        self.table_style = TableStyle(
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

    def table_data(self):
        """
        Generate table data compatible with reportlab's table

        Returns:
            list: A list of lists representing the table data, e.g.
                [
                    ["MAART 2024", "", ""],
                    ["3 Maart", "1", "Nicol van Wijk"],
                    ["", "2", "Pierre du Toit"],
                    ["", "3", "Mannes Nijeboer"],
                    ["", "4", "Ludwig Venter"],
                    ...
                ]
        """

        table_data = []
        first_sunday = self.sundays[0]["sondag_datum"]

        for index, sunday in enumerate(self.sundays):
            table_data_index = sunday["sondag_datum"].month - first_sunday.month

            is_new_month = True
            if index > 0:
                is_new_month = (
                    sunday["sondag_datum"].month
                    != self.sundays[index - 1]["sondag_datum"].month
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

        return table_data

    def build_tables(self, table_data):
        """
        Args:
            table_data (list): A list of table data

        Returns:
            list: A list tables
        """

        tables = []
        for data in table_data:
            table = Table(
                data=data,
                spaceAfter=20,
                style=self.table_style,
                repeatRows=1,
                rowSplitRange=1,
                colWidths=[80, 20, 150],
            )
            tables.append(table)

        return tables

    def build(self):
        """
        Builds elements to generate a PDF document
        """

        table_data = self.table_data()
        tables = self.build_tables(table_data)

        self.elements.append(Paragraph(PAGE_HEADING, self.styles["Heading1_center"]))
        self.elements.append(
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
            )
        )
        self.elements.append(
            Paragraph(
                "Punt 1 : Ouderlinge, Punt 2 : Middel, Punt 3 : Diakens, Punt 4 : Moederskamer",
                self.styles["Normal_center"],
            )
        )
        self.elements.append(
            Paragraph(
                f"Gemaak op {format_datetime_day_month_year_hour_minute()}",
                self.styles["Info_center"],
            )
        )

        super().build(self.elements)
