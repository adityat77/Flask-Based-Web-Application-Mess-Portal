from flask import Flask
from flask import session
from flask import redirect, url_for
from flask import render_template
from flask import request
import models as dbHandler
from flask import Response
import sqlite3 as sql
import ast
import datetime
import json
from flask import jsonify
import re
from flask import session as login_session
import os
from dateutil.relativedelta import relativedelta
app = Flask(__name__)
UPLOAD_FOLDER = os.path.basename('/static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'

##########################################################################################

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate,post-check=0, pre-check=0'"
    return response


###################### clender ##################################################
@app.route('/admin', methods=['GET','POST'])
def admin():
    if 'admin' in session:
        val = dbHandler.necessaryinfo(session['admin'])
        if request.method=='POST':
            if request.form['action']=='changeMenu':
                val = dbHandler.changeMessMenu(session['admin'],request)
                msg = "Success!"
                return render_template("admin.html",msg=val)
            elif request.form['action']=='changeBill':
                val = dbHandler.changeMessBill(session['admin'],request)
                msg = "Success!"
                return render_template("admin.html",msg=val)

        else:
            return render_template('admin.html',msg=val)
    else:
        return redirect(url_for('login'))

           

@app.route('/calendar', methods=['GET','POST'])
def calendar():
    if 'username' in session:
        return render_template("json.html")

    return redirect(url_for('login'))
#-----------------------------------------------------------------------------------
@app.route('/data',methods=['GET','POST'])
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    file_name = ".events_"+session['username']+".json"
    print(file_name)
    with open(file_name, "r") as input_data:
        return input_data.read()

###################################################################################
    
@app.route('/cancel', methods=['GET','POST'])
def cancel():
    if request.method=='POST':
            if dbHandler.cancelMeal(request,session['username']):
                msg = "success in changes"
                return render_template("cancel.html",message=msg)
            else:
                msg = "failed to make changes"
                return render_template("cancel.html", message=msg)    
    if 'username' in session:
        return render_template("cancel.html")
    return redirect(url_for('login'))

#########################################################################
@app.route('/feedback', methods=['GET','POST'])
def feedback():
    if 'admin' in session:
        if request.method=='POST':
            
            if request.form['prevnext'] == 'next':
                #database connection
                if(session['admin']=='admin_north'):
                    con = sql.connect("user.db")
                    sqlQuery = "select MAX(id) from complaint_north"
                    cur = con.cursor()
                    cur.execute(sqlQuery)
                    row = cur.fetchone()
                    con.close()
                    MAX = int(row[0])
                    if(feedback.northcomp==MAX):
                        imgq= str(feedback.northcomp)
                        con = sql.connect("user.db")
                        sqlQuery = "select message from complaint_north WHERE( id='"+str(feedback.northcomp)+"')"
                        cur = con.cursor()
                        cur.execute(sqlQuery)
                        row = cur.fetchone()
                        message= row[0]
                        con.close()

                        imgq = 'north_'+imgq
                        return render_template('feedback.html',imga=imgq,msg = message)
                    feedback.northcomp = feedback.northcomp +1
                    imgq= str(feedback.northcomp)
                    con = sql.connect("user.db")
                    sqlQuery = "select message from complaint_north WHERE( id='"+str(feedback.northcomp)+"')"
                    cur = con.cursor()
                    cur.execute(sqlQuery)
                    row = cur.fetchone()
                    message= row[0]
                    con.close()
                    imgq = 'north_'+imgq
                    return render_template('feedback.html',imga=imgq,msg= message)

                elif(session['admin']=='admin_south'):
                    con = sql.connect("user.db")
                    sqlQuery = "select MAX(id) from complaint_south"
                    cur = con.cursor()
                    cur.execute(sqlQuery)
                    row = cur.fetchone()
                    con.close()
                    MAX = int(row[0])
                    if(feedback.southcomp==MAX):
                        imgq= str(feedback.southcomp)

                        con = sql.connect("user.db")
                        sqlQuery = "select message from complaint_south WHERE( id='"+str(feedback.southcomp)+"')"
                        cur = con.cursor()
                        cur.execute(sqlQuery)
                        row = cur.fetchone()
                        message= row[0]
                        con.close()


                        imgq = 'south_'+imgq
                        return render_template('feedback.html',imga=imgq,msg = message)
                    feedback.southcomp = feedback.southcomp +1
                    imgq= str(feedback.southcomp)

                    con = sql.connect("user.db")
                    sqlQuery = "select message from complaint_south WHERE( id='"+str(feedback.southcomp)+"')"
                    cur = con.cursor()
                    cur.execute(sqlQuery)
                    row = cur.fetchone()
                    message= row[0]
                    con.close()

                    imgq = 'south_'+imgq
                    return render_template('feedback.html',imga=imgq,msg=message)

                elif(session['admin']=='admin_east'):
                    con = sql.connect("user.db")
                    sqlQuery = "select MAX(id) from complaint_east"
                    cur = con.cursor()
                    cur.execute(sqlQuery)
                    row = cur.fetchone()
                    con.close()
                    MAX = int(row[0])
                    if(feedback.eastcomp==MAX):
                        imgq= str(feedback.eastcomp)

                        con = sql.connect("user.db")
                        sqlQuery = "select message from complaint_east WHERE( id='"+str(feedback.eastcomp)+"')"
                        cur = con.cursor()
                        cur.execute(sqlQuery)
                        row = cur.fetchone()
                        message= row[0]
                        con.close()

                        imgq = 'east_'+imgq
                        return render_template('feedback.html',imga=imgq,msg= message)
                    feedback.eastcomp = feedback.eastcomp +1
                    imgq= str(feedback.eastcomp)

                    con = sql.connect("user.db")
                    sqlQuery = "select message from complaint_east WHERE( id='"+str(feedback.eastcomp)+"')"
                    cur = con.cursor()
                    cur.execute(sqlQuery)
                    row = cur.fetchone()
                    message= row[0]
                    con.close()

                    imgq = 'east_'+imgq
                    return render_template('feedback.html',imga=imgq,msg=message)  

                elif(session['admin']=='admin_west'):
                    con = sql.connect("user.db")
                    sqlQuery = "select MAX(id) from complaint_west"
                    cur = con.cursor()
                    cur.execute(sqlQuery)
                    row = cur.fetchone()
                    con.close()
                    MAX = int(row[0])
                    if(feedback.westcomp==MAX):
                        imgq= str(feedback.westcomp)
                        con = sql.connect("user.db")
                        sqlQuery = "select message from complaint_west WHERE( id='"+str(feedback.westcomp)+"')"
                        cur = con.cursor()
                        cur.execute(sqlQuery)
                        row = cur.fetchone()
                        message= row[0]
                        con.close()


                        imgq = 'west_'+imgq
                        return render_template('feedback.html',imga=imgq,msg=message)
                    feedback.westcomp = feedback.westcomp +1
                    imgq= str(feedback.westcomp)
                    imgq = 'west_'+imgq
                    return render_template('feedback.html',imga=imgq)  

            elif request.form['prevnext'] == 'prev':
                if(session['admin']=='admin_north'):
                    if(feedback.northcomp<=1):
                        imgq= str(feedback.northcomp)

                        con = sql.connect("user.db")
                        sqlQuery = "select message from complaint_north WHERE( id='"+str(feedback.northcomp)+"')"
                        cur = con.cursor()
                        cur.execute(sqlQuery)
                        row = cur.fetchone()
                        message= row[0]
                        con.close()


                        imgq = 'north_'+imgq
                        return render_template('feedback.html',imga=imgq,msg=message)
                    feedback.northcomp = feedback.northcomp -1
                    imgq= str(feedback.northcomp)

                    con = sql.connect("user.db")
                    sqlQuery = "select message from complaint_north WHERE( id='"+str(feedback.northcomp)+"')"
                    cur = con.cursor()
                    cur.execute(sqlQuery)
                    row = cur.fetchone()
                    message= row[0]
                    con.close()

                    imgq = 'north_'+imgq
                    return render_template('feedback.html',imga=imgq,msg = message)

                if(session['admin']=='admin_south'):
                    if(feedback.southcomp<=1):
                        imgq= str(feedback.southcomp)

                        con = sql.connect("user.db")
                        sqlQuery = "select message from complaint_south WHERE( id='"+str(feedback.southcomp)+"')"
                        cur = con.cursor()
                        cur.execute(sqlQuery)
                        row = cur.fetchone()
                        message= row[0]
                        con.close()

                        imgq = 'south_'+imgq
                        return render_template('feedback.html',imga=imgq,msg=message)
                    feedback.southcomp = feedback.southcomp -1
                    imgq= str(feedback.southcomp)

                    con = sql.connect("user.db")
                    sqlQuery = "select message from complaint_south WHERE( id='"+str(feedback.southcomp)+"')"
                    cur = con.cursor()
                    cur.execute(sqlQuery)
                    row = cur.fetchone()
                    message= row[0]
                    con.close()
                    imgq = 'south_'+imgq
                    return render_template('feedback.html',imga=imgq,msg=message)
                
                if(session['admin']=='admin_west'):
                    if(feedback.westcomp<=1):
                        imgq= str(feedback.westcomp)

                        con = sql.connect("user.db")
                        sqlQuery = "select message from complaint_west WHERE( id='"+str(feedback.westcomp)+"')"
                        cur = con.cursor()
                        cur.execute(sqlQuery)
                        row = cur.fetchone()
                        message= row[0]
                        con.close()

                        imgq = 'west_'+imgq
                        return render_template('feedback.html',imga=imgq,msg=message)
                    feedback.westcomp = feedback.westcomp -1
                    imgq= str(feedback.westcomp)

                    con = sql.connect("user.db")
                    sqlQuery = "select message from complaint_west WHERE( id='"+str(feedback.westcomp)+"')"
                    cur = con.cursor()
                    cur.execute(sqlQuery)
                    row = cur.fetchone()
                    message= row[0]
                    con.close()

                    imgq = 'west_'+imgq
                    return render_template('feedback.html',imga=imgq,msg=message)
                
                if(session['admin']=='admin_east'):
                    if(feedback.eastcomp<=1):
                        imgq= str(feedback.eastcomp)

                        con = sql.connect("user.db")
                        sqlQuery = "select message from complaint_east WHERE( id='"+str(feedback.eastcomp)+"')"
                        cur = con.cursor()
                        cur.execute(sqlQuery)
                        row = cur.fetchone()
                        message= row[0]
                        con.close()


                        imgq = 'east_'+imgq
                        return render_template('feedback.html',imga=imgq,msg=message)
                    feedback.eastcomp = feedback.eastcomp -1
                    imgq= str(feedback.eastcomp)

                    con = sql.connect("user.db")
                    sqlQuery = "select message from complaint_east WHERE( id='"+str(feedback.eastcomp)+"')"
                    cur = con.cursor()
                    cur.execute(sqlQuery)
                    row = cur.fetchone()
                    message= row[0]
                    con.close()
                    imgq = 'east_'+imgq
                    return render_template('feedback.html',imga=imgq,msg= message)
                
        else:

            if(session['admin']=='admin_north'):
                imgq= str(feedback.northcomp)
                imgq = 'north_'+imgq
                con = sql.connect("user.db")
                sqlQuery = "select message from complaint_north WHERE( id='"+str(feedback.northcomp)+"')"
                cur = con.cursor()
                cur.execute(sqlQuery)
                row = cur.fetchone()
                message= row[0]
                con.close()
                return render_template('feedback.html',imga=imgq,msg= message)
            if(session['admin']=='admin_south'):
                imgq= str(feedback.southcomp)
                imgq = 'south_'+imgq
                con = sql.connect("user.db")
                sqlQuery = "select message from complaint_south WHERE( id='"+str(feedback.southcomp)+"')"
                cur = con.cursor()
                cur.execute(sqlQuery)
                row = cur.fetchone()
                message= row[0]
                con.close()
                return render_template('feedback.html',imga=imgq,msg= message)
            
            if(session['admin']=='admin_east'):
                imgq= str(feedback.eastcomp)
                imgq = 'east_'+imgq
                con = sql.connect("user.db")
                sqlQuery = "select message from complaint_east WHERE( id='"+str(feedback.eastcomp)+"')"
                cur = con.cursor()
                cur.execute(sqlQuery)
                row = cur.fetchone()
                message= row[0]
                con.close()
                return render_template('feedback.html',imga=imgq,msg= message)
            
            else:
                imgq= str(feedback.westcomp)
                imgq = 'west_'+imgq
                con = sql.connect("user.db")
                sqlQuery = "select message from complaint_west WHERE( id='"+str(feedback.westcomp)+"')"
                cur = con.cursor()
                cur.execute(sqlQuery)
                row = cur.fetchone()
                message= row[0]
                con.close()
                return render_template('feedback.html',imga=imgq,msg= message)

    else:
        return redirect(url_for('login'))

##############################################################################
@app.route('/complaint', methods=['GET','POST'])
def complaint():
    
    if request.method=='POST':
        if dbHandler.complaint(request):
        #msg = "su c ce ss in changes"
        #return render_template("home.html",message=msg)
            return redirect(url_for('home'))
        #else:
        #    msg = "failed to make changes"
        #return render_template("cancel.html", message=msg)    
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


##############################################################################

@app.route('/changeReg', methods=['GET','POST'])
def changeReg():
    if 'admin' in session:
        #database connection
        return redirect(url_for('admin'))
    if request.method=='POST':
        if request.form['action']=='datewise':
                if dbHandler.changeRegistrationDatewise(request,session['username']):
                    msg = "success in changes"
                    return render_template("changeReg.html",message=msg)
                else:
                    msg = "failed to make changes"
                    return render_template("changeReg.html", message=msg)    

        if request.form['action']=='daywise':
            if dbHandler.changeRegistrationDaywise(request,session['username']):
                msg = "success in changes"
                return render_template("changeReg.html",message=msg)
            else:
                msg = "failed to make changes"
                return render_template("changeReg.html", message=msg)    
    if 'username' in session:
        return render_template("changeReg.html")
    else :
        return redirect(url_for('login'))


###################### root ##################################################



@app.route('/')
def index():
   if 'username' in session:
      return redirect(url_for('login'))
   else:
      return render_template("login.html", logged_in = False,  username=None)

 
####################### login #################################################
@app.route('/login', methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    if 'admin' in session:
        #database connection
        return redirect(url_for('admin'))
    if request.method == 'POST':
        lsadmin =['admin_north','admin_south','admin_east','admin_west']
        if request.form['username'] in lsadmin:
            if dbHandler.authenticate(request):
                session['admin'] = request.form['username']
                msg = "successful login"
                #rows = dbHandler.retrievePerson(session['username'])
                #print(rows)
                return redirect(url_for('admin'))
            else: 
                msg ="login failed"
                return (render_template('login.html',msg=msg))
        if dbHandler.authenticate(request):
            session['username'] = request.form['username']
            msg = "successful login"
            rows = dbHandler.retrievePerson(session['username'])
            print(rows)
            return redirect(url_for('home'))
        else: 
            msg ="login failed"
    return(render_template("login.html"))



####################### home #################################################
@app.route('/home', methods=['GET','POST'])
def home():
    rowss = []
    if 'admin' in session:
        #database connection
        return redirect(url_for('login'))
    if 'username' in session:
        print "yolo"
        dbHandler.calendarGenerate(session['username'])
        rows = dbHandler.retrievePerson(session['username'])
        mess = dbHandler.retrieveTodaysMess(session['username'])
        north = dbHandler.retrieveMessMenuNorth(session['username'])
        south = dbHandler.retrieveMessMenuSouth(session['username'])
        east = dbHandler.retrieveMessMenuEast(session['username'])
        west = dbHandler.retrieveMessMenuWest(session['username'])
        menu = dbHandler.retrieveTodaysMenu(mess,north,south,east,west)
        # print rows 
        return render_template("home.html", row=rows, tbf = mess[0][0].capitalize()
                                                    , tlu = mess[0][1].capitalize()
                                                    , tsn = mess[0][2].capitalize()
                                                    , tdn = mess[0][3].capitalize(),messt=mess,north=north,south=south,east=east,west=west,menu=menu)
    if request.method=='POST':
        if dbHandler.authenticate(request): 
            session['username'] = request.form['username']
            msg = "successful login"
            dbHandler.calendarGenerate(session['username'])
            rows = dbHandler.retrievePerson(session['username'])
            mess = dbHandler.retrieveTodaysMess(session['username'])
            north = dbHandler.retrieveMessMenuNorth(session['username'])
            south = dbHandler.retrieveMessMenuSouth(session['username'])
            east = dbHandler.retrieveMessMenuEast(session['username'])
            west = dbHandler.retrieveMessMenuWest(session['username'])
            menu = dbHandler.retrieveTodaysMenu(mess,north,south,east,west)
            # print rows
            # print rows
            rowss = rows 
            return render_template("home.html", row=rows, tbf = mess[0][0].capitalize()
                                                    , tlu = mess[0][1].capitalize()
                                                    , tsn = mess[0][2].capitalize()
                                                    , tdn = mess[0][3].capitalize(),messt=mess,north=north,south=south,east=east,west=west,menu=menu)
        # return render_template("home.html", row=rowss, tbf = mess[0].capitalize()
        #                                             , tlu = mess[1].capitalize()
        #                                             , tsn = mess[2].capitalize()
        #                                             , tdn = mess[3].capitalize(),north=north,south=south)
    else: 
        msg ="login failed"
        return render_template("login.html", message=msg)
    
    return redirect(url_for('login'))

	
                                                        

######################## logout #################################################
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'admin' in session:
        session.pop('admin')
        for key in session.keys():
            session.pop(key)
        #database connection
        return redirect(url_for('login'))

    if 'username' in session:
        file_name = ".events_"+session['username']+".json"
        # session.clear()
        session.pop('username')
        for key in session.keys():
            session.pop(key)

        os.remove(file_name)
    return redirect(url_for('login'))

######################### register ################################################
@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'admin' in session:
        return redirect(url_for('admin'))
    if 'username' in session:
        return redirect(url_for('home'))
    elif request.method=='POST':
        if dbHandler.insertUser(request):
            msg = "success in adding user"
            return render_template("login.html",message=msg)
        else:
            msg = "failed to add user"
	    

    return render_template("register.html")
    

######################### secret page: a password protected page ################################################ 
# @app.route('/secret_page')
# def secret_page():

#     #only logged in user is allowed see other users' details.
#     if 'username' in session :
#        rows = dbHandler.retrievePerson(session['username'])
#        print rows
#        return render_template("showall.html", rows = rows)
#     else:
#        return redirect(url_for('login'))

##########################################################################

@app.route('/view_bill', methods=['GET','POST'])
def view_bill():
    if 'admin' in session:
        return redirect(url_for('admin'))

    if request.method=='POST':

        if request.form['options']== 'sem':
            start = '01-08-2018'
            end = datetime.datetime.today().strftime('%d-%m-%Y')
            op = "Bill Till current Semester"

        elif request.form['options'] == 'month':
            x=datetime.datetime.today()+ relativedelta(months=-1)
            y = x+relativedelta(months=1)
            z = x.strftime('%d-%m-%Y')
            start = '01'+z[2:]
            e = datetime.datetime.strptime(start,"%d-%m-%Y")
            y = e+relativedelta(months=1)
            end=y.strftime('%d-%m-%Y')
            op = "Past Month ( "+start+" /  "+end+" )"
        
        elif request.form['options'] == 'week':
            start = datetime.datetime.today()+datetime.timedelta(days=-1)
            start=(start+datetime.timedelta(weeks=-1)).strftime('%d-%m-%Y')
            end = datetime.datetime.today().strftime('%d-%m-%Y')
            op = "Past Week ( "+start+" /  "+end+" )"
        value  = dbHandler.retrieveBill(session['username'],start,end)
        to = value[0]
        tc = value[1]
        b = value[2]
        l = value[3]
        s = value[4]
        d = value[5]
        meals = value[6]
        return render_template("viewbill.html",total=meals,operation=op,bill=to,cancelled=tc,b=b,l=l,s=s,d=d)


    if 'username' in session:
        return render_template("viewbill_data.html")

    return redirect(url_for('login'))







###########################################################################

if __name__ == '__main__':
    feedback.comp = 1
    feedback.northcomp = 1
    feedback.southcomp = 1
    feedback.eastcomp = 1
    feedback.westcomp = 1
    app.run(debug=True, host='127.0.0.1')

