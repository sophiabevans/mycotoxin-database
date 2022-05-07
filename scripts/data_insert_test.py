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
    link = form.getvalue("link", "")
    cite = form.getvalue("cite", "")
    context = form.getvalue("context", "")
    assay = form.getvalue("assay", "")
    cur_name = form.getvalue("curator", "")
    cur_notes = form.getvalue("cur_notes", "")
    cur_date = form.getvalue("cur_date", "")
    con_name = form.getvalue("con_name", "")
    con_date = form.getvalue("con_date", "")
    ad_info = form.getvalue("ad_info", "")
    org_name = form.getvalue("org_name", "").title()
    input_domain = form.getvalue("input_domain", "")
    input_path = form.getvalue("input_path", "")
    input_aeran = form.getvalue("input_aeran", "")
    env_other = form.getvalue("other_env_txt", "").title()
    rem_other = form.getvalue("other_input_rem", "").title()
    test_env = form.getlist("test_env")
    test_rem = form.getlist("test_rem")

    test_env = ";".join(test_env)
    test_rem = ";".join(test_rem)

    # try:
    #     cursor.execute(f'''
    #     insert into Literature (Context, Assay, Source, Link)
    #     values ("{context}", "{assay}", "{cite}", "{link}");''')
    #     cursor.execute("set @lid = LAST_INSERT_ID();")
    # except pymysql.Error as e:
    #     print(e)
    #     success = False
    # try:
    #     cursor.execute(f'''
    #     insert into Mycotoxin (Name, Removal_mech, Enzymatic_or_not, Location)
    #     values ("{myc_name}", "{rem}", "{enzymatic}", "{loc}");''')
    #     cursor.execute("set @mid = LAST_INSERT_ID();")
    # except pymysql.Error as e:
    #     print(e)
    #     success = False
    # try:
    #     cursor.execute(f'''
    #     insert into Organism (Domain, Name, Pathogenicity, Respiration, Environment)
    #     values ("{input_domain}", "{org_name}", "{input_path}", "{input_aeran}", "{env}");''')
    #     cursor.execute("set @oid = LAST_INSERT_ID();")
    # except pymysql.Error as e:
    #     print(e)
    #     success = False
    # try:
    #     cursor.execute(f'''
    #     insert into Curation_Contribution (Con_name, Con_date, Cur_name, Cur_date, Cur_notes, Additional_info)
    #     values ("{con_name}", "{con_date}", "{cur_name}", "{cur_date}", "{cur_notes}", "{ad_info}");''')
    #     cursor.execute("set @cid = LAST_INSERT_ID();")
    # except pymysql.Error as e:
    #     print(e)
    #     success = False
    # try:
    #     cursor.execute('''
    #     insert into Removal (OID, MID, LID, CID)
    #     values (@oid, @mid, @lid, @cid);''')
    # except pymysql.Error as e:
    #     print(e)
    #     success = False

else:
    success = False

if success:
    results = f"""Your data insertion was successful!\n
    {test_env}, {test_rem}"""
    #connection.commit()
else:
    results = "Your data insertion was unsuccessful"

# close cursor and connection
cursor.close()
connection.close()
print(json.dumps(results))
