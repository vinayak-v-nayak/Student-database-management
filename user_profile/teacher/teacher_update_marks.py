from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db

update_marks_route = Blueprint('update_marks', __name__)

# Database setup
mydb = get_db()
mycursor = mydb.cursor()

@update_marks_route.route('/update_marks', methods=['POST'])
def update_marks():
    # Retrieve form data for updating marks
    user_id = request.form['user_id']
    semester = request.form['semester']
    subject1_marks = request.form['subject1_marks']
    subject2_marks = request.form['subject2_marks']
    subject3_marks = request.form['subject3_marks']
    subject4_marks = request.form['subject4_marks']
    subject5_marks = request.form['subject5_marks']
    subject6_marks = request.form['subject6_marks']

    sql = "UPDATE student_marks SET subject1_marks=%s,subject2_marks=%s,subject3_marks=%s,subject4_marks=%s,subject5_marks=%s,subject6_marks=%s WHERE user_id=%s AND semester=%s"
    val = (subject1_marks,subject2_marks,subject3_marks,subject4_marks,subject5_marks,subject6_marks,user_id,semester)

    mycursor.execute(sql,val)
    mydb.commit()
    
    mycursor.execute("SELECT * FROM student_marks WHERE user_id = %s AND semester = %s", (user_id, semester))
    marks = mycursor.fetchall()
    if marks:
        mycursor.execute("SELECT * FROM semester")
        sem=mycursor.fetchall()
        mycursor.execute("SELECT user_id FROM users_reg where usertype='student'")
        user_id=mycursor.fetchall()
        return render_template('teacher/teacher.html', marks=marks,sem=sem,user_id=user_id)
