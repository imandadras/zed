import math

"""
NAME
    h_gen
DESCRIPTION
    data header files generation toolkit
    It can be used for any data file
FILE CONTENTS
    _hex32
    gen_hdata_file
    gen_signed_hdata_file
COPYRIGHT
    author= Giuseppe Sarda
    data=   01 XII 2021
    email=  sarda74@imec.be
"""

header_32_line="__attribute__((aligned(16))) uint32_t {}[] =" #need +'{\n'
footer_line="};\n"


def _hex32( x, l, ox=False):
    """_hex32( x, l, ox=False)

        Converts an integer into its corrispondent exadecimal string
        Parameters:
        x           (int): integer value to be converted
        l           (int): bit lenght of the number (32 --> 32//4 hex digits)
        ox          (bool): option to add "0x" in front of the string

        Returns:
        _           (string): exadecimal string corresponding to x
    """
    ln=2**(l+1)-1
    if ox:
        return "0x%s"%("00000000%x"%(x & ln))[(-(l//4)):]
    else:
        return "%s"%("00000000%x"%(x & ln))[(-(l//4)):]

def gen_hdata_file(f_name, sdata, out_par, in_par, data_name,endian="little"):
    """gen_hdata_file(f_name, sdata, out_par, in_par, data_name)
        Generates 
        Parameters:
        f_name      (string): .../path/name of the output file
        sdata       (list)  : list of integers (UNSIGNED!) to be exported in the h file
        out_par     (int)   : single output data parallelism
        in_par      (int)   : single input data parallelism
        data_name   (string): name of the data array to be added to header file

        Returns:
        None
    """
    word_count= out_par//in_par
    with open(f_name,"w") as fout_p:
        fout_p.write(header_32_line.format(data_name)+"{\n")
    mega_string=""
    cycles = math.ceil(len(sdata)/word_count)
    for b in range(cycles):
        num = 0
        for c in range(word_count):
            if endian=="little":
                num += 2**(in_par*c)*sdata[b*word_count+c]
            elif endian=="big":
                num += 2**(in_par*(word_count-1-c))*sdata[b*word_count+c]
        mega_string += (hex(num)+",\n")
    with open(f_name,"a") as fout_p:
        fout_p.write(mega_string)
        fout_p.write(footer_line)


#Doesn't work with in_par<4
def gen_signed_hdata_file(f_name, sdata, out_par, in_par, data_name):
    """gen_signed_hdata_file(f_name, sdata, out_par, in_par, data_name)
        Parameters:
        f_name      (string): ___
        sdata       (int)   : list of integers (SIGNED!) to be exported in the h file
        out_par     (int): ___
        in_par      (int): ___
        data_name   (string): ___

        Returns:
        None:___
    """
    word_count= out_par//in_par
    with open(f_name,"w") as fout_p:
        fout_p.write(header_32_line.format(data_name)+"{\n")
        cycles = math.ceil(len(sdata)/word_count)
        for b in range(cycles):
            num = ""
            for c in range(word_count):
                num = _hex32(sdata[b*word_count+c], in_par) + num
            num = "0x" + num
            if b==cycles:
                fout_p.write(num+"\n")
            else:
                fout_p.write(num+",\n")
        fout_p.write(footer_line)