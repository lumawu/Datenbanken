import re
import flask
from flask import json
from flask.json import jsonify
from flask import request
from flask import render_template
from werkzeug.utils import redirect
import backend

app = flask.Flask(__name__)
# app.config("DEBUG") = True

session_uid = ""
session_password = ""
session_role = ""

@app.route("/", methods = ["GET"])
def renderLogin():
    return render_template("loginPage.html")

@app.route("/submit", methods = ["GET", "POST"])
def login():
    username = request.form['username']
    global session_uid 
    global session_password
    global session_role
    session_uid = str(backend.getUid(username))
    session_password = request.form['password']
    session_role = backend.checkUserRole(session_uid)
    print("session_uid after login: " + str(session_uid))
    if backend.generatePWHash(session_password) == backend.getPWHash(session_uid):
        print("passwords match")
        if session_role == "Admin":
            return redirect("http://localhost:5000/api/admin/home")
        if session_role == "Teacher":
            return redirect("http://localhost:5000/api/teacher/home")
        if session_role == "Student":
            print("session_uid at redirect: " + str(session_uid))
            return redirect("http://localhost:5000/api/student/home")
    else:
        print("passwords don't match")
        return("Passwords don't match, try again")

# trial run admin view
# USERS

@app.route("/api/admin/home", methods=["GET", "POST"])
def adminHome():
    userdata = fetchAllUsers()
    classdata = fetchAllClasses()
    classattendancedata = fetchAllClassAttendances()
    subjectdata = fetchAllSubjects()
    return render_template("viewAdmin.html", userdata=userdata, classdata=classdata, classattendancedata=classattendancedata, subjectdata=subjectdata)

@app.route("/api/admin/users/all", methods=["GET"])
def fetchAllUsers():
    response = backend.fetchAllUsers()
    return response

@app.route("/api/admin/users/new", methods= ["GET", "POST"])
def renderAddUserToDB():
    return render_template("addUserToDB.html")

@app.route("/api/admin/users/new/submit", methods= ["GET", "POST"])
def addUserToDB():
    forename = request.form['forename']
    surname = request.form['surname']
    role = request.form['role']
    username = request.form['username']
    password = request.form['password']
    backend.addUserToDB(forename, surname, role, username, password)
    return render_template("success.html")

@app.route("/api/admin/users/change", methods= ["GET", "POST"])
def renderChangeUserAttribute():
    return render_template("changeUserAttribute.html")

@app.route("/api/admin/users/change/submit", methods= ["GET", "POST"])
def changeUserAttribute():
    uid = request.form['uid']
    attribute = request.form['attribute']
    value = request.form['value']
    backend.changeUserAttribute(uid, attribute, value)
    return render_template("success.html")

@app.route("/api/admin/users/remove", methods = ["GET", "POST"])
def renderRemoveUserFromDB():
    return render_template("removeUserFromDB.html")

@app.route("/api/admin/users/remove/submit", methods = ["GET", "POST"])
def removeUserFromDB():
    uid = request.form["uid"]
    response = backend.removeUserFromDB(uid)
    return render_template("success.html")

# CLASSES
@app.route("/api/admin/classes/all", methods=["GET"])
def fetchAllClasses():
    response = backend.fetchAllClasses()
    return response

@app.route("/api/admin/classes/new", methods= ["GET", "POST"])
def renderAddClassToDB():
    return render_template("addClassToDB.html")

@app.route("/api/admin/classes/new/submit", methods= ["GET", "POST"])
def addClassToDB():
    classname = request.form['classname']
    backend.addClassToDB(classname)
    return render_template("success.html")

@app.route("/api/admin/classes/change", methods= ["GET", "POST"])
def renderChangeClassName():
    return render_template("changeClassName.html")

@app.route("/api/admin/classes/change/submit", methods= ["GET", "POST"])
def changeClassName():
    classid = request.form["classid"]
    classname = request.form['classname']
    backend.changeClassName(classid, classname)
    return render_template("success.html")

