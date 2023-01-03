from matplotlib import pyplot as plt

from processing.Statistics import Statistics


class GraphsCreator:
    """
    Класс для создания диаграмм по статистике
    """

    def __init__(self, statistics):
        """
        Генерирует изображение c диаграммами

        Args:
            statistics (Statistics): Статистика по вакансиям
        """
        self.generate_image(statistics)

    def generate_image(self, statistics: Statistics) -> None:
        """
        Генерирует 4 диаграммы и сохраняет их в изображение

        Args:
            statistics (Statistics): Статистика по вакансиям
        """
        self.create_salary_by_year_plot(statistics)
        self.create_prof_salary_by_year_plot(statistics)
        self.create_count_by_year_plot(statistics)
        self.create_prof_count_by_year_plot(statistics)
        # self.create_salary_by_city_plot(statistics)
        # self.create_count_by_city_plot(statistics)
        self.create_skills_count_plot(statistics)

    def create_salary_by_year_plot(self, statistics: Statistics) -> None:
        """
        Генерирует столбчатую диаграмму по уровню зарплат по годам

        Args:
            statistics (Statistics): Статистика по вакансиям
        """
        plt.rcParams['font.size'] = 10
        graph = plt.subplot()
        graph.bar(statistics.years_df.index,
                  statistics.years_df['salary'], width=0.4,
                  label='Средняя з/п')
        plt.xticks(statistics.years_df.index, statistics.years_df.index, rotation=45)
        plt.legend()
        plt.savefig('processing/ProcessingModule/Results/years_salary.png')
        graph.remove()

    def create_prof_salary_by_year_plot(self, statistics: Statistics) -> None:
        """
        Генерирует столбчатую диаграмму по уровню зарплат по годам

        Args:
            statistics (Statistics): Статистика по вакансиям
        """
        plt.rcParams['font.size'] = 10
        graph = plt.subplot()
        graph.bar(statistics.years_df.index,
                  statistics.years_df['prof_salary'], width=0.4,
                  label=f'З/п {statistics.vacancie_name}')
        plt.xticks(statistics.years_df.index, statistics.years_df.index, rotation=45)
        plt.legend()
        plt.savefig('processing/ProcessingModule/Results/years_prof_salary.png')
        graph.remove()

    def create_count_by_year_plot(self, statistics: Statistics) -> None:
        """
        Генерирует столбчатую диаграмму по количеству вакансий по годам

        Args:
            statistics (Statistics): Статистика по вакансиям
        """
        plt.rcParams['font.size'] = 10
        graph = plt.subplot()
        graph.bar(statistics.years_df.index,
                   statistics.years_df['count'], width=0.4,
                   label='Количество вакансий')
        plt.xticks(statistics.years_df.index, statistics.years_df.index, rotation=45)
        plt.legend()
        plt.savefig('processing/ProcessingModule/Results/years_count.png')
        graph.remove()

    def create_prof_count_by_year_plot(self, statistics: Statistics) -> None:
        """
        Генерирует столбчатую диаграмму по количеству вакансий по годам

        Args:
            statistics (Statistics): Статистика по вакансиям
        """
        plt.rcParams['font.size'] = 10
        graph = plt.subplot()
        graph.bar(statistics.years_df.index,
                   statistics.years_df['prof_count'].to_list(), width=0.4,
                   label=f'Количество вакансий {statistics.vacancie_name}')
        plt.xticks(statistics.years_df.index, statistics.years_df.index, rotation=45)
        plt.legend()
        plt.savefig('processing/ProcessingModule/Results/years_prof_count.png')
        graph.remove()


    def create_salary_by_city_plot(self, statistics: Statistics) -> None:
        """
        Генерирует горизонтальную столбчатую диаграмму по уровню зарплат по городам

        Args:
            statistics (Statistics): Статистика по вакансиям
        """
        plt.rcParams['font.size'] = 12
        graph = plt.subplot()
        graph.barh(statistics.cities_salary_df.index, statistics.cities_salary_df['salary'])
        plt.savefig('processing/ProcessingModule/Results/cities_salary.png')
        graph.remove()

    def create_count_by_city_plot(self, statistics: Statistics) -> None:
        """
        Генерирует круговую диаграмму по количеству вакансий по городам

        Args:
            statistics (Statistics): Статистика по вакансиям
        """
        plt.rcParams['font.size'] = 20
        statistics.get_percent_of_other_cities()
        graph = plt.subplot()
        cities_df = statistics.cities_percent_df
        cities_df.loc['Другие'] = statistics.get_percent_of_other_cities()
        graph.pie(cities_df['percent'],
                   labels=cities_df.index,
                   colors=['r', 'g', 'b', 'm', 'y', 'c', 'orange', 'darkblue', 'pink', 'sienna', 'grey'])
        plt.savefig('processing/ProcessingModule/Results/cities_percent.png')
        graph.remove()
    def create_skills_count_plot(self, statistics: Statistics):
        """
        Генерирует столбчатую диаграмму по уровню зарплат по годам

        Args:
            statistics (Statistics): Статистика по вакансиям
        """
        plt.rcParams['font.size'] = 7

        plt.tight_layout()
        graph = plt.subplot()
        graph.patch.set_color('#E5E5E5')
        graph.bar(statistics.skills_df.index,
                  statistics.skills_df['count'], width=0.4,
                  label='Количество упоминаний')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig('processing/ProcessingModule/Results/skills.png')
        graph.remove()


