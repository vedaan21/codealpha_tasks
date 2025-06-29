from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
import shutil
from PIL import Image   
from datetime import datetime
from datetime import date
import datetime

import re
import random
import cv2
from random import seed
from random import randint
from werkzeug.utils import secure_filename
from flask import send_file
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import threading
import time
import shutil
import hashlib
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser

#drive

#ip,mac
import socket
import re, uuid
#dir
import subprocess

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="file_duplicate"
)

app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    msg=""
    
    return render_template('index.html',msg=msg)

@app.route('/login_user',methods=['POST','GET'])
def login_user():
    act=request.args.get("act")
    msg=""
   
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM fd_user where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            ff=open("static/user.txt","w")
            ff.write(username1)
            ff.close()
            
            return redirect(url_for('userhome')) 
        else:
            msg="You are logged in fail!!!"
        

    return render_template('login_user.html',msg=msg,act=act)

@app.route('/login',methods=['POST','GET'])
def login():
    act=request.args.get("act")
    msg=""
    
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM fd_admin where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('admin')) 
        else:
            msg="You are logged in fail!!!"
        

    return render_template('login.html',msg=msg,act=act)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    act=""
    mycursor = mydb.cursor()

    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']        
        uname=request.form['uname']
        pass1=request.form['pass']

        
        mycursor.execute("SELECT count(*) FROM fd_user where uname=%s",(uname,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
        
            mycursor.execute("SELECT max(id)+1 FROM fd_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO fd_user(id,name,mobile,email,uname,pass) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,mobile,email,uname,pass1)
            mycursor.execute(sql, val)
            mydb.commit()

            
            print(mycursor.rowcount, "Registered Success")
            msg="success"
            
            #if cursor.rowcount==1:
            #    return redirect(url_for('index',act='1'))
        else:
            
            msg='fail'
            
    
    return render_template('register.html', act=act,msg=msg)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    
        
    return render_template('web/admin.html')

def calculate_hash(file_path):
    # Calculate the hash value of a file
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)  # Read the file in chunks to avoid loading it entirely into memory
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    uname=""
    st=""
    data=[]
    drdata=[]
    fdata=[]
    s1=""
    s2=""
    fs=""
    sdata=[]
    vdata=[]
    listdrv=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']
    
    mycursor = mydb.cursor()    

    mycursor.execute("SELECT * FROM fd_user where uname=%s",(uname,))
    data = mycursor.fetchone()

    driveStr = subprocess.check_output("fsutil fsinfo drives")
    drv=driveStr.decode(encoding='utf-8')
    drv1=drv.split('Drives: ')
    drv2=drv1[1].split(' ')
    dlen=len(drv2)
    i=0
    for rr in drv2:
        if i<dlen-1:
            drdata.append(rr)
        i+=1

    if request.method=='POST':
        listdrv=request.form['listdrv']
        t1=request.form['t1']

        if listdrv=="":
            s=1
        else:
            s1="1"
            listdrv=request.form['listdrv']
            
            rootdir = listdrv
            
            for file in os.listdir(rootdir):
                
                d = os.path.join(rootdir, file)
                
                if os.path.isdir(d):
                    fb=os.path.basename(d)
                    if fb=="$RECYCLE.BIN" or fb=="Recovery" or fb=="System Volume Information":
                        s=1
                    else:
                        fd=[]
                        fd.append("dir")
                        fd.append(d)
                        print("dir="+d)
                        fdata.append(fd)
                    
                   

            for file in os.listdir(rootdir):
                
                d = os.path.join(rootdir, file)
                if os.path.isdir(d):
                    s=1
                else:
                    fb=os.path.basename(d)
                    if fb=="":
                        s=1
                    else:
                        fd1=[]
                        fd1.append("file")
                        fd1.append(d)
                        print("file="+d)
                        fdata.append(fd1)

        fn=request.form.getlist('c1[]')
        cnt=len(fn)
        hash1=""

        print("ttt")
        print(t1)
        print(act)
        if t1=="1":
            s1="2"
        if t1=="2":
            #delete
            print(fn)
            for bf in fn:
                mycursor.execute("SELECT count(*) FROM fd_selected where duplicate_id>0 && uname=%s",(uname,))
                bn = mycursor.fetchone()[0]
                if bn>0:
                    mycursor.execute("SELECT * FROM fd_selected where id=%s",(bf,))
                    bd = mycursor.fetchone()
                    bname=bd[2]
                    print(bname)
                    os.remove(bname)
                    mycursor.execute("delete from fd_selected where id=%s",(bf,))
                    mydb.commit()
                    msg="delete"
        ###
        file_root=[]

        if t1=="2" and act is None:
            if cnt>0:
                
                for c11 in fn:
                    cf=c11.split("|")
                    if cf[0]=="dir":
                        for root, dirs, files in os.walk(cf[1]):
                
                            for file in files:
                                with open(os.path.join(root, file), "r") as auto:
                                    if file=="$RECYCLE.BIN" or file=="Recovery" or file=="System Volume Information":
                                        s=1
                                    else:
                                        fs=file.split(".")
                                        if len(fs)>0:
                                            froot=os.path.join(root, file)
                                            cfile=froot
                                            file_root.append(cfile)
                    else:
                        file_root.append(cf[1])
                        
            cnt2=len(file_root)
            if cnt2>0:
                mycursor.execute("delete from fd_selected where uname=%s",(uname,))
                mydb.commit()
                for f_root in file_root:
                    
                    mycursor.execute("SELECT max(id)+1 FROM fd_selected")
                    maxid = mycursor.fetchone()[0]
                    if maxid is None:
                        maxid=1

                    
                    now = date.today() #datetime.datetime.now()
                    rdate=now.strftime("%d-%m-%Y")

                    
                    hash1 = calculate_hash(f_root)
                    
                    sql = "INSERT INTO fd_selected(id,uname,file_path,filetype,status,hash_val) VALUES (%s,%s,%s,%s,%s,%s)"
                    val = (maxid,uname,f_root,'file','0',hash1)
                    mycursor.execute(sql, val)
                    mydb.commit()
                msg="yes"

    mycursor.execute("SELECT count(*) FROM fd_selected where uname=%s",(uname,))
    fcnt = mycursor.fetchone          
    mycursor.execute("SELECT count(*) FROM fd_selected where duplicate_id>0 && uname=%s",(uname,))
    bn = mycursor.fetchone()[0]
    if bn>0:
            mycursor.execute("SELECT * FROM fd_selected where id=%s",(bf,))
            bd = mycursor.fetchone()
            bname=bd[2]
            print(bname)
            os.remove(bname)
            mycursor.execute("delete from fd_selected where id=%s",(bf,))
            mydb.commit()
            msg="delete"
###
    file_root=[]

    if t1=="2" and act is None:
            if cnt>0:
                
                for c11 in fn:
                    cf=c11.split("|")
                    if cf[0]=="dir":
                        for root, dirs, files in os.walk(cf[1]):
                
                            for file in files:
                                with open(os.path.join(root, file), "r") as auto:
                                    if file=="$RECYCLE.BIN" or file=="Recovery" or file=="System Volume Information":
                                        s=1
                                    else:
                                        fs=file.split(".")
                                        if len(fs)>0:
                                            froot=os.path.join(root, file)
                                            cfile=froot
                                            file_root.append(cfile)
                    else:
                        file_root.append(cf[1])
                        
            cnt2=len(file_root)
            if cnt2>0:
                mycursor.execute("delete from fd_selected where uname=%s",(uname,))
                mydb.commit()
                for f_root in file_root:
                    
                    mycursor.execute("SELECT max(id)+1 FROM fd_selected")
                    maxid = mycursor.fetchone()[0]
                    if maxid is None:
                        maxid=1
                    
                    now = date.today() #datetime.datetime.now()
                    rdate=now.strftime("%d-%m-%Y")

                    
                    hash1 = calculate_hash(f_root)
                    
                    sql = "INSERT INTO fd_selected(id,uname,file_path,filetype,status,hash_val) VALUES (%s,%s,%s,%s,%s,%s)"
                    val = (maxid,uname,f_root,'file','0',hash1)
                    mycursor.execute(sql, val)
                    mydb.commit()
                msg="yes"

    mycursor.execute("SELECT count(*) FROM fd_selected where uname=%s",(uname,))
    fcnt = mycursor.fetchone()[0]
    if fcnt>0:
        fs="1"
        mycursor.execute("SELECT * FROM fd_selected where uname=%s",(uname,))
        sdata = mycursor.fetchall()

        mycursor.execute("update fd_selected set status=0")
        mydb.commit()

        mycursor.execute("SELECT * FROM fd_selected group by hash_val having count(*)>1")
        hdd = mycursor.fetchall()
        for hdd1 in hdd:
            mycursor.execute("update fd_selected set status=1 where id=%s",(hdd1[0],))
            mydb.commit()

        mycursor.execute("SELECT * FROM fd_selected where status=1")
        jdd = mycursor.fetchall()
        for jdd1 in jdd:
            mycursor.execute("SELECT * FROM fd_selected where hash_val=%s",(jdd1[5],))
            jdd2 = mycursor.fetchall()
            for jdd3 in jdd2:
                mycursor.execute("update fd_selected set duplicate_id=%s where hash_val=%s && status=0",(jdd1[0],jdd1[5]))
                mydb.commit()

    ###
    mycursor.execute("SELECT count(*) FROM fd_selected where status=1")
    vcnt = mycursor.fetchone()[0]
    if vcnt>0:
        s2="1"
        mycursor.execute("SELECT * FROM fd_selected where status=1")
        vdd = mycursor.fetchall()
        for vdd1 in vdd:
            dt=[]

            dt.append(vdd1[0])
            dt.append(vdd1[2])
            mycursor.execute("SELECT * FROM fd_selected where duplicate_id=%s ",(vdd1[0],))
            vdd2 = mycursor.fetchall()
            dtt1=[]
            for vdd3 in vdd2:
                dtt=[]
                dtt.append(vdd3[0])
                dtt.append(vdd3[2])
                dtt1.append(dtt)
            dt.append(dtt1)
            vdata.append(dt)
    return render_template('web/userhome.html',msg=msg,act=act,data=data,drdata=drdata,fdata=fdata,vdata=vdata,listdrv=listdrv,s1=s1,s2=s2,fs=fs,sdata=sdata)

@app.route('/down', methods=['GET', 'POST'])
def down():
    fn = request.args.get('fname')
    path = request.args.get('path')
    pp=path.split("\\")
    print(pp)
    fv=""
    if len(pp)>0:
        for p1 in pp:
            fv+=p1+"/"

    print(fv)
    print(fn)
    path1=fv+fn
    
    return send_file(path1, as_attachment=True)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