@app.route("/api/admin/classes/remove", methods = ["GET", "POST"])
def renderRemoveClassFromDB():
    return render_template("removeClassFromDB.html")

@app.route("/api/admin/classes/remove/submit", methods = ["GET", "POST"])
def removeClassFromDB():
    classid = request.form["classid"]
    backend.removeClassFromDB(classid)
    return render_template("success.html")

# CLASSATTENDANCES
@app.route("/api/admin/classes/attendances/all", methods=["GET"])
def fetchAllClassAttendances():
    response = backend.fetchAllClassAttendances()
    return response

@app.route("/api/admin/classes/users/assign", methods = ["GET", "POST"])
def renderAddUserToClass():
    return render_template("addUserToClass.html")

@app.route("/api/admin/classes/users/assign/submit", methods = ["GET", "POST"])
def addUserToClass():
    uid = request.form["uid"]
    classid = request.form["classid"]
    backend.addUserToClass(uid, classid)
    return render_template("success.html")

@app.route("/api/admin/classes/users/deassign", methods = ["GET", "POST"])
def renderRemoveUserFromClass():
    return render_template("removeUserFromClass.html")

@app.route("/api/admin/classes/users/deassign/submit", methods = ["GET", "POST"])
def removeUserFromClass():
    uid = request.form["uid"]
    backend.removeUserFromClassByUid(uid)
    return render_template("success.html")

# SUBJECTS
@app.route("/api/admin/subjects/all", methods=["GET"])
def fetchAllSubjects():
    response = backend.fetchAllSubjects()
    return response

@app.route("/api/admin/subjects/new", methods=["GET", "POST"])
def renderAddSubjectToDB():
    return render_template("addSubjectToDB.html")

@app.route("/api/admin/subjects/new/submit", methods=["GET", "POST"])
def addSubjectToDB():
    name = request.form["name"]
    classid = request.form["classid"]
    uid = request.form["uid"]
    archived = request.form["archived"]
    backend.addSubjectToDB(name, classid, uid, archived)
    return render_template("success.html")

@app.route("/api/admin/subjects/change", methods= ["GET", "POST"])
def renderChangeSubjectAttribute():
    return render_template("changeSubjectAttribute.html")

@app.route("/api/admin/subjects/change/submit", methods= ["GET", "POST"])
def changeSubjectAttribute():
    subjid = request.form['subjid']
    attribute = request.form['attribute']
    value = request.form['value']
    backend.changeSubjectAttribute(subjid, attribute, value)
    return render_template("success.html")

@app.route("/api/admin/subjects/dispose", methods= ["GET", "POST"])
def renderDisposeOfSubject():
    return render_template("disposeOfSubject.html")

@app.route("/api/admin/subjects/dispose/submit", methods= ["GET", "POST"])
def disposeOfSubject():
    subjid = request.form['subjid']
    backend.disposeOfSubject(subjid)
    return render_template("success.html")

# trial run teacher view
@app.route("/api/teacher/home", methods=["GET", "POST"])
def teacherHome():
    pupildata = fetchAllPupilsAvgGrades()
    testdata = fetchAllTests()
    subjectdata = fetchAllSubjects()
    return render_template("viewTeacher.html", pupildata = pupildata, testdata = testdata, subjectdata = subjectdata)

@app.route("/api/teacher/users/all", methods=["GET"])
def fetchAllPupilsAvgGrades():
    response = backend.fetchAllPupilsAvgGrades()
    return response

@app.route("/api/teacher/tests/all", methods=["GET"])
def fetchAllTests():
    response = backend.fetchAllTests()
    return response

@app.route("/api/teacher/tests/new", methods= ["GET", "POST"])
def renderAddTestToDB():
    return render_template("addTestToDB.html")

@app.route("/api/teacher/tests/new/submit", methods= ["GET", "POST"])
def addTestToDB():
    name = request.form['name']
    date = request.form['date']
    subjid = request.form['subjid']
    uid = request.form['uid']
    grade = request.form['grade']
    backend.addTestToDB(name, date, subjid, uid, grade)
    return render_template("success.html")

