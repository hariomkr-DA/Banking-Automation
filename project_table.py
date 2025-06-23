import sqlite3



def create_db_and_table():
    mydatabase=sqlite3.connect(database='My_bank_Database.sqlite')
    mydatabase.execute("PRAGMA foreign_ky=ON")
    cur=mydatabase.cursor()
    user_ac_table="""create table if not exists user(Name text,Gender text,DOB date,Mob_No text,
    Email text,Aadhaar text, Pan text,Ac_number integer primary key AUTOINCREMENT,
    Password text,IFSC text default 'ABC123',Ac_type text,Balance 
    decimal(20,2) default 0,Opened_Date date default  CURRENT_TIMESTAMP)"""

    txn_table="""create table if not exists user_txn_history(Ac_number integer ,
    ref_no text ,mode text,amount decimal(20,2),desc text,
    date date default  CURRENT_TIMESTAMP 
    )"""
    
    mail="create table if not exists mail(email text,password text)"
    user_issue_table="""create table if not exists user_issue(ac_number integer,email text,date date default  CURRENT_TIMESTAMP,issue text)"""
    cur.execute(user_issue_table)
    cur.execute (user_ac_table)
    cur.execute(txn_table)
    cur.execute(mail)
    
    
    # cur.execute("select name from user where ac_number=?",(2,))
    # user_name=cur.fetchone()
    # print(user_name[0])
    
    mydatabase.close()
    
create_db_and_table()
