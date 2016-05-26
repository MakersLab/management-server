def generateNames(PRINTERS_PATH):
    printers = []
    with open(PRINTERS_PATH, 'r') as f:
        content = f.read()
        content = content.splitlines()
        for index, i in enumerate(content):
            info = {}
            name, address,api_key = i.split(' ')
            info['name'] = name
            info['index'] = index
            info['address'] = address
            info['api-key'] = api_key
            printers.append(info)
        f.close()
        return printers