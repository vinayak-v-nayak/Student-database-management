from flask import Flask, render_template, request ,redirect, url_for,flash
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db

view_marks_route = Blueprint('view_marks', __name__)

mydb=get_db()
mycursor = mydb.cursor()


    
@view_marks_route.route('/view_marks', methods=['POST'])
def view_marks():
    
    semester=request.form['semester']
    user_id = request.form['user_id']
    
    mydb.commit()
    mycursor.execute(f"SELECT * FROM student_marks WHERE user_id='{user_id}' AND semester={semester}")
    data = mycursor.fetchall()

    if data:       
        return render_template('student/student_check_marks.html',data=data,user_id=user_id)
    else: 
        return render_template('student/student_check_marks.html',error="Marks for this semester are not available",user_id=user_id)
    

