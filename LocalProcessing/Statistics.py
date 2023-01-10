import sqlite3
import pandas as pd
from GraphsCreator import GraphsCreator


class Statistics:
    """
    Класс для сбора статистики по вакансиям
    """

    def __init__(self):
        """
        Инициализирует класс, получает данные по вакансиям
        """
        self.vacancie_name = 'PHP'
        self.get_cities_statistics()

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
            'cities_percent': """SELECT area_name, 
                              ROUND((COUNT("index") * 100.0 / {0}), 2) as percent 
                              FROM vacancies 
                              GROUP BY area_name 
                              HAVING percent > 1 
                              ORDER BY percent DESC 
                              LIMIT 10""",
            'key_skills': """WITH split(word, str, year) AS (
                             SELECT '', key_skills||';', published_at From vacancies
                             WHERE CAST(SUBSTRING(published_at, 0, 5) as INTEGER) == {0}
                             UNION ALL SELECT
                             substr(str, 0, instr(str, ';')),
                             substr(str, instr(str, ';')+1),
                             CAST(SUBSTRING(year, 0, 5) as INTEGER)
                             FROM split WHERE str!=''
                             ) SELECT word as skill, COUNT(word) as count, year  FROM split WHERE word!=''
                             GROUP BY word
                             ORDER BY count DESC
                             LIMIT 10"""
        }

    def get_years_statistics(self) -> None:
        """
        Получает статистику по годам
        """
        connect = sqlite3.connect('Data/vacancies_database.db')

        years_df = pd.read_sql(self.sql_requests['years'], connect, index_col='year').fillna(0)\
            .astype({'salary': int, 'count': int,})
        GraphsCreator.create_salary_by_year_plot(years_df, 'years_salary')
        GraphsCreator.create_count_by_year_plot(years_df, 'years_count')
        self.create_html_table(years_df[['salary']], 'years_salary')
        self.create_html_table(years_df[['count']], 'years_count')

        prof_years_df = pd.read_sql(self.sql_requests['prof_years'], connect, index_col='year').fillna(0)\
            .astype({'prof_salary': int, 'prof_count': int})
        GraphsCreator.create_prof_salary_by_year_plot(prof_years_df, 'years_prof_salary')
        GraphsCreator.create_prof_count_by_year_plot(prof_years_df, 'years_prof_count')
        self.create_html_table(prof_years_df[['prof_salary']], 'years_prof_salary')
        self.create_html_table(prof_years_df[['prof_count']], 'prof_count')

    def get_cities_statistics(self):
        """
        Получает статистику по городам
        """
        connect = sqlite3.connect('Data/vacancies_database.db')
        cursor = connect.cursor()
        vacancies_count = cursor.execute(self.sql_requests['count']).fetchone()[0]

        cities_salary_df = pd.read_sql(self.sql_requests['cities_salary'],
                                            connect, index_col='area_name').fillna(0).astype({'salary': int})
        GraphsCreator.create_salary_by_city_plot(cities_salary_df, 'cities_salary')
        self.create_html_table(cities_salary_df, 'cities_salary')

        cities_percent_df = pd.read_sql(self.sql_requests['cities_percent'].format(vacancies_count), connect,
                                             index_col='area_name').fillna(0)
        GraphsCreator.create_count_by_city_plot(cities_percent_df, 'cities_percent')
        self.create_html_table(cities_percent_df, 'cities_percent')

    def get_skills_statistics(self):
        """
        Получает статистику по навыкам
        """
        connect = sqlite3.connect('Data/vacancies_with_skills.db')
        for year in range(2015, 2023):
            skills = pd.read_sql(self.sql_requests['key_skills'].format(year), connect, index_col='skill')
            GraphsCreator.create_skills_count_plot(skills, f'year-{year}')
            self.create_html_table(skills, f'year-{year}')

    def create_html_table(self, statistics: pd.DataFrame, name: str) -> str:
        """
        Создает html таблицу, заполненную данными по статистике

        Args:
            statistics (pd.DataFrame): Фрейм статистики
            name (str): Название таблицы
        Returns:
            str: Строка html таблицы
        """
        html = f'<table class="stats-table {name} hidden">'
        for row in statistics.itertuples():
            html += f'<tr><td class="stats-table-item">{row[0]}</td><td class="stats-table-item">{row[1]}</td></tr>'
        html += '</table>'
        return html
