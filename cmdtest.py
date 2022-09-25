import os
import shlex
import subprocess
command = shlex.split ("ssh zedb-diana 'ls'")
with open('log.txt', 'a') as f:
    P1=subprocess.Popen (command,  stdout=f,
                            stderr=subprocess.STDOUT, shell=True,)

#[print (l) for l in process.stdout]

