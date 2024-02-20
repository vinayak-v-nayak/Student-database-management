from flask import Flask, render_template, request ,redirect, url_for,flash
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db


register_route = Blueprint('submit', __name__)

mydb=get_db()
mycursor = mydb.cursor()


@register_route.route('/register_user', methods=['POST'])
def submit():
    name = request.form['name']
    user_id = request.form['user_id']
    email = request.form['email']
    phone = request.form['mobileNumber']
    gender = request.form['gender']
    usertype = request.form['usertype']

    mycursor.execute(f"SELECT count(1) FROM users_reg WHERE email='{email}'" )
    user2 = mycursor.fetchone()   
    if user2[0]>0:
        return render_template('admin/registration.html',error="Email already exist")
    
    mycursor.execute(f"SELECT count(1) FROM users_reg WHERE user_id='{user_id}'" )
    user1 = mycursor.fetchone()  
    if user1[0]>0:
        return render_template('admin/registration.html',error="User ID already exist")
    
    if len(phone)!=10:
        return render_template('admin/registration.html',error="Enter 10 digits phone number")
    

    sql = "INSERT INTO users_reg (name,user_id, email,phone,gender,usertype) VALUES (%s, %s, %s,%s,%s, %s)"
    val = (name,user_id, email,phone,gender,usertype)
    mycursor.execute(sql,val)
    mydb.commit()
    return render_template('admin/registration.html',success=user_id+" is registered")
