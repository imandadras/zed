export PULP_RISCV_GCC_TOOLCHAIN=/home/imandadras/v1.0.16-pulp-riscv-gcc-ubuntu-18/
export PULP_SDK_ROOT=/mnt/c/zedboard/diana
export DIANA_RISCV_SRC=$(pwd)

cd /mnt/c/zedboard/diana/pulp-sdk-diana/pkg/sdk/dev/
source ./sourceme.sh
source ./configs/pulpissimo.sh
source ./configs/platform-rtl.sh
cd $DIANA_RISCV_SRC