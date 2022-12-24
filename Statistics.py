import numpy as np
import sqlite3
import pandas as pd


class Statistics:
    """
    Класс для сбора статистики по вакансиям

    Attributes:
        vacancie_name (str): Название вакансии, для которой собирается статистика
        area_name (str): Название региона, для которого собирается статистика
        vacancies_count (int): Общее количество вакансий, вошедших в выборку
        years_df (DataFrame): Фрейм со статистиками по годам
        cities_salary_df (DataFrame): Фрейм со статистиками зарплат по городам
        cities_percent_df (DataFrame): Фрейм со статистиками количества вакансий по городам
    """

    def __init__(self, vacancie_name: str, area_name: str):
        """
        Инициализирует класс, получает данные по вакансиям

        Args:
            vacancie_name (str): Название вакансии, для которой собирается статистика
            area_name (str): Название региона, для которого собирается статистика
        """
        self.vacancie_name = vacancie_name
        self.area_name = area_name
        self.vacancies_count = 0
        self.years_df = pd.DataFrame()
        self.cities_salary_df = pd.DataFrame()
        self.cities_percent_df = pd.DataFrame()

    @property
    def sql_requests(self) -> dict[str, str]:
        """
        Возвращает словарь sql запросов
        """
        return {
            'years': 'SELECT CAST(SUBSTRING(published_at, 0, 5) as INTEGER) as year, '
                     'CAST(AVG(Salary) as INTEGER) as salary, '
                     'CAST(COUNT("index") as INTEGER) as count '
                     'FROM vacancies GROUP BY year',
            'prof_years': 'SELECT CAST(SUBSTRING(published_at, 0, 5) as INTEGER) as year, '
                          'CAST(AVG(Salary) as INTEGER) as prof_salary, '
                          'CAST(COUNT("index") as INTEGER) as prof_count '
                          'FROM vacancies '
                          f'WHERE name LIKE ("%{self.vacancie_name}%") '
                          f'AND area_name LIKE ("%{self.area_name}%") '
                          'GROUP BY year',
            'count': 'SELECT COUNT(*) FROM vacancies',
            'cities_salary': 'SELECT area_name, '
                             'CAST(AVG(Salary) as INTEGER) as salary '
                             'FROM vacancies '
                             'GROUP BY area_name '
                             'ORDER BY salary DESC '
                             'LIMIT 10',
            'cities_percent': 'SELECT area_name, '
                              f'(COUNT("index") * 100.0 / {self.vacancies_count}) as percent '
                              'FROM vacancies '
                              'GROUP BY area_name '
                              'HAVING percent > 1 '
                              'ORDER BY percent DESC '
                              'LIMIT 10'
        }

    def get_statistics(self) -> None:
        """
        Подсоединяется к базе данных и получает статистику из нее
        """
        connect = sqlite3.connect('Data/vacancies_database.db')
        cursor = connect.cursor()
        self.vacancies_count = cursor.execute(self.sql_requests['count']).fetchone()[0]

        years_df = pd.read_sql(self.sql_requests['years'], connect, index_col='year')
        prof_years_df = pd.read_sql(self.sql_requests['prof_years'], connect, index_col='year')
        self.years_df = years_df.join(prof_years_df).fillna(0) \
            .astype({'salary': np.int, 'count': np.int, 'prof_salary': np.int, 'prof_count': np.int})

        self.cities_salary_df = pd.read_sql(self.sql_requests['cities_salary'], connect, index_col='area_name').fillna(0)\
            .astype({'salary': np.int})

        self.cities_percent_df = pd.read_sql(self.sql_requests['cities_percent'], connect, index_col='area_name').fillna(0)

    def sort_dataframe(self, by: str) -> pd.DataFrame:
        """
        Сортирует фрейм по переданному столбцу и отбирает первые 10 значений

        Args:
            by (str): Столбец, по которому происходит сортировка
        Returns:
            pd. DataFrame: Отсортированный фрейм
        """
        return self.cities_salary_df.sort_values(by=by, ascending=False).head(10)

    def get_percent_of_other_cities(self) -> float:
        """
        Считает процент городов, не вошедших в статистику

        Returns:
            float: Процент городов, не вошедших в статистику
        """
        return 100 - self.cities_percent_df['percent'].sum()
