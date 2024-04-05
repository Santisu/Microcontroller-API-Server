import urequests as requests
import time

BASE_URL = "<Your API BASE URL>"
USERNAME = "client@test.com"
PASSWORD = "password"


def login() -> str:
    """Login en la API

    Returns:
        str: Token to save in headers
    """
    url_login = f"{BASE_URL}login/"
    datos_login = {
        "email" : USERNAME,
        "username" : USERNAME,
        "password" : PASSWORD
    }
    token = None
    try:
        login_response = requests.post(url_login, json=datos_login)
    except:
        return token
    if login_response.status_code == 200:
        token = (login_response.json())['key']
    login_response.close()
    return token

def get_task_list(headers:dict) -> list:
    """
    Request for the list of tasks that have not been executed and returns the list with each one of these, if nothing is received, returns an empty list.

    Args:
        headers (dict): Dict with the token

    Returns:
        list: List with the tasks that have not been executed
    """
    list_url = f"{BASE_URL}cmd/"
    tasks_list = []
    try:
        task_list_response = requests.get(list_url, headers=headers)
    except:
        return tasks_list
    if task_list_response.status_code == 200:
        tasks_list = task_list_response.json()
    task_list_response.close()
    return tasks_list

def report_task_done(orden:object, headers:dict):
    """
    Executes PUT in the web indicating that the task was executed

    Args:
        orden (object): Orden object that has been executed
        headers (dict): Dict with the token
    """
    orden_url = f"{BASE_URL}cmd/{orden.ide}/"
    # print(orden_url)
    # print("HEADER: ", headers)
    body = {
        "ejecutado" : True
    }
    try:
        put_response = requests.put(orden_url, json=body, headers=headers)
    except:
        return None
    if put_response:
        response_code = put_response.status_code
    put_response.close()
    return response_code

def get_time() -> dict:
    """
    Executes GET in the web to get the current time.

    Returns:
        dict: Dic with the current time
    Example:
        {
            "year": 2023, 
            "month": 12, 
            "day": 15, 
            "hour": 11, 
            "min": 47, 
            "sec": 6, 
            "wday": 4, 
            "yday": 349, 
            "is_dst": 1
        }
    """
    hora_url = f"{BASE_URL}time/"
    time_dict = None
    try:
        response = requests.get(hora_url)
    except:
        return time_dict
    if response.status_code == 200:
        time_dict = response.json()
    response.close()
    return time_dict