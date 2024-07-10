from flask import Flask, render_template
import csv
from flask import Flask, render_template, redirect, request, session
from flask import Flask, render_template
import firebase_admin
import random
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import os
from google.cloud.firestore_v1 import FieldFilter
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from flask import render_template, session, redirect, url_for
import firebase_admin
import random
from flask import Flask, request
from firebase_admin import credentials, firestore
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
app=Flask(__name__)
app.secret_key="SlotBooking@1234"
app.config['upload_folder']='/static/upload'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = 'static/upload'

sender = "dhanu.innovation@gmail.com"
password = "dkgppiexjwbznzcv"

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

@app.route('/')
def homepage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/usermainpage')
def usermainpage():
    try:
        with open('freespace.csv') as csvfile:
            csvreader = csv.reader(csvfile)
            data = [row[0] for row in csvreader]
            new_data = [4 - int(x) for x in data]
            print("Data : ", data)
            print("New Data : ", new_data)
        return render_template('mainpage.html', data=data, new_data=new_data)
    except Exception as e:
        return str(e)

@app.route('/index')
def indexpage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/logout')
def logoutpage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/loginpage', methods=["POST","GET"])
def loginpage():
    try:
        msg = ""
        if request.method == 'POST':
            uname = request.form['uname']
            pwd = request.form['pwd']
            db = firestore.client()
            print("Uname : ", uname, " Pwd : ", pwd)
            newdb_ref = db.collection('newuser')
            dbdata = newdb_ref.get()
            data = []
            flag = False
            for doc in dbdata:
                data = doc.to_dict()
                if (data['UserName'] == uname and data['Password'] == pwd):
                    flag = True
                    session['userid'] = data['id']
                    break
            if (flag):
                return redirect(url_for("usermainpage"))
            else:
                msg = "UserName/Password is Invalid"
                return render_template("loginpage.html", msg=msg)
        else:
            return render_template("loginpage.html", msg=msg)
    except Exception as e:
        return render_template("loginpage.html", msg=e)


@app.route('/registerpage', methods=["POST","GET"])
def registerpage():
    try:
        msg = ""
        if request.method == 'POST':
            print("Add New Register page")
            fname = request.form['fname']
            lname = request.form['lname']
            uname = request.form['uname']
            pwd = request.form['pwd']
            email = request.form['email']
            phnum = request.form['phnum']
            address = request.form['address']
            id = str(random.randint(1000, 9999))
            json = {'id': id,
                    'FirstName': fname,'LastName': lname,
                    'UserName': uname, 'Password': pwd,
                    'EmailId': email, 'PhoneNumber': phnum,
                    'Address': address}
            db = firestore.client()
            newuser_ref = db.collection('newuser')
            id = json['id']
            newuser_ref.document(id).set(json)
            msg = "New User Added Success"
            return render_template("registerpage.html", msg=msg)
        else:
            return render_template("registerpage.html", msg=msg)
    except Exception as e:
        return str(e)


@app.route('/contact', methods=["POST","GET"])
def contact():
    try:
        return render_template("contact.html")
    except Exception as e:
        return str(e)




if __name__ == '__main__':
    app.run(host ="localhost", port=int(5000), debug=True)
