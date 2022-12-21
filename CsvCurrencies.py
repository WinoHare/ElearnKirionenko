import math
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
        self.handleCsv(file_name)

    def handleCsv(self, file_name: str) -> None:
        """
        Создает новый файл со средними зарплатами в рублях

        Args:
            file_name (str): Имя обрабатываемого файла
        """
        vacancies_dataframe = pd.read_csv(file_name)
        vacancies_dataframe['salary'] = vacancies_dataframe.apply(lambda v: self.get_salary(v), axis=1)
        vacancies_dataframe = vacancies_dataframe.dropna(subset=['salary'])

        vacancies_dataframe[['name', 'salary', 'area_name', 'published_at']]\
            .to_csv('Data/csv_vacancies.csv', float_format='%.0f', index=False)

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
            return salary * float(self.currencies.loc[self.get_published_at_month_year(line['published_at'])]
                                  [line['salary_currency']])
        else:
            return salary

    def get_published_at_month_year(self, line: str) -> str:
        return f'{line[5:7]}/{line[:4]}'

CsvCurrencies('Data/vacancies_dif_currencies.csv')