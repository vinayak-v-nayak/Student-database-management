from flask import Flask, render_template, request ,redirect, url_for,flash
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db

student_payment_route = Blueprint('student_payment', __name__)

mydb=get_db()
mycursor = mydb.cursor()



@student_payment_route.route('/fees_payment', methods=['POST'])
def fees_payment():
    user_id = request.form['user_id']
    payment_category = request.form['payment_category']
    amount = request.form['amount']
    payment_id = request.form['payment_id']
    sql = "insert into payment(user_id,amount,payment_id,payment_category,payment_status) values(%s,%s,%s,%s,%s) "
    val = (user_id,amount,payment_id,payment_category,"Not Approved")
    mycursor.execute(sql,val)
    mydb.commit()
    
    mycursor.execute("SELECT * FROM users_reg WHERE user_id=%s", (user_id,))
    user = mycursor.fetchone()
    return render_template('student/student_fees_payment.html',success="Request sent successfully",user=user)


@student_payment_route.route('/check_payment_status', methods=['POST'])
def check_payment_status():
    user_id=request.form['user_id']
    mydb.commit()
    mycursor.execute(f"SELECT * FROM payment WHERE user_id='{user_id}'" )
    user = mycursor.fetchall()
        
    if user:
        return render_template('student/student_check_payment_status.html',users=user,user_id=user_id)

