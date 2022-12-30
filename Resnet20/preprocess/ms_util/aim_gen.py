import yaml
from c_util.h_gen import gen_hdata_file

"""
NAME
    aim_gen
DESCRIPTION
    RF memory generation toolkit
    It can be used for configuration registers, instruction memory, etc.
FILE CONTENTS
    get_reg_val
    gen_reg_list
    _main (usage example)
COPYRIGHT
    author= Giuseppe Sarda
    data=   29 XI 2021
    email=  sarda74@imec.be
"""

def get_reg_val(reg, ima_db):
    """
    get_reg_val(reg, ima_db)
        Generates the value of a single register (multiple fields), in the instruction memory
        INPUT PARAMS
        reg (dict): Template dictionary of a register with fields as key and value a list of values
            E.g.)
            OX_UNROLL      : <-- Name of the field
                - 4          <-- First value bit-width of the fiels
                - 1          <-- Second value (optional) default value if different than 0
            RES_WORD_SIZE  : <-- Name of the field
              - 4
            RESERVED       : <-- Name of the field
              - 8
        ima_db (dict): Dictionary of ALL the user specified field of a given instruction
            E.g.)
            OX_UNROLL       : 4
            RES_WORD_SIZE   : 2
        RETURN
        v_t (int): Value of the register
            E.g. with previous value
            v_t=0x14 (20) 
    """
    ima_k = ima_db.keys()
    reg_db = list(reg.values())[0]
    reg_k = reg_db.keys()
    v_t=0
    v_b=0
    for k in reg_k:
        if k in ima_k:          # case user specifies the value 
            v = ima_db[k]
        elif len(reg_db[k])==2: # case template specifies a default value(!=0)
            v = reg_db[k][1]
        else:                   # default 0 value
            v = 0
        v_t += v*2**v_b
        v_b += reg_db[k][0]
    return v_t

def gen_reg_list(ima, template):
    """
    gen_reg_list(ima, template)
        Generates the list of values of every register (32) of the instruction memory of analog core
        INPUT PARAMS
        ima (string, list): User specified .yaml file with all the fields which are meant to over-ride default values
            E.g. ima_ex.yaml-->
            OX_UNROLL       : 4
            RES_WORD_SIZE   : 2
        template (string): .yaml file with the instruction template
            E.g. ana_instr_template.yaml
            ...
            OX_UNROLL      : <-- Name of the field
                - 4          <-- First value bit-width of the fiels
                - 1          <-- Second value (optional) default value if different than 0
            RES_WORD_SIZE  : <-- Name of the field
              - 4
            RESERVED       : <-- Name of the field
              - 8
            ...
        RETURN
        ima_list (list): List of integers value representing each register
    """
    with open(template,"r") as stream:
        templ = yaml.load( stream, Loader=yaml.CLoader)
    if isinstance(ima, str):
        try:
            with open(ima,"r") as stream:
                ima_db = yaml.load( stream, Loader=yaml.CLoader)
        except FileNotFoundError:
            print("File {} not found. A dummy file will be generated!".format(ima))
            ima_db = [{"DUMMY0" : {"DUMMYFIELD" : None}}]
    elif isinstance(ima, list):
        ima_db = ima
    ima_list = []
    for i in ima_db:
        for reg in templ:
            ima_list.append(get_reg_val(reg,list(i.values())[0])) #list will have only one value
    return ima_list

def gen_row_block_instruction(ima, start_b, range_b,i_index, in_channels=64):
    print("The instruction will be modified for row block experiment")
    c = in_channels*range_b
    ima.set_field(i_index, "IN_CHANNEL", c)
    ima.set_field(i_index, "OUT_CHANNEL", 512)
    ima.set_field(i_index, "USE_BLK_COL", 0xffff)
    ima.set_field(i_index, "KERNEL_X", 1)
    ima.set_field(i_index, "KERNEL_Y", 1)
    ima.set_field(i_index, "PROCESSING_BLOCK", range_b)
    start_b = 15 if start_b>15 else start_b
    ima.set_field(i_index, "BUF_OFFSET", start_b)
    

if __name__ == '__main__':
    def _main():
        a = gen_reg_list( "input/ft_im.yaml", "mdata/ana_instr_template.yaml")
        gen_hdata_file("../functional_test/instruction_memory_ania.h", a, 32, 16, "im_ania")
    _main()