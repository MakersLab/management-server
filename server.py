import os
from flask import Flask, url_for, render_template, request, redirect
from time import localtime
from time import sleep
import json

app = Flask(__name__)
app.debug = True

CURA_SCRIPT_PATH = 'cura.sh'
STREAM_PORT = 4000

PRINTERS_PATH = 'printers.txt'
STL_PRICING_FILE_PATH = 'uploads/temporary.stl'

info = {
    'username': 'Jakub Zíka',
}

'''Hlavní stránka'''


@app.route('/')
def index():
    return render_template('pages/index.jinja2', info=info)


'''Ocenění modelů'''


@app.route('/stl-pricing', methods=['POST', 'GET'])
def upload():
    # Jestli je požadavek typu POST tak se uloží poslaný soubor a uživateli se zobrazí processing stránka
    if request.method == 'POST':
        file = request.files["file"]
        filename = file.filename

        # ověření že nahraný soubor je typu stl
        if (filename.split('.')[-1] == 'stl'):

            # cesta kde se uloží stl
            path = os.path.normcase(os.path.join(os.path.dirname(__file__), STL_PRICING_TEMPORARY_PATH))
            try:
                file.save(path)
            except(Exception):
                return 'File was not uploaded'

            return render_template('pages/processing.jinja2', filename=filename, info=info)
        return 'Wrong file type'

    # jestli je požadavek typu GET tak se uživateli zobrazí stránka kde může nahrát soubor
    elif request.method == 'GET':
        return render_template('pages/file_upload.jinja2', info=info)


#
@app.route('/stl-pricing/slice', methods=['POST'])
def slicing():
    state = {
        'price': 50,
        'successful': True,
    }
    filename=request.form['filename']
    # provedení skriptu cura.sh
    executeSlicingScript(filename)
    stateJson = json.dumps(state)
    return stateJson

#provedení skriptu + vygenerování jména pro gcode
def executeSlicingScript(filename):
    #generování jména
    time = localtime()
    gcoName = ''
    for i in range(3):
        gcoName += '_' + str(time[i])
    gcoName += '.'.join(filename.split('.')[0:-1])
    #provedení skriptu
    os.system('sudo sh ' + CURA_SCRIPT_PATH + ' ' + gcoName)
    print_time = 4
    return print_time


#stránka s ovládáním streamů
@app.route('/stream')
def stream():
    printers = generateNames()
    return render_template('pages/stream.jinja2', info=info, list=printers)

#převedení printers.txt na dictionary
def generateNames():
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


#Nenavrací html stránku ale JSON přes AJAX
@app.route('/stream/control', methods=['POST'])
def streamControl():
    #Zjištění adresy tiskárny podle jména
    printer = request.form['printer']
    list = generateNames()
    address = list[int(printer)]['address']

    # Zjištění jestli se stream má zastavit nebo spustit
    command = request.form['command']
    if (request.form['command'] == 'stop'):
        key = None
    else:
        key = request.form['key']

    # zaslání požadavku na příslušné raspberry pi
    successful, message = sendCommand(address, command, key)
    # vytvoření knihovny a převedení na JSON a poslání klientovi
    data = {
        'successful': successful,
        'message': message,
    }
    return json.dumps(data)

# poslání příkazu na vybranou adresu
def sendCommand(address, data, key):
    import socket
    #vytvoření soketu
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #navázání spojení
    try:
        connection.connect((address, STREAM_PORT))
    except Exception as e:
        print(e)
        return False, 'Could not connect to server. Invalid IP address'
    #poslání požadavku
    msgSend = {'control': data, 'key': key}
    connection.send(json.dumps(msgSend).encode())
    #přijmutí odpovědé
    msg_recv = connection.recv(256)
    msg_decoded = msg_recv.decode('utf8')
    msg_decoded = json.loads(msg_decoded)
    connection.close()
    #poslání zprávy uživatel
    # i
    return msg_decoded['successful'], msg_decoded['message']

#pokud je zavolán přímo tento skript tak se spustí defalutní server
if __name__ == '__main__':
    app.run('0.0.0.0')
