#!/usr/bin/env python3

#Query the miRNA database through the browser using a cgi program

import pymysql
import cgi
import cgitb
#next is for packaging the output into json format
import json
cgitb.enable()

query = """

"""

form = cgi.FieldStorage(keep_blank_values=True)
print("Content-type: text/html\n")

if form:
    organism = form.getvalue("organism", "")
    domain = form.getvalue("domain", "")
    pathogen = form.getvalue("pathogen", "")
    environment = form.getvalue("environment", "")
    aeran = form.getvalue("aeran", "")
    mycotoxin = form.getvalue("mycotoxin", "")
    removal = form.getvalue("removal", "")
    enzymatic = form.getvalue("enzymatic", "")
    intraextra = form.getvalue("intraextra", "")
    context = form.getvalue("context", "")
    assay = form.getvalue("assay", "")
    contributor = form.getvalue("contributor", "")
    curator = form.getvalue("curator", "")
    Source = form.getvalue("Source", "")
    Link = form.getvalue("Link", "")

    try:
      connection = pymysql.connect(
        host='bioed.bu.edu', 
        user='dgolden1',
        password='Square_Liters96', 
        db='group_M',
        port = 4253) 
    except pymysql.Error as e: 
        print(e)

      # get cursor
      cursor = connection.cursor()
      #execute query
      try: 
          cursor.execute(query1,[miRNA_seq_py])
      except pymysql.Error as e: 
          print(e,query1)

      results_seq = cursor.fetchall() 

      #format the output as json object
      print(json.dumps(results_seq))
  if (miRNA_name_py != ""):
      #establish the connection on bioed
      try:
          connection = pymysql.connect(
              host='bioed.bu.edu', 
              user='dgolden1',
              password='Square_Liters96', 
              db='miRNA',
              port = 4253) 
      except pymysql.Error as e: 
          print(e)

      # get cursor
      cursor = connection.cursor()
      #execute query
      try: 
          cursor.execute(query2,[miRNA_name_py])
      except pymysql.Error as e: 
          print(e,query1)

      results_name = cursor.fetchall() 
      if (results_name != ()):
          plot_data = [['target_score']]
          for row in results_name:
              plot_data.append([row[0]])
          print(json.dumps(plot_data))
else:
  print("Content-type: text/html\n")
