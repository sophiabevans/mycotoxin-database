# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import cgi
import pymysql
#from getpass import getpass
#pswd = getpass()

#the next two lines are useful for debugging
#they cause errors during execution to be sent back to the browser
import cgitb
cgitb.enable()

#the next line gives us a convenient way to insert values into strings
from string import Template 


html_form = """
            
            """
#retrieve form data from the web server
form = cgi.FieldStorage() 


#next line is always required as first part of html output
print("Content-type: text/html\n")

if (form):
    connection = pymysql.connect(host='bioed.bu.edu', 
                                 port=4253, 
                                 user='', 
                                 database='miRNA', 
                                 password = '')
    cursor = connection.cursor()
    query = """
            """
            
    try:
        cursor.execute(query)
        
    except pymysql.error as e:
        
else:
    html_table = """
    
                 """