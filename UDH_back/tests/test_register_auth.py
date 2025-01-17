import requests
import json
import unittest


class TestRegisterAuth(unittest.TestCase):
    url = "http://localhost"

    def test_invalid_user(self):
        data = {'login': 'INVALID_login123', 'password': 'INVALID_password123'}
        r = requests.post(url=TestRegisterAuth.url + "/login/", data=data)
        try:
            r_json = r.json()
        except requests.exceptions.JSONDecodeError:
            self.fail(f"Got non-serializable answer: {r.content}")
        expected_answer = json.dumps({"status": 0, "error": "Wrong login or password"})
        self.assertEqual(r_json, expected_answer, f"r_json ({r_json}) does not match expected_answer ({expected_answer})")






if __name__ == '__main__':
    unittest.main()