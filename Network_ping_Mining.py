import time, datetime, threading, _thread, csv, sys, subprocess, os, sqlite3

#Preferences
host = '192.168.1.' #The 192.168.1.[X] X where the Scripts gone Loop 1 To 254
Database_Location = '/home/pi/Desktop/LAN-Monitoring' #Path & Filename where your Datebase's gona be saved dont use .csv or.db it will be addet during the script
CreateDatabase_on_Startup = True #This Option will create a new Datebase everytime u start the script. Start it just for the first time for use
time_minute_1 = 30 #This means the it will ping for IP when it is HH:30 
time_minute_2 = 0 #This means the it will ping for IP when it is HH:00
time_Anytime = True #Change it to TRUE if you want that the script pings at any time
 #modyfiey for ur OS if necessary WIN(-n 1 -w 1000)

#Write to CSV File Funktion
def WriteCSV(content):
    f = open(Database_Location +'.csv','a')
    f.write(content)
    f.close()

#Create the SQLLite3 Tabelle
def CreateSQLLite_Table():
    #verbinden mit SQLLite
    connection = sqlite3.connect(Database_Location +'.db')
    cursor = connection.cursor()       
    for i in range(1,255,1):       
        sql = 'CREATE TABLE IP'+str(i)+'(Aktive TEXT, Timestamp)'       
        cursor.execute(sql)
        print('Table IP'+str(i)+' has been created',end='\r')
    connection.close()

#Insert to corresponding table
def InsertSQLLite_Table(TableNR,response,Timestamp):
    connection = sqlite3.connect(Database_Location +'.db')
    cursor = connection.cursor()
    sql = "INSERT INTO IP"+TableNR+" VALUES('"+response+"','"+Timestamp+"')"
    cursor.execute(sql)
    connection.commit()
    connection.close()
        
if os.name == 'nt':
    cmd1 = '-n 1'
    cmd2 = '-w 1000'
else:
    cmd1 = '-c 1'
    cmd2 = '-w 1'

#Ping Funktion Checking for WIN OS Externe Ping Defenition
def ping(host):
    process = subprocess.Popen(["ping", cmd1, cmd2,host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    streamdata = process.communicate()[0]
    if 'unreachable' in str(streamdata):
        return 1
    return process.returncode

#Ping and Write the things in to thery Datebase
def pingtest(ianfang,iende):    
    for i in range(ianfang,iende,1):              
        response = ping(host+str(i))
        if response == 0:
            print('Host up!   ', host + str(i),end='\r')
            content = 'ON;' + host + str(i) + ';' + now.strftime("%Y-%m-%d %H:%M") + '\n'
            WriteCSV(content)
            InsertSQLLite_Table(str(i),'True',now.strftime("%Y-%m-%d %H:%M"))
        else:
            print('Host down! ', host + str(i),end='\r')                
            content = 'OFF;' + host + str(i) + ';' + now.strftime("%Y-%m-%d %H:%M") + '\n'
            WriteCSV(content)
            InsertSQLLite_Table(str(i),'False',now.strftime("%Y-%m-%d %H:%M"))      

#Threading for faster speed [PI] U can use more or less
def Start_pingtest_threads():
        a = threading.Thread(target=pingtest,args=(1,49))      
        b = threading.Thread(target=pingtest,args=(50,99))
        c = threading.Thread(target=pingtest,args=(100,149))
        d = threading.Thread(target=pingtest,args=(150,199))
        e = threading.Thread(target=pingtest,args=(200,254))        
        a.start()       
        b.start()       
        c.start()#Starts 5 Threads 1-50 range in IP      
        d.start()        
        e.start()
        print('')
        print('IP-Ping started')
        a.join()
        b.join()
        c.join()#Waits until all the Treads are finished
        d.join()
        e.join()
        print('')
        print('IP-Ping finished')
        print('') #This is for bedder Looking inside the Terminal

#Prints the Time comperison to the User
def PrintWait():
    print('Wait for time',':'.join([str(now.hour), str(now.minute)]),
              ' To be ', ':'.join(['HH', str(time_minute_1)]),
              'or',
              ':'.join(['HH', str(time_minute_2)])
              ,end='\r')
    
#create Files Databses
if CreateDatabase_on_Startup == True:
    open(Database_Location+".db","w+")
    CreateSQLLite_Table()
    open(Database_Location+".csv","w+")
    
#MAIN Programm MAIN_Loop
while True:
    now = datetime.datetime.now()
    time.sleep(1) #checks every second if the Time is right
    if now.minute == time_minute_1 or now.minute == time_minute_2 or time_Anytime == True:
        Start_pingtest_threads()
        PrintWait()
        if time_Anytime == False:
            time.sleep(60) #Prevents doublechecking if your Computer is faster than a Raspberry Pi
    else:
        PrintWait()
