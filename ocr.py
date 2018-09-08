import os
from PIL import Image
import pytesseract
from flask import Flask, request, redirect, url_for,send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''<!doctype html>
<title>OCR to Xss</title>
<center><h1>OCR TO XSS POC</h1></center>
<form action="" method=post enctype=multipart/form-data>
<p><input type=file name=file>
<input type=submit value=Upload></form>
'''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/admin/ocr/files')
def parse_file():
	im=Image.open("uploads/pwned10.jpg")
	text=pytesseract.image_to_string(im,lang='eng')
	return '''<!doctype html>
<title>OCR to Xss</title>
<h1>Admin Panel</h1>
<h2>Files</h2> %s '''%text

if __name__ == '__main__':
    app.run(debug=True)
