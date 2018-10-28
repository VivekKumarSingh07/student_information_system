from flask import Flask, url_for, render_template, g, request, redirect
import os
import sqlite3


app = Flask(__name__)
DATABASE = "data.db"

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
		db.row_factory = sqlite3.Row
	return db

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

def change_db(query,args=()):
	cur = get_db().execute(query, args)
	get_db().commit()
	cur.close()

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()


@app.route("/")
def index():
	return render_template("index.html")

#
#
# STUDENT BLOCK
#
#


@app.route("/student")
def index_student():
	student_list = query_db("SELECT * FROM student")
	return render_template("/student/index_student.html", student_list=student_list)


@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
	if request.method == "GET":
		return render_template("/student/create_student.html",student=None)
	if request.method == "POST":
		student = request.form.to_dict()
		values = [student["USN"], student["Name"], student["Semester"], student["dob"], student["Section"], student["Class_ID"], student["Mentor"]]
		change_db("INSERT INTO Student VALUES (?, ?, ?, ?, ?, ?, ?)", values)
		return redirect(url_for("index_student"))

@app.route('/update_student/<string:USN>', methods=['GET', 'POST'])
def update_student(USN):
	if request.method == "GET":
		student = query_db("SELECT * FROM Student WHERE USN=?", [USN], one=True)
		print(student["Mentor"])
		return render_template("/student/update_student.html", student=student)
	if request.method == "POST":
		student = request.form.to_dict()

		#TODO
		print(student["Mentor"])

		values = [student["USN"], student["Name"], student["Semester"], student["dob"], student["Section"], student["Class_ID"], student["Mentor"], USN]
		change_db("UPDATE Student SET USN=?, Name=?, Semester=?, dob=?, Section=?, Class_ID=?, Mentor=? WHERE USN=?", values)

		return redirect(url_for("index_student"))

@app.route('/delete_student/<string:USN>', methods=['GET', 'POST'])
def delete_student(USN):
	if request.method == "GET":
		student = query_db("SELECT * FROM student WHERE USN=?", [USN], one=True)
		return render_template("/student/delete_student.html", student=student)
	if request.method == "POST":
		change_db("DELETE FROM student where USN=?", [USN])
		return redirect(url_for("index_student"))


#
#
# STUDENT BLOCK
#
#


#
#
# TEACHER BLOCK
#
#
@app.route("/teacher")
def index_teacher():
	teacher_list = query_db("SELECT * FROM teacher")
	return render_template("/teacher/index_teacher.html", teacher_list=teacher_list)

@app.route('/create_teacher', methods=['GET', 'POST'])
def create_teacher():
	if request.method == "GET":
		return render_template("/teacher/create_teacher.html", teacher=None)
	if request.method == "POST":
		teacher = request.form.to_dict()
		values = [teacher["Teacher"], teacher["Name"], teacher["Class_ID"], teacher["Sub"]]
		change_db("INSERT INTO Student VALUES (?, ?, ?, ?, ?, ?, ?)", values)
		return redirect(url_for("index_teacher"))


@app.route('/update_teacher/<string:Teacher_ID>', methods=['GET', 'POST'])
def update_teacher(Teacher_ID):
	if request.method == "GET":
		teacher = query_db("SELECT * FROM teacher WHERE Teacher_ID=?", [Teacher_ID], one=True)
		return render_template("/teacher/update_teacher.html", teacher=teacher)
	if request.method == "POST":
		teacher = request.form.to_dict()
		values = [teacher["Teacher_ID"], teacher["Name"], teacher["Class_ID"], teacher["Subject"], Teacher_ID]
		change_db("UPDATE Teacher SET Teacher_ID=?, Name=?, Class_ID=?, Sub=? WHERE Teacher_ID=?", values)

		return redirect(url_for("index_teacher"))

@app.route('/delete_teacher/<string:Teacher_Id>', methods=['GET', 'POST'])
def delete_teacher(Teacher_Id):
	if request.method == "GET":
		teacher = query_db("SELECT * FROM teacher WHERE Teacher_Id=?", [Teacher_Id], one=True)
		return render_template("/teacher/delete_teacher.html", teacher=teacher)
	if request.method == "POST":
		change_db("DELETE FROM teacher where Teacher_Id=?", [Teacher_Id])
		return redirect(url_for("index_teacher"))

#
#
# TEACHER BLOCK
#
#


#
#
# CLASS BLOCK
#
#

@app.route("/class")
def index_class():
	class_list = query_db("SELECT * FROM class")
	return render_template("/class/index_class.html", class_list=class_list)

#
#
# CLASS BLOCK
#
#

#
#
# PROJECT BLOCK
#
#

@app.route("/projects")
def index_class():
	project_list = query_db("SELECT * FROM Project")
	return render_template("/project/index_project.html", project_list=project_list)


#
#
# PROJECT BLOCK
#
#
if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000, debug=True)
