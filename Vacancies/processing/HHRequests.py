import datetime
import math
import pandas as pd
import requests
from prof_stats.models import LatestVacancies
from processing.Currencies import Currencies



class HHRequests:
    def __init__(self):
        self.currencies = Currencies.get_currencies_connection()
        self.cursor = self.currencies.cursor()
        self.cursor.execute('pragma table_info(currencies)')
        self.currencies_names = self.cursor.fetchall()
        self.currencies_names.append('RUR')
        self.count = 0
        self.upload_vacancies_by_day()

    def write_to_model(self, vacancies: list[dict]):
        LatestVacancies.objects.all().delete()
        for item in vacancies:
            LatestVacancies.objects.create(name=item['name'], description=['description'], skills=item['skills'],
                                           salary=item['salary'], company=item['company'],
                                           published_at=item['published_at'], area_name=item['area_name'], url=item['alternate_url'])

    def upload_vacancies_by_day(self):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        yesterday = datetime.datetime.strptime(f'{yesterday.year}-{yesterday.month}-{yesterday.day}T00:00:00+0000',
                                               '%Y-%m-%dT%H:%M:%S%z')
        delta = datetime.timedelta(hours=6)
        vacancies = []
        date_from = yesterday
        date_to = yesterday + delta
        print(date_from)
        print(date_to)
        for i in range(4):
            if self.count == 10:
                break
            if i > 0:
                date_from = date_from + delta
                date_to = date_to + delta
            for j in range(20):
                vac = self.send_request(j, datetime.datetime.strftime(date_from, '%Y-%m-%dT%H:%M:%S'),
                                        datetime.datetime.strftime(date_to, '%Y-%m-%dT%H:%M:%S'))
                vacancies += vac
                if self.count == 10:
                    break
        self.write_to_model(vacancies)


    def send_request(self, page: int, date_from: str, date_to: str):
        url = f'https://api.hh.ru/vacancies?specialization=1&only_with_salary=true&per_page=100&page={page}' \
              f'&date_from={date_from}&date_to={date_to}&text=PHP&search_field=name'
        req = requests.get(url).json()
        return self.handle_request(req)

    def handle_request(self, request: dict) -> list:
        vacancies = []
        for vacancy in request['items']:
            self.count += 1
            vacancies.append({
                'name': vacancy['name'],
                'description': vacancy['description'] if 'description' in vacancy.keys() else '',
                'skills': vacancy['key_skills'].replace('\n', ', ') if 'key_skills' in vacancy.keys() else '',
                'company': vacancy['employer']['name'] if 'employer' in vacancy.keys() else '',
                'salary': self.get_salary(vacancy),
                'area_name': vacancy['area']['name'] if 'area' in vacancy.keys() else '',
                'published_at': vacancy['published_at'] if 'published_at' in vacancy.keys() else '',
                'alternate_url': vacancy['alternate_url'],
            })
            if self.count == 10:
                break
        return vacancies

    def get_salary(self, line: pd.Series) -> float or None:
        """
        Определяет зарплату в зависимости от полей salary_to и salary_from и конвертирует в рубли

        Args:
            line (list): Словарь для всех полей вакансии
        Returns:
            float or None: Зарплата
        """
        if line['salary']['currency'] not in self.currencies_names:
            return 0
        if line['salary']['from'] is None and line['salary']['to'] is None:
            return 0
        elif line['salary']['from'] is None:
            salary = float(line['salary']['to'])
        elif line['salary']['to'] is None:
            salary = float(line['salary']['from'])
        else:
            salary = ((float(line['salary']['from']) + float(line['salary']['to'])) / 2)
        if line['salary']['currency'] != 'RUR':
            return math.floor(salary * self.get_currency_rate(line))
        else:
            return math.floor(salary)

    def get_currency_rate(self, line):
        return self.cursor.execute(f'SELECT {line["salary_currency"]} FROM currencies WHERE'
                                   f' date = "{self.get_published_at_month_year(line["published_at"])}"')\
            .fetchone()[0]

    def get_published_at_month_year(self, line: str) -> str:
        return f'{line[5:7]}/{line[:4]}'
