from matplotlib import pyplot as plt

from Statistics import Statistics


class GraphsCreator:
    """
    Класс для создания диаграмм по статистике
    """

    def __init__(self, stats):
        """
        Генерирует изображение c диаграммами

        Args:
            stats (Statistics): Статистика по вакансиям
        """
        self.generate_image(stats)

    def generate_image(self, stats: Statistics) -> None:
        """
        Генерирует 4 диаграммы и сохраняет их в изображение

        Args:
            stats (Statistics): Статистика по вакансиям
        """
        plt.subplots(figsize=(10, 7))
        plt.grid(True)

        self.create_salary_by_year_plot(stats)
        self.create_count_by_year_plot(stats)

        plt.subplots_adjust(wspace=0.5, hspace=0.5)
        plt.savefig('ReportModule/Results/graph.png')

    def create_salary_by_year_plot(self, stats: Statistics) -> None:
        """
        Генерирует столбчатую диаграмму по уровню зарплат по годам

        Args:
            stats (Statistics): Статистика по вакансиям
        """
        first = plt.subplot(221)
        plt.tick_params(axis='x', which='major', labelsize=8, rotation=90)
        plt.tick_params(axis='y', which='major', labelsize=8)
        first.bar(list(map(lambda y: y - 0.2, stats.stats.index)),
                  stats.stats['salary_by_year'], width=0.4,
                  label='Средняя з/п')
        first.bar(list(map(lambda y: y + 0.2, stats.stats.index)),
                  stats.stats['prof_salary_by_year'], width=0.4,
                  label=f'З/п {stats.vacancie_name}')
        plt.legend(fontsize=8)
        plt.title('Уровень зарплат по годам', fontsize=12)

    def create_count_by_year_plot(self, stats: Statistics) -> None:
        """
        Генерирует столбчатую диаграмму по количеству вакансий по годам

        Args:
            stats (Statistics): Статистика по вакансиям
        """
        second = plt.subplot(222)
        plt.tick_params(axis='x', which='major', labelsize=8, rotation=90)
        plt.tick_params(axis='y', which='major', labelsize=8)
        second.bar(list(map(lambda y: y - 0.2, stats.stats.index)),
                   stats.stats['count_by_year'], width=0.4,
                   label='Количество вакансий')
        second.bar(list(map(lambda y: y + 0.2, stats.stats.index)),
                   stats.stats['prof_count_by_year'], width=0.4,
                   label=f'Количество вакансий {stats.vacancie_name}')
        plt.legend(fontsize=8)
        plt.title('Количество вакансий по годам', fontsize=12)

    def create_salary_by_city_plot(self, stats: Statistics) -> None:
        """
        Генерирует горизонтальную столбчатую диаграмму по уровню зарплат по городам

        Args:
            stats (Statistics): Статистика по вакансиям
        """
        third = plt.subplot(223)
        plt.tick_params(axis='x', which='major', labelsize=8)
        plt.tick_params(axis='y', which='major', labelsize=6)
        third.barh(list(reversed(stats.salary_by_city.keys())),
                   list(reversed(stats.salary_by_city.values())))
        plt.title('Уровень зарплат по городам', fontsize=12)

    def create_count_by_city_plot(self, stats: Statistics) -> None:
        """
        Генерирует круговую диаграмму по количеству вакансий по городам

        Args:
            stats (Statistics): Статистика по вакансиям
        """
        stats.get_percent_of_other_cities()
        fourth = plt.subplot(224)
        plt.rc('xtick', labelsize=6)
        fourth.pie(list(map(lambda c: round(c * 100, 2), stats.count_by_city.values())),
                   labels=stats.count_by_city.keys(),
                   colors=['r', 'g', 'b', 'm', 'y', 'c', 'orange', 'darkblue', 'pink', 'sienna', 'grey'])
        plt.title('Доля вакансий по городам', fontsize=12)