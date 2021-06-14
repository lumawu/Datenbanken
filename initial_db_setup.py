# This file serves the initial setup of the database with relevant tables
# It should therefor only be executed once on startup

import sqlite3

conn = sqlite3.connect("GradingSystemDB.db")
print("Initialized Database")

# create table USERS
conn.execute('''CREATE TABLE USERS
            (UID INTEGER PRIMARY KEY,
            FORENAME    TEXT    NOT NULL,
            SURNAME     TEXT    NOT NULL,
            ROLE        TEXT    NOT NULL,
            USERNAME    TEXT    NOT NULL,
            PWHASH      TEXT    NOT NULL);''')
print("Table USERS created successfully")

# create table CLASSES
conn.execute('''CREATE TABLE CLASSES
            (CLASSID INTEGER PRIMARY KEY,
            NAME    TEXT    NOT NULL)''')
print("Table CLASSES created successfully")

# create table CLASSATTENDANCES
conn.execute('''CREATE TABLE CLASSATTENDANCES
            (CLASSID INTEGER NOT NULL,
            UID     INTEGER     NOT NULL);''')
print("Table CLASSATTENDANCES created successfully")

# create table SUBJECTS
conn.execute('''CREATE TABLE SUBJECTS
            (SUBJID INTEGER PRIMARY KEY,
            NAME    TEXT    NOT NULL,
            CLASSID INTEGER     NOT NULL,
            UID     INTEGER     NOT NULL,
            ARCHIVED    BIT NOT NULL);''')
print("Table SUBJECTS created successfully")

# create table TESTS
conn.execute('''CREATE TABLE TESTS
            (TESTID INTEGER PRIMARY KEY,
            NAME    TEXT    NOT NULL,
            DATE    DATE    NOT NULL,
            SUBJID  INTEGER     NOT NULL,
            UID     INTEGER     NOT NULL,
            GRADE   INTEGER     NOT NULL);''')
print("Table TESTS created successfully")