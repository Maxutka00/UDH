import unittest

import requests


class TestArticles(unittest.TestCase):
    url = "http://localhost:8000/"
    def test_no_token(self):
        r = requests.post(url=TestArticles.url + "test_token/")
        r_json = r.json()
        print("test_no_token:", r_json)
        print(r.url)
        self.assertTrue(r_json.get("code", None))

    def test_token(self):
        data = {"login": "popkakarasya", "password": "NoFade", "name": "Popka Karasya", "email": "popkakarasya@gmail.com"}
        r = requests.post(url=TestArticles.url + "register/", data=data)
        r_json = r.json()
        print("test_token:", r_json)
        if not r_json["status"]:
            print("test_token: User already exists. Logging in...")
            r = requests.post(url=TestArticles.url + "login/", data=data)
            r_json = r.json()
        self.assertTrue(r_json["status"])
        data = r_json["data"]
        token = data["token"]
        headers = {"Authorization": f"Basic {token}"}
        r = requests.post(url=TestArticles.url + "test_token/", headers=headers)
        r_json = r.json()
        print("test_token:", r_json)
        self.assertTrue(r_json["status"])


if __name__ == '__main__':
    unittest.main()
