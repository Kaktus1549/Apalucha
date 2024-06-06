import requests
from sys import path
path.append('.')
from API.pdf_ops import extract_qr_code

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
def api_change_settings(url, token, vote_duration):
    cookie = f"token={token}"
    url = url + "/managment"
    data = {
        "voteDuration": vote_duration
    }
    response = requests.post(url,headers={'Cookie': cookie} , json={"action":"change_settings", "data": data})
    if response.status_code == 200:
        return True
    return False
def api_get_voting_token(url, token, user_id):
    pdf_url = url + "/pdf?user=" + user_id
    cookie = f"token={token}"
    response = requests.get(pdf_url, headers={'Cookie': cookie})
    # if response is redirected, exit
    if response.status_code != 200:
        return None
    pdf_data = response.content
    login_url = extract_qr_code(pdf_data)

    if login_url is None:
        return None
    voting_token = login_url.split("?token=")[1]
    return voting_token
def api_vote(url, token, film_id):
    pass
    # {"1":"test","2":"test2"}
def api_start_voting(url, token, excepted_time):
    pass
def api_check_vote_results(url, token):
    pass
def api_reset_voting(url, token):
    pass