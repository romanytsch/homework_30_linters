import unittest
from remote_execution import app, run_python_code_in_subprocess

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def get_csrf_token_and_cookie(self):
        response = self.client.get('/get_csrf_token')  # Эндпоинт для токена
        csrf_token = response.get_json()['csrf_token']
        cookie = response.headers['Set-Cookie']
        return csrf_token, cookie

    def test_timeout_less_than_execution(self):
        csrf_token, cookie = self.get_csrf_token_and_cookie()
        headers = {'Cookie': cookie}
        data = {'code': 'import time; time.sleep(1); print("done")', 'timeout': 2, 'csrf_token': csrf_token}
        response = self.client.post('/run_code', data=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('done', json_data.get('output', ''))

    def test_invalid_form_data(self):
        csrf_token, cookie = self.get_csrf_token_and_cookie()
        headers = {'Cookie': cookie}
        # Отправляем без timeout
        data = {'code': 'print(1)', 'csrf_token': csrf_token}
        response = self.client.post('/run_code', data=data, headers=headers)
        self.assertEqual(response.status_code, 400)
        json_data = response.get_json()
        self.assertIn('messages', json_data)
        self.assertIn('timeout', json_data['messages'])

    def test_no_shell_true_usage(self):
        result = run_python_code_in_subprocess('print("test")', 5)
        self.assertIn('test', result['output'])


if __name__ == '__main__':
    unittest.main()