@app.route("/api/teacher/tests/change", methods= ["GET", "POST"])
def renderChangeTestAttribute():
    return render_template("changeTestAttribute.html")

@app.route("/api/teacher/tests/change/submit", methods= ["GET", "POST"])
def changeTestAttribute():
    testid = request.form['testid']
    attribute = request.form['attribute']
    value = request.form['value']
    backend.changeTestAttributeByTestId(testid, attribute, value)
    return render_template("success.html")

@app.route("/api/teacher/tests/results/query", methods=["GET", "POST"])
def renderFetchAllPupilsAndGradesForTest():
    return render_template("fetchAllPupilsAndGradesForTest.html")

@app.route("/api/teacher/tests/results/query/submit", methods=["GET", "POST"])
def fetchAllPupilsAndGradesForTest():
    name = request.form["name"]
    data = backend.fetchAllPupilsAndGradesForTest(name)
    return render_template("viewTeacherFetch.html", data = data)

@app.route("/api/teacher/tests/results/query/edit", methods=["GET", "POST"])
def renderEditGradeOfPupilInTest():
    return render_template("editGradeOfPupilInTest.html")

@app.route("/api/teacher/tests/results/query/edit/submit", methods=["GET", "POST"])
def editGradeOfPupilInTest():
    uid = request.form["uid"]
    testid = request.form["testid"]
    grade = request.form["grade"]
    backend.editGradeOfPupilInTest(uid, testid, grade)
    return render_template("success.html")

@app.route("/api/teacher/tests/remove", methods = ["GET", "POST"])
def renderRemoveTestFromDB():
    return render_template("removeTestFromDB.html")

@app.route("/api/teacher/tests/remove/submit", methods = ["GET", "POST"])
def removeTestFromDB():
    name = request.form["name"]
    backend.removeTestFromDB(name)
    return render_template("success.html")

@app.route("/api/teacher/attributes/change", methods= ["GET", "POST"])
def renderTeacherChangeUserAttribute():
    return render_template("teacherChangeUserAttribute.html")

@app.route("/api/teacher/attributes/change/submit", methods= ["GET", "POST"])
def teacherChangeUserAttribute():
    uid = session_uid
    attribute = request.form['attribute']
    value = request.form['value']
    backend.changeUserAttribute(uid, attribute, value)
    return render_template("success.html")

# trial run of pupil view
@app.route("/api/student/home", methods=["GET", "POST"])
def studentHome():
    print("session_uid at student home: " + str(session_uid))
    performancedata = backend.fetchAllSubjectsAndAvgGradesOneStudent(session_uid)
    print(performancedata)
    return render_template("viewPupil.html", performancedata = performancedata)

@app.route("/api/student/subjects/query", methods = ["GET"])
def renderFetchAllTestsAndGradesOneSubjectOneStudent():
    return render_template("fetchAllTestsAndGradesOneSubjectOneStudent.html")

@app.route("/api/student/subjects/query/submit", methods=["GET", "POST"])
def fetchAllTestsAndGradesOneSubjectOneStudent():
    subjid = request.form["subjid"]
    print("received subjid: " + str(subjid))
    data = backend.fetchAllTestsAndGradesOneSubjectOneStudent(subjid, session_uid)
    print(data)
    return render_template("viewPupilFetch.html", data = data)

@app.route("/api/student/attributes/change", methods= ["GET", "POST"])
def renderPupilChangeUserAttribute():
    return render_template("pupilChangeUserAttribute.html")

@app.route("/api/student/attributes/change/submit", methods= ["GET", "POST"])
def pupilchangeUserAttribute():
    uid = session_uid
    attribute = request.form['attribute']
    value = request.form['value']
    backend.changeUserAttribute(uid, attribute, value)
    return render_template("success.html")

app.run()