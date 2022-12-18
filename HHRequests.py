import csv
import datetime
import pandas as pd
import requests


class HHRequests:
    def __init__(self):
        req = self.upload_vacancies_by_day(datetime.datetime.strptime('2022-12-01T00:00:00+0000', '%Y-%m-%dT%H:%M:%S%z'))
        self.write_to_csv(req)

    def write_to_csv(self, vacancies: list[dict]):
        with open('Data/hh_results.csv', 'w', encoding='utf-8', newline='') as csv_file:
            file = csv.writer(csv_file)
            file.writerow(vacancies[0].keys())
            for vacancie in vacancies:
                file.writerow(vacancie.values())


    def upload_vacancies_by_day(self, date: datetime):
        delta = datetime.timedelta(hours=6)
        vacancies = []
        date_from = date
        date_to = date + delta
        for i in range(4):
            if i > 0:
                date_from = date_from + delta
                date_to = date_to + delta
            for j in range(20):
                vac = self.send_request(j, datetime.datetime.strftime(date_from, '%Y-%m-%dT%H:%M:%S'),
                                        datetime.datetime.strftime(date_to, '%Y-%m-%dT%H:%M:%S'))
                vacancies += vac
        return vacancies


    def send_request(self, page: int, date_from: str, date_to: str):
        url = f'https://api.hh.ru/vacancies?specialization=1&only_with_salary=true&per_page=100&page={page}' \
              f'&date_from={date_from}&date_to={date_to}'
        req = requests.get(url).json()
        return self.handle_request(req)

    def handle_request(self, request: dict) -> list:
        vacancies = []
        for vacancy in request['items']:
            vacancies.append({
                'name': vacancy['name'],
                'salary_from': vacancy['salary']['from'] if vacancy['salary']['from'] is not None else '',
                'salary_to': vacancy['salary']['to'] if vacancy['salary']['to'] is not None else '',
                'salary_currency': vacancy['salary']['currency'] if vacancy['salary']['currency'] is not None else '',
                'area_name': vacancy['area']['name'],
                'published_at': vacancy['published_at']
            })
        return vacancies

HHRequests()