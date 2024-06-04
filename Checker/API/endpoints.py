import requests

def api_login(url, username, password):
    response = requests.post(url + '/login', json={'username': username, 'password': password})
    cookie_header = response.headers.get('Set-Cookie')
    # Token is token=<token>
    token = cookie_header.split('=')[1].split(';')[0]
    return token
def api_create_user(url, token, is_admin, username=None, password=None):
    cookie = f"token={token}"
    url = url + "/managment"
    if is_admin:
        data = {
            "isAdmin": True,
            "username": username,
            "password": password
        }
    else:
        data = {
            "isAdmin": False,
            "username": None,
            "password": None
        }
    response = requests.post(url,headers={'Cookie': cookie} , json={"action":"add_user", "data": data})
    if is_admin:
        if response.status_code == 200:
            return True
        return False
    else:
        response_json = response.json()
        # pdfUrl
        return response_json['pdfUrl']
def api_delete_user(url, token, is_admin, username):
    cookie = f"token={token}"
    url = url + "/managment"
    data = {
        "isAdmin": is_admin,
        "user_id": username
    }
    response = requests.post(url,headers={'Cookie': cookie} , json={"action":"remove_user", "data": data})
    if response.status_code == 200:
        return True
    return False
def api_create_film(url, token, film_name, film_team):
    cookie = f"token={token}"
    url = url + "/managment"
    data = {
        "title": film_name,
        "team": film_team
    }
    response = requests.post(url,headers={'Cookie': cookie} , json={"action":"add_film", "data": data})
    if response.status_code == 200:
        return True
    return False
def api_delete_film(url, token, film_name):
    cookie = f"token={token}"
    url = url + "/managment"
    data = {
        "film_id": film_name
    }
    response = requests.post(url,headers={'Cookie': cookie} , json={"action":"remove_film", "data": data})
    if response.status_code == 200:
        return True
    return False