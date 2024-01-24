from flask import Flask, render_template, request ,redirect, url_for,flash, session
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db
from datetime import timedelta


student_login_route = Blueprint('student_login', __name__)
student_login_route.permanent_session_lifetime = timedelta(days=1)

mydb=get_db()
mycursor = mydb.cursor()


@student_login_route.route('/login_student', methods=['POST'])
def login_student():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        mydb.commit()

        mycursor.execute(f"SELECT count(1) FROM users_reg WHERE email='{email}' and usertype='student' " )
        user1 = mycursor.fetchone()
        
        if user1[0]<1:
            return render_template('student/student_login.html',error="Email does not exist")
        
        mycursor.execute(f"SELECT count(1) FROM users_reg WHERE email='{email}' AND password is null" )
        user2 = mycursor.fetchone()
        
        if user2[0]>0:
            return render_template('ChangePassword.html',email=email)
        
        mycursor.execute("SELECT * FROM users_reg WHERE email=%s AND password=%s", (email, password))
        user = mycursor.fetchone()
        if user==None:
            return render_template('student/student_login.html',error="Incorrect Password!! Please try again ")
    
        session["user_id"]=user[3]
        return render_template('student/index.html',users=user)
        
    return render_template('student/student_login.html')