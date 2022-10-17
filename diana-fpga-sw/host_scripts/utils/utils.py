import os
import shlex
import subprocess
from this import s
from threading import Timer
import datetime

from mako.template import Template

def drop_nl(txt):
    if txt[-1] == "\n":
        return txt[:-1]
    else:
        return txt

def listdirs(rootdir, rec=False):
    l = []
    for e in os.listdir(rootdir):
        d = os.path.join(rootdir, e)
        if os.path.isdir(d):
            if rec:
                l.append(listdirs(d))
            else:
                l.append(d)
    return l

def listfiles(rootdir, rec=False):
    if rec:
        raise NotImplementedError
    l = []
    for e in os.listdir(rootdir):
        ep = os.path.join(rootdir, e)
        if os.path.isfile(ep):
            l.append(ep)
    return l

def gen_file_from_template(template_file, out_file, args_dic):
    template_obj = Template(filename=template_file)
    s = template_obj.render(**args_dic)
    with open(out_file, "w", newline='\n') as out_pointer:
        out_pointer.write(s)

#TODO timer handler should be incluidede in a class
def timeout_handler(process,name,timer,loggers=None,kill=True):
    #print("Command {} timed out".format(name),error=True,loggers=loggers)
    if timer:
        timer.cancel()
        timer.join()
    if kill:
        #os.killpg(os.getpgid(process.pid), signal.SIGTERM) 
        process.terminate() #should be enough if shell==False
        process.stdout.close()
# to use cmd command with a singl-word command, set verbose = True
def cmd(text, timeout=60*3, loggers=None, verbose=True, shell=True):  #TODO improve in case of errors!
    cwd = str(os.getcwd())
    print( cwd + ": "+ " ".join(text.split())) #print it on a nice line
    if shell:
        command = text
    else:
        command = shlex.split(text)
    process = subprocess.Popen( command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=shell)
    timer = Timer(timeout,timeout_handler,args=[process,text,None ,loggers])
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
    
def non_blocking_cmd(text):
    cwd = str(os.getcwd())
    print( cwd + ": "+ text)
    command = shlex.split(text)
    process = subprocess.Popen( command, 
                                stdout = subprocess.PIPE, 
                                stderr = subprocess.STDOUT,
                                text = True,
                                universal_newlines = True)
    return process

def is_alive(process):
    p = process.poll()
    return True if (p is None) else False

def check_return_zero(ret_val):
    if not ret_val==0:
        print("An error occurred. Check STDOUT. Exiting...")
        exit()

def current_utctime_string(template):
     return datetime.datetime.now(datetime.timezone.utc).strftime(template)

class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class pushd:

    def __init__(self, newpath):
        self.newpath = cmd ("pushd {}".format(newpath), shell=False)

    def __enter__(self):
        self.savedPath = os.getcwd()
        cmd ("pushd {}".format(self.newpath))

    def __exit__(self, etype, value, traceback):
        cmd ("pushd {}".format(self.savedPath))
