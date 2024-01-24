from flask import Flask, render_template, request, redirect, url_for, flash,session
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db

see_marks_route = Blueprint('see_marks', __name__)

# Database setup
mydb = get_db()
mycursor = mydb.cursor()


@see_marks_route.route('/see_marks', methods=['POST','GET'])
def see_marks():
    # Retrieve form data
    if request.method == 'POST':
        semester = request.form['semester']
        user_id = request.form['user_id']
        
        # Check if marks exist for the user and semester
        mydb.commit()
        mycursor.execute("SELECT * FROM student_marks WHERE user_id = %s AND semester = %s", (user_id, semester))
        marks = mycursor.fetchall()
        
        if marks:
            mycursor.execute("SELECT * FROM semester")
            sem=mycursor.fetchall()
            mycursor.execute("SELECT user_id FROM users_reg where usertype='student'")
            user_id=mycursor.fetchall()
            return render_template('teacher/teacher.html', marks=marks,sem=sem,user_id=user_id)
        else:
            # Update the semester for the user if marks not found
            sql = "INSERT INTO student_marks (user_id, semester, subject1_marks, subject2_marks, subject3_marks, subject4_marks, subject5_marks, subject6_marks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (user_id, semester,0,0,0,0,0,0)

            mycursor.execute(sql, val)   
            mydb.commit() 
            mycursor.execute("SELECT * FROM semester")
            sem=mycursor.fetchall()
            mycursor.execute("SELECT * FROM student_marks WHERE user_id = %s AND semester = %s", (user_id, semester))
            marks = mycursor.fetchall()
            mycursor.execute("SELECT user_id FROM users_reg where usertype='student'")
            user_id=mycursor.fetchall()
            return render_template('teacher/teacher.html',marks=marks,sem=sem,user_id=user_id)  
    elif request.method == 'GET':
        if "user_id1" in session:
            mydb.commit()
            mycursor.execute("SELECT * FROM semester")
            sem=mycursor.fetchall()
            mycursor.execute("SELECT user_id FROM users_reg where usertype='student'")
            user_id=mycursor.fetchall()
            return render_template('teacher/teacher.html',sem=sem,user_id=user_id)  

