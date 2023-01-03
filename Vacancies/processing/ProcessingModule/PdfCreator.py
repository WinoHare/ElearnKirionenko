import pdfkit
from jinja2 import Environment, FileSystemLoader
from openpyxl import Workbook


class PdfCreator:
    """
    Класс для создания отчета в виде pdf файла
    """
    def __init__(self, vacancie_name: str, area_name: str, workbook: Workbook, years_sheet_rows: int):
        """Задает настройки и создает pdf отчет

        Args:
            vacancie_name (str): Название вакансии, по которой была собрана статистика
            workbook (Workbook): Таблица excel
            years_sheet_rows (int): Количество строк в таблице по годам
        """
        config = pdfkit.configuration(wkhtmltopdf=r'D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        options = {'enable-local-file-access': None}
        pdfkit.from_string(self.fill_pdf_template(vacancie_name,
                                                  area_name,
                                                  workbook["Статистика по годам"],
                                                  workbook["Статистика по городам"],
                                                  years_sheet_rows),
                           'ReportModule/Results/report.pdf', configuration=config, options=options)

    def fill_pdf_template(self, vacancie_name: str, area_name: str, years_sheet: Workbook.worksheets,
                          cities_sheet: Workbook.worksheets, years_sheet_rows: int) -> str:
        """
        Заполняет html template данными из таблицы

        Args:
            vacancie_name (str): Название вакансии, по которой была собрана статистика
            area_name (str): Название региона, по которому была собрана статистика
            years_sheet (Workbook.worksheets): Excel лист с статистикой по годам
            cities_sheet (Workbook.worksheets): Excel лист с статистикой по городам
            years_sheet_rows (int): Количество строк в таблице по годам
        Returns:
            str: Заполненный данными из таблицы html template
        """
        env = Environment(loader=FileSystemLoader('./ReportModule'))
        template = env.get_template('pdf_template.html')
        pdf_template = template.render({'vacancie_name': vacancie_name,
                                        'area_name': area_name,
                                        'years_table': self.create_html_table(years_sheet, years_sheet_rows),
                                        'cities_table_first': self.create_html_table(cities_sheet, 10, last_column=2),
                                        'cities_table_second': self.create_html_table(cities_sheet, 10, 4)})
        return pdf_template

    def create_html_table(self, ws: Workbook.worksheets, rows_count: int, first_column: int = 1,
                          last_column: int = 5) -> str:
        """Создает html таблицу, заполненную данными из ws

        Args:
            ws: Workbook.worksheets: Лист таблицы excel
            rows_count (int): Количество строк
            first_column (int): Первая колонка
            last_column (int): Последняя колонка
        Returns:
            str: Строка html таблицы
        """
        html = ''
        is_first = True
        for row in ws.iter_rows(min_row=1, min_col=first_column, max_col=last_column, max_row=rows_count + 1):
            html += '<tr>'
            for cell in row:
                html += '<td><b>' + str(cell.value) + '</b></td>' if is_first else '<td>' + str(cell.value) + '</td>'
            html += '</tr>'
            is_first = False
        return html