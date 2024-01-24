from flask import Flask, render_template, request ,redirect, url_for,flash
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db

admin_login_route = Blueprint('admin_login', __name__)

mydb=get_db()
mycursor = mydb.cursor()


@admin_login_route.route('/admin_login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        mycursor.execute("SELECT * FROM users_reg WHERE user_id=%s AND password=%s AND usertype='Admin'" , (username, password))
        user = mycursor.fetchone()
        
        if user:
            return render_template('admin/registration.html',users=user)
        else:
            return render_template('admin/admin_login.html',error="Incorrect Username or Password!! Please try again ")
