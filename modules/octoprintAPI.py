import requests


def sendFile(file_name, printer):
    url = 'http://' + printer['address'] + "/api/files/local"

    files = {'file': open('data/gcodes/' + file_name, 'rb')}
    headers = {'X-Api-Key': printer['api-key']}
    r = requests.post(url, files=files, headers=headers)
    return r


def startPrint(file_name, printer):
    url = 'http://' + printer['address'] + '/api/files/local/' + file_name
    headers = {'X-Api-Key': printer['api-key']}
    command = {
        'commands':'select',
        'print': True,
    }
    r = requests.post(url, json=command,headers=headers)
    return r
