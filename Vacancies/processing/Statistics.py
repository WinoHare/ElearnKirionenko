import numpy as np
import sqlite3
import pandas as pd
from prof_stats.models import YearsTable, CitiesSalaryTable, CitiesPercentTable, SkillsTable

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
        self.skills_df = pd.DataFrame()
        self.get_statistics()
        self.add_statistics_to_df()

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
                              'LIMIT 10',
            'key_skills': """WITH split(word, str) AS (
                             SELECT '', key_skills||';' From vacancies
                             UNION ALL SELECT
                             substr(str, 0, instr(str, ';')),
                             substr(str, instr(str, ';')+1)
                             FROM split WHERE str!=''
                             ) SELECT word as skill, COUNT(word) as count FROM split WHERE word!=''
                             GROUP BY word
                             ORDER BY count DESC
                             LIMIT 10"""
        }

    def add_statistics_to_df(self):
        YearsTable.objects.all().delete()
        # CitiesSalaryTable.objects.all().delete()
        # CitiesPercentTable.objects.all().delete()
        SkillsTable.objects.all().delete()
        for item in self.years_df.itertuples():
            YearsTable.objects.create(year=item[0], salary=item[1], count=item[2], prof_salary=item[3], prof_count=item[4])
        # for item in self.cities_salary_df.itertuples():
        #     CitiesSalaryTable.objects.create(city=item[0], salary=item[1])
        # for item in self.cities_percent_df.itertuples():
        #     CitiesPercentTable.objects.create(city=item[0], percent=item[1])
        for item in self.skills_df.itertuples():
            SkillsTable.objects.create(skill=item[0], count=item[1])

    def get_statistics(self) -> None:
        """
        Подсоединяется к базе данных и получает статистику из нее
        """
        connect = sqlite3.connect('processing/ProcessingModule/Data/vacancies_with_skills.db')
        cursor = connect.cursor()
        self.vacancies_count = cursor.execute(self.sql_requests['count']).fetchone()[0]

        years_df = pd.read_sql(self.sql_requests['years'], connect, index_col='year')
        prof_years_df = pd.read_sql(self.sql_requests['prof_years'], connect, index_col='year')
        self.years_df = years_df.join(prof_years_df).fillna(0) \
            .astype({'salary': int, 'count': int, 'prof_salary': int, 'prof_count': int})

        # self.cities_salary_df = pd.read_sql(self.sql_requests['cities_salary'], connect, index_col='area_name').fillna(0)\
        #     .astype({'salary': int})
        #
        # self.cities_percent_df = pd.read_sql(self.sql_requests['cities_percent'], connect, index_col='area_name').fillna(0)

        self.skills_df = pd.read_sql(self.sql_requests['key_skills'], connect, index_col='skill')
        print(self.skills_df)

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
