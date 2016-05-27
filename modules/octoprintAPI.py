import requests


def sendFile(file_name, printer):
    url = 'http://' + printer['address'] + "/api/files/local"

    files = {'file': open('data/gcodes/' + file_name, 'rb')}
    headers = {'X-Api-Key': printer['api-key']}
    r = requests.post(url, files=files, headers=headers)
    return r


def startPrint(name, printer):
    url = 'http://' + printer + '/api/files/local/' + name
    headers = {'X-Api-Key': printer['api-key']}
    command = {
        'select': True,
        'print': True,
    }
    r = requests.post(url, params=command,headers=headers)
    return r
