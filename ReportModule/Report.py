from ReportModule.ExcelCreator import ExcelCreator
from ReportModule.GraphsCreator import GraphsCreator
from ReportModule.PdfCreator import PdfCreator
from Statistics import Statistics


class Report:
    """
    Класс для создания отчета: excel таблицы, изображения с диаграммами и общего отчета в pdf

    Attributes:
        statistics (Statistics): Статистика по вакансиям
    """

    def __init__(self, vacancie_name: str):
        """
        Собирает статистику и создает отчет

        Args:
            vacancie_name (str): Название вакансии, по которой собирается статистика
        """
        self.statistics = Statistics(vacancie_name)
        self.statistics.get_statistics()

        GraphsCreator(self.statistics)
        PdfCreator(vacancie_name, ExcelCreator(self.statistics).workbook, len(self.statistics.salary_by_year.keys()),
                   len(self.statistics.salary_by_city.keys()))