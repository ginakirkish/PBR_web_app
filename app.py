from flask import Flask, redirect, render_template
from glob import glob
from flask import request
import os

mse_folder = "temp/"
allowed_extensions = set(['txt'])

app = Flask(__name__)
app.config['upload_folder'] = mse_folder

def allowed_file(filename):
    if '.' in filename and filename.rsplit('.',1).lower() in allowed_extensions:
        return True
    else:
        return False

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if 'mses' not in request.files:
            flash('No file part')
            return redirect(request.url)
        textfile = request.files['mses']
        if textfile == '':
            flash('No selected file')
            return redirect(request.url)
        if textfile and allowed_file(textfile):
            textfile_name = secure_filename(textfile.filename)
            textfile.save(os.path.join(app.config['upload_folder'], textfile_name))
    with open('static/index.html') as html_code:
        html_text = html_code.readlines()
    my_html = ''.join(html_text)
    return my_html


@app.route('/msid/<msid>')
def show_msid_images(msid):
    # show the user profile for that user
    msid_images = sorted(glob("static/images/{}-*".format(msid)))
    return generate_html(msid_images, msid)

@app.route('/saveForm')
def save_form():
    print(request.args)
    # show the user profile for that user
    return redirect("/")

from flask import Flask, redirect, jsonify

@app.route("/getData/<globStr>", methods=['GET'])
def get_data(globStr):
    image_folders = sorted(glob("static/images/{}*/anatomical_image.png".format(globStr)))
    output_urls = ["/"+s for s in image_folders] #static is in root
    output_data = [{"url": url, "type": None, "part": None,
                    "pbr_name": image_folders[i].split("/")[-2]} for i, url in enumerate(output_urls)]
    return jsonify(output_data)

import json
@app.route("/saveData/", methods=['POST'])
def save_data():
    data = json.loads(request.get_data().decode('utf-8'))
    print(data)
    #do something with the data here -- save it to a file? 
    return "Success! This message is from the server"

if __name__ == "__main__":
    app.run(port=1116)
