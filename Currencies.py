import calendar
import csv
import datetime
import requests
import xmltodict
import pandas as pd


class Currencies:
    """
    Получает информацию о валютах по файлу, считывает ее в DataFrame
    """
    @staticmethod
    def get_currencies_in_dataframe() -> pd.DataFrame:
        """
        Считывает данные о валютах из csv файла и возвращает DataFrame

        Returns:
            DataFrame: Таблица с курсами вакансий
        """
        csv_file = pd.read_csv('Data/currencies.csv', index_col='date')
        return pd.DataFrame(csv_file)

    @staticmethod
    def save_currencies_in_csv(file_name: str) -> None:
        """
        Получает с сайта ЦБ данные по курсам за каждый месяц

        Args:
            file_name (str): Файл, для которого необходимо получить данные по валютам
        """
        min_date, max_date = Currencies.__get_min_max_dates(file_name)
        dates = []
        currencies = Currencies.__get_currencies_with_enough_count(file_name)
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
        df = pd.DataFrame(data=currencies, index=dates)
        df.to_csv('Data/currencies')

    @staticmethod
    def __get_min_max_dates(file_name: str) -> tuple[datetime, datetime]:
        """
        Получает самую раннюю и позднюю даты по csv файлу

        Args:
            file_name (str): Имя файла, по которому идет поиск
        Returns:
             tuple[datetime, datetime]: Самая ранняя и поздняя даты
        """
        min_date = datetime.datetime.strptime('3000-01-01T00:00:00+0000', '%Y-%m-%dT%H:%M:%S%z')
        max_date = datetime.datetime.strptime('1000-01-01T00:00:00+0000', '%Y-%m-%dT%H:%M:%S%z')
        with open(file_name, encoding='utf-8') as csv_file:
            file = csv.reader(csv_file)
            for line in file:
                date = datetime.datetime.strptime(line[5], '%Y-%m-%dT%H:%M:%S%z')
                if date > max_date:
                    max_date = date
                if date < min_date:
                    min_date = date
        min_date = datetime.datetime.strptime(f'{min_date.month}/{min_date.year}', '%m/%Y')
        max_date = datetime.datetime.strptime(f'{max_date.month}/{max_date.year}', '%m/%Y')
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
        currencies = {}
        with open(file_name, encoding='utf-8') as csv_file:
            file = csv.reader(csv_file)
            for line in file:
                cur = line[4]
                if cur in currencies.keys():
                    currencies[cur] += 1
                else:
                    currencies[cur] = 1
        result_currencies = {}
        for key, value in currencies.items():
            if value > 5000:
                result_currencies[key] = []
        return result_currencies
