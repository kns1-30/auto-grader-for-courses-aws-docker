import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'cc'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message="";
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            message = 'No file part'
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            message = 'No selected file'
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('check_file'),filename)
    message ='In comaptible Extension not allowed'       
    return render_template('hello.html', var= message)
    
@app.route('/compile')
def check_file(filename):
	var="Could not display, try again";
	corr=""
	err=0;
	import os
	import subprocess
	subprocess.call("rm -f ./a.out", shell=True)
	retcode = subprocess.call("/usr/bin/g++ uploads/walk.cc", shell=True)
	if retcode:
		corr="failed to compile walk.cc"
		exit
	err=1;	
	subprocess.call("rm -f ./output", shell=True)
	retcode = subprocess.call("./test.sh", shell=True)
	corr= "Score: " + str(retcode) + " out of 2 correct."
	
	with open('uploads/walk.cc','r') as fs:
		var= fs.read()
	return render_template('code.html', variable=var, correct= corr)
		

@app.route('/walk')
def download_file():
    return send_from_directory(app.config["UPLOAD_FOLDER"], 'walk.cc')   
    
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
     
