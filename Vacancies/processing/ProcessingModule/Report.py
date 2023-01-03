from processing.ProcessingModule.GraphsCreator import GraphsCreator
from processing.Statistics import Statistics


class Report:
    """
    Класс для создания отчета: excel таблицы, изображения с диаграммами и общего отчета в pdf

    Attributes:
        statistics (Statistics): Статистика по вакансиям
    """

    def __init__(self, vacancie_name: str, area_name: str):
        """
        Собирает статистику и создает отчет

        Args:
            vacancie_name (str): Название вакансии, по которой собирается статистика
            area_name (str): Название региона, по которому собирается статистика
        """
        self.statistics = Statistics(vacancie_name, area_name)
        GraphsCreator(self.statistics)
