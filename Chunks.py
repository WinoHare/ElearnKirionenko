import csv


class Chunks:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.split_file()

    def split_file(self) -> None:
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
        with open(f'Chunks/{year}.csv', 'w', encoding='utf-8', newline='') as new_file:
            writer = csv.writer(new_file)
            writer.writerow(header)
            writer.writerows(filter(lambda row: row[-1][:4] == year, data))



Chunks('StatsFiles/vacancies_by_year.csv')