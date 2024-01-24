from flask import Flask, render_template, request ,redirect, url_for,flash
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db

admin_payment_route = Blueprint('admin_payment', __name__)

mydb=get_db()
mycursor = mydb.cursor()

@admin_payment_route.route('/check_payment', methods=['POST'])
def fees_payment():
    user_id = request.form['user_id']
    mydb.commit()
    mycursor.execute(f"SELECT count(1) FROM payment WHERE user_id='{user_id}'" )
    user1 = mycursor.fetchone()
        
    if user1[0]<1:
        return render_template('admin/Admin_check_payment.html',error="USN does not exist")
    
    mycursor.execute(f"SELECT * FROM payment WHERE user_id='{user_id}'AND payment_status='Not Approved'" )
    user = mycursor.fetchall()
    if not user:
        return render_template('admin/Admin_check_payment.html',error="No request found")
    if user:
        return render_template('admin/Admin_check_payment.html',users=user,)  
     
   
@admin_payment_route.route('/approve_payment', methods=['POST'])
def approve_payment():
    p_id = request.form['p_id']

    sql = "update payment set payment_status=%s where id=%s"
    val = ("Approved",p_id)
    mycursor.execute(sql,val)
    mydb.commit()
    return render_template('admin/Admin_check_payment.html',success="Approved successfully")

