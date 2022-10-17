import utils.power as power
from utils.settings import chdic
import time

session = power.power()
session.power_set()
session.initiate()

_ = input ("press to shutdown")
session.force_terminate()

