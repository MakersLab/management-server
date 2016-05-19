#!/usr/bin/python
import sys
import os
from flask import Flask, url_for, render_template, request, redirect


app = Flask(__name__)

UPLOADS_PATH = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.debug = True

@app.route('/')
def index():
    return render_template('index.jinja2', )


@app.route('/image_upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files["file"]
        filename = file.filename
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'empty.txt'))
        path=os.path.normcase(os.path.join(os.path.dirname(__file__), 'uploads/temporary.stl'))
        print(path)
        file.save(path)
        return 'File was succesfully uploaded'



with app.test_request_context():
    url_for('static', filename='*')

if __name__ == '__main__':
    app.run()
