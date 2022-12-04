import math
from DataSet import DataSet


class Statistics:
    """Класс для сбора статистики по вакансиям

    Attributes:
        vacancies (list): Список вакансий
        vacancie_name (str): Название вакансии, для которой собирается статистика
        salary_by_year (dict): Статистика зарплат по годам
        count_by_year (dict): Статистика количества вакансий по годам
        prof_salary_by_year (dict): Статистика зарплат по годам для заданной профессии
        prof_count_by_year (dict):Статистика количества вакансий по годам для заданной профессии
        salary_by_city (dict): Статистика зарплат по городам
        count_by_city (dict): Статистика количества вакансий по городам
    """

    def __init__(self, file_name: str, vacancie_name: str):
        """Инициализирует класс, получает данные по вакансиям

        Args:
            file_name (str): Имя csv файла, откуда взять вакансии
        """
        self.vacancies = DataSet(file_name).vacancies_objects
        self.vacancie_name = vacancie_name
        self.salary_by_year = {}
        self.count_by_year = {}
        self.prof_salary_by_year = {}
        self.prof_count_by_year = {}
        self.salary_by_city = {}
        self.count_by_city = {}

    def get_statistics(self) -> None:
        """Собирает статистику по вакансиям и выводит ее в консоль"""
        for vacancy in self.vacancies:
            self.update_stats(vacancy.get_published_at_year(), vacancy.salary.average_salary, self.salary_by_year)
            self.update_stats(vacancy.get_published_at_year(), 1, self.count_by_year)
            self.update_stats(vacancy.area_name, vacancy.salary.average_salary, self.salary_by_city)
            self.update_stats(vacancy.area_name, 1, self.count_by_city)
            if self.vacancie_name in vacancy.name:
                self.update_stats(vacancy.get_published_at_year(), vacancy.salary.average_salary,
                                  self.prof_salary_by_year)
                self.update_stats(vacancy.get_published_at_year(), 1, self.prof_count_by_year)

        self.get_average_salary(self.salary_by_year, self.count_by_year)
        self.get_average_salary(self.prof_salary_by_year, self.prof_count_by_year)
        self.get_average_salary(self.salary_by_city, self.count_by_city)
        self.get_percentage_of_total(self.count_by_city, len(self.vacancies))

        self.get_cities_with_enough_count()
        self.sort_statistics()
        self.print_stats()

    def update_stats(self, key: str, value: int or float, stats: dict) -> None:
        """Обновляет статистику для новой вакансии

        Args:
            key (str): Ключ, для которого необходимо обновить статистику
            value (int or float): На сколько необходимо увеличить статистику
            stats (dict): Для какой статистики необходимо обновить данные
        """
        if key in stats.keys():
            stats[key] += value
        else:
            stats[key] = value

    def get_average_salary(self, salary_stats: dict, count_stats: dict) -> None:
        """Считает среднюю зарплату для каждого ключа статистики

        Args:
            salary_stats (dict): Статистика зарплат
            count_stats (dict): Статистика количества вакансий
        """
        for key in count_stats.keys():
            salary_stats[key] = math.floor(salary_stats[key] / count_stats[key])

    def get_percentage_of_total(self, stats: dict, count: int) -> None:
        """Считает процент количества вакансий по городам от общего количества

        Args:
            stats (dict): Статистика для изменения
            count (int): Общее количество вакансий
        """
        for key in stats.keys():
            stats[key] = round(stats[key] / count, 4)

    def get_cities_with_enough_count(self) -> None:
        """Отбирает города с достаточным количеством вакансий"""
        new_salary_by_city = {}
        new_count_by_city = {}
        for key, value in self.count_by_city.items():
            if value * 100 < 1:
                continue
            new_salary_by_city[key] = self.salary_by_city[key]
            new_count_by_city[key] = value
        self.salary_by_city = new_salary_by_city
        self.count_by_city = new_count_by_city

    def sort_statistics(self) -> None:
        """Сортирует статистику"""
        self.prof_salary_by_year = self.prof_salary_by_year if len(self.prof_salary_by_year) != 0 else {2022: 0}
        self.prof_count_by_year = self.prof_count_by_year if len(self.prof_count_by_year) != 0 else {2022: 0}
        self.salary_by_city = dict(sorted(self.salary_by_city.items(), key=lambda x: x[1], reverse=True)[:10])
        self.count_by_city = dict(sorted(self.count_by_city.items(), key=lambda x: x[1], reverse=True)[:10])

    def get_percent_of_other_cities(self) -> None:
        """Считает процент городов, не вошедших в статистику"""
        others_percent = 1
        for city_percent in self.count_by_city.values():
            others_percent -= city_percent
        self.count_by_city['Другие'] = others_percent

    def print_stats(self) -> None:
        """Выводит в консоль статистику"""
        print('Динамика уровня зарплат по годам:', self.salary_by_year)
        print('Динамика количества вакансий по годам:', self.count_by_year)
        print('Динамика уровня зарплат по годам для выбранной профессии:', self.prof_salary_by_year)
        print('Динамика количества вакансий по годам для выбранной профессии:', self.prof_count_by_year)
        print('Уровень зарплат по городам (в порядке убывания):', self.salary_by_city)
        print('Доля вакансий по городам (в порядке убывания):', self.count_by_city)