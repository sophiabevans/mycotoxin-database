#!/usr/bin/python3
import pymysql

# connecting Python to MySQL
connection = pymysql.connect(
    host="bioed.bu.edu",
    db="sbevans",
    user="sbevans",
    passwd="3d3np33d3n",
    port=4253,
    local_infile=True)

#connection.begin()
cursor = connection.cursor()

queries = ['DROP TABLE IF EXISTS Removal, Curation_Contribution, Organism, Mycotoxin, Literature;',
'''CREATE TABLE Literature (
LID INTEGER NOT NULL AUTO_INCREMENT,
Context VARCHAR(100),
Assay VARCHAR(100),
Source VARCHAR(500) character set utf8,
Link VARCHAR(100),
PRIMARY KEY(LID)
);
''',
'''
CREATE TABLE Mycotoxin (
MID INTEGER NOT NULL AUTO_INCREMENT,
Name VARCHAR(50),
Removal_mech VARCHAR(30),
Enzymatic_or_not VARCHAR(20),
Location VARCHAR(100),
PRIMARY KEY(MID)
);
''',
'''CREATE TABLE Organism (
OID INTEGER NOT NULL AUTO_INCREMENT,
Domain VARCHAR(40),
Name VARCHAR(100),
Pathogenicity VARCHAR(50),
Respiration VARCHAR(30),
Environment VARCHAR(100),
PRIMARY KEY(OID)
);
''',
'''CREATE TABLE Curation_Contribution (
CID INTEGER NOT NULL AUTO_INCREMENT,
Con_name VARCHAR(30),
Con_date DATE,
Cur_name VARCHAR(30),
Cur_date DATE,
Cur_notes VARCHAR(500) character set utf8,
PRIMARY KEY(CID)
);''',
'''CREATE TABLE Removal (
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
''']

for q in queries:
	try:
	    cursor.execute(q)
	except pymysql.Error as e:
	    print(e)

allN = []
orgN = []
mycN = []
curconN = []
litN = []

with open("../data/allN.txt", "r") as f:
    allN = list(f.readline().strip().split(" "))

with open("../data/orgN.txt", "r") as f:
    orgN = list(f.readline().strip().split(" "))

with open("../data/mycN.txt", "r") as f:
    mycN = list(f.readline().strip().split(" "))

with open("../data/curconN.txt", "r") as f:
    curconN = list(f.readline().strip().split(" "))

with open("../data/litN.txt", "r") as f:
    litN = list(f.readline().strip().split(" "))

org_dict = {}
myc_dict = {}
lit_dict = {}
cur_dict = {}

with open("../data/mycotoxinN.tsv", "r") as f:
    line = f.readline()  # skip header
    line = f.readline()
    while line:
        fields = line.strip().split("\t")
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
        ON = fields[20]
        MN = fields[21]
        LN = fields[22]
        CN = fields [23]

        print(f"ON: {ON}, MN: {MN}, LN: {LN}, CN: {CN}")

        # print(N, Domain, Organism, Pathogenicity, Respiration, Environment,
        # Mycotoxin, Removal_mech, Enzymatic, Location, Char_con, Char_assay,
        # Source, Link, Add_info, Contributor, Cont_date, Curator, Cur_date, Cur_notes)

        if N in litN:
            try:
                cursor.execute(f'''
                insert into Literature (Context, Assay, Source, Link)
                values ("{Char_con}", "{Char_assay}", "{Source}", "{Link}");''')
                cursor.execute("select LAST_INSERT_ID();")
                lid = cursor.fetchall()[0][0]
                lit_dict[N] = lid
            except pymysql.Error as e:
                print(e)
        if N in mycN:
            try:
                cursor.execute(f'''
                insert into Mycotoxin (Name, Removal_mech, Enzymatic_or_not, Location)
                values ("{Mycotoxin}", "{Removal_mech}", "{Enzymatic}", "{Location}");''')
                cursor.execute("select LAST_INSERT_ID();")
                mid = cursor.fetchall()[0][0]
                myc_dict[N] = mid
            except pymysql.Error as e:
                print(e)
        if N in orgN:
            try:
                cursor.execute(f'''
                insert into Organism (Domain, Name, Pathogenicity, Respiration, Environment)
                values ("{Domain}", "{Organism}", "{Pathogenicity}", "{Respiration}", "{Environment}");''')
                cursor.execute("select LAST_INSERT_ID();")
                oid = cursor.fetchall()[0][0]
                org_dict[N] = oid
            except pymysql.Error as e:
                print(e)
        if N in curconN:
            try:
                if Cont_date == "NULL" and Cur_date == "NULL":
                    cursor.execute(f'''
                    insert into Curation_Contribution (Con_name, Con_date, Cur_name, Cur_date, Cur_notes)
                    values ("{Contributor}", NULL, "{Curator}", NULL, "{Cur_notes}");''')
                else:
                    cursor.execute(f'''
                    insert into Curation_Contribution (Con_name, Con_date, Cur_name, Cur_date, Cur_notes)
                    values ("{Contributor}", "{Cont_date}", "{Curator}", "{Cur_date}", "{Cur_notes}");''')
                cursor.execute("select LAST_INSERT_ID();")
                cid = cursor.fetchall()[0][0]
                cur_dict[N] = cid
            except pymysql.Error as e:
                print(e)
        print(org_dict, "\n", myc_dict, "\n",lit_dict, "\n",cur_dict, "\n")
        try:
            cursor.execute(f'''
            insert into Removal (OID, MID, LID, CID)
            values ({org_dict[ON]}, {myc_dict[MN]}, {lit_dict[LN]}, {cur_dict[CN]});''')
        except pymysql.Error as e:
            print(e)
       	line = f.readline()

#commit changes
connection.commit()

#close cursor and connection
cursor.close()
connection.close()
