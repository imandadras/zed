import argparse
import os

class FPGAScriptParserClass():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Gets options from command line.')
        self._init_parser()
        self.args = self.parser.parse_args()
        self.tx_link = False
        self.rx_link = False 
        self._check_args()
        self._reduce_args()

    def _init_parser(self):
        self.parser.add_argument("-p","--dump_path", action="store", type=str, help="Path where to dump measurement results")
        self.parser.add_argument("-c","--fll_clk", action="store", type=int, help="Fll clock to be set in MHz. Min 70, Max 350. Default 260MHz")
        self.parser.add_argument("-rp","--rx_packet_size", action="store", type=int, help="Packet size (# of 32b words) of every receiving iteration")
        self.parser.add_argument("--rx_packet_num", action="store", type=int, help="Number of packets per experiment. Must be equal to loop cycles in C code")
        self._set_defaults()

    def _set_defaults(self):
        self.parser.set_defaults(dump_path=None)
        self.parser.set_defaults(fll_clk=260)
        self.parser.set_defaults(rx_packet_num=1)

    def _reduce_args(self):
        if self.args.dump_path:
            self.rx_link = True

    def _check_args(self):
        if self.args.dump_path:
            if not os.path.isdir(self.args.dump_path): #checks the directory
                print("ERROR. Dump path not found!")
                raise ValueError
        if not ( 70 <= self.args.fll_clk <= 350):
            print("ERROR. FLL frequency out of range!")
            raise ValueError
