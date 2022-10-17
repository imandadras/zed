ZED_TARGET=zedb-diana
read -p "Zedboard $ZED_TARGET directory diana-fpga-sw will be flashed. Are you sure? [Y/n]" -n 1 -r

if [[ $REPLY =~ ^[Yy]$ ]]
then
    printf "\nFlashing target...\n"
    ssh $ZED_TARGET 'rm -rf /root/diana-fpga-sw'
    ssh $ZED_TARGET 'mkdir /root/diana-fpga-sw'
    scp -r ../diana-fpga-sw/fpga_script/* $ZED_TARGET:~/diana-fpga-sw/
fi