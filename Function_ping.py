#This is the Main Part of this Programm if ur just interested to ping some Stuff urself!

#Ping Funktion Checking for WIN OS Externe Ping Defenition
import  sys, subprocess, os
def ping(host):
    process = subprocess.Popen(["ping", cmd1, cmd2,host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    streamdata = process.communicate()[0]
    if 'unreachable' in str(streamdata):
        return 1
    return process.returncode
