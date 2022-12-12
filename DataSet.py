import csv
import math
import re
from VacancyInf.Vacancy import Vacancy

"""Рейтинг опыта работы"""
experience_rate = {"noExperience": 0, "between1And3": 1, "between3And6": 2, "moreThan6": 3}


class DataSet:
    """Класс для обработки csv файла

    Attributes:
        is_empty (bool): Показывает, пустой ли файл
        error_massage (str): Сообщение об ошибке
        file_name (str): Имя обрабатываемого файла
        vacancies_objects (list): Объекты вакансий
    """
    def __init__(self, file_name):
        """Инициализирует объект DataSet, парсит csv файл

        Args:
            file_name (str): Имя обрабатываемого файла
        """
        self.is_empty = False
        self.error_massage = ''
        self.file_name = file_name
        self.vacancies_objects = self.csv_reader()

    @property
    def filter_parameters(self):
        return {
            '': lambda vacancies, some_param: vacancies,
            "Навыки": lambda vacancies, skills: filter(lambda v: all(s in v.key_skills for s in skills), vacancies),
            "Оклад": lambda vacancies, salary:
            filter(
                lambda v: math.floor(v.salary.salary_from) <= math.floor(float(salary)) <= math.floor(v.salary.salary_to),
                vacancies),
            "Дата публикации вакансии": lambda vacancies, date:
            filter(lambda v: f'{v.published_at[8:10]}.{v.published_at[5:7]}.{v.published_at[0:4]}' == date, vacancies),
            "Опыт работы": lambda vacancies, experience:
            filter(lambda v: v.experience_id == v.reversedTranslate[experience], vacancies),
            "Премиум-вакансия": lambda vacancies, premium: filter(lambda v: v.premium == v.reverse_premium(premium),
                                                                  vacancies),
            "Идентификатор валюты оклада": lambda vacancies, currency:
            filter(lambda v: v.salary.salary_currency == v.reversedTranslate[currency], vacancies),
            "Название": lambda vacancies, name: filter(lambda v: v.name == name, vacancies),
            "Название региона": lambda vacancies, area: filter(lambda v: v.area_name == area, vacancies),
            "Компания": lambda vacancies, employer_name: filter(lambda v: v.employer_name == employer_name, vacancies)
        }

    @property
    def sort_parameters(self):
        return {
            'Название': lambda v: v.name,
            'Описание': lambda v: v.description,
            'Навыки': lambda v: len(v.key_skills),
            'Опыт работы': lambda v: experience_rate[v.experience_id],
            'Премиум-вакансия': lambda v: v.premium,
            'Компания': lambda v: v.employer_name,
            'Оклад': lambda v: v.salary.average_salary,
            'Название региона': lambda v: v.area_name,
            'Дата публикации вакансии': lambda v:
            (f'{v.published_at[0:4]}.{v.published_at[5:7]}.{v.published_at[8:10]}',
             f'{v.published_at[11:13]}.{v.published_at[14:16]}.{v.published_at[17:19]}')
        }

    def csv_reader(self) -> tuple or str:
        """Проходится по csv файлу и парсит данные

        :return: list or str: Возвращает список вакансий либо строку в случае ошибки
        """
        with open(self.file_name, encoding='utf-8') as csv_file:
            file = csv.reader(csv_file)
            vacancies = []
            header = next(file)
            header_length = len(header)
            for row in file:
                if self.is_correct_line(row, header_length):
                    vacancies.append(row)
            csv_file.close()
        if len(header) == 0:
            self.is_empty = True
            self.error_massage = 'Пустой файл'
        elif len(vacancies) == 0:
            self.is_empty = True
            self.error_massage = 'Нет данных'
        return self.formatter(header, vacancies)

    def is_correct_line(self, line: list, header_length: int) -> bool:
        """Проверяет строку на пустые ячейки и наличие всех ячеек

        Args:
            line (list): Строка для проверки
            header_length (int): Необходимое количество ячеек
        Returns:
             bool: Значение, корректна ли строка
        """
        return '' not in line and len(line) == header_length

    def clean_line(self, line: str) -> str:
        """Чистит строку от лишних пробелов и html тэгов

        Args:
            line (str): Строка для очистки
        Returns:
            str: Очищенная строка
        """
        line = re.sub('<[^<]+?>', '', line).replace('\xa0', ' ').replace(" ", ' ').strip()
        while '  ' in line:
            line = line.replace('  ', ' ')
        return line

    def formatter(self, header: list, rows: list) -> list:
        """Очищает все строки csv таблицы и превращает их в объекты вакансий

        Args:
            header (list): Список заголовков
            rows (list): Список строк
        Returns:
             list: Список вакансий
        """
        vacancies = []
        for row in rows:
            vacancies_dict = {}
            for i in range(len(header)):
                vacancies_dict[header[i]] = self.clean_line(row[i])
            vacancies.append(Vacancy(vacancies_dict))
        return vacancies

    def filter_sort_data(self, filter_key: str, filter_value: str, sort_param: str, is_rev):
        """Фильтрует и сортирует вакансии по заданным параметрам

        Args:
            filter_key (str): Ключ, по которому будет произведена фильтрация (Название столбца)
            filter_value (str): Значение, по которому будет происходить фильтрация
            sort_param (str): Название столбца по которому будет произведена сортировка
            is_rev (bool): Значение, определяющее порядок сортировки
        """
        self.vacancies_objects = list(self.filter_parameters[filter_key](self.vacancies_objects, filter_value))
        self.vacancies_objects = self.vacancies_objects if sort_param == '' \
            else sorted(self.vacancies_objects, key=self.sort_parameters[sort_param], reverse=is_rev)

