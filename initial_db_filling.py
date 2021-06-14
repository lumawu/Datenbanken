# This file serves the filling of the db with test data
# It should therefor only be executed after database has been set up

import sqlite3

conn = sqlite3.connect("GradingSystemDB.db")
print("Connected to database")

# create Users
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Lucia", "Wuckert", "Admin", "lumawu", "c4ca4238a0b923820dcc509a6f75849b"))
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Stu1", "dent1", "Student", "student1", "c81e728d9d4c2f636f067f89cc14862c"))
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Stu2", "dent2", "Student", "student2", "eccbc87e4b5ce2fe28308fd9f2a7baf3"))
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Stu3", "dent3", "Student", "student3", "a87ff679a2f3e71d9181a67b7542122c"))
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Stu4", "dent4", "Student", "student4", "e4da3b7fbbce2345d7772b0674a318d5"))
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Stu5", "dent5", "Student", "student5", "1679091c5a880faf6fb5e6087eb1b2dc"))
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Stu6", "dent6", "Student", "student6", "8f14e45fceea167a5a36dedd4bea2543"))
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Stu7", "dent7", "Student", "student7", "c9f0f895fb98ab9159f51fd0297e236d"))
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Stu8", "dent8", "Student", "student8", "45c48cce2e2d7fbdea1afc51c7c6ad26"))
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Stu9", "dent9", "Student", "student9", "d3d9446802a44259755d38e6d163e820"))
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Tea1", "cher1", "Teacher", "teacher1", "6512bd43d9caa6e02c990b0a82652dca"))
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Tea2", "cher2", "Teacher", "teacher2", "c20ad4d76fe97759aa27a0c99bff6710"))
conn.execute("INSERT INTO USERS (FORENAME, SURNAME, ROLE, USERNAME, PWHASH) \
            VALUES (?, ?, ?, ?, ?)", ("Tea3", "cher3", "Teacher", "teacher3", "c51ce410c124a10e0db5e4b97fc2af39"))
print("Created Testbatch of users")

# create classes
conn.execute("INSERT INTO CLASSES (NAME)\
            VALUES (?)", ("Regenbogenklasse A",))
conn.execute("INSERT INTO CLASSES (NAME)\
            VALUES (?)", ("Regenbogenklasse B",))
print("Created Testbatch of classes")

# create subjects
conn.execute("INSERT INTO SUBJECTS (NAME, CLASSID, UID, ARCHIVED) \
            VALUES (?, ?, ?, ?)", ("Biology", "1", "11", "0"))
conn.execute("INSERT INTO SUBJECTS (NAME, CLASSID, UID, ARCHIVED) \
            VALUES (?, ?, ?, ?)", ("German", "1", "12", "0"))
conn.execute("INSERT INTO SUBJECTS (NAME, CLASSID, UID, ARCHIVED) \
            VALUES (?, ?, ?, ?)", ("English", "1", "11", "0"))
conn.execute("INSERT INTO SUBJECTS (NAME, CLASSID, UID, ARCHIVED) \
            VALUES (?, ?, ?, ?)", ("PE", "2", "12", "0"))
conn.execute("INSERT INTO SUBJECTS (NAME, CLASSID, UID, ARCHIVED) \
            VALUES (?, ?, ?, ?)", ("Ethics", "2", "11", "0"))
conn.execute("INSERT INTO SUBJECTS (NAME, CLASSID, UID, ARCHIVED) \
            VALUES (?, ?, ?, ?)", ("Computer Science", "2", "12", "0"))
print("Created Testbatch of Subjects")

# set classattendances
conn.execute("INSERT INTO CLASSATTENDANCES(CLASSID, UID) \
            VALUES (?, ?)", ("1", "2"))
conn.execute("INSERT INTO CLASSATTENDANCES(CLASSID, UID) \
            VALUES (?, ?)", ("1", "3"))
conn.execute("INSERT INTO CLASSATTENDANCES(CLASSID, UID) \
            VALUES (?, ?)", ("1", "4"))
conn.execute("INSERT INTO CLASSATTENDANCES(CLASSID, UID) \
            VALUES (?, ?)", ("1", "5"))
conn.execute("INSERT INTO CLASSATTENDANCES(CLASSID, UID) \
            VALUES (?, ?)", ("2", "6"))
conn.execute("INSERT INTO CLASSATTENDANCES(CLASSID, UID) \
            VALUES (?, ?)", ("2", "7"))
conn.execute("INSERT INTO CLASSATTENDANCES(CLASSID, UID) \
            VALUES (?, ?)", ("2", "8"))
conn.execute("INSERT INTO CLASSATTENDANCES(CLASSID, UID) \
            VALUES (?, ?)", ("2", "9"))
print("Created Testbatch of Classattendances")

# create tests
conn.execute("INSERT INTO TESTS (NAME, DATE, SUBJID, UID, GRADE)\
            VALUES (?, ?, ?, ?, ?)", ("Biology Test 1", "1996-08-08", "1", "2", "1"))
conn.execute("INSERT INTO TESTS (NAME, DATE, SUBJID, UID, GRADE)\
            VALUES (?, ?, ?, ?, ?)", ("Biology Test 2", "1996-08-09", "1", "3", "2.3"))
conn.execute("INSERT INTO TESTS (NAME, DATE, SUBJID, UID, GRADE)\
            VALUES (?, ?, ?, ?, ?)", ("Biology Test 3", "1996-08-10", "1", "4", "3.7"))
conn.execute("INSERT INTO TESTS (NAME, DATE, SUBJID, UID, GRADE)\
            VALUES (?, ?, ?, ?, ?)", ("German Test 1", "1996-08-08", "2", "5", "1"))
conn.execute("INSERT INTO TESTS (NAME, DATE, SUBJID, UID, GRADE)\
            VALUES (?, ?, ?, ?, ?)", ("PE Test 1", "1996-08-08", "4", "6", "1"))
conn.execute("INSERT INTO TESTS (NAME, DATE, SUBJID, UID, GRADE)\
            VALUES (?, ?, ?, ?, ?)", ("PE Test 2", "1996-08-09", "4", "7", "2.3"))
conn.execute("INSERT INTO TESTS (NAME, DATE, SUBJID, UID, GRADE)\
            VALUES (?, ?, ?, ?, ?)", ("PE Test 1", "1996-08-10", "4", "8", "3.7"))
conn.execute("INSERT INTO TESTS (NAME, DATE, SUBJID, UID, GRADE)\
            VALUES (?, ?, ?, ?, ?)", ("Ethics Test 1", "1996-08-08", "5", "9", "1"))
print("Created Testbatch of Tests")
    
conn.commit()
conn.close()