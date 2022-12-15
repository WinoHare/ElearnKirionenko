import math
import os
from multiprocessing import Process, Queue
from DataSet import DataSet


class Statistics:
    """
    Класс для сбора статистики по вакансиям

    Attributes:
        vacancie_name (str): Название вакансии, для которой собирается статистика
        salary_by_year (dict): Статистика зарплат по годам
        count_by_year (dict): Статистика количества вакансий по годам
        prof_salary_by_year (dict): Статистика зарплат по годам для заданной профессии
        prof_count_by_year (dict):Статистика количества вакансий по годам для заданной профессии
        salary_by_city (dict): Статистика зарплат по городам
        count_by_city (dict): Статистика количества вакансий по городам
        vacancies_count (int): Общее количество вакансий, вошедших в выборку
    """

    def __init__(self, vacancie_name: str):
        """
        Инициализирует класс, получает данные по вакансиям
        """
        self.vacancie_name = vacancie_name
        self.salary_by_year = {}
        self.count_by_year = {}
        self.prof_salary_by_year = {}
        self.prof_count_by_year = {}
        self.salary_by_city = {}
        self.count_by_city = {}
        self.vacancies_count = 0

    def get_statistics(self) -> None:
        """
        Собирает все статистику
        """
        all_stats = self.start_multiprocessing()
        self.union_stats(all_stats)
        self.get_average_salary(self.salary_by_city, self.count_by_city)
        self.get_percentage_of_total(self.count_by_city, self.vacancies_count)
        self.get_cities_with_enough_count()
        self.sort_statistics()
        self.print_stats()

    def start_multiprocessing(self) -> list:
        """
        Запускает потоки для сбора статистики

        Returns:
             list: Список статистик для каждого года
        """
        chunks_names = os.listdir('Chunks')
        procs = []
        stats_queue = Queue()
        count_queue = Queue()
        all_stats = []

        for chunk in chunks_names:
            p = Process(target=self.get_statistics_in_thread, args=(chunk, stats_queue, count_queue))
            procs.append(p)
            p.start()

        for p in procs:
            p.join(0.75)

        while not stats_queue.empty():
            all_stats.append(stats_queue.get())
        while not count_queue.empty():
            self.vacancies_count += count_queue.get()
        return all_stats

    def get_statistics_in_thread(self, file_name: str, stats_queue: Queue, count_queue: Queue) -> None:
        """
        Собирает статистику по вакансиям в потоке

        Args:
            file_name (str): Имя обрабатываемого файла
            stats_queue (Queue):Многопоточная очередь, содержащая статистику для текущего файла
            count_queue (Queue): Многопоточная очередь, содержащая количество вакансий для текущего файла
        """
        vacancies = DataSet(f'Chunks/{file_name}').vacancies_objects
        count = len(vacancies)
        year = int(file_name[:4])
        stats = {'salary_by_year': {}, 'count_by_year': {}, 'prof_salary_by_year': {}, 'prof_count_by_year': {},
                 'salary_by_city': {}, 'count_by_city': {}}

        for vacancy in vacancies:
            self.update_stats(year, vacancy.salary, stats['salary_by_year'])
            self.update_stats(year, 1, stats['count_by_year'])
            if self.vacancie_name in vacancy.name:
                self.update_stats(year, vacancy.salary,
                                  stats['prof_salary_by_year'])
                self.update_stats(year, 1, stats['prof_count_by_year'])
            self.update_stats(vacancy.area_name, vacancy.salary, stats['salary_by_city'])
            self.update_stats(vacancy.area_name, 1, stats['count_by_city'])
        self.get_average_salary(stats['salary_by_year'], stats['count_by_year'])
        self.get_average_salary(stats['prof_salary_by_year'], stats['prof_count_by_year'])
        stats_queue.put(stats)
        count_queue.put(count)


    def union_stats(self, stats: list) -> None:
        """
        Объединяет список статистик в одну

        Args:
            stats (list): Список статистик
        """
        for stat in stats:
            for name, child_dict in stat.items():
                for key, value in child_dict.items():
                    if name == 'salary_by_year':
                        self.salary_by_year[key] = value
                    if name == 'count_by_year':
                        self.count_by_year[key] = value
                    if name == 'prof_salary_by_year':
                        self.prof_salary_by_year[key] = value
                    if name == 'prof_count_by_year':
                        self.prof_count_by_year[key] = value
                    if name == 'salary_by_city':
                        self.update_stats(key, value, self.salary_by_city)
                    if name == 'count_by_city':
                        self.update_stats(key, value, self.count_by_city)

    def update_stats(self, key: int or str, value: int or float, stats: dict) -> None:
        """Обновляет статистику для новой вакансии

        Args:
            key (str or int): Ключ, для которого необходимо обновить статистику
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
        """
        Сортирует статистику
        """
        self.salary_by_year = dict(sorted(self.salary_by_year.items(), key=lambda x: x[0]))
        self.count_by_year = dict(sorted(self.count_by_year.items(), key=lambda x: x[0]))
        self.prof_salary_by_year = dict(sorted(self.prof_salary_by_year.items(), key=lambda x: x[0]))
        self.prof_count_by_year = dict(sorted(self.prof_count_by_year.items(), key=lambda x: x[0]))
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

