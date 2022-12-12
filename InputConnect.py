from prettytable import prettytable
from DataSet import DataSet
from ReportModule.Report import Report

"""Названия столбцов файла"""
titles = ['Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания', 'Оклад', 'Название региона',
          'Дата публикации вакансии']


class InputConnect:
    """Класс для обработки ввода и вызова дальнейших инструкций, в зависимости от ввода (точка входа)

    Attributes:
        function_selection (str): Выбор программы (Вакансии/Статистика)
        is_input_correct (bool): Является ли ввод корректным
        error_message (str): Сообщение об ошибке при некорректном вводе
    """

    def __init__(self):
        """Запрашивает данные из консоли, и, в зависимости от ввода, выбирает дальнейшие инструкции"""
        self.function_selection = 'Статистика'
        if self.function_selection == 'Вакансии':
            self.error_message = ''
            self.is_input_correct = True
            if not self.is_input_correct:
                print(self.error_message)
                return
            self.print_vacancies()
        elif self.function_selection == 'Статистика':
            self.get_report()
        elif self.function_selection == 'Время':
            data = DataSet(input('Название файла: '))
            time = 0
            for item in data.vacancies_objects:
                time += item.get_published_at_year_second()
            print(time)
        else:
            print('Неверный ввод данных')

    def print_vacancies(self) -> None:
        """Собирает параметры печати таблица и вызывает печать"""
        file_name = input('Введите название файла: ')
        filter_key, filter_value = self.get_filter_parameter()
        sort_parameter = self.get_sort_parameter()
        sort_reversed = self.get_sort_reversed()
        range_to_print = self.get_range_to_print()
        titles_to_print = self.get_titles_to_print()

        self.print_table(file_name, filter_key, filter_value, sort_parameter, sort_reversed, range_to_print,
                         titles_to_print)

    def get_report(self) -> None:
        """Собирает параметры отчета и вызывает формирование отчета"""
        file_name = ''
        vacancy_name = 'Аналитик'
        Report(file_name, vacancy_name)

    def get_filter_parameter(self) -> tuple:
        """Получает и обрабатывает параметр фильтрации

        Returns:
            tuple: Ключ и значение для фильтрации
        """
        filter_parameter = input('Введите параметр фильтрации: ')
        key, value = '', ''
        if ': ' in filter_parameter:
            key, value = filter_parameter.split(': ')
            if key == "Навыки":
                value = value.split(', ')

        if filter_parameter != '' and ': ' not in filter_parameter:
            self.error_message = "Формат ввода некорректен"
            self.is_input_correct = False

        return key, value

    def get_sort_parameter(self) -> str:
        """Получает и обрабатывает параметр сортировки

        Returns:
            str: Параметр сортировки
        """
        sort_parameter = input('Введите параметр сортировки: ')
        if sort_parameter not in titles and sort_parameter != '':
            self.error_message = "Параметр сортировки некорректен" if self.error_message == '' else self.error_message
            self.is_input_correct = False
        return sort_parameter

    def get_sort_reversed(self) -> bool:
        """Получает и обрабатывает направление сортировки

        Returns:
            bool: Значение, обратный ли порядок
        """
        sort_direction = input('Обратный порядок сортировки (Да / Нет): ')
        if sort_direction == 'Да':
            sort_direction = True
        elif sort_direction == 'Нет' or sort_direction == '':
            sort_direction = False
        if type(sort_direction) != bool:
            self.error_message = "Порядок сортировки задан некорректно" if self.error_message == '' else self.error_message
            self.is_input_correct = False
        return sort_direction

    def get_range_to_print(self) -> tuple:
        """Получает и обрабатывает диапазон

        Returns:
            tuple: Первый и последний элемент диапазона
        """
        start = 0
        end = 100000000000
        range_to_print = input('Введите диапазон вывода: ').split()
        if len(range_to_print) == 2:
            start, end = int(range_to_print[0]) - 1, int(range_to_print[1]) - 1
        elif len(range_to_print) == 1:
            start = int(range_to_print[0]) - 1
        return start, end

    def get_titles_to_print(self) -> list or str:
        """Получает и обрабатывает заголовки, которые необходимо напечатать

        Returns:
            list or str: Заголовки, которые необходимо напечатать
        """
        titles_to_print = input('Введите требуемые столбцы: ')
        return titles_to_print.split(', ') if len(titles_to_print) > 1 else titles_to_print

    def print_table(self, file_name: str, filter_key: str, filter_value: str, sort_parameter: str, sort_reversed: bool,
                    range_to_print: tuple, titles_to_print: list) -> None:
        """Печатает таблицу с вакансиями в консоль

        Args:
            file_name (str): Имя файла
            filter_key (str): Ключ фильтрации
            filter_value (str): Значение фильтрации
            sort_parameter (str): Параметр сортировки
            sort_reversed (bool): Является ли сортировка обратной
            range_to_print (tuple): Диапазон печати
            titles_to_print (list): Столбцы для печати
        """
        data_set = DataSet(file_name)
        if data_set.is_empty:
            print(data_set.error_massage)
            return
        data_set.filter_sort_data(filter_key, filter_value, sort_parameter, sort_reversed)
        if len(data_set.vacancies_objects) == 0:
            print('Ничего не найдено')
            return

        counter = 0
        table = prettytable.PrettyTable(
            hrules=prettytable.ALL,
            align='l',
            field_names=['№'] + titles,
            max_width=20)
        for vacancie in data_set.vacancies_objects:
            counter += 1
            table.add_row([counter] + vacancie.get_russian_format())
        print(table.get_string(start=range_to_print[0],
                               end=range_to_print[1],
                               fields=['№'] + titles_to_print if len(titles_to_print) != 0 else [
                                                                                                    '№'] + table.field_names))
