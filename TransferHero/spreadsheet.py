from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill, Border
from openpyxl.formatting.rule import FormulaRule


class Spreadsheet:
    def __init__(self, sheet_title, header_row):
        self.workbook = self.initialize_workbook(sheet_title, header_row)

    @staticmethod
    def initialize_workbook(sheet_title, header_row):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = sheet_title
        sheet.append(header_row)
        # Make the header row bold
        for col in range(1, len(header_row) + 1):
            cell = sheet.cell(row=1, column=col)
            cell.font = Font(bold=True)
        return workbook

    def add_row(self, row_data):
        sheet = self.workbook.active
        sheet.append(row_data)

    def add_hyperlink(self, cell_row, cell_col, url):
        sheet = self.workbook.active
        cell = sheet.cell(row=cell_row, column=cell_col)
        cell.hyperlink = url
        cell.style = 'Hyperlink'

    def prettify(self):
        sheet = self.workbook.active

        # Fix column widths
        column_widths = []
        for row in sheet.iter_rows():
            for i, cell in enumerate(row):
                try:
                    column_widths[i] = max(column_widths[i], len(str(cell.value)))
                except IndexError:
                    column_widths.append(len(str(cell.value)))
        for i, column_width in enumerate(column_widths):
            sheet.column_dimensions[get_column_letter(i + 1)].width = column_width

        # Conditional formatting for "Offered?" column
        red = 'ffc7ce'
        green = 'c6efce'
        red_fill = PatternFill(start_color=red, end_color=red, fill_type='solid')
        green_fill = PatternFill(start_color=green, end_color=green, fill_type='solid')

        # TODO get column letter for Offered column instead of hardcoding D
        sheet.conditional_formatting.add('D2:D1000', FormulaRule(formula=['NOT(ISERROR(SEARCH("N",D2)))'], stopIfTrue=True, fill=red_fill))
        sheet.conditional_formatting.add('D2:D1000', FormulaRule(formula=['NOT(ISERROR(SEARCH("Y",D2)))'], stopIfTrue=True, fill=green_fill))

    def save(self, output_filename):
        self.prettify()
        self.workbook.save(output_filename)
