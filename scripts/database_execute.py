#!/usr/bin/python3
import pymysql
import sys

# to print program usage when called with no parameters
# note that sys.arv[0] is the program name
if len(sys.argv) != 3:  # number of parameters +1 for program name
   print("Usage is: %s username password" % sys.argv[0])
   sys.exit(0)

usr = sys.argv[1]
pswd = sys.argv[2]

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
           """CREATE TABLE Literature (
LID INTEGER NOT NULL AUTO_INCREMENT,
Context VARCHAR(100),
Assay VARCHAR(100),
Source VARCHAR(100),
Link VARCHAR(100),
PRIMARY KEY(LID)
);""",
           """CREATE TABLE Organism (
OID INTEGER NOT NULL AUTO_INCREMENT,
Domain VARCHAR(40),
Name VARCHAR(100),
Pathogenicity VARCHAR(50),
Respiration VARCHAR(30),
Environment VARCHAR(100),
PRIMARY KEY(OID)
);""",
           """CREATE TABLE Mycotoxin (
MID INTEGER NOT NULL AUTO_INCREMENT,
Name VARCHAR(100),
Removal_mech VARCHAR(50),
Enzymatic_or_not VARCHAR(20),
Location VARCHAR(50),
PRIMARY KEY(MID)
);""",
           """CREATE TABLE Curation_Contribution (
CID INTEGER NOT NULL AUTO_INCREMENT,
Con_name VARCHAR(30),
Con_date DATE,
Cur_name VARCHAR(30),
Cur_date DATE,
Cur_notes VARCHAR(200),
PRIMARY KEY(CID)
);""",
           """CREATE TABLE Removal (
OID INT NOT NULL,
MID INT NOT NULL,
LID INT NOT NULL,
PRIMARY KEY(OID,MID),
FOREIGN KEY(OID) REFERENCES Organism(OID),
FOREIGN KEY(MID) REFERENCES Mycotoxin(MID),
FOREIGN KEY(LID) REFERENCES Literature(LID)
);""",
           'load data local infile "../data/curation.tsv" into table Curation_Contribution ignore 1 lines (Con_name, Con_date, Cur_name, Cur_date, Cur_notes);',
           'load data local infile "../data/mycotoxin.tsv" into table Mycotoxin ignore 1 lines (Name, Removal_mech, Enzymatic_or_not, Location);',
           'load data local infile "../data/organism.tsv" into table Organism ignore 1 lines (Name, Domain, Pathogenicity, Respiration, Environment);',
           'load data local infile "../data/literature.tsv" into table Literature ignore 1 lines (Context, Assay, Source, Link);']

for q in queries:
	try:
	    cursor.execute(q)
	except pymysql.Error as e:
	    print(e)

cursor.execute("select OID from Organism;")
oids = cursor.fetchall()
cursor.execute("select Name from Organism;")
onames = cursor.fetchall()
cursor.execute("select MID from Mycotoxin;")
mids = cursor.fetchall()
cursor.execute("select Name from Mycotoxin;")
mnames = cursor.fetchall()
cursor.execute("select LID from Literature;")
lids = cursor.fetchall()
cursor.execute("select Link from Literature;")
lnames = cursor.fetchall()

organism_dict = {}
mycotoxin_dict = {}
lit_dict = {}

for i, j in zip(onames, oids):
    if i[0] in organism_dict:
        organism_dict[i[0]].append(j[0])
    else:
        organism_dict[i[0]] = [j[0]]

for i, j in zip(mnames, mids):
    if i[0] in mycotoxin_dict:
        mycotoxin_dict[i[0]].append(j[0])
    else:
        mycotoxin_dict[i[0]] = [j[0]]

for i, j in zip(lnames, lids):
    if i[0] in lit_dict:
        lit_dict[i[0]].append(j[0])
    else:
        lit_dict[i[0]] = [j[0]]

print(organism_dict)
print(mycotoxin_dict)
print(lit_dict)

with open("../data/mycotoxin_removal.tsv", "r") as f:
    line = f.readline()  # skip header
    line = f.readline()
    while line:
        fields = line.strip().split("\t")
        lid = lit_dict[fields[1]]
        oid = organism_dict[fields[2]]
        mid = mycotoxin_dict[fields[7]]
        #there can be multiple ids for the same key, need multiple rows
        #these are all lists, usually of length 1
        for i in oid:
            for j in mid:
                for k in lid:
                    cursor.execute(f"""insert into Removal (OID, MID, LID)
                    values ({i}, {j}, {k})""")
        line = f.readline()

#commit changes
connection.commit()

#close cursor and connection
cursor.close()
connection.close()
