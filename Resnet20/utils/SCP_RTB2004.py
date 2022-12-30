from utils.lab_utils import InstumentClass
from RsInstrument import RsInstrument as RSI

# manual website --> https://www.rohde-schwarz.com/webhelp/RTB_HTML_UserManual_en/Content/f04d8c7e15c9475d.htm 
class SCP_RTB2004(InstumentClass):
    def __init__(self, name, ip_addr, **res_manager_args):
        super(SCP_RTB2004, self).__init__(name, ip_addr, **res_manager_args)

    @staticmethod
    def _open_resource(IP, id_query=True, reset=False, **args):
        return RSI(IP, id_query, reset, **args)

    def _init_instrument(self):
        self.tool.assert_minimum_version('1.9.0')
        self.tool.visa_timeout = 3000  # Timeout for VISA Read Operations [millisec]; recommended max 10s
        self.tool.opc_timeout = 3000   # Timeout for opc-synchronised operations (OPC = OPerationComplete; instrument finishes all pending tasks before continuing)
        self.tool.instrument_status_checking = True # Error check after each command
        self._init_measurements()

    def _init_measurements(self):
        pass
        #self.tool.write_str('MEASurement1:TIMeout:AUTO ON') # Automatic setup time after selecting measurements

    def status(self):
        idn = self.tool.query_str('*IDN?')
        print("Hello, I am: '{}'".format(idn))
        print('RsInstrument driver version: {}'.format(self.tool.driver_version))
        print('Visa manufacturer: {}'.format(self.tool.visa_manufacturer))
        print('Instrument full name: {}'.format(self.tool.full_instrument_model_name))
        print('Instrument installed options: {}'.format(",".join(self.tool.instrument_options)))

    
    def set_horizontal(self, scale, position=0, reference=8.33):
        self.tool.write_str("TIM:SCAL {}".format(scale))
        self.tool.write_str("TIM:POS {}".format(position))
        self.tool.write_str("TIM:REF {}".format(reference))

    #Suggested points for digital 20e6
    def set_acquisition(self, points):
        self.tool.write_str("ACQ:POIN:VAL {}".format(points))

    def set_digital_analyzer(self, pods=1, VDDIO=1.8, hysteresis="MED"):
        for i in range(1,pods+1):
            self.tool.write_str("LOG{}:STAT ON".format(i))
            self.tool.write_str("LOG{}:THR USER".format(i))
            self.tool.write_str("LOG{}:HYST {}".format(i, hysteresis))
        for i in range(1,pods*8+1):
            self.tool.write_str("DIG{}:THR {}".format(i, VDDIO/2))



    def set_trigger(self, source, mode="AUTO", _type="EDGE", slope="POS"):
        self.tool.write_str("TRIG:A:MODE {}".format(mode))
        self.tool.write_str("TRIG:A:SOUR {}".format(source))
        self.tool.write_str("TRIG:A:TYPE {}".format(_type))
        self.tool.write_str("TRIG:A:EDGE:SLOP {}".format(slope))

    """
    slope1 and slop2 can be either "POS" or "NEG"
    """
    def get_delay(self, signal_source1, slope1, signal_source2, slope2, place=0):
        raise NotImplementedError
        #TODO set orizontal!
        self.tool.write_str('MEAS{place}:SOUR {source1}, {source2}'.format(place=place, source1=signal_source1, source2=signal_source2))
        self.tool.write_str('MEAS{place}:DEL:SLOP {slope1}, {slope2}'.format(place=place, slope1=slope1, slope2=slope2))
        #TODO add readout function

    def edge_count(self, source, period, t_frame=0, rising=1, place=1):

        #SETUP
        self.tool.write_str("MEAS{} ON".format(place))

        if t_frame:
            scale = period*t_frame/12
        else: #default
            scale = period/2*20e6/12 #MAX, Nyquist theroem
        self.set_acquisition(20e6)
        self.set_horizontal(scale)
        self.set_digital_analyzer()
        self.set_trigger("D6")
        if rising:
            CMD = "REC"
        else:
            CMD = "FEC"
        
        self.tool.write_str('MEAS{place}:SOUR {source}'.format(place=place, source=source))
        #RUN
        #self.tool.write_str('MEAS:MAIN {}'.format(CMD)) #
        measure = self.tool.query_int('MEAS{}:RES? {}'.format(place,CMD))
        return scale*12, measure

    def get_logic_waveform(self, channels, period, wav_data_poin_str='DMAX'):
        """
        Read waveform data
        Note: data_read_speed: ASC < REAL < INT
        """
        scale = period/12
        self.set_horizontal(scale)
        self.set_acquisition(20e6)
        self.set_digital_analyzer()
        self.set_trigger("D6")

        channel_list = channels if type(channels)==list else [channels]
        #self.instr.write_str_with_opc("SINGle")    # SINGLE should be handled by user before invoking this function
        # defines the format for data export. Valid settings for RTB2000:
        #   ASCii, REAL 32, UINT 8|16|32
        #self.tool.write_str('FORM UINT, 8')
        # set nr of waveform points to transfer. For RTB2000:
        #   DEFault: visible points on screen
        #   MAX: all points stored in mem; only available when acquisition is stopped
        #   DMAX: all stored points, but only those for the displayed time range
        data_dic = {}
        for c in channel_list:
            self.tool.write_str('DIG{:d}:DATA:POIN {:s}'.format(c,wav_data_poin_str))
            # Actual data transfer
            #   temp change the visa_timeout to accomodate large waveforms
            nr_points = int(self.tool.query_str('DIG{:d}:DATA:POIN?'.format(c)))
            nr_points_MSa_ceil = (nr_points//1e6) + 1
            vt = self.tool.visa_timeout
            self.tool.visa_timeout = 3000*nr_points_MSa_ceil
            data_dic["d{}".format(c)] = self.tool.query_bin_or_ascii_int_list('FORM ASC,0; DIG{:d}:DATA?'.format(c))
            self.tool.visa_timeout = vt
            # Also read waveform header
            data_dic["dh{}".format(c)] = self.tool.query_bin_or_ascii_float_list('FORM REAL,32; DIG{:d}:DATA:HEAD?'.format(c)) 
            print('Finished transferring waveform channel{:d}, nr_wav_points:{:.2f}MSa'.format(c,nr_points/1e6))

        return data_dic