import re
import pandas as pd
from VacancyInf.Vacancy import Vacancy

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

    def csv_reader(self) -> list:
        """
        Проходится по csv файлу и парсит данные

        Returns:
             list: Возвращает список вакансий
        """
        csv_dataframe = pd.read_csv(self.file_name)
        header = list(csv_dataframe)
        header_length = len(header)
        vacancies = []
        for line in csv_dataframe.itertuples():
            line = line[1:]
            if self.is_correct_line(line, header_length):
                vacancies.append(line)
        self.check_for_error(header_length, vacancies)
        return self.formatter(header, vacancies)

    def check_for_error(self, header_length: int, vacancies: list) -> None:
        """
        Проверяет, пустой ли файл

        Args:
            header_length (int): Длина зоголовка
            vacancies (list): Список вакансий
        """
        if header_length == 0:
            self.is_empty = True
            self.error_massage = 'Пустой файл'
        elif len(vacancies) == 0:
            self.is_empty = True
            self.error_massage = 'Нет данных'

    def is_correct_line(self, line: tuple, header_length: int) -> bool:
        """
        Проверяет строку на пустые ячейки и наличие всех ячеек

        Args:
            line (tuple): Строка для проверки
            header_length (int): Необходимое количество ячеек
        Returns:
             bool: Значение, корректна ли строка
        """
        return len(list(filter(None, line))) >= header_length - 1

    def clean_line(self, line: str) -> str:
        """
        Чистит строку от лишних пробелов и html тэгов

        Args:
            line (str): Строка для очистки
        Returns:
            str: Очищенная строка
        """
        if type(line) == str:
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
            vacancies.append(Vacancy(vacancies_dict))
        return vacancies

