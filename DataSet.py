import csv
import math
import re
from VacancyInf.Vacancie import Vacancie

"""Рейтинг опыта работы"""
experience_rate = {"noExperience": 0, "between1And3": 1, "between3And6": 2, "moreThan6": 3}


class DataSet:
    """
    Класс для обработки csv файла

    Attributes:
        is_empty (bool): Показывает, пустой ли файл
        error_massage (str): Сообщение об ошибке
        file_name (str): Имя обрабатываемого файла
        vacancies_objects (list): Объекты вакансий
    """
    def __init__(self, file_name):
        """
        Инициализирует объект DataSet, парсит csv файл

        Args:
            file_name (str): Имя обрабатываемого файла
        """
        self.is_empty = False
        self.error_massage = ''
        self.file_name = file_name
        self.vacancies_objects = self.csv_reader()

    def csv_reader(self) -> tuple or str:
        """
        Проходится по csv файлу и парсит данные

        Returns:
             list or str: Возвращает список вакансий либо строку в случае ошибки
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
        """
        Проверяет строку на пустые ячейки и наличие всех ячеек

        Args:
            line (list): Строка для проверки
            header_length (int): Необходимое количество ячеек
        Returns:
             bool: Значение, корректна ли строка
        """
        return '' not in line and len(line) == header_length

    def clean_line(self, line: str) -> str:
        """
        Чистит строку от лишних пробелов и html тэгов

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
        """
        Очищает все строки csv таблицы и превращает их в объекты вакансий

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
            vacancies.append(Vacancie(vacancies_dict))
        return vacancies

