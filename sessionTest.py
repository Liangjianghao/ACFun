import requests, json
cookieJar = requests.cookies.RequestsCookieJar()
session = requests.Session()

login_url = "http://example.com/login"
user_data = {"username": "admin", "password": "apasswd"}
reload_url = "http://example.com/reload"

login_resp = session.request("POST", login_url, 
            cookies=cookieJar, data=json.dumps(user_data))

reload_resp = session.request("GET", click_url,
            cookies=cookieJar)
