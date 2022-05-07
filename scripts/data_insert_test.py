#!/usr/bin/env python3
import pymysql
import cgi
import cgitb
import json

cgitb.enable()
form = cgi.FieldStorage(keep_blank_values=True)
success = True

try:
    connection = pymysql.connect(
        host='bioed.bu.edu',
        user="sbevans",
        password='3d3np33d3n',
        db='sbevans',
        port=4253)
except pymysql.Error as e:
    print(e)
    success = False
cursor = connection.cursor()

print("Content-type: text/html\n")

if (form):
    link = form.getvalue("link", "NULL")
    cite = form.getvalue("cite")
    context = form.getvalue("context", "NULL")
    assay = form.getvalue("assay", "NULL")
    cur_name = form.getvalue("curator")
    cur_notes = form.getvalue("cur_notes", "NULL")
    cur_date = form.getvalue("cur_date")
    con_name = form.getvalue("con_name", "NULL")
    con_date = form.getvalue("con_date")
    ad_info = form.getvalue("ad_info", "NULL")
    org_name = form.getvalue("org_name").title()
    input_domain = form.getvalue("input_domain", "NULL")
    input_path = form.getvalue("input_path", "NULL")
    input_aeran = form.getvalue("input_aeran", "NULL")
    env_other = form.getvalue("other_env_txt", "NULL").title()
    rem_other = form.getvalue("other_rem_txt", "NULL").title()
    environment = form.getvalue("list_env", "NULL")
    rem = form.getvalue("list_rem", "NULL")
    myc_name = form.getvalue("myc_name").title()
    enzymatic = form.getvalue("enzymatic", "NULL")
    loc = form.getvalue("loc", "NULL")

    if "Other" in environment:
        environment = environment.replace("Other", env_other)

    if "Other" in rem:
        rem = rem.replace("Other", rem_other)

    try:
        cursor.execute(f'''
        insert into Literature (Context, Assay, Source, Link)
        values ("{context}", "{assay}", "{cite}", "{link}");''')
        cursor.execute("set @lid = LAST_INSERT_ID();")
    except pymysql.Error as e:
        print(e)
        success = False
    try:
        cursor.execute(f'''
        insert into Mycotoxin (Name, Removal_mech, Enzymatic_or_not, Location)
        values ("{myc_name}", "{rem}", "{enzymatic}", "{loc}");''')
        cursor.execute("set @mid = LAST_INSERT_ID();")
    except pymysql.Error as e:
        print(e)
        success = False
    try:
        cursor.execute(f'''
        insert into Organism (Domain, Name, Pathogenicity, Respiration, Environment)
        values ("{input_domain}", "{org_name}", "{input_path}", "{input_aeran}", "{environment}");''')
        cursor.execute("set @oid = LAST_INSERT_ID();")
    except pymysql.Error as e:
        print(e)
        success = False
    try:
        cursor.execute(f'''
        insert into Curation_Contribution (Con_name, Con_date, Cur_name, Cur_date, Cur_notes, Additional_info)
        values ("{con_name}", "{con_date}", "{cur_name}", "{cur_date}", "{cur_notes}", "{ad_info}");''')
        cursor.execute("set @cid = LAST_INSERT_ID();")
    except pymysql.Error as e:
        print(e)
        success = False
    try:
        cursor.execute('''
        insert into Removal (OID, MID, LID, CID)
        values (@oid, @mid, @lid, @cid);''')
    except pymysql.Error as e:
        print(e)
        success = False

    # try:
    #     for value in ["Domain", "Pathogenicity", "Respiration", "Enviroment"]:
    #         cursor.execute(
    #             f"UPDATE Organism SET {value}=NULL WHERE {value}='NULL' and OID=@oid;")
    #     for value in ["Removal_mech", "Enzymatic_or_not", "Location"]:
    #         cursor.execute(
    #             f"UPDATE Mycotoxin SET {value}=NULL WHERE {value}='NULL' and MID=@mid;")
    #     for value in ["Con_name", "Cur_notes", "Additional_info"]:
    #         cursor.execute(
    #             f"UPDATE Curation_Contribution SET {value}=NULL WHERE {value}='NULL' and CID=@cid;")
    #     for value in ["Context", "Assay", "Link"]:
    #         cursor.execute(
    #             f"UPDATE Literature SET {value}=NULL WHERE {value}='NULL' and LID=@lid;")
    # except pymysql.Error as e:
    #     print(e)

else:
    success = False

if success:
    #results = "Your data insertion was successful!\n"
    #conection.commit()
    results = ""
    for value in ["Domain", "Pathogenicity", "Respiration", "Enviroment"]:
        results += f"UPDATE Organism SET {value}=NULL WHERE {value}='NULL' and OID=@oid;"
else:
    results = "Your data insertion was unsuccessful"

# close cursor and connection
cursor.close()
connection.close()
print(json.dumps(results))
