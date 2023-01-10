import datetime
import math
import re
import sqlite3
import requests

class HHRequests:
    def __init__(self):
        self.currencies = sqlite3.connect('currencies_database.db')
        self.cursor = self.currencies.cursor()
        self.cursor.execute('pragma table_info(currencies)')
        self.currencies_names = self.cursor.fetchall()
        self.currencies_names.append('RUR')
        self.count = 0

    def upload_vacancies_by_day(self, day: str):
        date = datetime.datetime.strptime(f'2022-12-{day}T00:00:00+0000',
                                               '%Y-%m-%dT%H:%M:%S%z')
        delta = datetime.timedelta(hours=6)
        vacancies = []
        date_from = date
        date_to = date + delta
        for i in range(4):
            if self.count == 10:
                break
            if i > 0:
                date_from = date_from + delta
                date_to = date_to + delta
                self.send_request(datetime.datetime.strftime(date_from, '%Y-%m-%dT%H:%M:%S'),
                                  datetime.datetime.strftime(date_to, '%Y-%m-%dT%H:%M:%S'), vacancies)
                if len(vacancies) >= 10:
                    break
        return vacancies


    def send_request(self, date_from: str, date_to: str, vacancies: list):
        url = f'https://api.hh.ru/vacancies?specialization=1&only_with_salary=true&per_page=10' \
              f'&date_from={date_from}&date_to={date_to}&text=PHP&search_field=name'
        req = requests.get(url).json()
        for vacancy in req['items']:
            vacancies.append(self.handle_request(requests.get(f'https://api.hh.ru/vacancies/{vacancy["id"]}').json()))
            if len(vacancies) >= 10:
                break


    def handle_request(self, vacancy: dict) -> dict:
        return { "name": vacancy['name'],
                 "description": re.sub('<[^<]+?>', '', vacancy['description'])
                    if 'description' in vacancy.keys() else '',
                 "skills": ', '.join(map(lambda v: v['name'], vacancy['key_skills']))
                    if 'key_skills' in vacancy.keys() else '',
                 "salary": self.get_salary(vacancy),
                 "company": vacancy['employer']['name'] if 'employer' in vacancy.keys() else '',
                 "published_at": vacancy['published_at'] if 'published_at' in vacancy.keys() else '',
                 "area_name": vacancy['area']['name'] if 'area' in vacancy.keys() else '',
                 "url": vacancy['alternate_url']
        }

    def get_salary(self, line: dict) -> float or None:
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

