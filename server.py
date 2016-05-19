import os
from flask import Flask, url_for, render_template, request, redirect
from time import localtime
from time import sleep
import json

app = Flask(__name__)

UPLOADS_PATH = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

CURA_SCRIPT_PATH='cura.sh'

app.debug = True


@app.route('/')
def index():
    return render_template('index.jinja2', )


@app.route('/image_upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files["file"]
        filename = file.filename
        if(filename.split('.')[-1]=='stl'):
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'empty.txt'))
            path = os.path.normcase(os.path.join(os.path.dirname(__file__), 'uploads/temporary.stl'))
            try:
                file.save(path)
            except(Exception):
                return 'File was not uploaded'
            #executeFromFile(filename)
            return render_template('processing.jinja2',filename=filename)
    return 'Wrong file type'

@app.route('/slicing', methods=['POST'])
def slicing():
    sleep(500)
    state={
        'price':50,
        'successful':True,
    }
    stateJson=json.dumps(state)
    return stateJson


def executeFromFile(filename):
    time=localtime()
    gcoName=''
    for i in range(3):
        gcoName += '_'+str(time[i])
    gcoName += '.'.join(filename.split('.')[0:-1])
    os.system('sudo sh '+CURA_SCRIPT_PATH+' '+gcoName)


with app.test_request_context():
    url_for('static', filename='*')

if __name__ == '__main__':
    app.run()
