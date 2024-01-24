from flask import Flask, render_template, request ,redirect, url_for,flash, session
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db

contact_route = Blueprint('contact', __name__)

mydb=get_db()
mycursor = mydb.cursor()


@contact_route.route('/contact', methods=['POST'])
def login_user():
    email = request.form['email']
    user_id = request.form['user_id']
    subject = request.form['subject']
    message = request.form['message']

    sql = "INSERT INTO contact (user_id, email, subject, message, solution) VALUES (%s, %s, %s, %s, 'pending')"
    val = (user_id, email, subject, message)
    mycursor.execute(sql, val)
    mydb.commit()
    return render_template('contact.html',success="Successfully sent")
