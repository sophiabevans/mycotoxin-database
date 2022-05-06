#!/usr/bin/env python3
import pymysql
import cgi
import cgitb
import json

cgitb.enable()
form = cgi.FieldStorage()
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
cursor = connection.cursor()

#next line is always required as first part of http output
print("Content-type: text/html\n")

if (form):
      link = form.getvalue("link", "")
      # cite = form.getvalue("cite", "")
      # context = form.getvalue("context", "")
      # assay = form.getvalue("assay", "")
      # curator = form.getvalue("curator", "")
      # cur_notes = form.getvalue("cur_notes", "")
      # cur_date = form.getvalue("cur_date", "")
      # con_name = form.getvalue("con_name", "")
      # con_date = form.getvalue("con_date", "")
      # ad_info = form.getvalue("ad_info", "")
      # org_name = form.getvalue("org_name", "")
      # input_domain = form.getvalue("input_domain", "")
      # input_path = form.getvalue("input_path", "")
      # input_aeran = form.getvalue("input_aeran", "")
      # env_hum = form.getvalue("env_hum", "")
      # env_anim = form.getvalue("env_anim", "")
      # env_plant = form.getvalue("env_plant", "")
      # env_soil = form.getvalue("env_soil", "")
      # env_water = form.getvalue("env_water", "")
      # env_food = form.getvalue("env_food", "")
      # env_other = form.getvalue("env_other", "")
      # myc_name= form.getvalue("myc_name", "")
      # removal = form.getvalue("removal", "")
      # enzymatic = form.getvalue("enzymatic", "")
      # loc = form.getvalue("loc", "")
      #
      # env = ""
      # for e in [env_anim, env_food, env_hum, env_other, env_plant, env_soil, env_water]:
      #     if e != "":
      #         env += f"{e};"

      #if link != "": #and org_name != "" and myc_name != "":
          #pass
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
          #     values ("{myc_name}", "{removal}", "{enzymatic}", "{loc}");''')
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
          #     cursor.execute(f'''
          #     insert into Removal (OID, MID, LID, CID)
          #     values (@oid, @mid, @lid, @cid);''')
          # except pymysql.Error as e:
          #     print(e)
          #     success = False
      #else:
        #  success = False

results = f'you entered: [{link}], link == "": [{link == ""}]'
# if success:
#     results = f"Entry into database successful! entered: {link}"
#     #connection.commit()
# if not success:
#     results = f"Your data insertion was unsuccessful. entered: {link}"

#close cursor and connection
cursor.close()
connection.close()
print(json.dumps(results))
