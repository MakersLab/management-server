import os
from flask import Flask, url_for, render_template, request, redirect
from time import localtime, strftime
import json
from modules.generateNames import generateNames
from modules.backup import backup as dataBackup
from modules.octoprintAPI import sendFile, startPrint
import threading

app = Flask(__name__)
app.debug = True

CURA_SCRIPT_PATH = 'cura.sh'
STREAM_PORT = 4000

PRINTERS_PATH = 'printers.txt'
STL_PRICING_FILE_PATH = 'uploads/temporary.stl'
STL_PRICING_TEMPORARY_PATH = 'uploads/'

current_gcode = ''

PRICING = 200

info = {
    'username': 'Jakub Zíka',
}


@app.route('/')
def index():
    return render_template('pages/index.jinja2', info=info)


@app.route('/stl-pricing', methods=['POST', 'GET'])
def upload():
    # Jestli je požadavek typu POST tak se uloží poslaný soubor a uživateli se zobrazí processing stránka
    if request.method == 'POST':
        file = request.files["file"]
        filename = file.filename

        # ověření že nahraný soubor je typu stl
        if (filename.split('.')[-1].lower() == 'stl'):

            # cesta kde se uloží stl
            path = os.path.normcase(os.path.join(os.path.dirname(__file__), STL_PRICING_FILE_PATH))
            try:
                file.save(path)
            except(Exception):
                return 'File was not uploaded'
            list = generateNames(PRINTERS_PATH)
            return render_template('pages/processing.jinja2', filename=filename, info=info, list=list)
        return 'Wrong file type'

    # jestli je požadavek typu GET tak se uživateli zobrazí stránka kde může nahrát soubor
    elif request.method == 'GET':
        return render_template('pages/file_upload.jinja2', info=info)


@app.route('/stl-pricing/slice', methods=['POST'])
def slicing():
    filename = request.form['filename']
    state = {}
    # provedení skriptu cura.sh
    print_time = 0
    try:
        print_time, current_gcode = executeSlicingScript(filename)
    except Exception as e:
        state = {
            'print_time': 0,
            'successful': True,
            'message': str(e),
        }
        stateJson = json.dumps(state)
        return stateJson
    print(print_time)
    print_time = round(print_time / 60, 1)
    price = 200
    state = {
        'print_time': print_time,
        'price': round(print_time / 60 * price, 1),
        'successful': True,
        'message': 'none'
    }

    stateJson = json.dumps(state)
    return stateJson


@app.route('/stl-pricing/print')
def stl_pricing_print():
    printer_index = int(request.form['printer'])
    list = generateNames(PRINTERS_PATH)
    printer = list[printer_index]
    print(current_gcode)
    r = sendFile(current_gcode, printer)
    print(r.text)
    if (r.status_code != 200):
        response = {'successful': False,}
        return json.dumps(response)

    r = startPrint(current_gcode, printer)
    print(r.text)
    if (r.status_code == 200):
        response = {'successful': True}
        return json.dumps(response)
    else:
        response = {'successful': False}
        return json.dumps(response)


#
@app.route('/management')
def management():
    return render_template('pages/management.jinja2', info=info)


@app.route('/management/backup', methods=['POST', ])
def backup():
    t = threading.Thread(target=dataBackup, args=[])
    if (request.form['backup'] == 'true'):
        t.start()
    data = {
        'successful': True,
        'message': 'Backup should start.',
    }
    return json.dumps(data)


# provedení skriptu + vygenerování jména pro gcode
def executeSlicingScript(filename):
    # generování jména
    time = localtime()
    gcoName = ''

    gcoName += strftime("%Y_%m_%d_%H_%M", localtime()) + '.'.join(filename.split('.')[0:-1])
    # provedení skriptu
    response = os.popen('sudo sh ' + CURA_SCRIPT_PATH + ' ' + 'data/gcodes/' + gcoName)
    for i in response:
        return int(i), gcoName + '.gcode'


# stránka s ovládáním streamů
@app.route('/stream')
def stream():
    printers = generateNames(PRINTERS_PATH)
    return render_template('pages/stream.jinja2', info=info, list=printers)


# Nenavrací html stránku ale JSON přes AJAX
@app.route('/stream/control', methods=['POST'])
def streamControl():
    # Zjištění adresy tiskárny podle jména
    printer = request.form['printer']
    list = generateNames(PRINTERS_PATH)
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
    # vytvoření soketu
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # navázání spojení
    try:
        connection.connect((address, STREAM_PORT))
    except Exception as e:
        print(e)
        return False, 'Could not connect to server. Invalid IP address'
    # poslání požadavku
    msgSend = {'control': data, 'key': key}
    connection.send(json.dumps(msgSend).encode())
    # přijmutí odpovědé
    msg_recv = connection.recv(256)
    msg_decoded = msg_recv.decode('utf8')
    msg_decoded = json.loads(msg_decoded)
    connection.close()
    # poslání zprávy uživatel
    return msg_decoded['successful'], msg_decoded['message']


# pokud je zavolán přímo tento skript tak se spustí defalutní server
if __name__ == '__main__':
    app.run('0.0.0.0')
