import unittest
from accounting import app, storage


class FinanceAppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

        # Восстанавливаем storage перед каждым тестом, чтобы тесты были изолированы
        storage.clear()
        storage.update({
            2023: {
                5: {1: 100, 2: 150, 'total': 250},
                'total': 250,
            },
            2024: {
                1: {10: 200, 'total': 200},
                'total': 200,
            }
        })

    # Тесты /add/<date>/<int:number>
    def test_add_expense_valid(self):
        response = self.client.get('/add/20230917/500')
        self.assertIn('Записано: 20230917, траты: 500', response.data.decode('utf-8'))
        self.assertEqual(storage[2023][9][17], 500)
        self.assertEqual(storage[2023][9]['total'], 500)
        self.assertEqual(storage[2023]['total'], 750)

    def test_add_expense_invalid_date(self):
        response = self.client.get('/add/202319/100')
        self.assertEqual(response.status_code, 400)

    def test_add_expense_invalid_date_non_digits(self):
        response = self.client.get('/add/aaaa1111/100')
        self.assertEqual(response.status_code, 400)

    # Тесты /calculate/<int:year>
    def test_calculate_year_existing(self):
        response = self.client.get('/calculate/2023')
        self.assertIn('Год: 2023, Траты: 250', response.data.decode('utf-8'))

    def test_calculate_year_nonexisting(self):
        # Год, которого нет в storage
        response = self.client.get('/calculate/1999')
        self.assertIn('Год: 1999, Траты: 0', response.data.decode('utf-8'))

    def test_calculate_year_empty_storage(self):
        storage.clear()
        response = self.client.get('/calculate/2023')
        self.assertIn('Год: 2023, Траты: 0', response.data.decode('utf-8'))


    # Тесты /calculate/<int:year>/<int:month>
    def test_calculate_year_month_existing(self):
        response = self.client.get('/calculate/2023/5')
        self.assertIn('Год: 2023, месяц: 5 -> траты: 250', response.data.decode('utf-8'))

    def test_calculate_year_month_nonexisting_year(self):
        response = self.client.get('/calculate/1999/5')
        self.assertIn('Год: 1999, месяц: 5 -> траты: 0', response.data.decode('utf-8'))

    def test_calculate_year_month_nonexisting_month(self):
        response = self.client.get('/calculate/2023/12')
        self.assertIn('Год: 2023, месяц: 12 -> траты: 0', response.data.decode('utf-8'))

    def test_calculate_year_month_empty_storage(self):
        storage.clear()
        response = self.client.get('/calculate/2023/5')
        self.assertIn('Год: 2023, месяц: 5 -> траты: 0', response.data.decode('utf-8'))

