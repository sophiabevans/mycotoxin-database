#!/usr/bin/python3
import pymysql
import sys

# to print program usage when called with no parameters
# note that sys.arv[0] is the program name
if len(sys.argv) != 3: #number of parameters +1 for program name
   print ("Usage is: %s username password" % sys.argv[0])
   sys.exit(0)

usr = sys.argv[1]
pswd  = sys.argv[2]

# connecting Python to MySQL
connection = pymysql.connect(
host="bioed.bu.edu",
db="Group_M",
user=usr,
passwd=pswd,
port=4253,
local_infile=True)

#connection.begin()
cursor = connection.cursor()

queries = ['DROP TABLE IF EXISTS Removal, Curation_Contribution, Organism, Mycotoxin, Literature;',
"""
CREATE TABLE Literature (
LID INTEGER NOT NULL AUTO_INCREMENT,
Context VARCHAR(100),
Assay VARCHAR(100),
Source VARCHAR(100),
Link VARCHAR(100),
PRIMARY KEY(LID)
);
""",
"""
CREATE TABLE Mycotoxin (
MID INTEGER NOT NULL AUTO_INCREMENT,
Name VARCHAR(50),
Removal_mech VARCHAR(30),
Enzymatic_or_not VARCHAR(20),
Location VARCHAR(100),
PRIMARY KEY(MID)
);
""",
"""
CREATE TABLE Organism (
OID INTEGER NOT NULL AUTO_INCREMENT,
Domain VARCHAR(20),
Name VARCHAR(30),
Pathogenicity VARCHAR(30),
Respiration VARCHAR(30),
Environment VARCHAR(30),
PRIMARY KEY(OID)
);
""",
"""
CREATE TABLE Curation_Contribution (
CID INTEGER NOT NULL AUTO_INCREMENT,
Con_name VARCHAR(30),
Con_date DATE,
Cur_name VARCHAR(30),
Cur_date DATE,
Cur_notes VARCHAR(200),
PRIMARY KEY(CID)
);
""",
"""
CREATE TABLE Removal (
OID INT NOT NULL,
MID INT NOT NULL,
LID INT NOT NULL,
PRIMARY KEY(OID,MID),
FOREIGN KEY(OID) REFERENCES Organism(OID),
FOREIGN KEY(MID) REFERENCES Mycotoxin(MID),
FOREIGN KEY(LID) REFERENCES Literature(LID)
);
""",
'load data local infile "../data/curation.tsv" into table Curation_Contribution ignore 1 lines (Con_name, Con_date, Cur_name, Cur_date, Cur_notes);',
'load data local infile "../data/mycotoxin.tsv" into table Mycotoxin ignore 1 lines (Name, Removal_mech, Enzymatic_or_not, Location);',
'load data local infile "../data/organism.tsv" into table Organism ignore 1 lines (Domain, Name, Pathogenicity, Respiration, Environment);',
'load data local infile "../data/literature.tsv" into table Literature ignore 1 lines (Context, Assay, Source, Link);']

for q in queries:
	try:
	    cursor.execute(q)
	except pymysql.Error as e:
	    print(e)

#commit changes
connection.commit()

#close cursor and connection
cursor.close()
connection.close()
