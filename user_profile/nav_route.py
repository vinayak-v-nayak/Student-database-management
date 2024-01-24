from flask import Flask, render_template, request ,redirect, url_for,flash,session
import mysql.connector
from flask import Blueprint
from db.db_connect import get_db
#from datetime import timedelta


nav_route = Blueprint('navigation', __name__)
#nav_route.permanent_session_lifetime = timedelta(days=1)


mydb=get_db()
mycursor = mydb.cursor()

@nav_route.route('/go_to_homepage')
def go_to_homepage():
    return render_template('base.html')


@nav_route.route('/go_to_contact')
def go_to_about():
    return render_template('contact.html')


@nav_route.route('/go_to_library')
def go_to_library():
    return render_template('library.html')


@nav_route.route('/admin_login')
def admin_login():
    return render_template('admin/admin_login.html')

@nav_route.route('/student_login')
def student_login():
    if "user_id" in session:
        user_id=session["user_id"]
        mycursor.execute("SELECT * FROM users_reg WHERE user_id=%s", (user_id,))
        user = mycursor.fetchone()
        if user[9]=='student':
            return render_template('student/index.html',users=user)
        else:
            return render_template('student/student_login.html')
    else:
        return render_template('student/student_login.html')
    
    
@nav_route.route('/teacher_login')
def teacher_login():
    if "user_id1" in session:
        user_id=session["user_id1"]
        mycursor.execute("SELECT * FROM users_reg WHERE user_id=%s", (user_id,))
        user = mycursor.fetchone()
        if user[9]=='teacher':
            mycursor.execute("SELECT * FROM semester")
            sem=mycursor.fetchall()
            mycursor.execute("SELECT user_id FROM users_reg where usertype='student'")
            user_id=mycursor.fetchall()
            return render_template('teacher/teacher.html',user_id=user_id,sem=sem)
        else:
            return render_template('teacher/teacher_login.html')
        
    else:
        return render_template('teacher/teacher_login.html')



@nav_route.route('/go_to_admin_payment')
def go_to_admin_payment():
    return render_template('admin/Admin_check_payment.html')


@nav_route.route('/admin_payment_to_register')
def admin_payment_to_register():
    return render_template('admin/registration.html')


@nav_route.route('/logout')
def logout():
    session.pop("user_id", None)
    return render_template('homepage.html')

@nav_route.route('/logout_teacher')
def logout_teacher():
    session.pop("user_id1", None)
    return render_template('homepage.html')


@nav_route.route('/go_to_student_payment')
def go_to_student_payment():
    return render_template('student/student_fees_payment.html')


@nav_route.route('/student_check_payment_status')
def student_check_payment_status():
    if "user_id" in session:
        user_id=session["user_id"]
        mycursor.execute("SELECT * FROM users_reg WHERE user_id=%s", (user_id,))
        user = mycursor.fetchone()
        if user[9]=='student':
            return render_template('student/student_check_payment_status.html',user_id=user_id)
        else:
            return render_template('student/student_login.html')
        
    else:
        return render_template('student/student_login.html')



@nav_route.route('/student_check_marks')
def student_check_marks():
    if "user_id" in session:
        user_id=session["user_id"]
        mycursor.execute("SELECT * FROM users_reg WHERE user_id=%s", (user_id,))
        user = mycursor.fetchone()
        if user[9]=='student':
            return render_template('student/student_check_marks.html',user_id=user_id)
        else:
            return render_template('student/student_login.html')
    else:
        return render_template('student/student_login.html')


    
@nav_route.route('/go_to_student_profile')
def go_to_student_profile():
    if "user_id" in session:
        user_id=session["user_id"]
        mycursor.execute("SELECT * FROM users_reg WHERE user_id=%s", (user_id,))
        user = mycursor.fetchone()
        if user[9]=='student':
            mycursor.execute("SELECT * FROM users_reg WHERE user_id=%s", (user_id,))
            user = mycursor.fetchone()
            return render_template('student/index.html',users=user)
        else:
            return render_template('student/student_login.html')    
    else:
        return render_template('student/student_login.html')

@nav_route.route('/messages')
def messages():
    mydb.commit()
    mycursor.execute("SELECT * FROM contact WHERE solution='pending' " )
    user = mycursor.fetchall()
    if user:
        return render_template('admin/messages.html',user=user)
    else:
        return render_template('admin/messages.html',success="NO Messages")

