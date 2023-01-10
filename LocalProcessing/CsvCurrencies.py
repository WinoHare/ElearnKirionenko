import math
import re
import sqlite3
import pandas as pd


class CsvCurrencies:
    """
    Обрабатывает поля, связанные с вакансиями и объединяет их в одно поле

    Attributes:
        currencies (DataFrame): Таблица с курсами вакансий по месяцам
        cursor (sqlite3.cursor): Курсор БД
        currencies_names (list): Лист с кодами валют
    """

    def __init__(self, file_name: str):
        """
        Инициализирует класс и запускает обработку файла

        Args:
            file_name (str): Имя файла для обработки
        """
        self.currencies = sqlite3.connect('Data/currencies_database.db')
        self.cursor = self.currencies.cursor()
        self.cursor.execute('pragma table_info(currencies)')
        self.currencies_names = self.cursor.fetchall()
        self.currencies_names.append('RUR')
        self.save_vacancies_in_db(file_name)

    def save_vacancies_in_db(self, file_name: str) -> None:
        """
        Сохранят обработанные вакансии в базу данных

        Args:
            file_name: Имя обрабатываемого файла
        """
        vacancies_dataframe = self.handleCsv(file_name)

        connect = sqlite3.connect('Data/vacancies_database.db')
        cursor = connect.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS vacancies (name TEXT)')
        connect.commit()
        vacancies_dataframe.to_sql('vacancies', connect, if_exists='replace')

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

    def get_salary(self, line: pd.Series) -> float:
        """
        Определяет зарплату в зависимости от полей salary_to и salary_from и конвертирует в рубли

        Args:
            line (pd.Series): Серия со всеми полями вакансии
        Returns:
            float: Зарплата
        """
        if line['salary_currency'] not in self.currencies_names:
            return math.nan
        if math.isnan(line['salary_from']) and math.isnan(line['salary_to']):
            return math.nan
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

    def get_currency_rate(self, line: pd.Series) -> float:
        """
        Высчитывает мультипликатор для перевода зарплаты в рубли

        Args:
            line (pd.Series): Серия всех полей вакансии
        Returns:
            float: Мультипликатор для перевода зарплаты в рубли
        """
        return self.cursor.execute(f'SELECT {line["salary_currency"]} FROM currencies WHERE'
                                   f' date = "{self.get_published_at_month_year(line["published_at"])}"').fetchone()[0]

    def clean_line(self, line: pd.Series) -> str:
        """
        Чистит строку от лишних пробелов и html тэгов

        Args:
            line (pd.Series): Серия всех полей вакансии
        Returns:
            str: Очищенная строка
        """
        string = line['area_name']
        string = re.sub('<[^<]+?>', '', string).replace('\xa0', ' ').replace(" ", ' ').strip()
        while '  ' in string:
            string = string.replace('  ', ' ')
        return string

    def get_published_at_month_year(self, line: str) -> str:
        """
        По строке даты возвращает месяц и год в формате MM/YYYY

        Args:
            line: Строка даты
        Returns:
            str: Строка обработанной даты
        """
        return f'{line[5:7]}/{line[:4]}'


CsvCurrencies('Data/vacancies_dif_currencies.csv')
