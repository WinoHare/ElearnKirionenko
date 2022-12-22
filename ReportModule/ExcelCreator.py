from openpyxl.styles import Side, Border, Font
from openpyxl.workbook import Workbook
from Statistics import Statistics


class ExcelCreator:
    """
    Класс для создания Excel таблицы со статистикой

    Attributes:
        workbook (Workbook): Excel таблица
    """

    def __init__(self, stats: Statistics):
        """
        Инициализирует класс, создавая таблицу

        Args:
            stats (Statistics): Статистика по вакансиям
        """
        self.workbook = self.initialize_workbook(stats)

    def initialize_workbook(self, statistics: Statistics) -> Workbook:
        """
        Инициализирует таблицу и добавляет в нее данные

        Args:
            statistics (Statistics): Статистика по вакансиям
        Returns:
            Workbook: excel таблица
        """
        workbook, years_sheet, cities_sheet = self.create_workbook(statistics)
        self.add_stats_to_excel(statistics, years_sheet, cities_sheet)
        self.set_sheets_settings(statistics, years_sheet, cities_sheet)
        workbook.save('ReportModule/Results/report.xlsx')
        return workbook

    def create_workbook(self, statistics: Statistics) -> tuple:
        """
        Создает excel таблицу, добавляет в нее 2 листа, задает заголовки

        Args:
            statistics (Statistics): Название профессии, по которой собрана статистика
        Returns:
            tuple: Excel таблица, 2 листа таблицы
        """
        workbook = Workbook()

        years_sheet = workbook.active
        years_sheet.title = 'Статистика по годам'
        cities_sheet = workbook.create_sheet('Статистика по городам')

        years_sheet.append(
            ['Год', 'Средняя зарплата', f'Средняя зарплата - {statistics.vacancie_name} по региону {statistics.area_name}',
             'Количество вакансий', f'Количество вакансий - {statistics.vacancie_name} по региону {statistics.area_name}'])
        cities_sheet.append(['Город', 'Уровень зарплат', '', 'Город', 'Доля Вакансий'])

        return workbook, years_sheet, cities_sheet

    def add_stats_to_excel(self, statistics: Statistics, years_sheet: Workbook.worksheets,
                           cities_sheet: Workbook.worksheets):
        """
        Добавляет статистику в таблицу excel

        Args:
            statistics (Statistics): Статистика по вакансиям
            years_sheet (Workbook.worksheets): Excel лист с статистикой по годам
            cities_sheet (Workbook.worksheets): Excel лист с статистикой по городам
        """
        for year in statistics.years_dataframe.index:
            years_sheet.append([year,
                                statistics.years_dataframe.loc[year]['salary'],
                                statistics.years_dataframe.loc[year]['prof_salary'],
                                statistics.years_dataframe.loc[year]['count'],
                                statistics.years_dataframe.loc[year]['prof_count']])

        cities_df = statistics.sort_dataframe('salary')
        for city in cities_df.index:
            cities_sheet.append([city, cities_df.loc[city]['salary']])

        cities_df = statistics.sort_dataframe('percent')
        for i, city in enumerate(cities_df.index, 2):
            cities_sheet[f'D{i}'].value = city
            cities_sheet[f'E{i}'].value = f'{round(cities_df.loc[city]["percent"], 2)}%'

    def set_sheets_settings(self, stats: Statistics, years_sheet: Workbook.worksheets,
                            cities_sheet: Workbook.worksheets) -> None:
        """
        Устанавливает настройки для таблицы

        Args:
            stats (Statistics): Статистика по вакансиям
            years_sheet (Workbook.worksheets): Excel лист с статистикой по годам
            cities_sheet (Workbook.worksheets): Excel лист с статистикой по городам
        """
        used_columns = ['A', 'B', 'C', 'D', 'E']
        for i in used_columns:
            years_sheet[f'{i}1'].font = Font(bold=True)
            cities_sheet[f'{i}1'].font = Font(bold=True)
            years_sheet.column_dimensions[i].width = max(map(lambda x: len(str(x.value)), years_sheet[i])) + 1
            cities_sheet.column_dimensions[i].width = max(
                map(lambda x: len(str(x.value)), cities_sheet[i])) + 1

        thins = Side(border_style="thin")
        for column in used_columns:
            for row in range(1, len(stats.years_dataframe.index) + 2):
                years_sheet[f'{column}{row}'].border = Border(top=thins, bottom=thins, left=thins, right=thins)

        for column in used_columns:
            for row in range(1, len(stats.years_dataframe.index) + 2):
                if column == 'C':
                    break
                cities_sheet[f'{column}{row}'].border = Border(top=thins, bottom=thins, left=thins, right=thins)