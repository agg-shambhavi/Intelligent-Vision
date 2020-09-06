import pandas as pd
from pipeline_ml import img_to_vid_match
from flask import Flask, session
import os
import shutil
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import sys
from flask_mysqldb import MySQL
import pathlib
sys.path.append(".")

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, static_url_path="/static")

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG', 'm4v', 'mp4'}

# db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db1'

mysql = MySQL(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['DEBUG'] = True


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/file', methods=['GET', 'POST'])
def file():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        filename1 = file1.filename
        filename2 = file2.filename
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        vid_path = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        matcher = img_to_vid_match(img_path, vid_path)
        result_df = matcher.Final_Match()
        files = list(result_df['filepath'])
        dest_folder = pathlib.PurePath(
            'intelligent_vision V1.0\\resultant_images')
        for f in files:
            f_path = pathlib.PurePath(f)
            name_of_file = f_path.name
            shutil.copy(f, dest_folder / name_of_file)
        image_names = os.listdir('intelligent_vision V1.0\\resultant_images')
        return render_template('output.html', image_names=image_names)
        # return "Successful"
    return "Error"


@ app.route("/index2", methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        frames_dir = pathlib.PurePath('intelligent_vision V1.0\\Frames_dir')
        resultant_dir = pathlib.PurePath(
            'intelligent_vision V1.0\\resultant_images')
        delete_contents(frames_dir)
        delete_contents(resultant_dir)
    return render_template('index2.html')


@ app.route("/team")
def team():
    return render_template("team.html")


@ app.route('/', methods=['GET', 'POST'])
def index_main():
    return render_template('index.html')


@ app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE uname = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            return render_template('feed.html')
        else:
            msg = 'Incorrect username/password!'
    return render_template('cards.html')


@ app.route('/contact', methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        details = request.form
        name = details['name']
        email = details['email']
        subject = details['subject']
        message = details['message']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contact(name,email,subject,message) VALUES(%s,%s,%s,%s)",
                    (name, email, subject, message))
        mysql.connection.commit()
        cur.close()
        return render_template('contact.html')
    return render_template('contact.html')


@ app.route('/support', methods=['GET', 'POST'])
def support():
    if (request.method == 'POST'):
        details2 = request.form
        name = details2['name2']
        email = details2['email2']
        subject = details2['subject2']
        message = details2['m2']
        cur2 = mysql.connection.cursor()
        cur2.execute("INSERT INTO support(name,subject,email,message) VALUES(%s,%s,%s,%s)",
                     (name, email, subject, message))
        mysql.connection.commit()
        cur2.close()
        return render_template('support.html')
    return render_template('support.html')


@ app.route("/output")
def output():
    return render_template("output.html")


@ app.route("/feed")
def feed():
    return render_template("feed.html")


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("C:\\Users\\DELL\\Desktop\\Intelligent-Vision\\intelligent_vision V1.0\\resultant_images", filename)


def delete_contents(dir):
    filelist = [f for f in os.listdir(dir)]
    for f in filelist:
        os.remove(os.path.join(dir, f))


if __name__ == "__main__":
    app.run(debug=True)
