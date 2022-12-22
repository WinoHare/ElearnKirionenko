import math
import os
from multiprocessing import Process, Queue
import pandas as pd


class Statistics:
    """
    Класс для сбора статистики по вакансиям

    Attributes:
        vacancie_name (str): Название вакансии, для которой собирается статистика
        area_name (str): Название региона, для которого собирается статистика
        vacancies_count (int): Общее количество вакансий, вошедших в выборку
        years_dataframe (DataFrame): Фрейм со статистиками по годам
        cities_dataframe (DataFrame): Фрейм со статистиками по городам
    """

    def __init__(self, vacancie_name: str, area_name: str):
        """
        Инициализирует класс, получает данные по вакансиям

        Args:
            vacancie_name (str): Название вакансии, для которой собирается статистика
            area_name (str): Название региона, для которого собирается статистика
        """
        self.vacancie_name = vacancie_name
        self.area_name = area_name
        self.vacancies_count = 0
        self.years_dataframe = pd.DataFrame(columns=['salary', 'prof_salary', 'count', 'prof_count'])
        self.cities_dataframe = pd.DataFrame(columns=['salary', 'count'])
        self.years_dataframe.index.rename('year', inplace=True)

    def get_statistics(self) -> None:
        """
        Собирает все статистику
        """
        self.__start_multiprocessing()
        self.years_dataframe = self.years_dataframe.sort_index() \
            .assign(salary=lambda df: [math.floor(c) for c in df['salary']]) \
            .assign(prof_salary=lambda df: [math.floor(c) for c in df['prof_salary']])
        self.vacancies_count = self.years_dataframe['count'].sum()
        self.__get_percentage_of_total()

    def __start_multiprocessing(self) -> None:
        """
        Запускает потоки для сбора статистики
        """
        processes = []
        queue = Queue()

        for chunk in os.listdir('Chunks'):
            process = Process(target=self.get_statistics_in_thread, name=chunk, args=(chunk, queue))
            processes.append(process)
            process.start()

        for process in processes:
            process.join(0.35)

        while not queue.empty():
            self.__union_stats(queue.get())

    def get_statistics_in_thread(self, file_name: str, queue: Queue) -> None:
        """
        Собирает статистику по вакансиям в потоке

        Args:
            file_name (str): Имя обрабатываемого файла
            queue (Queue):Многопоточная очередь, содержащая статистику текущего файла
        """
        vacancies_dataframe = pd.read_csv(f'Chunks/{file_name}')
        year = int(file_name[:4])
        year_stats = self.__get_year_stats(vacancies_dataframe, year)
        cities_stats = self.__get_cities_stats(vacancies_dataframe)

        queue.put((year_stats, cities_stats))

    def __union_stats(self, stats: tuple[pd.Series, pd.DataFrame]) -> None:
        """
        Объединяет список статистик в одну

        Args:
            stats (tuple[pd.Series, pd.DataFrame]): Кортеж из статистики по году и по городам
        """
        self.years_dataframe.loc[stats[0]['year']] = stats[0]
        self.cities_dataframe = self.cities_dataframe.add(stats[1], fill_value=0)

    def __get_year_stats(self, vacancies: pd.DataFrame, year: int) -> pd.Series:
        """
        Обновляет статистику для новой вакансии для текущего года

        Args:
            vacancies: Фрейм вакансий, по которым необходимо получить статистику
        """
        year_stats = pd.Series(index=['year', 'salary', 'prof_salary', 'count', 'prof_count'], data=[year, 0, 0, 0, 0])
        salary = vacancies.agg({'salary': 'mean'}).values[0]
        year_stats['salary'] = math.floor(salary) if not math.isnan(salary) else 0
        count = vacancies.shape[0]
        year_stats['count'] = math.floor(count) if not math.isnan(count) else 0
        prof_salary = vacancies[(vacancies['name'].str.contains(self.vacancie_name))
                                & (vacancies['area_name'].str.contains(self.area_name))] \
                                 .agg({'salary': 'mean'}).values[0]
        year_stats['prof_salary'] = math.floor(prof_salary) if not math.isnan(prof_salary) else 0
        prof_count = vacancies[(vacancies['name'].str.contains(self.vacancie_name))
                                & (vacancies['area_name'].str.contains(self.area_name))].shape[0]
        year_stats['prof_count'] = math.floor(prof_count) if not math.isnan(prof_count) else 0
        return year_stats

    def __get_cities_stats(self, vacancies: pd.DataFrame) -> pd.DataFrame:
        """
        Обновляет статистику для новой вакансии для текущего года

        Args:
            vacancies: Фрейм вакансий, по которым необходимо получить статистику
        """
        cities_stats = vacancies.groupby('area_name').agg({'salary': 'mean', 'area_name': "count"})
        cities_stats.index.rename('city', inplace=True)
        cities_stats.rename(columns={'area_name': 'count'}, inplace=True)
        return cities_stats

    def __get_percentage_of_total(self) -> None:
        """
        Считает процент количества вакансий по городам от общего количества
        """
        self.cities_dataframe = self.cities_dataframe.assign(salary=lambda df: [math.floor(c) for c in df['salary']]) \
            .assign(percent=lambda df: df['count'] / self.vacancies_count * 100) \
            .assign(percent=lambda df: [round(c, 2) for c in df['percent']]) \
            .query('percent > 1')

    def sort_dataframe(self, by: str) -> pd.DataFrame:
        """
        Сортирует фрейм по переданному столбцу и отбирает первые 10 значений

        Args:
            by (str): Столбец, по которому происходит сортировка
        Returns:
            pd. DataFrame: Отсортированный фрейм
        """
        return self.cities_dataframe.sort_values(by=by, ascending=False).head(10)

    def get_percent_of_other_cities(self) -> float:
        """
        Считает процент городов, не вошедших в статистику

        Returns:
            float: Процент городов, не вошедших в статистику
        """
        return 100 - self.cities_dataframe['percent'].sum()
