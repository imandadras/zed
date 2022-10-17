#!/usr/bin/env python
from os import chdir
import utils.power as power
from utils.settings import chdic
import atexit



#OPENING PSU
session = power.power()
atexit.register(session.terminate)
#setting up PSU
session.power_set()

#TURNING ON DIGITAL SUPPLIES
_ = input ("press enter to turn on board supplies")
session.channel_active(chdic['plus'])
session.channel_active(chdic['minus'])

_ = input ("press enter to turn on vddio")
session.channel_active(chdic['vddio'])


_ = input ("press enter to turn on vdd and vddmem")
session.channel_active(chdic['vdd'])
session.channel_active(chdic['vddmem'])

#session.channel_active(chdic['vddmem'])

_ = input ("press enter to turn on vdde")

session.channel_active(chdic['vdde'])



_ = input ("press enter to turn on ana_vh")
session.channel_active(chdic['vh'])

_ = input ("press enter to turn on ana_CS bias")
session.channel_active(chdic['csbias'])

_ = input ("Press enter to start measurement")
session.initiate()

_=input('press inter to turn off')
#session.terminate()


