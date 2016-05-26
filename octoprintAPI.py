import requests

url="http://192.168.2.13/api/files/local"

files={'file':open('data/gcodes/2016_05_26_14_21Cover.gcode','rb')}
headers = {'X-Api-Key':'75A9801367354C78BB55C6BE2EA41368'}
r=requests.post(url, files=files,headers=headers)

print(r.text)
