import calendar
import datetime
import requests
import xmltodict
import pandas as pd
import sqlite3


class Currencies:
    """
    Получает информацию о валютах по файлу, считывает ее в DataFrame
    """
    @staticmethod
    def get_currencies_connection() -> sqlite3.connect:
        """
        Считывает данные о валютах из csv файла и возвращает DataFrame

        Returns:
            DataFrame: Таблица с курсами вакансий
        """
        connection = sqlite3.connect('Data/currencies_database.db')
        return connection


    @staticmethod
    def save_currencies_in_csv(file_name: str) -> None:
        """
        Получает с сайта ЦБ данные по курсам за каждый месяц

        Args:
            file_name (str): Файл, для которого необходимо получить данные по валютам
        """
        min_date, max_date = Currencies.__get_min_max_dates(file_name)
        currencies = Currencies.__get_currencies_with_enough_count(file_name)
        dates = []
        while min_date <= max_date:
            str_date = datetime.datetime.strftime(min_date, "%m/%Y")
            url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{str_date}=1'
            req = requests.get(url).content
            res = xmltodict.parse(req)['ValCurs']['Valute']
            dates.append(str_date)
            for cur in res:
                if cur['CharCode'] in currencies.keys():
                    currencies[cur['CharCode']].append(float(cur['Value'].replace(',', '.')) / float(cur['Nominal']))
                if cur['CharCode'] == 'BYN':
                    currencies['BYR'].append(float(cur['Value'].replace(',', '.')) / float(cur['Nominal']))
            days_in_month = calendar.monthrange(min_date.year, min_date.month)[1]
            min_date += datetime.timedelta(days=days_in_month)
        for key, value in currencies.items():
            print(f'{key} {value}')
        df = pd.DataFrame(data=currencies, index=dates)
        df.index.rename('date', inplace=True)

        df.to_csv('Data/currencies.csv', )

    @staticmethod
    def __get_min_max_dates(file_name: str) -> tuple[datetime, datetime]:
        """
        Получает самую раннюю и позднюю даты по csv файлу

        Args:
            file_name (str): Имя файла, по которому идет поиск
        Returns:
             tuple[datetime, datetime]: Самая ранняя и поздняя даты
        """
        vacancies_dataframe = pd.read_csv(file_name)
        min_date = vacancies_dataframe.agg({'published_at': 'min'})
        max_date = vacancies_dataframe.agg({'published_at': 'max'})
        return min_date, max_date

    @staticmethod
    def __get_currencies_with_enough_count(file_name: str) -> dict[str, list]:
        """
        Считает частотность появления валют и отбирает валюты с частотностью > 5000

        Args:
            file_name (str): Имя файла, по которому собираются данные
        Return:
            dict[str, list]: Словарь с ключом-валютой и значением-листом для последующей обработки
        """
        vacancies_dataframe = pd.read_csv(file_name)
        frequency = vacancies_dataframe.groupby('salary_currency').agg({'salary_currency': 'count'})\
            .query('salary_currency > 5000 & index != "RUR"')
        currencies = {}
        for currency in frequency.index:
            currencies[currency] = []
        return currencies
