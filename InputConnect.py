import time
from ReportModule.Report import Report


def profiler(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        func(*args, **kwargs)
        after = time.time()
        print(after - before)

    return wrapper


class InputConnect:
    """
    Класс для обработки ввода и вызова дальнейших инструкций, в зависимости от ввода (точка входа)
    """

    def __init__(self):
        """
        Запрашивает данные из консоли, и, в зависимости от ввода, выбирает дальнейшие инструкции
        """
        vacancie_name = input('Введите название вакансии: ')
        self.get_report(vacancie_name)

    @profiler
    def get_report(self, vacancie_name: str) -> None:
        """
        Собирает параметры отчета и вызывает формирование отчета
        """
        Report(vacancie_name)

