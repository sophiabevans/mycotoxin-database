#!/usr/bin/python3
import pymysql

# connecting Python to MySQL
connection = pymysql.connect(
    host="bioed.bu.edu",
    #db="Group_M",
    #user="Group_M",
    #passwd="Group_M",
    db ="sbevans",
    user="sbevans",
    passwd="3d3np33d3n",
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
"""CREATE TABLE Organism (
OID INTEGER NOT NULL AUTO_INCREMENT,
Domain VARCHAR(40),
Name VARCHAR(100),
Pathogenicity VARCHAR(50),
Respiration VARCHAR(30),
Environment VARCHAR(100),
PRIMARY KEY(OID)
);
""",
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
CID INT NOT NULL,
PRIMARY KEY(OID,MID,LID),
FOREIGN KEY(OID) REFERENCES Organism(OID),
FOREIGN KEY(MID) REFERENCES Mycotoxin(MID),
FOREIGN KEY(LID) REFERENCES Literature(LID),
FOREIGN KEY(CID) REFERENCES Curation_Contribution(CID)
);
"""]
#'load data local infile "../data/curation.tsv" into table Curation_Contribution ignore 1 lines (Con_name, Con_date, Cur_name, Cur_date, Cur_notes);',
#'load data local infile "../data/mycotoxin.tsv" into table Mycotoxin ignore 1 lines (Name, Removal_mech, Enzymatic_or_not, Location);',
#'load data local infile "../data/organism.tsv" into table Organism ignore 1 lines (Domain, Name, Pathogenicity, Respiration, Environment);',
#'load data local infile "../data/literature.tsv" into table Literature ignore 1 lines (Context, Assay, Source, Link);'

for q in queries:
	try:
	    cursor.execute(q)
	except pymysql.Error as e:
	    print(e)

# cursor.execute("select OID from Organism;")
# oids = cursor.fetchall()
# cursor.execute("select Name from Organism;")
# onames = cursor.fetchall()
# cursor.execute("select MID from Mycotoxin;")
# mids = cursor.fetchall()
# cursor.execute("select Name from Mycotoxin;")
# mnames = cursor.fetchall()
# cursor.execute("select LID from Literature;")
# lids = cursor.fetchall()
# cursor.execute("select Link from Literature;")
# lnames = cursor.fetchall()
# cursor.execute("select CID from Curation_Contribution;")
# cids = cursor.fetchall()
# cursor.execute("select Con_name from Curation_Contribution;")
# cnames = cursor.fetchall()

# organism_dict = {}
# mycotoxin_dict = {}
# lit_dict = {}
#
# for i, j in zip(onames, oids):
#     if i[0] in organism_dict:
#         organism_dict[i[0]].append(j[0])
#     else:
#         organism_dict[i[0]] = [j[0]]
#
# for i, j in zip(mnames, mids):
#     if i[0] in mycotoxin_dict:
#         mycotoxin_dict[i[0]].append(j[0])
#     else:
#         mycotoxin_dict[i[0]] = [j[0]]
#
# for i, j in zip(lnames, lids):
#     if i[0] in lit_dict:
#         lit_dict[i[0]].append(j[0])
#     else:
#         lit_dict[i[0]] = [j[0]]

with open("../data/orgN.txt", "r") as f:
    orgN = list(f.readline().strip().split(" "))

with open("../data/mycN.txt", "r") as f:
    mycN = list(f.readline().strip().split(" "))

with open("../data/curconN.txt", "r") as f:
    curconN = list(f.readline().strip().split(" "))

with open("../data/litN.txt", "r") as f:
    litN = list(f.readline().strip().split(" "))

with open("../data/mycotoxinN.csv", "r") as f:
    line = f.readline()  # skip header
    line = f.readline()
    while line:
        fields = line.strip().split(",")
        N = fields[0]
        Domain = fields[1]
        Organism = fields[2]
        Pathogenicity = fields[3]
        Respiration = fields[4]
        Environment = fields[5]
        Mycotoxin = fields[6]
        Removal_mech = fields[7]
        Enzymatic = fields[8]
        Location = fields[9]
        Char_con = fields[10]
        Char_assay = fields[11]
        Source = fields[12]
        Link = fields[13]
        Add_info = fields[14]
        Contributor = fields[15]
        Cont_date = fields[16]
        Curator = fields[17]
        Cur_date = fields[18]
        Cur_notes = fields[19]

        if N in litN:
            try:
                cursor.execute(f"""
                insert into Literature (Context, Assay, Source, Link)
                values ({Char_con}, {Char_assay}, {Source}, {Link})""")
                cursor.execute("set @lid = LAST_INSERT_ID();")
            except pymysql.Error as e:
                print(e)
        if N in mycN:
            try:
                cursor.execute(f"""
                insert into Mycotoxin (Name, Removal_mech, Enzymatic_or_not, Location)
                values ({Mycotoxin}, {Removal_mech}, {Enzymatic}, {Location})""")
                cursor.execute("set @mid = LAST_INSERT_ID();")
            except pymysql.Error as e:
                print(e)
        if N in orgN:
            try:
                cursor.execute(f"""
                insert into Organism (Domain, Name, Pathogenicity, Respiration, Environment)
                values ({Domain}, {Organism}, {Pathogenicity}, {Respiration}, {Environment})""")
                cursor.execute("set @oid = LAST_INSERT_ID();")
            except pymysql.Error as e:
                print(e)
        if N in curconN:
            try:
                cursor.execute(f"""
                insert into Curation_Contribution (Con_name, Con_date, Cur_name, Cur_date, Cur_notes)
                values ({Contributor}, {Cont_date}, {Curator}, {Cur_date}, {Cur_notes})""")
                cursor.execute("set @cid = LAST_INSERT_ID();")
            except pymysql.Error as e:
                print(e)
        try:
            cursor.execute(f"""
            insert into Removal (OID, MID, LID, CID)
            values (@oid @mid @lid @cid)""")
        except pymysql.Error as e:
            print(e)
       	line = f.readline()

#commit changes
connection.commit()

#close cursor and connection
cursor.close()
connection.close()
