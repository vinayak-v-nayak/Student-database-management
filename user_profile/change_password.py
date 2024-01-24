from flask import Flask, render_template, request ,redirect, url_for,flash
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db


change_password_route = Blueprint('changepassword', __name__)

mydb=get_db()
mycursor = mydb.cursor()

@change_password_route.route('/changepassword', methods=['POST'])
def changepassword():
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['cpassword']
    
    if password!=cpassword:
        return render_template('ChangePassword.html',email=email,error="Passwords are not matching")

    sql = "update users_reg set password=%s where email=%s"
    val = (password, email)
    mycursor.execute(sql,val)
    mydb.commit()  

    mycursor.execute(f"SELECT count(1) FROM users_reg WHERE email='{email}' AND password is null" )
    user2 = mycursor.fetchone()
        
    if user2[0]>0:
        return render_template('ChangePassword.html',email=email)
    
    mycursor.execute(f"SELECT * FROM users_reg WHERE email='{email}' " )
    user3 = mycursor.fetchone()
    if user3[9]=='student':
        return render_template('student/student_login.html')
    elif user3[9]=='teacher':
        return render_template('teacher/teacher_login.html')


