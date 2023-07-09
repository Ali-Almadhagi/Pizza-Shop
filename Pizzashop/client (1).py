import requests

def client(username, password):
    url = "https://cis294.hfcc.edu/api/login"

    data = {

        "username": username,
        "password": password,
    }

    response = requests.post(url, json=data)

    print("Status Code", response.status_code)
    print("JSON Response ", response.json())
    
    body = response.json()
    
    return response
