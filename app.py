from flask import Flask, render_template,session
import mysql.connector
from datetime import timedelta
from user_profile.change_password import change_password_route
from user_profile.Admin.register import register_route
from user_profile.student.student_login import student_login_route
from user_profile.teacher.teacher_login import teacher_login_route
from user_profile.Admin.Admin_login import admin_login_route
from user_profile.student.student_update_profile import update_route
from user_profile.student.student_view_marks import view_marks_route
from user_profile.teacher.teacher_see_marks import see_marks_route
from user_profile.teacher.teacher_update_marks import update_marks_route
from user_profile.Admin.Admin_payment import admin_payment_route
from user_profile.student.student_payment import student_payment_route
from user_profile.library import library_route
from user_profile.contact import contact_route
from user_profile.Admin.Admin_message_resolved import admin_message_route

from user_profile.nav_route import nav_route
from db.db_connect import get_db

app = Flask(__name__)
app.secret_key="mysecretkey"
app.permanent_session_lifetime = timedelta(days=3)


app.register_blueprint(register_route)
app.register_blueprint(student_login_route)
app.register_blueprint(teacher_login_route)
app.register_blueprint(update_route)
app.register_blueprint(change_password_route)
app.register_blueprint(admin_login_route)
app.register_blueprint(view_marks_route)
app.register_blueprint(update_marks_route)
app.register_blueprint(see_marks_route)
app.register_blueprint(admin_payment_route)
app.register_blueprint(student_payment_route)
app.register_blueprint(nav_route)
app.register_blueprint(library_route)
app.register_blueprint(contact_route)
app.register_blueprint(admin_message_route)


mydb=get_db()
mycursor = mydb.cursor()

# Create a table to store registration data if it doesn't exist
mycursor.execute('''
CREATE TABLE IF NOT EXISTS users_reg (
id INT AUTO_INCREMENT  ,
name VARCHAR(255),
email VARCHAR(255),
user_id VARCHAR(20) UNIQUE,
phone VARCHAR(10),
gender VARCHAR(10),
birthdate DATE,
adress VARCHAR(255),
password VARCHAR(255),
usertype VARCHAR(255),
PRIMARY KEY (id,user_id)
)
''')
mycursor.execute('''
CREATE TABLE IF NOT EXISTS student_marks (
id INT AUTO_INCREMENT PRIMARY KEY,
user_id VARCHAR(20), 
semester INT NOT NULL,
subject1_marks FLOAT,
subject2_marks FLOAT,
subject3_marks FLOAT,
subject4_marks FLOAT,
subject5_marks FLOAT,
subject6_marks FLOAT,
FOREIGN KEY (user_id) REFERENCES users_reg (user_id)
)
''')

mycursor.execute('''
CREATE TABLE IF NOT EXISTS semester(
id INT AUTO_INCREMENT PRIMARY KEY,
sem INT NOT NULL
)
''')

mycursor.execute('''
CREATE TABLE IF NOT EXISTS contact(
id INT AUTO_INCREMENT PRIMARY KEY,
user_id varchar(100),
email varchar(100),
subject varchar(255),
message varchar(1000),
solution varchar(10)
)
''')

mycursor.execute('''
CREATE TABLE IF NOT EXISTS payment(
id INT AUTO_INCREMENT PRIMARY KEY,
user_id varchar(100),
amount VARCHAR(255),
payment_id VARCHAR(255),
payment_category VARCHAR(255),
payment_status VARCHAR(255)
)
''')
mycursor.execute("SELECT * FROM semester")
result = mycursor.fetchall()

if not result:
    mycursor.execute("INSERT INTO semester (sem) VALUES(1), (2), (3), (4),(5), (6), (7), (8)")
    
mydb.commit()

#start
@app.route('/')
def registration_form():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)