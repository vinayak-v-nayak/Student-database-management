from flask import Flask, render_template, request ,redirect, url_for,flash
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db

update_route = Blueprint('update', __name__)

mydb=get_db()
mycursor = mydb.cursor()

@update_route.route('/update', methods=['POST'])
def update():
    email = request.form['email']
    phone = request.form['mobileNumber']
    birthdate = request.form['dob']
    adress=request.form['address']
    
    if len(phone)!=10 and len(phone)!=0 :
        mycursor.execute(f"SELECT * FROM users_reg WHERE email='{email}'" )
        user = mycursor.fetchone()
        return render_template('student/index.html',users=user,error="Please enter a valid 10-digit phone number")

    sql = "update users_reg set phone=%s,birthdate=%s,address=%s where email=%s"
    val = (phone,birthdate,adress,email)
    mycursor.execute(sql,val)
    mydb.commit()
    mycursor.execute(f"SELECT * FROM users_reg WHERE email='{email}'" )
    user = mycursor.fetchone()
        
    if user:
        return render_template('student/index.html',users=user,success="Successfully Updated")

