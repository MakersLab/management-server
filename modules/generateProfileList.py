def generateProfileList(path):
    import json
    fileContent=""
    with open(path,'r') as f:
        fileContent = f.read()
    data=json.loads(fileContent)
    return data['profiles']

def generateProfileDict(path):
    import json
    fileContent=""
    with open(path,'r') as f:
        fileContent = f.read()
    data=json.loads(fileContent)
    return data

if __name__ == '__main__':
    data = generateProfileList('../data/profiles.json')
    print(data)