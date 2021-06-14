import sqlite3
import hashlib
from sqlite3.dbapi2 import TimeFromTicks, connect

## Checks if given uid exists in table USERS
def checkUidExists(uid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT * FROM USERS WHERE UID = ?", (str(uid),))
    if cursor.fetchone() == None:
        print("No user with given uid found")
        return False
    else:
        print("User found")
        return True

def getUid(username):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT UID FROM USERS WHERE USERNAME = ?", (str(username),))
    result = cursor.fetchone()
    conn.close()
    if  result == None:
        print("No user with given username found")
    else:
        print("Uid found")
        return result[0]

## Checks if given classid exists in table CLASSES
def checkClassIdExists(classid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT * FROM CLASSES WHERE CLASSID = ?", (str(classid),))
    if cursor.fetchone() == None:
        print("No class with given classid found")
        return False
    else:
        print("Class found")
        return True

## Checks if given testid exists in table TESTS
def checkTestIdExists(testid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT * FROM TESTS WHERE TESTID = ?", (str(testid),))
    if cursor.fetchone() == None:
        print("No test with given testid found")
        return False
    else:
        print("Test found")
        return True

## Checks if given classid exists in table CLASSES
def checkTestNameExists(testname):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT * FROM TESTS WHERE NAME= ?", (str(testname),))
    if cursor.fetchone() == None:
        print("No test with given testname found")
        return False
    else:
        print("Test found")
        return True

## returns classid of given classname
def getClassID(classname):
    conn = sqlite3.connect("GradingSystemDB.db")
    try:
        cursor = conn.execute("SELECT * FROM CLASSES WHERE NAME = ?", (str(classname),))
        conn.close()
        return cursor.fetchone()[0]
        print("Retrieved classid for given classname")
    except:
        print("Given Classname does not exist in CLASSES")

## checks what role the given uid has
def checkUserRole(uid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT ROLE FROM USERS WHERE UID = ?", (str(uid),))
    role = cursor.fetchone()[0]
    return role

## returns list of dictionaries containing one user each
def fetchAllUsers():
    conn = sqlite3.connect('GradingSystemDB.db')
    cursor = conn.execute('''SELECT * FROM USERS;''')
    responseList = []
    for row in cursor:
        tempdict = {
                "UID": row[0],
                "Forename": row[1],
                "Surname": row[2],
                "Role": row[3],
                "Username": row[4],
        }
        responseList.append(tempdict)
    conn.close()
    print("Fetched ALL from STUDENTS")
    return responseList

## adds user with given variables to table USERS
def addUserToDB(forename, surname, role, username, password):
    pwhash = generatePWHash(password)
    conn = sqlite3.connect("GradingSystemDB.db")
    conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
                VALUES (?, ?, ?, ?, ?)", (str(forename), str(surname), str(role), str(username), str(pwhash),))
    conn.commit()
    conn.close()
    print("Added user to USERS")

## Helper for addUserToDB: returns hexcode of hash of password given
def generatePWHash(password):
    pwhash = hashlib.md5(password.encode()).hexdigest()
    return pwhash

def getPWHash(uid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT PWHASH FROM USERS WHERE UID = ?", (str(uid),))
    result = cursor.fetchone()
    conn.close()
    if  result == None:
        print("No user with given uid found")
    else:
        print("Uid found")
        return result[0]

## changes given attribute to value for given uid
def changeUserAttribute(uid, attribute, value):
    if checkUidExists(uid) == False:
        return
    if attribute == "Role":
        print("Roll cannot be changed")
        return
    if attribute == "UID":
        print("UID cannot be changed")
        return
    conn = sqlite3.connect("GradingSystemDB.db")
    conn.execute("UPDATE USERS SET "+str(attribute)+"= ? WHERE UID = ?", (str(value), str(uid),))
    conn.commit()
    conn.close()

## removes entry of given uid from table USERS
## if role == Teacher, check if they are assigned to at least one subject, if not remove from USERS
## if role == Student, remove all tests of student, remove student from CLASSATTENDANCES, remove student from USERS
def removeUserFromDB(uid):
    if checkUidExists(uid) == False:
        return
    conn = sqlite3.connect("GradingSystemDB.db")
    role = checkUserRole(uid)
    if role == "Teacher":
        if checkTeacherAssigned(uid) == True:
            conn.close()
            print("Teacher is assigned to at least one Subject and cannot be removed")
        else:
            conn.execute("DELETE FROM USERS WHERE UID = ?", (str(uid),))
            conn.commit()
            conn.close()
            print("Teacher removed from DB")
    elif role == "Student":
        purgeStudentTests(uid)
        removeUserFromClassByUid(uid)
        conn.execute("DELETE FROM USERS WHERE UID = ?", (str(uid),))
        conn.commit()
        conn.close()
        print("Student and relevant tests and classattendance removed from DB")
    else:
        conn.execute("DELETE FROM USERS WHERE UID = ?", (str(uid),))
        conn.commit()
        conn.close()
        print("User/Admin removed from DB")

## Helper for removeUserFromDB: check if given uid is a teacher and if so, check if they are assigned to at least one subject
def checkTeacherAssigned(uid):
    conn = sqlite3.connect("GradingSystemDB.db")
    role = checkUserRole(uid)
    if role == "Teacher":
        cursor = conn.execute("SELECT SUBJID FROM SUBJECTS WHERE UID = ?", (str(uid),))
        if cursor.fetchone() == None:
            print("Teacher Assigned: False")
            conn.close()
            return False
        else:
            print("Teacher Assigned: True")
            conn.close()
            return True
    else: 
        print("User is not a Teacher")
        conn.close()
        return False

## Helper for removeUserFromDB: check if given uid is a student, if so remove their tests from TESTS
def purgeStudentTests(uid):
    conn = sqlite3.connect('GradingSystemDB.db')
    role = checkUserRole(uid)
    if role == "Student":
        conn.execute("DELETE FROM TESTS WHERE UID = ?", (str(uid),))
        conn.commit()
        conn.close()
        print("Removed tests related to uid")
    else:
        conn.close()
        print("Given uid doesn't belong to a Student")

## Fetches all entries from Classes, returns list of dictionaries
def fetchAllClasses():
    conn = sqlite3.connect('GradingSystemDB.db')
    cursor = conn.execute('''SELECT * FROM CLASSES;''')
    responseList = []
    for row in cursor:
        tempdict = {
                "ClassID": row[0],
                "Name": row[1],
        }
        responseList.append(tempdict)
    conn.close()
    print("Fetched ALL from CLASSES")
    return responseList

## Fetches all entries from Classes, returns list of dictionaries
def fetchAllClassAttendances():
    conn = sqlite3.connect('GradingSystemDB.db')
    cursor = conn.execute('''SELECT * FROM CLASSATTENDANCES;''')
    responseList = []
    for row in cursor:
        tempdict = {
                "ClassID": row[0],
                "Uid": row[1],
        }
        responseList.append(tempdict)
    conn.close()
    print("Fetched ALL from CLASSATTENDANCES")
    return responseList

## adds given class name to CLASSES
def addClassToDB(classname):
    if checkClassNameTaken(classname) == False:
        conn = sqlite3.connect("GradingSystemDB.db")
        conn.execute("INSERT INTO CLASSES (NAME) \
                    VALUES (?)", (str(classname),))
        conn.commit()
        conn.close()
        print("Added class to CLASSES")
    else:
        print("Class not added because classname already taken")

## Helper for addClassToDB: checks if given classname is already taken
def checkClassNameTaken(classname):
    conn = sqlite3.connect('GradingSystemDB.db')
    cursor = conn.execute("SELECT * FROM CLASSES WHERE NAME = ?", (str(classname),))
    if cursor.fetchone() == None:
        print("Given Classname not taken")
        return False
    else:
        print("Given Classname already taken")
        return True

## changes attribute for given classid to value
def changeClassName(classid, name):
    if checkClassIdExists(classid) == False:
        return
    conn = sqlite3.connect("GradingSystemDB.db")
    conn.execute("UPDATE CLASSES SET NAME = ? WHERE CLASSID = ?", (str(name), str(classid)))
    conn.commit()
    conn.close()
    print("Changed name to given value for given classid")

## adds entry of given uid to CLASSATTENDANCES for given classid 
def addUserToClass(uid, classid):
    if checkUidExists(uid) == False:
        return
    if checkClassIdExists(classid) == False:
        return
    if checkUserRole(uid) == "Student":
        userassigned = checkUserAssignedClass(uid)
        if userassigned != None:
            removeUserFromClassByUid(uid)
        conn = sqlite3.connect('GradingSystemDB.db')
        conn.execute("INSERT INTO CLASSATTENDANCES (CLASSID, UID) \
                    VALUES (?, ?)", (str(classid), str(uid),))
        conn.commit()
        conn.close()
        print("Added user to relevant class")
    else:
        print("Uid doesn't belong to a student")

## Helper for addUserToClass: Checks whether Student is already assigned to a class
def checkUserAssignedClass(uid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT CLASSID FROM CLASSATTENDANCES WHERE UID = ?", (str(uid),))
    classid = cursor.fetchone()
    conn.close()
    if classid == None:
        print("Student isn't assigned to any class")
        return classid
    else:
        print("Student assigned to class, returning classid")
        return classid[0]

## removes entry of given uid from CLASSATTENDANCES, archives subjects with tests associated with the user
def removeUserFromClassByUid(uid):
    if checkUidExists(uid) == False:
        return
    if checkUserRole(uid) == "Student":
        archiveSubjectsOfRemovedUser(uid)
        conn = sqlite3.connect('GradingSystemDB.db')
        conn.execute("DELETE FROM CLASSATTENDANCES WHERE UID = ?", (str(uid),))
        conn.commit()
        conn.close()
        print("Student removed from relevant class")
    else:
        print("Uid doesn't belong to Student")

## Helper for removeUserFromClassByUid: checks if user is assigned to class, creates archived copy of subject with tests of user
def archiveSubjectsOfRemovedUser(uid):
    subjids = getStudentSubjects(uid)
    print(subjids)
    for subjid in subjids:
        if originalHasTestsAssigned(uid, subjid) == True:
            copysubjid = createCopyOfSubject(subjid, uid)
            redirectTests(uid, subjid, copysubjid)    

## Helper for archiveSubjectsofRemovedUser: retrieves all relevant subjids for given uid
def getStudentSubjects(uid):
    conn = sqlite3.connect("GradingSystemDB.db")
    classid = checkUserAssignedClass(uid)
    cursor = conn.execute("SELECT SUBJID FROM SUBJECTS WHERE CLASSID = ?", (str(classid),))
    results = cursor.fetchall()
    conn.close()
    subjids = []
    for result in results:
        subjid = result[0]
        subjids.append(subjid)
    print("Retrieved relevant subjects for uid")
    return subjids

## Helper of archiveSubjectsofRemovedUser: redirect tests for given uid to given subjid
def redirectTests(uid, subjid, copysubjid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT TESTID FROM TESTS WHERE UID = ? AND SUBJID = ?", (str(uid), str(subjid)))
    results = cursor.fetchall()
    for result in results:
        testid = result[0]
        print("test id = " + str(testid))
        conn.execute("UPDATE TESTS SET SUBJID = ? WHERE TESTID = ?", (str(copysubjid), str(testid)))
    conn.commit()
    conn.close()
    print("Redirected Tests of given uid"+ str(uid) +"to given subjid" + str(subjid))

## Helper of archiveSubjetcsofRemovedUser: checks whether original subject had tests, returns list of testids
def originalHasTestsAssigned(uid, subjid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT TESTID FROM TESTS WHERE SUBJID = ? AND UID = ?", (str(subjid), str(uid)))
    results = cursor.fetchone()
    # resultlist = []
    # for result in results:
    #     resultlist.append(result[0])
    if results != None:
        print("original test assigned: True")
        return True
    else:
        print("original test assigned: False")
        return False

## Helper of archiveSubjectsofRemovedUser: create archived copy of given subjid's entry in SUBJECTS, returns subjid of said subject
def createCopyOfSubject(subjid, uid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT * FROM SUBJECTS WHERE SUBJID = ?", (str(subjid),))
    result = cursor.fetchall()
    result = result[0]
    name = result[1] + createUniqueSubjName(uid)
    classid = result[2] 
    uid = result[3] 
    conn.execute("INSERT INTO SUBJECTS (NAME, CLASSID, UID, ARCHIVED) \
                VALUES (?, ?, ?, ?)", (str(name), str(classid), str(uid), str(1)))
    print("Created copy of given subject")
    cursor = conn.execute("SELECT SUBJID FROM SUBJECTS WHERE NAME = ? AND ARCHIVED = 1", (str(name),))
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    print("Retrieved subjid of created copy")
    return result[0][0]

## helper of createCopyOfSubject: retrieves StudentName of given uid, generates unique subject name
def createUniqueSubjName(uid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT FORENAME, SURNAME FROM USERS WHERE UID = ?", (str(uid),))
    result = cursor.fetchall()
    namestring = result[0][0] + result[0][1] + " class: " + str(checkUserAssignedClass(uid))
    print("Created unique namestring")
    return namestring

## removes given classid from CLASSES
def removeClassFromDB(classid):
    if checkClassIdExists == False:
        return
    removeUserFromClassByClassId(classid)
    disposeOfSubject(None, classid)
    conn = sqlite3.connect("GradingSystemDB.db")
    conn.execute("DELETE FROM CLASSES WHERE CLASSID = ?", (str(classid),))
    conn.commit()
    conn.close()
    print("Removed entry of given classid from CLASSES")

## Helper for removeClassFromDB: removes entries of uids associated with classid from CLASSATTENDANCES
def removeUserFromClassByClassId(classid):
    for uid in getUidByClassId(classid):
        # archiveSubjectsOfRemovedUser(uid)
        conn = sqlite3.connect('GradingSystemDB.db')
        conn.execute("DELETE FROM CLASSATTENDANCES WHERE UID = ?", (str(uid),))
        conn.commit()
        conn.close()
        print("Student removed from relevant class")

## helper of removeUserFromClassByClassId: returns all uids associated with classid
def getUidByClassId(classid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT UID FROM CLASSATTENDANCES WHERE CLASSID = ?", (str(classid)))
    results = cursor.fetchall()
    uidlist = []
    for result in results:
        uid = result[0]
        uidlist.append(uid)
    conn.close()
    print("Retrieved list of subjids associated with classid")
    return uidlist

## returns all subjects as list of dictionaries
def fetchAllSubjects():
    conn = sqlite3.connect('GradingSystemDB.db')
    cursor = conn.execute('''SELECT * FROM SUBJECTS;''')
    responseList = []
    for row in cursor:
        tempdict = {
                "SubjID": row[0],
                "Name": row[1],
                "ClassID": row[2],
                "UID": row[3],
                "Archived": row[4]
        }
        responseList.append(tempdict)
    conn.close()
    print("Fetched ALL from Subjects")
    return responseList

# adds subject with given parameters to SUBJECTS
def addSubjectToDB(name, classid, uid, archived):
    if checkClassIdExists(classid) == False:
        print("Subject could not be created: Class does not exist")
        return
    if checkUidExists(uid) == False:
        print("Subject could not be created: User does not exist")
        return
    if checkSubjectNameTaken(name, classid) == True:
        return
    if checkUserRole(uid) != "Teacher":
        print("Given User is not a Teacher")
        return
    conn = sqlite3.connect("GradingSystemDB.db")
    conn.execute("INSERT INTO SUBJECTS (NAME, CLASSID, UID, ARCHIVED) \
                VALUES (?, ?, ?, ?)", (str(name), str(classid), str(uid), str(archived)))
    conn.commit()
    conn.close()
    print("Added subject to SUBJECTS")

## Helper for addClassToDB: checks if given subject name is already taken
def checkSubjectNameTaken(subjectname, classid):
    conn = sqlite3.connect('GradingSystemDB.db')
    cursor = conn.execute("SELECT * FROM SUBJECTS WHERE NAME = ? AND CLASSID = ?", (str(subjectname), str(classid)))
    if cursor.fetchone() == None:
        print("Given Subjectname not taken for given class")
        return False
    else:
        print("Given Subjectname already taken for given class")
        return True

## changes attribute to value for given subjid
def changeSubjectAttribute(subjid, attribute, value):
    if checkSubjIdExists(subjid) == False:
        return
    if checkSubjectArchived(subjid) == True:
        print("No further changes can be made to archived subject")
        return
    conn = sqlite3.connect("GradingSystemDB.db")
    conn.execute("UPDATE SUBJECTS SET "+str(attribute)+"= ? WHERE SUBJID = ?", (str(value), str(subjid),))
    conn.commit()
    conn.close()
    print("Changed attribute to value for given subjid")

## Helper of changeSubjectAttribute: Checks if given subjid exists in table SUBJECTS
def checkSubjIdExists(subjid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT * FROM SUBJECTS WHERE SUBJID = ?", (str(subjid),))
    if cursor.fetchone() == None:
        print("No subject with given subjid found")
        conn.close()
        return False
    else:
        print("Subject found")
        conn.close()
        return True

## Helper of changeSubjectAttribute: Checks if given subjid has archived flag enabled
def checkSubjectArchived(subjid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT ARCHIVED FROM SUBJECTS WHERE SUBJID = ?", (str(subjid),))
    result = cursor.fetchone()[0]
    conn.close()
    if result == 0:
        print("Subject not archived")
        return False
    else:
        print("Subject archived")
        return True

## either removes or archives subject, or subjects if classid is given
def disposeOfSubject(subjid = None, classid = None):
    if subjid != None and classid == None:
        if checkSubjIdExists(subjid) == False:
            return
        removeOrArchiveSubjectFromDB(subjid)
    elif subjid == None and classid != None:
        subjids = getSubjIdByClassId(classid)
        for subjid in subjids:
            if checkSubjIdExists(subjid) == False:
                continue
            removeOrArchiveSubjectFromDB(subjid)
    else:
        print("Incorrect input, XOR required")


## Helper of disposeOfSubject: returns list of subjids for given classids
def getSubjIdByClassId(classid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT SUBJID FROM SUBJECTS WHERE CLASSID = ?", (str(classid)))
    results = cursor.fetchall()
    subjidlist = []
    for result in results:
        subjid = result[0]
        subjidlist.append(subjid)
    conn.close()
    print("Retrieved list of subjids associated with classid")
    return subjidlist

## Helper for disposeOfSubject: removes entry of given subjid from SUBJECTS
def removeOrArchiveSubjectFromDB(subjid):
    if checkTestsAssigned(subjid) == False:
        conn = sqlite3.connect("GradingSystemDB.db")
        conn.execute("DELETE FROM SUBJECTS WHERE SUBJID = ?", (str(subjid),))
        conn.commit()
        conn.close()
        print("Removed entry of given subjid from SUBJECTS")
    if checkTestsAssigned(subjid) == True:
        conn = sqlite3.connect("GradingSystemDB.db")
        conn.execute("UPDATE SUBJECTS SET ARCHIVED = 1 WHERE SUBJID = ?", (str(subjid),))
        conn.commit()
        conn.close()
        print("Subject archived")

# Helper for removeOrArchiveSubjectFromDB: checks if tests are assigned to given subject
def checkTestsAssigned(subjid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT * FROM TESTS WHERE SUBJID = ?", (str(subjid),))
    if cursor.fetchone() == None:
        print("Tests Assigned: False")
        conn.close()
        return False
    else:
        print("Tests Assigned: True")
        conn.close()
        return True

## returns all subjects as list of dictionaries
def fetchAllTests():
    conn = sqlite3.connect('GradingSystemDB.db')
    cursor = conn.execute('''SELECT * FROM TESTS;''')
    responseList = []
    for row in cursor:
        tempdict = {
                "TestID": row[0],
                "Name": row[1],
                "Date": row[2],
                "SubjId": row[3],
                "Uid": row[4],
                "Grade": row[5]
        }
        responseList.append(tempdict)
    conn.close()
    print("Fetched ALL from Subjects")
    return responseList

## returns list of dictionaries containing user info as well as their average grades
def fetchAllPupilsAvgGrades():
    conn = sqlite3.connect('GradingSystemDB.db')
    cursor = conn.execute("SELECT * FROM USERS WHERE ROLE = ?", ("Student",))
    results = cursor.fetchall()
    resultlist = []
    print(results)
    for row in results:
        tempdict = {
                "UID": row[0],
                "Forename": row[1],
                "Surname": row[2],
                "Average Grades": fetchAvgGradesAllSubjects(row[0])
        }
        resultlist.append(tempdict)
    conn.close()
    print("Fetched ALL from Subjects")
    return resultlist

# Helper of fetchAllPupilsAvgGrades: fetches all grades associated with given uid, returns average
def fetchAvgGradesAllSubjects(uid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT GRADE FROM TESTS WHERE UID = ?", (str(uid),))
    results = cursor.fetchall()
    conn.close()
    gradesacc = 0
    divisor = 0
    for row in results:
        gradesacc += row[0]
        divisor += 1
    try:
        print("Average grade calculated")
        return (gradesacc / divisor)
    except:
        print("Student has no grades")
        return 0

# Adds Test with given values to TESTS
def addTestToDB(name, date, subjid, uid, grade):
    conn = sqlite3.connect("GradingSystemDB.db")
    conn.execute("INSERT INTO TESTS (NAME, DATE, SUBJID, UID, GRADE) \
                VALUES (?, ?, ?, ?, ?)", (str(name), str(date), str(subjid), str(uid), str(grade)))
    conn.commit()
    conn.close()
    print("Added test to TESTS")

## changes attribute to value for given testid
def changeTestAttributeByTestId(testid, attribute, value):
    if checkTestIdExists(testid) == False:
        return
    conn = sqlite3.connect("GradingSystemDB.db")
    conn.execute("UPDATE TESTS SET "+str(attribute)+"= ? WHERE TESTID = ?", (str(value), str(testid),))
    conn.commit()
    conn.close()
    print("Changed attribute to value for given testid")

## returns users and their grades for given test name
def fetchAllPupilsAndGradesForTest(name):
    conn = sqlite3.connect('GradingSystemDB.db')
    cursor = conn.execute("SELECT UID, TESTID, GRADE FROM TESTS WHERE NAME = ?", (str(name),))
    results = cursor.fetchall()
    resultlist = []
    for row in results:
        tempdict = {
                "UID": row[0],
                "TESTID": row[1],
                "Forename": getUserName(row[0])[0],
                "Surname": getUserName(row[0])[1],
                "Grade:": row[2]
        }
        resultlist.append(tempdict)
    conn.close()
    print("Fetched Users and grades for given test")
    return resultlist

## Helper of fetchAllPupilsAndGradesForTest: returns forename, surname for given uid
def getUserName(uid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT FORENAME, SURNAME FROM USERS WHERE UID = ?", (str(uid),))
    results = cursor.fetchall()
    return [results[0][0], results[0][1]]

## changes grade for given uid and testid in TESTS
def editGradeOfPupilInTest(uid, testid, grade):
    if checkUidExists(uid) == False:
        return
    if checkTestIdExists(testid) == False:
        return
    conn = sqlite3.connect('GradingSystemDB.db')
    conn.execute("UPDATE TESTS SET GRADE = ? WHERE UID = ? AND TESTID = ?", (str(grade), str(uid), str(testid)))
    conn.commit()
    conn.close()
    print("Changed grade of given student for given test")

## removes all relevant entries of given test from TESTS
def removeTestFromDB(name):
    conn = sqlite3.connect('GradingSystemDB.db')
    conn.execute("DELETE FROM TESTS WHERE NAME = ?", (str(name),))
    conn.commit()
    conn.close()
    print("Removed all relevant entries of given test from TESTS")

## Retrieves Average grades for all subjects of given uid
def fetchAllSubjectsAndAvgGradesOneStudent(uid):
    if checkUidExists(uid) == False:
        return
    if checkUserRole(uid) != "Student":
        print("Given user is not a Student, returning")
        return
    subjids = getStudentSubjects(uid)
    resultlist = []
    for subjid in subjids:
        tempdict = {
            "SubjID": subjid,
            "Subject": getSubjectName(subjid),
            "Average Grade": fetchAvgGradesOneSubjectOneStudent(subjid, uid)
        }
        resultlist.append(tempdict)
    print("Retrieved Average grades for all subjects of given uid")
    return resultlist
 
## Helper of fetchAllSubjectsAndAVgGradesOneStudent: retrieves subjectname for given subjid from SUBJECTS
def getSubjectName(subjid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT NAME FROM SUBJECTS WHERE SUBJID = ?", (str(subjid),))
    result = cursor.fetchall()[0][0]
    conn.close()
    print("Fetched Subject name for given subjid")
    return result

## Helper for fetchAllSubjectsAndAvgGradesOneStudent: calculates average grade for given subject for given student
def fetchAvgGradesOneSubjectOneStudent(subjid, uid):
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT GRADE FROM TESTS WHERE SUBJID = ? AND UID = ?", (str(subjid), str(uid)))
    results = cursor.fetchall()
    gradesacc = 0
    divisor = 0 
    for row in results:
        gradesacc += row[0]
        divisor += 1
    try:
        print("Average grade calculated")
        return(gradesacc / divisor)
    except:
        print("Student has no grades")
        return 0

## Retrieves all tests and grades of given subjid for given uid
def fetchAllTestsAndGradesOneSubjectOneStudent(subjid, uid):
    if checkUidExists(uid) == False:
        return
    if checkSubjIdExists(subjid) == False:
        return
    if checkUserRole(uid) != "Student":
        print("Given user not a student, returning")
        return
    conn = sqlite3.connect("GradingSystemDB.db")
    cursor = conn.execute("SELECT TESTID, NAME, GRADE FROM TESTS WHERE SUBJID = ? AND UID = ?", (str(subjid), str(uid)))
    results = cursor.fetchall()
    conn.close()
    resultlist = []
    for row in results:
        tempdict = {
            "TestID": row[0],
            "Test": row[1],
            "Grade": row[2]
        }
        resultlist.append(tempdict)
    print("Retrieved all tests and grades of given subject for given student")
    return resultlist

# removeUserFromDB(1)
# addUserToDB("Lucia", "Wuckert", "Student", "lumawu", "password")
# addUserToDB("Kenneth", "Otto", "Admin", "kotto", "password")
# addUserToClass(14, 1)
# addTestToDB("ubertest 1", "2020-01-01", 1, 14, 2.5)
# addTestToDB("ubertest 2", "2020-01-02", 1, 14, 5.0)
# addTestToDB("ubertest 3", "2020-01-03", 2, 14, 3.5)
# addTestToDB("ubertest 4", "2020-01-04", 2, 14, 1)


