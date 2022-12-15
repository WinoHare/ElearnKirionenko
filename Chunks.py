import csv


class Chunks:
    """
    Разбивает файл csv на чанки по годам

    Attributes:
        file_name (str): Имя файла, который разбивается на чанки
    """
    def __init__(self, file_name: str):
        """
        Инициализирует класс и инициирует разбиение на чанки

        Args:
            file_name(str): Имя файла, который разбивается на чанки
        """
        self.file_name = file_name
        self.split_file()

    def split_file(self) -> None:
        """
        Разбивает файл на чанки
        """
        with open(self.file_name, encoding='utf-8') as csv_file:
            file = csv.reader(csv_file)
            header = next(file)
            file = list(file)
            created_files = []
            for line in file:
                year = line[-1][:4]
                if year not in created_files:
                    created_files.append(year)
                    self.fill_csv(year, file, header)

    def fill_csv(self, year: str, data: list, header: list) -> None:
        """
        Создает новый файл и заполняет данными
        Args:
            year (str): Год, по которому отбираются строки
            data (list): Список строк начального файла
            header (list): Строка заголовков
        """
        with open(f'Chunks/{year}.csv', 'w', encoding='utf-8', newline='') as new_file:
            writer = csv.writer(new_file)
            writer.writerow(header)
            writer.writerows(filter(lambda row: row[-1][:4] == year, data))


Chunks('Data/vacancies_dif_currencies.csv')