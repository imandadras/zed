
from pickle import TRUE
import nidcpower
import csv
import datetime
import os
from bidict import bidict
from utils.settings import chdic

class power:
    def __init__(self, board_plus=5, board_minus=-5, vddio=1.8, vdd=0.8, vdd_mem=0.8, vdde=0.8, ana_vh=0.8, ana_csbias=0.6, measurementFolder="./log/"):
        self.session = nidcpower.Session(['SMU1/0:3', 'SMU2/0:3'], reset=True)
        self.channel_indices = '0-{0}'.format(self.session.channel_count - 1)
        self.channels = self.session.get_channel_names(self.channel_indices)
        self.board_plus = board_plus
        self.board_minus = board_minus
        self.vddio = vddio
        self.vdd = vdd
        self.vdd_mem = vdd_mem
        self.vdde = vdde
        self.ana_vh = ana_vh
        self.ana_csbias = ana_csbias
        self.logfile = "{}/info.txt".format(measurementFolder)
        self.measurementFolder = measurementFolder
        os.makedirs(os.path.dirname(self.logfile), exist_ok=True)
        self.session.compliance_limit_symmetry = nidcpower.ComplianceLimitSymmetry.ASYMMETRIC
        self.session.output_function = nidcpower.OutputFunction.DC_VOLTAGE
        #self.session.channels['SMU1/0'].current_limit_high = 0.5
        #self.session.channels['SMU1/0'].current_limit_high = 0.5
        #self.session.channels['SMU1/3'].current_limit_high = 0.5
        self.session.current_limit_high = 0.5
        self.session.current_limit_low = -0.5
        

    def power_on (self):
        self.session.channels['SMU1/0'].voltage_level = self.board_plus
        self.session.channels['SMU1/3'].voltage_level = self.board_minus
        self.session.channels['SMU2/0'].voltage_level = self.vddio
        self.session.channels['SMU2/1'].voltage_level = self.vdd
        self.session.channels['SMU2/2'].voltage_level = self.vdd_mem
        self.session.channels['SMU2/3'].voltage_level = self.vdde
        self.session.channels['SMU1/2'].voltage_level = self.ana_vh
        self.session.channels['SMU1/1'].voltage_level = self.ana_csbias

        with open (self.logfile, 'w+') as f :
                f.write("Powering time= {}\n".format(datetime.datetime.now()))
        self.session.channels['SMU1/0'].initiate()
        self.session.channels['SMU1/3'].initiate()
        self.session.channels['SMU2/0'].initiate()
        self.session.channels['SMU2/1'].initiate()
        self.session.channels['SMU2/2'].initiate()
        self.session.channels['SMU2/3'].initiate()
        self.session.channels['SMU1/2'].initiate()
        self.session.channels['SMU1/1'].initiate()

    def current_limit(self, channel, limit) :
        self.session.channels[channel].current_limit=limit

    def power_set(self):
        self.session.channels['SMU1/0'].voltage_level = self.board_plus
        self.session.channels['SMU1/3'].voltage_level = self.board_minus
        self.session.channels['SMU2/0'].voltage_level = self.vddio
        self.session.channels['SMU2/1'].voltage_level = self.vdd
        self.session.channels['SMU2/2'].voltage_level = self.vdd_mem
        self.session.channels['SMU2/3'].voltage_level = self.vdde
        self.session.channels['SMU1/2'].voltage_level = self.ana_vh
        self.session.channels['SMU1/1'].voltage_level = self.ana_csbias
        with open (self.logfile, 'w+') as f :
            f.write("Voltages are set at {}\n".format(datetime.datetime.now()))

    def channel_active(self, channel):
        self.session.channels[channel].initiate()
        dic = bidict (chdic)
        with open (self.logfile, 'a+') as f :
            f.write("Channel {} is activated at {}\n".format(dic.inverse[channel], datetime.datetime.now()))

    def initiate (self):
        # Configure the session.
        with open (self.logfile, 'a') as f :
            f.write("Measurement time = {}\n".format(datetime.datetime.now()))
        self.session.abort()
        self.session.sense = nidcpower.Sense.LOCAL
        self.session.measure_record_length_is_finite = False
        self.session.measure_when = nidcpower.MeasureWhen.AUTOMATICALLY_AFTER_SOURCE_COMPLETE
        self.session.commit()
        self.session.initiate()

    def measure (self):
        with open (self.logfile, 'a') as f :
            f.write("Measurement time = {}\n".format(datetime.datetime.now()))
            self.session.abort()
            self.session.sense = nidcpower.Sense.LOCAL
            self.session.measure_record_length_is_finite = False
            self.session.measure_when = nidcpower.MeasureWhen.AUTOMATICALLY_AFTER_SOURCE_COMPLETE
            
    def terminate (self) :
        dic = bidict(chdic)
        for channel in (self.channels):
            measurement = self.session.channels[channel].fetch_multiple(self.session.channels[channel].fetch_backlog)
            with open('{}/{}.csv'.format(self.measurementFolder, dic.inverse[channel]),'w+',newline='') as f :
                writer = csv.writer (f)
                writer.writerows(measurement)
        self.session.abort()
        self.session.channels['SMU1/1'].voltage_level = 0
        self.session.channels['SMU1/2'].voltage_level = 0
        self.session.channels['SMU2/3'].voltage_level = 0
        self.session.channels['SMU2/2'].voltage_level = 0
        self.session.channels['SMU2/1'].voltage_level = 0
        self.session.channels['SMU2/0'].voltage_level = 0
        self.session.channels['SMU1/3'].voltage_level = 0
        self.session.channels['SMU1/0'].voltage_level = 0

        with open (self.logfile, 'a') as f :
            f.write("Termination time= {}\n".format(datetime.datetime.now()))   

        self.session.channels['SMU1/1'].initiate()
        self.session.channels['SMU1/2'].initiate()
        self.session.channels['SMU2/3'].initiate()
        self.session.channels['SMU2/2'].initiate()
        self.session.channels['SMU2/1'].initiate()
        self.session.channels['SMU2/0'].initiate()
        self.session.channels['SMU1/3'].initiate()
        self.session.channels['SMU1/0'].initiate()
        self.session.close()

    def force_terminate (self):
        self.session.abort()
        self.session.channels['SMU1/1'].voltage_level = 0
        self.session.channels['SMU1/2'].voltage_level = 0
        self.session.channels['SMU2/3'].voltage_level = 0
        self.session.channels['SMU2/2'].voltage_level = 0
        self.session.channels['SMU2/1'].voltage_level = 0
        self.session.channels['SMU2/0'].voltage_level = 0
        self.session.channels['SMU1/3'].voltage_level = 0
        self.session.channels['SMU1/0'].voltage_level = 0

        with open (self.logfile, 'a') as f :
            f.write("The measurement is forcefully closed at {} without measurement\n".format(datetime.datetime.now()))   

        self.session.channels['SMU1/1'].initiate()
        self.session.channels['SMU1/2'].initiate()
        self.session.channels['SMU2/3'].initiate()
        self.session.channels['SMU2/2'].initiate()
        self.session.channels['SMU2/1'].initiate()
        self.session.channels['SMU2/0'].initiate()
        self.session.channels['SMU1/3'].initiate()
        self.session.channels['SMU1/0'].initiate()
        self.session.close()
