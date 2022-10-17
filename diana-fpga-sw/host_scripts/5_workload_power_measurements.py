#!/usr/bin/env python
import  pyvisa
import  time
import  yaml
from    utils.utils import cmd, cd, check_return_zero, current_utctime_string, listdirs, listfiles
import  utils.settings as settings
import  utils.procedures as procedures
from    utils.parser import HostScriptParserClass
from    utils.SCP_RTB2004 import SCP_RTB2004

def change_ut(ima_file, ut):
    with open(ima_file, "r") as f:
        list_doc = yaml.safe_load(f)
        for i in range(len(list_doc)):
            i_name = list(list_doc[i].keys())[0]
            list_doc[i][i_name]["UNIT_TIME"] = ut
    with open(ima_file, "w") as f:
        yaml.dump(list_doc, f)

parser = HostScriptParserClass()

#OPENING PSU
RM = pyvisa.ResourceManager()
PSU_N6705B = RM.open_resource(settings.PSU_N6705B_addr,read_termination='\n')
PSU_E36312A = RM.open_resource(settings.PSU_E36312A_addr,read_termination='\n')
SCOPE_RTB2004 = SCP_RTB2004("SCP_RS", settings.SCP_RTB2004_addr)

#setting up PSU
procedures.set_psu(PSU_N6705B,PSU_E36312A)

#---------experiments----------------------------------//
print("Making parent directory for experiment results...")
RESULT_PARENT_DIR="WL_power_data_" + current_utctime_string(settings.TIME_FORMAT) + "/"
p = cmd("mkdir ../data/{}".format(RESULT_PARENT_DIR))
check_return_zero(p)
print("Starting the loop experiments...")

MAX_TRIALS=2
DEADLOCK=False
EXP_ROOT = settings.DIANA_SDK_PATH + "measurement_inputs/aim/peak_wl_JSSC/"

i=0
for d in listdirs(EXP_ROOT):
    metadataf = d + "/metadata.yaml"
    with open(metadataf) as inp:
        metadata = yaml.safe_load(inp)
    for f in listfiles(d):
        print("Processing {}",format(f))
        if f == metadataf or not ("post_proc_w" in f):
            pass
        else:
            DONE = False
            csbias_V    = metadata["CSBIAS"]
            act_size    = metadata["ACT_SIZE"]
            act_sigma   = metadata["ACT_SIGMA"]
            bn_size     = metadata["BN_PARAM"]
            w_tiles     = metadata["TILES"]
            ut          = metadata["UT"]
            crp         = metadata["CGR_F"]

            params={"UT"        : ut,
                    "CBV"       : csbias_V,
                    "WL"        : f,
                    "I"         : i}
            #add here possible parameter sweep
            PSU_E36312A.write('SOUR:VOLT {}, (@1)'.format(str(csbias_V)))
            print("Generating header data files for the experiment...")
            with cd(settings.DIANA_SDK_PATH + "tests"):
                change_ut(f, ut)
                imp = "/".join(f.split("/")[-3:])
                print(imp)
                p = cmd("""python3 {sdk_script_name}    -p ana_power_meas\
                                                        -imp {imp}\
                                                        -ima\
                                                        -a NOR\
                                                        -as {activation_size}\
                                                        --actv_loc 0\
                                                        --actv_scale {actv_dev}\
                                                        --actv_clip 1\
                                                        --actv_range 7\
                                                        -w RPD\
                                                        --weight_tiles {weight_tiles}
                                                        --weight_nd 30\
                                                        --weight_pd 30\
                                                        -bn RAN\
                                                        --batch_norm_size {bn_size}\ 
                                                        -crp {crp}\
                                                        -cra""".format(     sdk_script_name=parser.args.sdk_script_name,
                                                                            imp=imp,
                                                                            activation_size=act_size,
                                                                            actv_dev=act_sigma,
                                                                            weight_tiles=w_tiles,
                                                                            bn_size=bn_size,
                                                                            crp=crp
                                                                            ), verbose=False, timeout=10*60)
                check_return_zero(p)
            print("Compiling C code...")
            procedures.c_compile(parser)
            print("Running the experiment on chip...")
            dump_path = "../data/" + RESULT_PARENT_DIR
            trials = 0
            while(not DONE):
                if trials:
                    DEADLOCK = True
                trials = 0
                while( (procedures.run_diana_experiment(parser, PSU_N6705B, PSU_E36312A, SCOPE_RTB2004, power_path=dump_path, sync_out=False, dump_path=".", params=params)) and (trials<MAX_TRIALS)):
                    print("Experiment with path {} failed! Trying again {}...".format(dump_path,trials))
                    p = cmd("rm -rf {}/*".format(dump_path))
                    check_return_zero(p)
                    trials+=1
                if(trials==MAX_TRIALS):
                    procedures.reset(PSU_N6705B, PSU_E36312A, parser)
                else:
                    DEADLOCK=False
                    DONE=True
                if DEADLOCK:
                    print("Deadlock in execution of experiment {}. Please recover from here...".format(dump_path))
                    with open("checkpoint.txt","w") as logp:
                        logp.write(dump_path)
                    exit()
            i+=1
            #_ = input("{} press enter after you are done!".format(f))