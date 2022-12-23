import math
import re
import sqlite3
import numpy as np
import pandas as pd
from Currencies import Currencies


class CsvCurrencies:
    """
    Обрабатывает поля, связанные с вакансиями и объединяет их в одно поле

    Attributes:
        currencies (DataFrame): Таблица с курсами вакансий по месяцам
    """

    def __init__(self, file_name: str):
        """
        Инициализирует класс и запускает обработку файла

        Args:
            file_name (str): Имя файла для обработки
        """
        self.currencies = Currencies.get_currencies_in_dataframe()
        self.currencies_names = list(self.currencies)
        self.currencies_names.append('RUR')
        self.cursor = self.get_database_cursor()
        self.save_vacancies_in_db(file_name)

    def handleCsv(self, file_name: str) -> pd.DataFrame:
        """
        Создает новый файл со средними зарплатами в рублях

        Args:
            file_name (str): Имя обрабатываемого файла
        Returns:
            DataFrame: Фрейм с вакансиями
        """
        vacancies_dataframe = pd.read_csv(file_name)
        vacancies_dataframe['area_name'] = vacancies_dataframe.apply(lambda v: self.clean_line(v), axis=1)
        vacancies_dataframe['salary'] = vacancies_dataframe.apply(lambda v: self.get_salary(v), axis=1)
        vacancies_dataframe = vacancies_dataframe.dropna(subset=['salary'])
        return vacancies_dataframe[['name', 'salary', 'area_name', 'published_at']]

    def save_vacancies_in_db(self, file_name: str):
        vacancies_dataframe = self.handleCsv(file_name)

        connect = sqlite3.connect('Data/vacancies_database.db')
        cursor = connect.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS vacancies (name TEXT)')
        connect.commit()
        vacancies_dataframe.to_sql('vacancies', connect, if_exists='replace')

    def get_database_cursor(self):
        connect = sqlite3.connect('Data/currencies_database.db')
        cursor = connect.cursor()
        return cursor

    def new_get_salary(self, df_):
        return np.select(
            condlist=(
                df_.isin({'salary_from': range(1000000), 'salary_to': range(1000000)}),
                df_.isin({'salary_from': range(1000000), 'salary_to': range(1000000)}),
                df_.isin({'salary_from': range(1000000), 'salary_to': range(1000000)}),
            ),
            choicelist=(((float(df_['salary_from']) + float(df_['salary_to'])) / 2),
                        float(df_['salary_to']), float(df_['salary_from'])),
            default=math.nan
        )

    def get_salary(self, line: pd.Series) -> float or None:
        """
        Определяет зарплату в зависимости от полей salary_to и salary_from и конвертирует в рубли

        Args:
            line (list): Словарь для всех полей вакансии
        Returns:
            float or None: Зарплата
        """
        if line['salary_currency'] not in self.currencies_names:
            return math.nan
        if math.isnan(line['salary_from']) and math.isnan(line['salary_to']):
            return None
        elif math.isnan(line['salary_from']):
            salary = float(line['salary_to'])
        elif math.isnan(line['salary_to']):
            salary = float(line['salary_from'])
        else:
            salary = ((float(line['salary_from']) + float(line['salary_to'])) / 2)
        if line['salary_currency'] != 'RUR':
            return math.floor(salary * self.get_currency_rate(line))
        else:
            return math.floor(salary)

    def get_currency_rate(self, line):
        return self.cursor.execute(f'SELECT {line["salary_currency"]} FROM currencies WHERE'
                                   f' date = "{self.get_published_at_month_year(line["published_at"])}"')\
            .fetchone()[0]

    def clean_line(self, line) -> str:
        """Чистит строку от лишних пробелов и html тэгов
        Args:
            line (str): Строка для очистки
        Returns:
            str: Очищенная строка
        'string to clean'
        """
        string = line['area_name']
        string = re.sub('<[^<]+?>', '', string).replace('\xa0', ' ').replace(" ", ' ').strip()
        while '  ' in string:
            string = string.replace('  ', ' ')
        return string

    def get_published_at_month_year(self, line: str) -> str:
        return f'{line[5:7]}/{line[:4]}'


CsvCurrencies('Data/vacancies_dif_currencies.csv')
