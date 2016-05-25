def generateNames(PRINTERS_PATH):
    printers = []
    with open(PRINTERS_PATH, 'r') as f:
        content = f.read()
        content = content.splitlines()
        for index, i in enumerate(content):
            info = {}
            name, address = i.split(' ')
            info['name'] = name
            info['index'] = index
            info['address'] = address
            printers.append(info)
        f.close()
        return printers