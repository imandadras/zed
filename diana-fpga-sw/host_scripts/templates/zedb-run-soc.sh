source ~/env/bin/activate
SCRIPT_NAME="run-diana-soc.py"
SCRIPT_ARGS=""
cd diana-fpga-sw
python3 -u $SCRIPT_NAME $SCRIPT_ARGS &> log2.txt
#python3 $SCRIPT_NAME &> log2.txt
