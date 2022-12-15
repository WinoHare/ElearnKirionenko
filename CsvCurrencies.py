from Currencies import Currencies
import csv


class CsvCurrencies:
    """
    Обрабатывает поля, связанные с вакансиями и объединяет их в одно поле

    Attributes:
        currencies (DataFrame): Таблица с курсами вакансий по месяцам
    """
    def __init__(self, file_name: str):
        """
        Инициализирует класс и запускает обработку файла

        Args:
            file_name (str): Имя файла для обработки
        """
        self.currencies = Currencies.get_currencies_in_dataframe()
        self.handleCsv(file_name)

    def handleCsv(self, file_name: str) -> None:
        """
        Обрабатывает csv файл и записывает результат в новый

        Args:
            file_name (str): Имя файла для обработки
        """
        header = ['name', 'salary', 'area_name', 'published_at']
        with open(file_name, encoding='utf-8') as csv_file:
            with open('Data/result_vacancies.csv', 'w', encoding='utf-8', newline='') as result_file:
                csv_file = csv.reader(csv_file)
                result_file = csv.writer(result_file)
                result_file.writerow(header)
                csv_file.__next__()
                count = 0
                for line in csv_file:
                    if self.is_correct_line(line, 6):
                        salary = self.get_salary(line)
                        if salary is not None:
                            result_file.writerow([line[0], salary, line[4], line[5]])
                            count += 1
                    if count == 100:
                        break

    def is_correct_line(self, line: list, header_length: int) -> bool:
        """
        Проверяет строку на пустые ячейки и наличие всех ячеек

        Args:
            line (list): Строка для проверки
            header_length (int): Необходимое количество ячеек
        Returns:
             bool: Значение, корректна ли строка
        """
        return len(list(filter(None, line))) >= header_length - 1 and line[3] in ['RUR', 'USD', 'EUR', 'KZT', 'UAH',
                                                                                  'BYR']


    def get_salary(self, line: list) -> float or None:
        """
        Определяет зарплату в зависимости от полей salary_to и salary_from и конвертирует в рубли

        Args:
            line (list): Словарь для всех полей вакансии
        Returns:
            float or None: Зарплата
        """
        if line[1] == '' and line[2] == '':
            return None
        elif line[1] == '':
            salary = float(line[2])
        elif line[2] == '':
            salary = float(line[1])
        else:
            salary = ((float(line[1]) + float(line[2])) / 2)
        if line[3] != 'RUR':
            return salary * float(self.currencies.loc[self.get_published_at_month_year(line)][line[3]])
        else:
            return salary

    def get_published_at_month_year(self, line) -> str:
        return f'{line[5][5:7]}/{line[5][:4]}'

CsvCurrencies('Data/vacancies_dif_currencies.csv')