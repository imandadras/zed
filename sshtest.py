import os
import shlex
import subprocess
from threading import Timer
import datetime

def cmd(text, timeout=60*3, loggers=None, verbose=False, shell=False):  #TODO improve in case of errors!
    cwd = str(os.getcwd())
    print( cwd + ": "+ " ".join(text.split())) #print it on a nice line
    if shell:
        command = text
    else:
        command = shlex.split(text)
    process = subprocess.Popen( command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=shell)
    timer = Timer(timeout,timeout_handler,args=[process,text,None,loggers])
    timer.start()
    for l in process.stdout:
        timer.cancel()
        timer = Timer(timeout,timeout_handler,args=[process,os.getcwd() + ": " + text, timer, loggers])
        timer.start()
        if verbose:
            print(l)
    retcode = process.wait()
    process.stdout.close()
    timer.cancel()
    timer.join()
    return retcode

def timeout_handler(process,name,timer,loggers=None,kill=True):
    #print("Command {} timed out".format(name),error=True,loggers=loggers)
    timer.cancel()
    timer.join()
    if kill:
        #os.killpg(os.getpgid(process.pid), signal.SIGTERM) 
        process.terminate() #should be enough if shell==False
        process.stdout.close()

print (cmd('dir', shell=True))