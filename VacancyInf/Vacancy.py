import math
from pandas import DataFrame
from VacancyInf.Salary import Salary


class Vacancy:
    """
    Класс для представления вакансий

    Attributes:
        name (str): Имя вакансии
        description (str): Описание вакансии
        key_skills (list): Необходимые навыки
        experience_id (str): Необходимый опыт работы
        premium (str): Является ли вакансия премиум
        employer_name (str): Имя работодателя
        salary (Salary): Информация о зарплате
        area_name (str): Место работы
        published_at (str): Время публикации
    """

    def __init__(self, args: dict):
        """
        Инициализирует вакансию

        Args:
            args (dict): Словарь для всех полей вакансии
        """
        self.name = args['name'] if 'name' in args.keys() else ''
        self.description = args['description'] if 'description' in args.keys() else ''
        self.key_skills = args['key_skills'].split('\n') if 'key_skills' in args.keys() else ''
        self.experience_id = args['experience_id'] if 'experience_id' in args.keys() else ''
        self.premium = args['premium'] if 'premium' in args.keys() else ''
        self.employer_name = args['employer_name'] if 'employer_name' in args.keys() else ''
        self.published_at = args['published_at'] if 'published_at' in args.keys() else ''
        self.salary = args['salary'] if 'salary' in args.keys() else ''
        self.area_name = args['area_name'] if 'area_name' in args.keys() else ''

    @property
    def translate(self) -> dict:
        """
        Словарь с переводом на русский
        """
        return {"noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет", "between3And6": "От 3 до 6 лет",
                "moreThan6": "Более 6 лет", "AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро",
                "GEL": "Грузинский лари", "KGS": "Киргизский сом", "KZT": "Тенге", "RUR": "Рубли", "UAH": "Гривны",
                "USD": "Доллары", "UZS": "Узбекский сум", "TRUE": 'Без вычета налогов', "True": 'Без вычета налогов',
                "FALSE": 'С вычетом налогов', "False": 'С вычетом налогов'
                }

    @property
    def reversedTranslate(self):
        """
        Словарь с переводом на английский
        """
        return dict(zip(self.translate.values(), self.translate.keys()))

    def get_published_at_year(self) -> int:
        """
        Возвращает год публикации

        Returns:
            int: Год публикации
        """
        return int(self.published_at[0:4])

    def get_russian_format(self) -> list:
        """
        Возвращает список из полей вакансии в русском формате

        Returns:
            list: Список форматированных полей
        """
        return [self.name, self.cut_line(self.description), self.cut_line('\n'.join(self.key_skills)),
                self.translate[self.experience_id], self.premium_yes_no(), self.employer_name,
                f'{self.format_number(self.salary.salary_from)} - {self.format_number(self.salary.salary_to)}'
                f' ({self.translate[self.salary.salary_currency]}) ({self.translate[self.salary.salary_gross]})',
                self.area_name, f'{self.published_at[8:10]}.{self.published_at[5:7]}.{self.published_at[0:4]}']

    def premium_yes_no(self) -> str:
        """
        Возвращает Да/Нет в зависимости от булева значения premium

        Returns:
            str: Да/Нет
        """
        return 'Да' if self.premium == 'True' else 'Нет'

    def cut_line(self, line: str) -> str:
        """
        Обрезает линию до 100 символов и добавляет в конце многоточие

        Args:
            line (str): Линия для обрезки
        Returns:
            str: Обрезанная линия
        """
        return line[0:100] + '...' if len(line) > 100 else line

    def format_number(self, number: float) -> str:
        """
        Задает формат числу вида "ddd ddd"

        Args:
            number (int): Число для форматирования
        Returns:
            int: Отформатированное число
        """
        return '{:3,d}'.format(math.floor(float(number))).replace(',', ' ')

    def reverse_premium(self, premium: str) -> str:
        """
        Возвращает булево значение в зависимости от вхождения Да/Нет

        Args:
            premium (str): Да/Нет
        Returns:
             str: строковое представление булева значения
        """
        return 'True' if premium == 'Да' else 'False'
