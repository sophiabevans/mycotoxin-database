#!/usr/bin/env python3

#Query the miRNA database through the browser using a cgi program

import pymysql
import cgi
import cgitb
#next is for packaging the output into json format
import json
cgitb.enable()

query1 = """

"""
query2 = """
"""
query3 = """
"""
query4 = """
"""
query5 = """
"""
query6 = """
"""

form = cgi.FieldStorage(keep_blank_values=True)
print("Content-type: text/html\n")

if form:
    organism_check = form.getvalue("organism_check", "")
    domain_check = form.getvalue("domain_check", "")
    pathogenicity_check = form.getvalue("pathogenicity_check", "")
    environment_check = form.getvalue("environment_check", "")
    aeran_check = form.getvalue("aeran_check", "")
    mycotoxin_check = form.getvalue("mycotoxin_check", "")
    removal_check = form.getvalue("removal_check", "")
    enzymatic_check = form.getvalue("enzymatic_check", "")
    intraextra_check = form.getvalue("intraextra_check", "")
    context_check = form.getvalue("context_check", "")
    assay_check = form.getvalue("assay_check", "")
    contributor_check = form.getvalue("contributor_check", "")
    curator_check = form.getvalue("curator_check", "")
    Source_check = form.getvalue("Source_check", "")
    Link_check = form.getvalue("Link_check", "")
    choose_domain = form.getvalue("choose_domain", "")
    choose_path = form.getvalue("choose_path", "")
    choose_aeran = form.getvalue("choose_aeran", "")
    choose_removal = form.getvalue("choose_removal", "")
    choose_enz = form.getvalue("choose_enz", "")
    choose_location = form.getvalue("choose_location", "")
    where_input = form.getvalue("where_input", "")
    choose_spec_value = form.getvalue("choose_spec_value", "")
    csv = form.getvalue("csv", "")
    txt = form.getvalue("txt", "")
    tsv = form.getvalue("tsv", "")

    try:
      connection = pymysql.connect(
        host='bioed.bu.edu', 
        user='dgolden1',
        password='Square_Liters96', 
        db='Group_M',
        port = 4253) 
    except pymysql.Error as e: 
        print(e)

    cursor = connection.cursor()
    if (QUERY1 CONDITION):
        try: 
            cursor.execute(query1, [SUB1])
        except pymysql.Error as e: 
            print(e)
        results1 = cursor.fetchall() 
        print(json.dumps(results1))
    if (QUERY1 CONDITION):
        try: 
            cursor.execute(query1, [SUB1])
        except pymysql.Error as e: 
            print(e)
        results1 = cursor.fetchall() 
        print(json.dumps(results1))
    if (QUERY1 CONDITION):
        try: 
            cursor.execute(query1, [SUB1])
        except pymysql.Error as e: 
            print(e)
        results1 = cursor.fetchall() 
        print(json.dumps(results1))
    if (QUERY1 CONDITION):
        try: 
            cursor.execute(query1, [SUB1])
        except pymysql.Error as e: 
            print(e)
        results1 = cursor.fetchall() 
        print(json.dumps(results1))
    if (QUERY1 CONDITION):
        try: 
            cursor.execute(query1, [SUB1])
        except pymysql.Error as e: 
            print(e)
        results1 = cursor.fetchall() 
        print(json.dumps(results1))
    if (QUERY1 CONDITION):
        try: 
            cursor.execute(query1, [SUB1])
        except pymysql.Error as e: 
            print(e)
        results1 = cursor.fetchall() 
        print(json.dumps(results1))
  
else:
  print("Content-type: text/html\n")
