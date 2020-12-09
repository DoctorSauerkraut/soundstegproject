from datetime import datetime

DBG = ("DEBUG", 4)
VER = ("INFO", 3)
NOR = ("RESULT", 2)
WAR = ("WARNING", 1)
ERR = ("!ERROR!", 0)

LOGLEVEL = NOR

def uprint(s):
    dprint(s, DBG)

def errprint(s):
    dprint(s, ERR)

def dbgprint(s):
    dprint(s, DBG)

def dprint(s, loglvl):
    if(loglvl[1] <= LOGLEVEL[1]):
        now = datetime.now()
        current_time = now.strftime("%d/%M/%Y - %H:%M:%S")
        print(str(LOGLEVEL[0])+":"+current_time+"\t\t"+s)

def logResult(s):
    f = open("report.txt", "a")
    f.write(s)
    f.close()