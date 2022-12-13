import math


class Salary:
    """
    Класс для представления зарплаты

    Attributes:
        salary_from (float): Нижняя граница оклада
        salary_to (float): Верхняя граница оклада
        salary_gross (str): Строковое представления, указан ли оклад до вычета налогов
        salary_currency (str): Валюта оклада
        average_salary (float): Среднее между нижней и верхней границами
    """

    def __init__(self, args: dict):
        """
        Инициализирует класс, выполняет конвертацию

        Args:
            args (dict): Словарь с ключами для каждого поля класса
        """
        self.salary_from = float(args['salary_from']) if 'salary_from' in args.keys() else 0.0
        self.salary_to = float(args['salary_to']) if 'salary_to' in args.keys() else 0.0
        self.salary_gross = args['salary_gross'] if 'salary_gross' in args.keys() else 'False'
        self.salary_currency = args['salary_currency'] if 'salary_currency' in args.keys() else 'RUR'
        self.average_salary = math.floor(
            ((self.salary_from + self.salary_to) / 2) * self.currency_to_rub[self.salary_currency])

    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }
