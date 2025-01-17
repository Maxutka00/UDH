import unittest

import requests


class TestToken(unittest.TestCase):
    url = "http://localhost:8000/"
    def test_no_token(self):
        r = requests.post(url=TestToken.url + "create_article/")
        r_json = r.json()
        print("test_no_token:", r_json)
        print(r.url)
        self.assertTrue(r_json.get("code", None))

    def test_token(self):
        data = {"login": "popkakarasya", "password": "NoFade", "name": "Popka Karasya", "email": "popkakarasya@gmail.com"}
        r = requests.post(url=TestToken.url + "register/", data=data)
        r_json = r.json()
        print("test_token:", r_json)
        if not r_json["status"]:
            print("test_token: User already exists. Logging in...")
            r = requests.post(url=TestToken.url + "login/", data=data)
            r_json = r.json()
        self.assertTrue(r_json["status"])
        data = r_json["data"]
        token = data["token"]
        headers = {"Authorization": f"Basic {token}"}
        data = {"body": "body", "annotations": "annotations",
                "title": "title", "picture": b"\x02\x43\x92\x03", "access": 0,
                "topics": ["topic1", "topic2"]}

        r = requests.post(url=TestToken.url + "create_article/", headers=headers, data=data)
        r_json = r.json()
        print("test_token:", r_json)
        self.assertTrue(r_json["status"])
#     body = request.POST.get("body")
#     annotations = request.POST.get("annotations")
#     title = request.POST.get("title")
#     picture = request.POST.get("picture")
#     # author = request.POST.get("author")
#     access = request.POST.get("access")
#     topics_ = request.POST.get("topics")

if __name__ == '__main__':
    unittest.main()
