import unittest
from DataSet import DataSet
from VacancyInf.Vacancie import Vacancie


class FormatterTests(unittest.TestCase):

    def test_formatter_name(self):
        header = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_from',
                  'salary_to', 'salary_gross', 'salary_currency', 'area_name', 'published_at']
        input_value = [['Программист', 'JS developer', 'HTML, CSS, JS', 'between1And3', 'True', 'Google', '50000',
                        '75000', 'True', 'RUR', 'Москва', '2022-07-05T18:19:30+0300']]
        output_value = [Vacancie({'name': 'Программист', 'description': 'JS developer', 'key_skills': 'HTML, CSS, JS',
                                 'experience_id': 'between1And3', 'premium': 'True', 'salary_from': '50000',
                                 'salary_to': '75000', 'salary_gross': 'True', 'salary_currency': 'RUR',
                                 'area_name': 'Москва', 'published_at': '2022-07-05T18:19:30+0300'})]
        self.assertEqual(DataSet('../Data/vacancies.csv').formatter(header, input_value)[0].name,
                         output_value[0].name)

    def test_formatter_description(self):
        header = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_from',
                  'salary_to', 'salary_gross', 'salary_currency', 'area_name', 'published_at']
        input_value = [['Программист', 'JS developer', 'HTML, CSS, JS', 'between1And3', 'True', 'Google', '50000',
                        '75000', 'True', 'RUR', 'Москва', '2022-07-05T18:19:30+0300']]
        output_value = [Vacancie({'name': 'Программист', 'description': 'JS developer', 'key_skills': 'HTML, CSS, JS',
                                 'experience_id': 'between1And3', 'premium': 'True', 'salary_from': '50000',
                                 'salary_to': '75000', 'salary_gross': 'True', 'salary_currency': 'RUR',
                                 'area_name': 'Москва', 'published_at': '2022-07-05T18:19:30+0300'})]
        self.assertEqual(DataSet('../Data/vacancies.csv').formatter(header, input_value)[0].description,
                         output_value[0].description)

    def test_formatter_experience_id(self):
        header = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_from',
                  'salary_to', 'salary_gross', 'salary_currency', 'area_name', 'published_at']
        input_value = [['Программист', 'JS developer', 'HTML, CSS, JS', 'between1And3', 'True', 'Google', '50000',
                        '75000', 'True', 'RUR', 'Москва', '2022-07-05T18:19:30+0300']]
        output_value = [
            Vacancie({'name': 'Программист', 'description': 'JS developer', 'key_skills': 'HTML, CSS, JS',
                     'experience_id': 'between1And3', 'premium': 'True', 'salary_from': '50000',
                     'salary_to': '75000', 'salary_gross': 'True', 'salary_currency': 'RUR',
                     'area_name': 'Москва', 'published_at': '2022-07-05T18:19:30+0300'})]
        self.assertEqual(DataSet('../Data/vacancies.csv').formatter(header, input_value)[0].experience_id,
                         output_value[0].experience_id)

    def test_formatter_premium(self):
        header = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_from',
                  'salary_to', 'salary_gross', 'salary_currency', 'area_name', 'published_at']
        input_value = [['Программист', 'JS developer', 'HTML, CSS, JS', 'between1And3', 'True', 'Google', '50000',
                        '75000', 'True', 'RUR', 'Москва', '2022-07-05T18:19:30+0300']]
        output_value = [Vacancie({'name': 'Программист', 'description': 'JS developer', 'key_skills': 'HTML, CSS, JS',
                                 'experience_id': 'between1And3', 'premium': 'True', 'salary_from': '50000',
                                 'salary_to': '75000', 'salary_gross': 'True', 'salary_currency': 'RUR',
                                 'area_name': 'Москва', 'published_at': '2022-07-05T18:19:30+0300'})]
        self.assertEqual(DataSet('../Data/vacancies.csv').formatter(header, input_value)[0].premium,
                         output_value[0].premium)

    def test_formatter_salary_from(self):
        header = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_from',
                  'salary_to', 'salary_gross', 'salary_currency', 'area_name', 'published_at']
        input_value = [['Программист', 'JS developer', 'HTML, CSS, JS', 'between1And3', 'True', 'Google', '50000',
                        '75000', 'True', 'RUR', 'Москва', '2022-07-05T18:19:30+0300']]
        output_value = [Vacancie({'name': 'Программист', 'description': 'JS developer', 'key_skills': 'HTML, CSS, JS',
                                 'experience_id': 'between1And3', 'premium': 'True', 'salary_from': '50000',
                                 'salary_to': '75000', 'salary_gross': 'True', 'salary_currency': 'RUR',
                                 'area_name': 'Москва', 'published_at': '2022-07-05T18:19:30+0300'})]
        self.assertEqual(DataSet('../Data/vacancies.csv').formatter(header, input_value)[0].salary.salary_from,
                         output_value[0].salary.salary_from)

    def test_formatter_salary_to(self):
        header = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_from',
                  'salary_to', 'salary_gross', 'salary_currency', 'area_name', 'published_at']
        input_value = [['Программист', 'JS developer', 'HTML, CSS, JS', 'between1And3', 'True', 'Google', '50000',
                        '75000', 'True', 'RUR', 'Москва', '2022-07-05T18:19:30+0300']]
        output_value = [Vacancie({'name': 'Программист', 'description': 'JS developer', 'key_skills': 'HTML, CSS, JS',
                                 'experience_id': 'between1And3', 'premium': 'True', 'salary_from': '50000',
                                 'salary_to': '75000', 'salary_gross': 'True', 'salary_currency': 'RUR',
                                 'area_name': 'Москва', 'published_at': '2022-07-05T18:19:30+0300'})]
        self.assertEqual(DataSet('../Data/vacancies.csv').formatter(header, input_value)[0].salary.salary_to,
                         output_value[0].salary.salary_to)

    def test_formatter_salary_gross(self):
        header = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_from',
                  'salary_to', 'salary_gross', 'salary_currency', 'area_name', 'published_at']
        input_value = [['Программист', 'JS developer', 'HTML, CSS, JS', 'between1And3', 'True', 'Google', '50000',
                        '75000', 'True', 'RUR', 'Москва', '2022-07-05T18:19:30+0300']]
        output_value = [Vacancie({'name': 'Программист', 'description': 'JS developer', 'key_skills': 'HTML, CSS, JS',
                                 'experience_id': 'between1And3', 'premium': 'True', 'salary_from': '50000',
                                 'salary_to': '75000', 'salary_gross': 'True', 'salary_currency': 'RUR',
                                 'area_name': 'Москва', 'published_at': '2022-07-05T18:19:30+0300'})]
        self.assertEqual(DataSet('../Data/vacancies.csv').formatter(header, input_value)[0].salary.salary_gross,
                         output_value[0].salary.salary_gross)

    def test_formatter_salary_currency(self):
        header = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_from',
                  'salary_to', 'salary_gross', 'salary_currency', 'area_name', 'published_at']
        input_value = [['Программист', 'JS developer', 'HTML, CSS, JS', 'between1And3', 'True', 'Google', '50000',
                        '75000', 'True', 'RUR', 'Москва', '2022-07-05T18:19:30+0300']]
        output_value = [Vacancie({'name': 'Программист', 'description': 'JS developer', 'key_skills': 'HTML, CSS, JS',
                                 'experience_id': 'between1And3', 'premium': 'True', 'salary_from': '50000',
                                 'salary_to': '75000', 'salary_gross': 'True', 'salary_currency': 'RUR',
                                 'area_name': 'Москва', 'published_at': '2022-07-05T18:19:30+0300'})]
        self.assertEqual(DataSet('../Data/vacancies.csv').formatter(header, input_value)[0].salary.salary_currency,
                         output_value[0].salary.salary_currency)

    def test_formatter_average_salary(self):
        header = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_from',
                  'salary_to', 'salary_gross', 'salary_currency', 'area_name', 'published_at']
        input_value = [['Программист', 'JS developer', 'HTML, CSS, JS', 'between1And3', 'True', 'Google', '50000',
                        '75000', 'True', 'RUR', 'Москва', '2022-07-05T18:19:30+0300']]
        output_value = [Vacancie({'name': 'Программист', 'description': 'JS developer', 'key_skills': 'HTML, CSS, JS',
                                 'experience_id': 'between1And3', 'premium': 'True', 'salary_from': '50000',
                                 'salary_to': '75000', 'salary_gross': 'True', 'salary_currency': 'RUR',
                                 'area_name': 'Москва', 'published_at': '2022-07-05T18:19:30+0300'})]
        self.assertEqual(DataSet('../Data/vacancies.csv').formatter(header, input_value)[0].salary.average_salary,
                         output_value[0].salary.average_salary)

    def test_formatter_area_name(self):
        header = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_from',
                  'salary_to', 'salary_gross', 'salary_currency', 'area_name', 'published_at']
        input_value = [['Программист', 'JS developer', 'HTML, CSS, JS', 'between1And3', 'True', 'Google', '50000',
                        '75000', 'True', 'RUR', 'Москва', '2022-07-05T18:19:30+0300']]
        output_value = [Vacancie({'name': 'Программист', 'description': 'JS developer', 'key_skills': 'HTML, CSS, JS',
                                 'experience_id': 'between1And3', 'premium': 'True', 'salary_from': '50000',
                                 'salary_to': '75000', 'salary_gross': 'True', 'salary_currency': 'RUR',
                                 'area_name': 'Москва', 'published_at': '2022-07-05T18:19:30+0300'})]
        self.assertEqual(DataSet('../Data/vacancies.csv').formatter(header, input_value)[0].area_name,
                         output_value[0].area_name)

    def test_formatter_published_at(self):
        header = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary_from',
                  'salary_to', 'salary_gross', 'salary_currency', 'area_name', 'published_at']
        input_value = [['Программист', 'JS developer', 'HTML, CSS, JS', 'between1And3', 'True', 'Google', '50000',
                        '75000', 'True', 'RUR', 'Москва', '2022-07-05T18:19:30+0300']]
        output_value = [Vacancie({'name': 'Программист', 'description': 'JS developer', 'key_skills': 'HTML, CSS, JS',
                                 'experience_id': 'between1And3', 'premium': 'True', 'salary_from': '50000',
                                 'salary_to': '75000', 'salary_gross': 'True', 'salary_currency': 'RUR',
                                 'area_name': 'Москва', 'published_at': '2022-07-05T18:19:30+0300'})]
        self.assertEqual(DataSet('../Data/vacancies.csv').formatter(header, input_value)[0].published_at,
                         output_value[0].published_at)


class IsCorrectLineTests(unittest.TestCase):
    def test_IsCorrectLine_correct(self):
        line = ['some', 'body', 'once', 'told', 'me']
        header_length = 5
        self.assertEqual(DataSet('../Data/vacancies.csv').is_correct_line(line, header_length), True)

    def test_IsCorrectLine_incorrect_length(self):
        line = ['some', 'body', 'once', 'told', 'me']
        header_length = 6
        self.assertEqual(DataSet('../Data/vacancies.csv').is_correct_line(line, header_length), False)

    def test_IsCorrectLine_incorrect_empty(self):
        line = ['some', 'body', '', 'told', 'me']
        header_length = 5
        self.assertEqual(DataSet('../Data/vacancies.csv').is_correct_line(line, header_length), False)

    def test_IsCorrectLine_incorrect_length_empty(self):
        line = ['some', 'body', '', 'told', 'me']
        header_length = 6
        self.assertEqual(DataSet('../Data/vacancies.csv').is_correct_line(line, header_length), False)

if __name__ == '__main__':
    unittest.main()
