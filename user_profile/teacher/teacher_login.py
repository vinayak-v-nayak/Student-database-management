from tokenize import blank_re
from flask import Flask, render_template, request ,redirect, url_for,flash, session
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db

teacher_login_route = Blueprint('teacher_login', __name__)

mydb=get_db()
mycursor = mydb.cursor()


@teacher_login_route.route('/login_teacher', methods=['POST'])
def login_teacher():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        mydb.commit()

        mycursor.execute(f"SELECT count(1) FROM users_reg WHERE email='{email}' and usertype='teacher' " )
        user1 = mycursor.fetchone()
        
        if user1[0]<1:
            return render_template('teacher/teacher_login.html',error="Email does not exist")
        
        mycursor.execute(f"SELECT count(1) FROM users_reg WHERE email='{email}' AND password is null" )
        user2 = mycursor.fetchone()
        
        if user2[0]>0:
            return render_template('ChangePassword.html',email=email)
        
        mycursor.execute("SELECT * FROM users_reg WHERE email=%s AND password=%s", (email, password))
        user = mycursor.fetchone()
        if user==None:
            return render_template('teacher/teacher_login.html',error="Incorrect Password!! Please try again ")
        session["user_id1"]=user[3]
        mycursor.execute("SELECT * FROM semester")
        sem=mycursor.fetchall()
        mycursor.execute("SELECT user_id FROM users_reg where usertype='student'")
        user_id=mycursor.fetchall()
        return render_template('teacher/teacher.html',user_id=user_id,sem=sem)
        
    return render_template('teacher/teacher_login.html')