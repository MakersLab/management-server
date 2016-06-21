import os
from flask import Flask, url_for, render_template, request, redirect
from time import localtime, strftime
import json
from modules.generateNames import generateNames
from modules.generateProfileList import generateProfileList, generateProfileDict
from modules.backup import backup as dataBackup
from modules.octoprintAPI import sendFile, startPrint
import threading

app = Flask(__name__)
app.debug = True

CURA_SCRIPT_PATH = 'cura.sh'
STREAM_PORT = 4000

PRINTERS_PATH = 'data/printers.txt'
PROFILES_PATH = "data/profiles.json"

STL_PRICING_FILE_PATH = 'uploads/temporary.stl'
STL_PRICING_TEMPORARY_PATH = 'uploads/'

PRICING = 200

info = {
    'username': 'Jakub Zíka',
}


@app.route('/')
def index():
    return render_template('pages/index.jinja2', info=info)


@app.route('/stl-pricing', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files["file"]
        filename = file.filename

        if (filename.split('.')[-1].lower() == 'stl'):

            path = os.path.normcase(os.path.join(os.path.dirname(__file__), STL_PRICING_FILE_PATH))
            try:
                file.save(path)
            except(Exception):
                return 'File was not uploaded'
            list = generateNames(PRINTERS_PATH)

            path = os.path.normcase(os.path.join(os.path.dirname(__file__), PROFILES_PATH))
            profilesList = generateProfileList(path)

            return render_template('pages/processing.jinja2', filename=filename, info=info, list=list,
                                   profilesList=profilesList)

        return 'Wrong file type'

    elif request.method == 'GET':
        return render_template('pages/file_upload.jinja2', info=info)


@app.route('/stl-pricing/slice', methods=['POST',])
def slicing():
    filename = request.form['filename']
    profiles = json.loads(request.form['profiles'])
    state = {
        'results':[]
    }
    print_time = 0
    profilesList = generateProfileDict(PROFILES_PATH)
    successful = False
    for profile in profiles:
        path = profilesList['slic3r-profile-path'] + profilesList['profiles'][int(profile['index'])]['slic3r-path']

        if (profile['slice']):
            # try:
            print(path)
            print_time, gcode_name = executeSlicingScript(filename, path,profilesList['profiles'][int(profile['index'])]['name'])
            successful = True
            # except Exception as e:
            #     successful = False
            #     print(e)
            print_time = round(print_time / 60, 1)
            price = round(print_time / 60 * PRICING, 1)
            temp={
                'print_time':print_time,
                'price':price,
                'succesful':successful,
                'used-profile':profilesList['profiles'][int(profile['index'])]['name'],
            }
            state['results'].append(temp)
    # '''state = {
    #     'print_time': print_time,
    #     'price': round(print_time / 60 * PRICING, 1),
    #     'successful': True,
    #     'message': 'none',
    #     'gcode': gcode_name,
    # }'''

    stateJson = json.dumps(state)
    return stateJson


@app.route('/stl-pricing/print', methods=['POST'])
def stl_pricing_print():
    printer_index = int(request.form['printer'])
    gcode_name = request.form['gcode']
    list = generateNames(PRINTERS_PATH)
    printer = list[printer_index]
    r, apiResponse = sendFile(gcode_name, printer)
    if (r.status_code != 201):
        response = {'successful': False, 'status-code': r.status_code, 'message': 'Failed at send file'}
        return json.dumps(response)

    r, apiResponse = startPrint(gcode_name, printer)
    if (r.status_code == 204):
        response = {'successful': True, 'status-code': r.status_code, 'message': 'Failed at print file',
                    'print_successful': apiResponse['done']}
        return json.dumps(response)
    else:
        response = {'successful': False, 'status-code': r.status_code, 'message': 'All done',
                    'print_successful': apiResponse['done']}
        return json.dumps(response)


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


def executeSlicingScript(filename, parameters, profile):
    time = localtime()
    gcoName = ''
    print(filename,parameters,profile)
    gcoName += strftime("%Y_%m_%d_%H_%M", localtime()) + '_' + profile + '_' + '.'.join(filename.split('.')[0:-1])
    response = os.popen('sudo sh ' + CURA_SCRIPT_PATH + ' ' + 'data/gcodes/' + gcoName + ' ' + parameters)
    for i in response:
        return int(i), gcoName + '.gcode'


@app.route('/stream')
def stream():
    printers = generateNames(PRINTERS_PATH)
    return render_template('pages/stream.jinja2', info=info, list=printers)


@app.route('/stream/control', methods=['POST'])
def streamControl():
    printer = request.form['printer']
    list = generateNames(PRINTERS_PATH)
    address = list[int(printer)]['address']

    command = request.form['command']
    if (request.form['command'] == 'stop'):
        key = None
    else:
        key = request.form['key']

    successful, message = sendCommand(address, command, key)
    data = {
        'successful': successful,
        'message': message,
    }
    return json.dumps(data)


def sendCommand(address, data, key):
    import socket
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection.connect((address, STREAM_PORT))
    except Exception as e:
        print(e)
        return False, 'Could not connect to server. Invalid IP address'
    msgSend = {'control': data, 'key': key}
    connection.send(json.dumps(msgSend).encode())
    msg_recv = connection.recv(256)
    msg_decoded = msg_recv.decode('utf8')
    msg_decoded = json.loads(msg_decoded)
    connection.close()
    return msg_decoded['successful'], msg_decoded['message']


if __name__ == '__main__':
    app.run('0.0.0.0')
