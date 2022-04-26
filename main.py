from msilib.schema import Error
from multiprocessing import connection
from flask import Flask, redirect,render_template,request,session,flash
import mysql.connector
from flask_mysqldb import MySQL
import os
from os import *



app = Flask(__name__)

app.secret_key=os.urandom(24)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="rohit@2310"
app.config['MYSQL_DB']="usr"

mysql=MySQL(app)

@app.route("/")
def login():
    if 'u_id' not in session:
        return render_template("login.html")
    else:
        return render_template("home.html")

@app.route("/register")
def register():
    return render_template("register.html")

    
@app.route("/home")
def home():
    if 'u_id' in session:
        return render_template("home.html")
    else:
        return redirect('/')

@app.route("/login_validation",methods=["POST"])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    cur=mysql.connection.cursor()
    cur.execute(""" SELECT * FROM info WHERE email LIKE '{}' AND password LIKE '{}'""".format(email,password))
    user=cur.fetchall()
    if len(user)>0:
        session['u_id']=user[0][0]
        flash("You have log in..")
        return redirect("/home")
    else:
        return redirect("/")

@app.route("/add_user",methods=["POST"])
def add_user():
    name=request.form.get("uname")
    email=request.form.get("uemail")
    password=request.form.get("upassword")
    cur=mysql.connection.cursor()
    cur.execute("""INSERT INTO info (name,email,password) VALUES
    ('{}','{}','{}')""".format(name,email,password))
    mysql.connection.commit()
    cur.execute(""" SELECT * FROM info WHERE email LIKE '{}'""".format(email))
    newuser=cur.fetchall()
    session['u_id']=newuser[0][0]
    flash("You have Register successfully")
    return redirect("/home")

@app.route("/logout")
def logout():
    session.pop('u_id')
    flash("You have logout")
    return redirect('/')



if __name__=="__main__":
    app.run(debug=True)