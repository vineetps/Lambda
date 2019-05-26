#!/usr/bin/python
import sys, logging, pymysql, os

rds_endpoint = os.environ['rds_endpoint']
name = os.environ['name']
password = os.environ['password']
db_name = os.environ['db_name']
port = 3306

Account_Number = os.environ['accNo']
resId = 'i-xxxx'
Creator = 'vineet'

tags = {"Account_Number": Account_Number, "Creator": Creator.lower()}

try:
    conn = pymysql.connect(rds_endpoint, user=name, passwd=password,
                        db=db_name, connect_timeout=5)
    print '\n----------------------------\nDatabase Connected\n----------------------------'
    print 'Querying with account number: '+str(Account_Number)+'\n'
    with conn.cursor() as cur:
        cur.execute(
            'select * from vineet.tagset where Account_Number = '+str(Account_Number))
        for row in cur:
            query = {"Account_Number": str(row[0]), "Creator": row[2].lower()}

    for i in query:
        if query[i] == tags[i]:
            print 'Compliant Tag:', i
        else:
            print 'Non-compliant Tag:', i
except:
    print '\n----------------------------\nDatabase Not Connected\n----------------------------'

