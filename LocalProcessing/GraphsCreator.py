import pandas as pd
from matplotlib import pyplot as plt


class GraphsCreator:
    """
    Класс для создания диаграмм по статистике
    """

    @staticmethod
    def create_salary_by_year_plot(statistics: pd.DataFrame, name: str) -> None:
        """
        Генерирует столбчатую диаграмму по уровню зарплат по годам

        Args:
            statistics (pd.DataFrame): Статистика уровня зарплат по годам
            name (str): Название статистики
        """
        plt.rcParams['font.size'] = 10
        graph = plt.subplot()
        graph.bar(statistics.index,
                  statistics['salary'], width=0.4,
                  label='Средняя з/п')
        plt.xticks(statistics.index, statistics.index, rotation=45)
        plt.legend()
        plt.savefig(f'Results/{name}.png')
        graph.remove()

    @staticmethod
    def create_prof_salary_by_year_plot(statistics: pd.DataFrame, name: str) -> None:
        """
        Генерирует столбчатую диаграмму по уровню зарплат по годам для заданной профессии

        Args:
            statistics (pd.DataFrame): Статистика уровня зарплат по годам для заданной профессии
            name (str): Название статистики
        """
        plt.rcParams['font.size'] = 10
        graph = plt.subplot()
        graph.bar(statistics.index,
                  statistics['prof_salary'], width=0.4,
                  label=f'З/п PHP разработчик')
        plt.xticks(statistics.index, statistics.index, rotation=45)
        plt.legend()
        plt.savefig(f'Results/{name}.png')
        graph.remove()

    @staticmethod
    def create_count_by_year_plot(statistics: pd.DataFrame, name: str) -> None:
        """
        Генерирует столбчатую диаграмму по количеству вакансий по годам

        Args:
            statistics (pd.DataFrame): Статистика по количеству зарплат по годам
            name (str): Название статистики
        """
        plt.rcParams['font.size'] = 10
        graph = plt.subplot()
        graph.bar(statistics.index,
                   statistics['count'], width=0.4,
                   label='Количество вакансий')
        plt.xticks(statistics.index, statistics.index, rotation=45)
        plt.legend()
        plt.savefig(f'Results/{name}.png')
        graph.remove()

    @staticmethod
    def create_prof_count_by_year_plot(statistics: pd.DataFrame, name: str) -> None:
        """
        Генерирует столбчатую диаграмму по количеству вакансий по годам

        Args:
            statistics (pd.DataFrame): Статистика по количеству зарплат по годам для заданной профессии по годам
            name (str): Название статистики
        """
        plt.rcParams['font.size'] = 10
        graph = plt.subplot()
        graph.bar(statistics.index,
                   statistics['prof_count'].to_list(), width=0.4,
                   label=f'Количество вакансий PHP разработчик')
        plt.xticks(statistics.index, statistics.index, rotation=45)
        plt.legend()
        plt.savefig(f'Results/{name}.png')
        graph.remove()

    @staticmethod
    def create_salary_by_city_plot(statistics: pd.DataFrame, name: str) -> None:
        """
        Генерирует горизонтальную столбчатую диаграмму по уровню зарплат по городам

        Args:
            statistics (pd.DataFrame): Статистика по уровню зарплат по городам
            name (str): Название статистики
        """
        plt.rcParams['font.size'] = 12
        graph = plt.subplot()
        graph.barh(statistics.index, statistics['salary'])
        plt.savefig(f'Results/{name}.png')
        graph.remove()

    @staticmethod
    def create_count_by_city_plot(statistics: pd.DataFrame, name: str) -> None:
        """
        Генерирует круговую диаграмму по количеству вакансий по городам

        Args:
            statistics (pd.DataFrame): Статистика по доле вакансий по городам
            name (str): Название статистики
        """
        plt.rcParams['font.size'] = 12
        graph = plt.subplot()
        cities_df = statistics
        cities_df.loc['Другие'] = 100 - cities_df['percent'].sum()
        graph.pie(cities_df['percent'],
                   labels=cities_df.index,
                   colors=['r', 'g', 'b', 'm', 'y', 'c', 'orange', 'darkblue', 'pink', 'sienna', 'grey'])
        plt.savefig(f'Results/{name}.png')
        graph.remove()

    @staticmethod
    def create_skills_count_plot(skills: pd.DataFrame, name: str):
        """
        Генерирует столбчатую диаграмму по популярности навыков за год

        Args:
            skills (pd.DataFrame): Топ 10 скиллов за год
            name (str): Год, по которому собрана статистика
        """
        plt.rcParams['font.size'] = 7

        plt.tight_layout()
        graph = plt.subplot()
        graph.patch.set_color('#E5E5E5')
        graph.bar(skills.index,
                  skills['count'], width=0.4,
                  label='Количество упоминаний')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'Results/{name}.png')
        graph.remove()


