import sqlite3 as sql
from flask import session
from passlib.hash import sha256_crypt
import datetime
import ast
import json
import re
import os

def datelist():
    ls=[]
    #date = datetime.datetime.now().date()
    date = datetime.datetime(2018,8,1,12,4,5)
    dstr = date.strftime("%d-%m-%Y")
    year = dstr.split('-')[2]
    year = int(year)
    if (year)%400==0 or (year+1)%400==0:
        loop=366
    elif (year)%100==0 or (year+1)%100==0:
        loop=365
    elif (year)%4==0 or (year+1)%4==0:
        loop=366
    else:
        loop=365
    for i in range(loop):
        ls.append(date.strftime("%d-%m-%Y"))
        date += datetime.timedelta(days=1)
    return ls
def insertUser(request):
    con = sql.connect("user.db")
    
    sqlQuery = "select username from user_info where (username ='" + request.form['username'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    
    if not row:
        ls = datelist()
        breakfast = request.form['defaultb']
        lunch = request.form['defaultl']
        snack = request.form['defaults']
        dinner = request.form['defaultd']
        datedict = dict()
        meal=[breakfast,lunch,snack,dinner]
        for a in ls:
            datedict[a]=meal
        datestr= str(datedict)
        cur.execute("INSERT INTO user_info (username,password,name,default_breakfast,default_lunch,default_snacks,default_dinner,mess_reg) VALUES (?,?,?,?,?,?,?,?)", (request.form['username'], 
                   sha256_crypt.encrypt(request.form['password']),request.form['name'],request.form['defaultb'],request.form['defaultl'],request.form['defaults'],request.form['defaultd'],datestr))
        con.commit()
        print "added user successfully"
       
    con.close()
    return not row

def cancelMeal(request,username):
    drange = (request.form['daterange'].encode("ascii"))
    dates = drange.split('-')
    
    start = dates[0].strip()
    start = start.replace('/','-')
    end =  dates[1].strip()
    end = end.replace('/','-')
    print start
    change = []
    try :
        request.form['b']
        change.append(0)
    except :
        pass
    try :
        request.form['l']
        change.append(1)
    except :
        pass
    try :
        request.form['s']
        change.append(2)
    except :
        pass
    try :
        request.form['d']
        change.append(3)
    except :
        pass
    # print change
    con = sql.connect("user.db")
    sqlQuery = "select * from user_info where username = '%s'"%username
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    dictionary = ast.literal_eval(row[6])
    sdate = datetime.datetime.strptime(start,"%d-%m-%Y")
    edate = datetime.datetime.strptime(end,"%d-%m-%Y")
    print type(sdate)
    dayst = (edate-sdate)
    t = dayst.days+1
    i =0
    print start
    print end
    print t
    while i<t:
        dstr = sdate.strftime("%d-%m-%Y")
        sdate += datetime.timedelta(days=1)
        prev = dictionary[dstr]
        for x in change:
            prev[x] = 'Cancelled'
        dictionary[dstr]=prev
        print(dictionary[dstr])
        i=i+1

    con = sql.connect("user.db")
    cur=con.cursor()
    sqlq ="UPDATE user_info SET mess_reg = ? WHERE (username = ?)"
    cur.execute(sqlq,(str(dictionary),username))
    con.commit()
    con.close()
    calendarGenerate(username)
    
  

def changeRegistrationDatewise(request,username):
    drange = (request.form['daterange'].encode("ascii"))
    dates = drange.split('-')
    start = dates[0].strip()
    start = start.replace('/','-')
    end =  dates[1].strip()
    end = end.replace('/','-')
    print start
    change = []
    try :
        request.form['b']
        change.append(0)
    except :
        pass
    try :
        request.form['l']
        change.append(1)
    except :
        pass
    try :
        request.form['s']
        change.append(2)
    except :
        pass
    try :
        request.form['d']
        change.append(3)
    except :
        pass
    # print change
    mess_val = request.form['options']
    con = sql.connect("user.db")
    sqlQuery = "select * from user_info where username = '%s'"%username
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    dictionary = ast.literal_eval(row[6])
    sdate = datetime.datetime.strptime(start,"%d-%m-%Y")
    edate = datetime.datetime.strptime(end,"%d-%m-%Y")
    print type(sdate)
    dayst = (edate-sdate)
    t = dayst.days+1
    i =0
    print start
    print end
    print t
    while i<t:
        dstr = sdate.strftime("%d-%m-%Y")
        sdate += datetime.timedelta(days=1)
        prev = dictionary[dstr]
        for x in change:
            prev[x] = mess_val
        dictionary[dstr]=prev
        print(dictionary[dstr])
        i=i+1

    con = sql.connect("user.db")
    cur=con.cursor()
    sqlq ="UPDATE user_info SET mess_reg = ? WHERE (username = ?)"
    cur.execute(sqlq,(str(dictionary),username))
    con.commit()
    con.close()
    calendarGenerate(username)



def changeRegistrationDaywise(request,username):
    # drange = (request.form['daterange'].encode("ascii"))
    # dates = drange.split('-')
    # start = dates[0].strip()
    # start = start.replace('/','-')
    # end =  dates[1].strip()
    # end = end.replace('/','-')
    # print start
    change = []
    try :
        request.form['b']
        change.append(0)
    except :
        pass
    try :
        request.form['l']
        change.append(1)
    except :
        pass
    try :
        request.form['s']
        change.append(2)
    except :
        pass
    try :
        request.form['d']
        change.append(3)
    except :
        pass
    # print change
    start =datetime.datetime.today()
    week = (request.form['day'].encode("ascii"))
    print(type(week))
    print week
    while start.weekday() != int(week): #0 for monday
        start += datetime.timedelta(days=1)
    print start
    mess_val = request.form['options']
    con = sql.connect("user.db")
    sqlQuery = "select * from user_info where username = '%s'"%username
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    dictionary = ast.literal_eval(row[6])
    sdate = start
    edate = datetime.datetime(2019,7,31,12,4,5)
    print type(sdate)
    i =0
    print start
    print edate
    while (edate-sdate).days >0:
        dstr = sdate.strftime("%d-%m-%Y")
        sdate += datetime.timedelta(weeks=1)
        prev = dictionary[dstr]
        for x in change:
            prev[x] = mess_val
        dictionary[dstr]=prev
        print(dictionary[dstr])
        i=i+1

    con = sql.connect("user.db")
    cur=con.cursor()
    sqlq ="UPDATE user_info SET mess_reg = ? WHERE (username = ?)"
    cur.execute(sqlq,(str(dictionary),username))
    con.commit()
    con.close()
    calendarGenerate(username)
    

def authenticate(request):
    con = sql.connect("user.db")
    sqlQuery = "select password from user_info where username = '%s'"%request.form['username'] 
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    con.close()
    if row:
       return sha256_crypt.verify(request.form['password'], row[0])
    else:
       return False


def retrieveUsers(): 
	con = sql.connect("user.db")
        # Uncomment line below if you want output in dictionary format
	#con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM user_info;")
	rows = cur.fetchall()
	con.close()
	return rows
    
def retrievePerson(username):
    con = sql.connect("user.db")
    sqlQuery = "select * from user_info where username = '%s'"%username
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    con.close()
    # print(row)
    return row

def retrieveTodaysMess(username):
    con = sql.connect("user.db")
    sqlQuery = "select * from user_info where username = '%s'"%username
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    # string to Dictionary
    dictionary = ast.literal_eval(row[6])
    # retrieve todays meal
    y =datetime.datetime.today().strftime('%d-%m-%Y')
    tom = (datetime.datetime.today()+datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    # print y
    todays_mess = dictionary[y]
    tomorrow = dictionary[tom]
    con.close()
    mess = [todays_mess,tomorrow]
    return mess

##todays menu 

def retrieveTodaysMenu(mess,north,south,east,west):
    menu = []
    bre = mess[0][0]
    lun = mess[0][1]
    sna = mess[0][2]
    din = mess[0][3]
    day = datetime.datetime.today().weekday()
    if bre.lower() == 'north':
        menu.append(north[day][0][0])
    elif bre.lower() == 'south':
        menu.append(south[day][0][0])
    elif bre.lower() == 'east':
        menu.append(east[day][0][0])
    elif bre.lower() == 'west':
        menu.append(west[day][0][0])
    else:
        menu.append('Dominos Opens at 11')
    
    if lun.lower() == 'north':
        menu.append(north[day][1][0])
    elif lun.lower() == 'south':
        menu.append(south[day][1][0])
    elif lun.lower() == 'east':
        menu.append(east[day][1][0])
    elif lun.lower() == 'west':
        menu.append(west[day][1][0])
    else:
        menu.append('Dominos')   

    if sna.lower() == 'north':
        menu.append(north[day][2][0])
    elif sna.lower() == 'south':
        menu.append(south[day][2][0])
    elif sna.lower() == 'east':
        menu.append(east[day][2][0])
    elif sna.lower() == 'west':
        menu.append(west[day][2][0])
    else:
        menu.append('Canteen') 
    
    if din.lower() == 'north':
        menu.append(north[day][3][0])
    elif din.lower() == 'south':
        menu.append(south[day][3][0])
    elif din.lower() == 'east':
        menu.append(east[day][3][0])
    elif din.lower() == 'west':
        menu.append(west[day][3][0])
    else:
        menu.append('Burger King!') 

    return menu

def calendarGenerate(username):
    con = sql.connect("user.db")
    sqlQuery = "select * from user_info where username = '%s'"%username
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    # string to Dictionary
    dictionary = ast.literal_eval(row[6])
    y =datetime.datetime.today().strftime('%d-%m-%Y')
    t = "title"
    st = "start"
    li = ["T07:00:00-05:00","T12:00:00-05:00","T17:00:00-01:00","T20:00:00-05:00"]
    list_json =[]
    for key, value in dictionary.items():
        s = key.split('-')
        d = s[2]+'-'+s[1]+'-'+s[0]
        x=0
        for i in value:
            data = {}
            data['title'] = i.capitalize()
            data['start'] = d+li[x]
            x=x+1
            list_json.append(json.dumps(data))
    con.close()
    line = re.sub("'", "", str(list_json))
    # return Response(json.dumps(list_json),  mimetype='application/json')
    # print(line)
    file_name = ".events_"+username+".json"
    with open(file_name,"w") as f:
        f.write(line)
        f.close()






########----- Refer Ipynb for more details on input and output ###############################
def updateMess(request):
    con = sql.connect("admin.db")
    
    sqlQuery = "select Admin from mess_menu where (Admin ='" + request.form['Admin'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    if row:
        admin = request.form['Admin']
        day = request.form['day']

        ls = ['breakfast','lunch','snack','dinner']
        
        mess = request.form['mess']
        
        breakfast = request.form['bmenu']
        lunch = request.form['lmenu']
        snack = request.form['smenu']
        dinner = request.form['dmenu']
        

        ##---------Menu change
        menu=[breakfast,lunch,snack,dinner]  ## for a particular day
        i=0
        menu_dict = dict()
        for a in ls:
            menu_dict[a]=menu[i]
            i=i+1
            
        menu_dic = str(menu_dict)

        ##-------------
    
        breakfast_b = request.form['bb']
        lunch_b = request.form['lb']
        snack_b = request.form['sb']
        dinner_b = request.form['db']
        bill=[breakfast_b,lunch_b,snack_b,dinner_b]  ## for a particular day

        # bill change

        bill_dict = dict()
        i=0
        for a in ls:
            bill_dict[a]=bill[i]
            i=i+1
        bill_dic = str(bill_dict)

        # if day == 'Mon':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Mon =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        # elif day == 'Tue':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Tue =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        # elif day == 'Wed':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Wed =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        # elif day == 'Thu':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Thu =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        # elif day == 'Fri':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Fri =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        # elif day == 'Sat':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Sat =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        # elif day == 'Sun':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Sun =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        
        sqlq ="UPDATE mess_menu SET Bill = ?,"+day+"=? WHERE (Admin = ?)"
        cur.execute(sqlq,(bill_dic,menu_dic,admin))
        
        con.commit()
    con.close()
    return not row


#############################################################################################################


def retrieveMessMenuNorth(username):

    con = sql.connect("admin.db")
    sqlQuery = "select * from mess_menu where (mess ='" + 'North' + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    # list_north = [[[]]]

    ###      list[Day][Meals]   Day:: 0->mon, 1->tue ... Meal:: 0->break, 1->lunch, 2->snack, 3->Dinner

    list_north = [[ [] for col in range(4)] for rows in range(7)]
    d_m = ast.literal_eval(row[2])
    d_t = ast.literal_eval(row[3])
    d_w = ast.literal_eval(row[4])
    d_th = ast.literal_eval(row[5])
    d_f = ast.literal_eval(row[6])
    d_s = ast.literal_eval(row[7])
    d_su = ast.literal_eval(row[8])
    list_north[0][0].append(d_m['breakfast'])
    list_north[0][1].append(d_m['lunch'])
    list_north[0][2].append(d_m['snack'])
    list_north[0][3].append(d_m['dinner'])

    list_north[1][0].append(d_t['breakfast'])
    list_north[1][1].append(d_t['lunch'])
    list_north[1][2].append(d_t['snack'])
    list_north[1][3].append(d_t['dinner'])

    list_north[2][0].append(d_w['breakfast'])
    list_north[2][1].append(d_w['lunch'])
    list_north[2][2].append(d_w['snack'])
    list_north[2][3].append(d_w['dinner'])

    list_north[3][0].append(d_th['breakfast'])
    list_north[3][1].append(d_th['lunch'])
    list_north[3][2].append(d_th['snack'])
    list_north[3][3].append(d_th['dinner'])

    list_north[4][0].append(d_f['breakfast'])
    list_north[4][1].append(d_f['lunch'])
    list_north[4][2].append(d_f['snack'])
    list_north[4][3].append(d_f['dinner'])

    list_north[5][0].append(d_s['breakfast'])
    list_north[5][1].append(d_s['lunch'])
    list_north[5][2].append(d_s['snack'])
    list_north[5][3].append(d_s['dinner'])

    list_north[6][0].append(d_su['breakfast'])
    list_north[6][1].append(d_su['lunch'])
    list_north[6][2].append(d_su['snack'])
    list_north[6][3].append(d_su['dinner'])
    
    con.close()    

    return list_north

#########################################################################################################


def retrieveMessMenuSouth(username):

    con = sql.connect("admin.db")
    sqlQuery = "select * from mess_menu where (mess ='" + 'South' + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    # list_south = [[[]]]

    ###      list[Day][Meals]   Day:: 0->mon, 1->tue ... Meal:: 0->break, 1->lunch, 2->snack, 3->Dinner

    list_south = [[ [] for col in range(4)] for rows in range(7)]
    d_m = ast.literal_eval(row[2])
    d_t = ast.literal_eval(row[3])
    d_w = ast.literal_eval(row[4])
    d_th = ast.literal_eval(row[5])
    d_f = ast.literal_eval(row[6])
    d_s = ast.literal_eval(row[7])
    d_su = ast.literal_eval(row[8])
    list_south[0][0].append(d_m['breakfast'])
    list_south[0][1].append(d_m['lunch'])
    list_south[0][2].append(d_m['snack'])
    list_south[0][3].append(d_m['dinner'])

    list_south[1][0].append(d_t['breakfast'])
    list_south[1][1].append(d_t['lunch'])
    list_south[1][2].append(d_t['snack'])
    list_south[1][3].append(d_t['dinner'])

    list_south[2][0].append(d_w['breakfast'])
    list_south[2][1].append(d_w['lunch'])
    list_south[2][2].append(d_w['snack'])
    list_south[2][3].append(d_w['dinner'])

    list_south[3][0].append(d_th['breakfast'])
    list_south[3][1].append(d_th['lunch'])
    list_south[3][2].append(d_th['snack'])
    list_south[3][3].append(d_th['dinner'])

    list_south[4][0].append(d_f['breakfast'])
    list_south[4][1].append(d_f['lunch'])
    list_south[4][2].append(d_f['snack'])
    list_south[4][3].append(d_f['dinner'])

    list_south[5][0].append(d_s['breakfast'])
    list_south[5][1].append(d_s['lunch'])
    list_south[5][2].append(d_s['snack'])
    list_south[5][3].append(d_s['dinner'])

    list_south[6][0].append(d_su['breakfast'])
    list_south[6][1].append(d_su['lunch'])
    list_south[6][2].append(d_su['snack'])
    list_south[6][3].append(d_su['dinner'])
    
    con.close()    

    return list_south
#########################################################################################################


def retrieveMessMenuEast(username):

    con = sql.connect("admin.db")
    sqlQuery = "select * from mess_menu where (mess ='" + 'East' + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    # list_east = [[[]]]

    ###      list[Day][Meals]   Day:: 0->mon, 1->tue ... Meal:: 0->break, 1->lunch, 2->snack, 3->Dinner

    list_east = [[ [] for col in range(4)] for rows in range(7)]
    d_m = ast.literal_eval(row[2])
    d_t = ast.literal_eval(row[3])
    d_w = ast.literal_eval(row[4])
    d_th = ast.literal_eval(row[5])
    d_f = ast.literal_eval(row[6])
    d_s = ast.literal_eval(row[7])
    d_su = ast.literal_eval(row[8])
    list_east[0][0].append(d_m['breakfast'])
    list_east[0][1].append(d_m['lunch'])
    list_east[0][2].append(d_m['snack'])
    list_east[0][3].append(d_m['dinner'])

    list_east[1][0].append(d_t['breakfast'])
    list_east[1][1].append(d_t['lunch'])
    list_east[1][2].append(d_t['snack'])
    list_east[1][3].append(d_t['dinner'])

    list_east[2][0].append(d_w['breakfast'])
    list_east[2][1].append(d_w['lunch'])
    list_east[2][2].append(d_w['snack'])
    list_east[2][3].append(d_w['dinner'])

    list_east[3][0].append(d_th['breakfast'])
    list_east[3][1].append(d_th['lunch'])
    list_east[3][2].append(d_th['snack'])
    list_east[3][3].append(d_th['dinner'])

    list_east[4][0].append(d_f['breakfast'])
    list_east[4][1].append(d_f['lunch'])
    list_east[4][2].append(d_f['snack'])
    list_east[4][3].append(d_f['dinner'])

    list_east[5][0].append(d_s['breakfast'])
    list_east[5][1].append(d_s['lunch'])
    list_east[5][2].append(d_s['snack'])
    list_east[5][3].append(d_s['dinner'])

    list_east[6][0].append(d_su['breakfast'])
    list_east[6][1].append(d_su['lunch'])
    list_east[6][2].append(d_su['snack'])
    list_east[6][3].append(d_su['dinner'])
    
    con.close()    

    return list_east

#########################################################################################################



def retrieveMessMenuWest(username):

    con = sql.connect("admin.db")
    sqlQuery = "select * from mess_menu where (mess ='" + 'West' + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    # list_west = [[[]]]

    ###      list[Day][Meals]   Day:: 0->mon, 1->tue ... Meal:: 0->break, 1->lunch, 2->snack, 3->Dinner

    list_west = [[ [] for col in range(4)] for rows in range(7)]
    d_m = ast.literal_eval(row[2])
    d_t = ast.literal_eval(row[3])
    d_w = ast.literal_eval(row[4])
    d_th = ast.literal_eval(row[5])
    d_f = ast.literal_eval(row[6])
    d_s = ast.literal_eval(row[7])
    d_su = ast.literal_eval(row[8])
    list_west[0][0].append(d_m['breakfast'])
    list_west[0][1].append(d_m['lunch'])
    list_west[0][2].append(d_m['snack'])
    list_west[0][3].append(d_m['dinner'])

    list_west[1][0].append(d_t['breakfast'])
    list_west[1][1].append(d_t['lunch'])
    list_west[1][2].append(d_t['snack'])
    list_west[1][3].append(d_t['dinner'])

    list_west[2][0].append(d_w['breakfast'])
    list_west[2][1].append(d_w['lunch'])
    list_west[2][2].append(d_w['snack'])
    list_west[2][3].append(d_w['dinner'])

    list_west[3][0].append(d_th['breakfast'])
    list_west[3][1].append(d_th['lunch'])
    list_west[3][2].append(d_th['snack'])
    list_west[3][3].append(d_th['dinner'])

    list_west[4][0].append(d_f['breakfast'])
    list_west[4][1].append(d_f['lunch'])
    list_west[4][2].append(d_f['snack'])
    list_west[4][3].append(d_f['dinner'])

    list_west[5][0].append(d_s['breakfast'])
    list_west[5][1].append(d_s['lunch'])
    list_west[5][2].append(d_s['snack'])
    list_west[5][3].append(d_s['dinner'])

    list_west[6][0].append(d_su['breakfast'])
    list_west[6][1].append(d_su['lunch'])
    list_west[6][2].append(d_su['snack'])
    list_west[6][3].append(d_su['dinner'])
    
    con.close()    

    return list_west


########################################################################################################
########################################################################################################
def complaint(request):
    f2 = os.path.basename('/static')
    #print request.form
    #print "NOICE"
    mess = request.form['options']
    msg  = request.form['message']
    
    file = request.files['image']

    
    #print (row[0])
    
    
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    if(mess=='north'):
        con = sql.connect("user.db")
        sqlQuery = "select MAX(id) from complaint_north"
        cur = con.cursor()
        cur.execute(sqlQuery)
        row = cur.fetchone()
        con.close()
    
        ids = int(row[0])
        ids = ids+1
        filename= str(ids)
        filename= 'north_'+filename
        ima="yes"
        #print file
        #f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        ## ima="yes"
        f = os.path.join(f2, filename)
        file.save(f)
        if(os.stat(f2+'/'+filename).st_size == 0):
            ima="no"

        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("INSERT INTO complaint_north (message,image) VALUES (?,?)", (msg,ima))
        con.commit()
        con.close()
    
    if(mess=='south'):
        con = sql.connect("user.db")
        sqlQuery = "select MAX(id) from complaint_south"
        cur = con.cursor()
        cur.execute(sqlQuery)
        row = cur.fetchone()
        con.close()
    
        ids = int(row[0])
        ids = ids+1
        filename= str(ids)
        filename= 'south_'+filename
        ima="yes"
        #print file
        #f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        ## ima="yes"
        f = os.path.join(f2, filename)
        file.save(f)
        if(os.stat(f2+'/'+filename).st_size == 0):
            ima="no"
            
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("INSERT INTO complaint_south (message,image) VALUES (?,?)", (msg,ima))
        con.commit()
        con.close()
    
    if(mess=='east'):
        con = sql.connect("user.db")
        sqlQuery = "select MAX(id) from complaint_east"
        cur = con.cursor()
        cur.execute(sqlQuery)
        row = cur.fetchone()
        con.close()
    
        ids = int(row[0])
        ids = ids+1
        filename= str(ids)
        filename= 'east_'+filename
        ima="yes"
        #print file
        #f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        ## ima="yes"
        f = os.path.join(f2, filename)
        file.save(f)
        if(os.stat(f2+'/'+filename).st_size == 0):
            ima="no"
            
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("INSERT INTO complaint_east (message,image) VALUES (?,?)", (msg,ima))
        con.commit()
        con.close()
    #################################
    #  cur.execute("INSERT INTO user_info (username,password,name,default_breakfast,default_lunch,default_snacks,default_dinner,mess_reg) VALUES (?,?,?,?,?,?,?,?)", (request.form['username'], 
    #                sha256_crypt.encrypt(request.form['password']),request.form['name'],request.form['defaultb'],request.form['defaultl'],request.form['defaults'],request.form['defaultd'],datestr))
    #     con.commit()


    if(mess=='west'):
        con = sql.connect("user.db")
        sqlQuery = "select MAX(id) from complaint_west"
        cur = con.cursor()
        cur.execute(sqlQuery)
        row = cur.fetchone()
        con.close()
    
        ids = int(row[0])
        ids = ids+1
        filename= str(ids)
        filename= 'west_'+filename
        ima="yes"
        #print file
        #f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        ## ima="yes"
        f = os.path.join(f2, filename)
        file.save(f)
        if(os.stat(f2+'/'+filename).st_size == 0):
            ima="no"
            
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("INSERT INTO complaint_west (message,image) VALUES (?,?)", (msg,ima))
        con.commit()
        con.close()

    #check for if the file is sent or not
    

    
    return "Done"

    ########################################################################

########################################################################################################


def retrieveBill(username,start,end):
    ## Calculate Bill
    # username = 'zero'
    con = sql.connect("user.db")
    cur = con.cursor()
    # cur.execute("Select * from user_info WHERE username=?",(username))
    # sqlQuery = "select username from user_info where (username ='" + request.form['username'] + "')"
    sqlQuery = "select * from user_info where (username ='" + username + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    dictionary = ast.literal_eval(row[6])
    con.close()

    con = sql.connect("admin.db")
    cur = con.cursor()
    cur.execute("Select price from view_bill WHERE Mess='North'")
    n = cur.fetchone()
    north = ast.literal_eval(n[0])
    cur.execute("Select * from view_bill WHERE Mess='South'")
    s = cur.fetchone()
    south = ast.literal_eval(s[1])
    cur.execute("Select * from view_bill WHERE Mess='East'")
    n = cur.fetchone()
    east = ast.literal_eval(n[1])
    cur.execute("Select * from view_bill WHERE Mess='West'")
    n = cur.fetchone()
    west = ast.literal_eval(n[1])
    con.close()

    # for key in dictionary:
    
    end = datetime.datetime.strptime(end,"%d-%m-%Y")
    start = datetime.datetime.strptime(start,"%d-%m-%Y")
    count = (end-start).days

    breakfast = 0
    lunch = 0
    snacks = 0
    dinner = 0
    bre = [0,0,0,0]
    lun = [0,0,0,0]
    sna = [0,0,0,0]
    din = [0,0,0,0]
    cb = 0 
    cl = 0
    cd = 0
    cs = 0
    ccb = 0
    ccl = 0
    ccs = 0
    ccd = 0

    while count>0:
        
        day = start.strftime('%d-%m-%Y')
        meals = dictionary[day]
        
        b = meals[0]
        l = meals[1]
        s = meals[2]
        d = meals[3]
        
        if b.lower() == 'north':
            t = north[day]
            bre[0]=bre[0]+1
            cb = cb+1
            breakfast = breakfast + int(t[0])
        elif b.lower() == 'south':
            cb = cb+1
            bre[1]=bre[1]+1
            t = south[day]
            breakfast = breakfast + int(t[0])
        elif b.lower() == 'east':
            cb = cb+1
            bre[2]=bre[2]+1
            t = east[day]
            breakfast = breakfast + int(t[0])
        elif b.lower() == 'west':
            cb = cb+1
            bre[3]=bre[3]+1
            t = west[day]
            breakfast = breakfast + int(t[0])
        else: 
            ccb = ccb+1
            
        if l.lower() == 'north':
            t = north[day]
            lun[0]=lun[0]+1
            cl = cl+1
            lunch = lunch + int(t[1])
        elif l.lower() == 'south':
            cl = cl+1
            lun[1]=lun[1]+1
            t = south[day]
            lunch = lunch + int(t[1])
        elif l.lower() == 'east':
            cl = cl+1
            lun[2]=lun[2]+1
            t = east[day]
            lunch = lunch + int(t[1])
        elif l.lower() == 'west':
            cl = cl+1
            lun[3]=lun[3]+1
            t = west[day]
            lunch = lunch + int(t[1])
        else: 
            ccl = ccl+1    
        
        if s.lower() == 'north':
            t = north[day]
            sna[0]=sna[0]+1
            cs = cs+1
            snacks = snacks + int(t[2])
        elif s.lower() == 'south':
            cs = cs+1
            sna[1]=sna[1]+1
            t = south[day]
            snacks = snacks + int(t[2])
        elif s.lower() == 'east':
            t = east[day]
            sna[2]=sna[2]+1
            cs = cs+1
            snacks = snacks + int(t[2])
        elif s.lower() == 'west':
            t = west[day]
            sna[3]=sna[3]+1
            cs = cs+1
            snacks = snacks + int(t[2])
        else: 
            ccs = ccs+1    
            
        if d.lower() == 'north':
            t = north[day]
            din[0]=din[0]+1
            cd = cd+1
            dinner = dinner + int(t[3])
        elif d.lower() == 'south':
            t = south[day]
            din[1]=din[1]+1
            cd = cd+1
            dinner = dinner + int(t[3])
        elif d.lower() == 'east':
            t = east[day]
            din[2]=din[2]+1
            cd = cd+1
            dinner = dinner + int(t[3])
        elif d.lower() == 'west':
            t = west[day]
            din[3]=din[3]+1
            cd = cd+1
            dinner = dinner + int(t[3])
        else:
            ccd = ccd+1
        
        start=start + datetime.timedelta(days=1)
        count=count-1
        totalbill = breakfast+lunch+snacks+dinner
        totalmeal = cb+cl+cs+cd
        totalcancel = ccb+ccl+ccd+ccs
        b = [breakfast,cb,ccb,bre]
        l = [lunch,cl,ccl,lun]
        s = [snacks,cs,ccs,sna]
        d = [dinner,cd,ccd,din]
    return [totalbill,totalcancel,b,l,s,d,totalmeal]



############################################################################################

def updateMessMenu(mess_data):
        
    mess = mess_data.capitalize()
    con = sql.connect("admin.db")
    cur = con.cursor()

    date = datetime.datetime(2018,8,1,12,4,5)
    end = datetime.datetime(2019,8,1,12,4,5)

    dfrom = date.strftime("%d-%m-%Y")
    # dateto = datetime.datetime(2018,8,1,12,4,5)
    date_end = date + datetime.timedelta(days=365)
    dto = date_end.strftime("%d-%m-%Y")
    # print(dateto)

    sqlq = "select Bill from mess_menu WHERE (mess = '" + mess +"')"
    # print(sqlq)
    cur.execute(sqlq)

    bill = cur.fetchone()
    dictionary = ast.literal_eval(bill[0])
    meal =[]
    for key in dictionary:
            meal.append(dictionary[key])
    start = datetime.datetime.today()+datetime.timedelta(days=1)
    count = (end-start).days

    while count<0:
        day = start.strftime('%d-%m-%Y')
        dictionary[day]=meal
        start=start + datetime.timedelta(days=1)
        count = count-1
    sqlq ="UPDATE view_bill SET price = ? WHERE (Mess = ?)"
    cur.execute(sqlq,(str(dictionary),mess))


def changeMessMenu(admin,request):

    # admin = "admin_north"
    day = request.form['days']
    meal = request.form['meals']
    msg = request.form['menu']
    con = sql.connect("admin.db")
    cur = con.cursor()
    sqlq = "Select "+day+" from mess_menu Where Admin ='"+admin+"'"
    cur.execute(sqlq)
    t = cur.fetchone()
    dictionary = ast.literal_eval(t[0])
    dictionary[meal.lower()] = msg

    # sqlq ="UPDATE view_bill SET price = ? WHERE (Mess = ?)"

    sqlq="UPDATE mess_menu SET "+day+" = ? Where Admin = ?"
    cur.execute(sqlq,(str(dictionary),admin))
    # print sqlq
    # print dictionary
    # print admin
    # print day
    # print meal

    con.commit()
    con.close()
    return "Yesssss"

def necessaryinfo(admin):

    mess = admin[6:]
    con = sql.connect("user.db")
    cona = sql.connect("admin.db")
    cur = con.cursor()
    cura = cona.cursor()
    sqlq = "Select price from view_bill WHERE (Mess='"+mess.capitalize()+"')"
    cura.execute(sqlq)
    n = cura.fetchone()
    north = ast.literal_eval(n[0])
    # print(type(n))
    cur.execute("Select * from user_info")
    rows = cur.fetchall()
    con.close()
    count = (len(rows))-1
    br = 0
    lu = 0
    dn = 0
    sn = 0
    bill = [0,0,0,0]
    start = datetime.datetime(2018,8,1,12,4,5)
    # aug sep oct nov
    while count>=0:
        t = rows[count]
        x = start
        end = datetime.datetime.today()
        dictionary = ast.literal_eval(t[6])
        c = (end-start).days+1
        while c>0:
            d = dictionary[x.strftime('%d-%m-%Y')]
            if d[0].lower() == mess:
                bill[0]=bill[0]+int(north[x.strftime('%d-%m-%Y')][0])
                br = br+1
            if d[1].lower() == mess:
                lu = lu+1
                bill[1]=bill[1]+int(north[x.strftime('%d-%m-%Y')][1])
            if d[2].lower() == mess:
                bill[2]=bill[2]+int(north[x.strftime('%d-%m-%Y')][2])
                sn = sn+1
            if d[3].lower() == mess:
                bill[3]=bill[3]+int(north[x.strftime('%d-%m-%Y')][3])
                dn = dn+1
            c =c-1
            x = x+datetime.timedelta(days=1)    
        count = count-1
        
    meals=[br,lu,dn,sn]
    return [meals,bill]
