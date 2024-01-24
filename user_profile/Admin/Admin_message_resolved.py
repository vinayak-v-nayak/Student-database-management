from flask import Flask, render_template, request ,redirect, url_for,flash
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db

admin_message_route = Blueprint('admin_message', __name__)

mydb=get_db()
mycursor = mydb.cursor()

@admin_message_route.route('/request_resolved', methods=['POST'])
def request_resolved():
    message_id = request.form['message_id']

    sql = "update contact set solution=%s where id=%s"
    val = ("Resolved",message_id)
    mycursor.execute(sql,val)
    mydb.commit()
    mycursor.execute("SELECT * FROM contact WHERE solution='pending' " )
    user = mycursor.fetchall()
    if user:
        return render_template('admin/messages.html',user=user)
    else:
        return render_template('admin/messages.html',success="NO Messages")
