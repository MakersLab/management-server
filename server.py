import os
from flask import Flask, url_for, render_template, request, redirect
from time import localtime
from time import sleep
import json

app = Flask(__name__)

UPLOADS_PATH = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

CURA_SCRIPT_PATH = 'cura.sh'
STREAM_PORT = 4000

app.debug = True


@app.route('/')
def index():
    return render_template('pages/index.jinja2', )


@app.route('/stl-pricing', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files["file"]
        filename = file.filename
        if (filename.split('.')[-1] == 'stl'):
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'empty.txt'))
            path = os.path.normcase(os.path.join(os.path.dirname(__file__), 'uploads/temporary.stl'))
            try:
                file.save(path)
            except(Exception):
                return 'File was not uploaded'
            # executeFromFile(filename)
            return render_template('pages/processing.jinja2', filename=filename)
        return 'Wrong file type'
    elif request.method == 'GET':
        return render_template('pages/file_upload.jinja2', )


@app.route('/stl-pricing/slice', methods=['POST'])
def slicing():
    sleep(3)
    state = {
        'price': 50,
        'successful': True,
    }
    stateJson = json.dumps(state)
    return stateJson


def executeFromFile(filename):
    time = localtime()
    gcoName = ''
    for i in range(3):
        gcoName += '_' + str(time[i])
    gcoName += '.'.join(filename.split('.')[0:-1])
    os.system('sudo sh ' + CURA_SCRIPT_PATH + ' ' + gcoName)


@app.route('/stream')
def stream():
    return render_template('pages/stream.jinja2')


@app.route('/stream/control', methods=['POST'])
def streamControl():
    '''Put here socket which connects to raspberry running server and control it'''
    adress = request.form['adress']
    command = request.form['command']
    key = request.form['key']
    successful, message = sendCommand(adress, command,key)
    data = {
        'successful': successful,
        'message': message,
    }
    print(data)
    return json.dumps(data)


def sendCommand(adress, data,key):
    import socket
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection.connect((adress, STREAM_PORT))
        msgSend = {'control': data,'key':key}
        connection.send(json.dumps(msgSend).encode())
        msgRecv = connection.recv(1024)
        msg_decoded = msgRecv.decode('utf8')
        msg_decoded = json.loads(msg_decoded)
        return msg_decoded['successful'], msg_decoded['message']

    except Exception as e:
        print(e)
        return False, 'Could not connect to server'


with app.test_request_context():
    url_for('static', filename='*')

if __name__ == '__main__':
    app.run()
