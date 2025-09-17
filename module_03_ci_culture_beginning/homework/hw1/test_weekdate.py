import unittest
from freezegun import freeze_time
import datetime
from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app


class TestWeekdate(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_can_get_correct_username_with_weekdate(self):
        username = 'username'
        with freeze_time("2025-09-08"):
            response = self.app.get(self.base_url + username)
            response_text = response.data.decode()
            self.assertTrue(username in response_text)
            self.assertEqual(datetime.datetime.now().date(), datetime.date(2025, 9, 8))

    def test_weekday_name_and_greeting_in_username(self):
        weekdays = [
            "понедельника", "вторника", "среды",
            "четверга", "пятницы", "субботы", "воскресенья"
        ]
        start_day = datetime.date(2025, 9, 7)  # понедельник по календарю

        for i in range(7):
            current_day = start_day + datetime.timedelta(days=i)
            expected_weekday = weekdays[current_day.weekday()]

            # Тест с обычным username
            with freeze_time(current_day):
                username = 'user'
                response = self.app.get(self.base_url + username)
                response_text = response.data.decode()
                self.assertIn(expected_weekday, response_text,
                              msg=f"Дата: {current_day} ожидался день недели '{expected_weekday}'")
                self.assertIn(username, response_text)

            # Тест с пожеланием в username
            with freeze_time(current_day):
                greeting_username = f"Хорошей {expected_weekday}"
                response = self.app.get(self.base_url + greeting_username)
                response_text = response.data.decode()
                self.assertIn(expected_weekday, response_text,
                              msg=f"Дата: {current_day} ожидался день недели '{expected_weekday}'")
                self.assertIn(greeting_username, response_text)
