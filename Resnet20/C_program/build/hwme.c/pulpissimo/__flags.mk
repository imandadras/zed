PULP_LDFLAGS      += 
PULP_CFLAGS       += 
PULP_FC_ARCH_CFLAGS ?=  -march=rv32imfcxpulpv2 -mfdiv -D__riscv__
PULP_FC_CFLAGS    += -fdata-sections -ffunction-sections -I/mnt/c/zedboard/diana/pulp-sdk-diana/pkg/sdk/dev/install/include/io -I/mnt/c/zedboard/diana/pulp-sdk-diana/pkg/sdk/dev/install/include -include /mnt/c/zedboard/Resnet20/C_program/build/hwme.c/pulpissimo/fc_config.h
PULP_FC_OMP_CFLAGS    += -fopenmp -mnativeomp
ifdef PULP_RISCV_GCC_TOOLCHAIN
PULP_FC_CC = $(PULP_RISCV_GCC_TOOLCHAIN)/bin/riscv32-unknown-elf-gcc 
PULP_CC = $(PULP_RISCV_GCC_TOOLCHAIN)/bin/riscv32-unknown-elf-gcc 
PULP_AR ?= $(PULP_RISCV_GCC_TOOLCHAIN)/bin/riscv32-unknown-elf-ar
PULP_LD ?= $(PULP_RISCV_GCC_TOOLCHAIN)/bin/riscv32-unknown-elf-gcc
PULP_FC_OBJDUMP ?= $(PULP_RISCV_GCC_TOOLCHAIN)/bin/riscv32-unknown-elf-objdump
PULP_OBJDUMP ?= $(PULP_RISCV_GCC_TOOLCHAIN)/bin/riscv32-unknown-elf-objdump
else
PULP_FC_CC = $(PULP_RISCV_GCC_TOOLCHAIN_CI)/bin/riscv32-unknown-elf-gcc 
PULP_CC = $(PULP_RISCV_GCC_TOOLCHAIN_CI)/bin/riscv32-unknown-elf-gcc 
PULP_AR ?= $(PULP_RISCV_GCC_TOOLCHAIN_CI)/bin/riscv32-unknown-elf-ar
PULP_LD ?= $(PULP_RISCV_GCC_TOOLCHAIN_CI)/bin/riscv32-unknown-elf-gcc
PULP_FC_OBJDUMP ?= $(PULP_RISCV_GCC_TOOLCHAIN_CI)/bin/riscv32-unknown-elf-objdump
PULP_OBJDUMP ?= $(PULP_RISCV_GCC_TOOLCHAIN_CI)/bin/riscv32-unknown-elf-objdump
endif
PULP_ARCH_FC_OBJDFLAGS ?= -Mmarch=rv32imfcxpulpv2
PULP_ARCH_OBJDFLAGS ?= -Mmarch=rv32imfcxpulpv2
PULP_ARCH_LDFLAGS ?=  -march=rv32imfcxpulpv2 -mfdiv -D__riscv__
PULP_LDFLAGS_hwme = -nostartfiles -nostdlib -Wl,--gc-sections -L/mnt/c/zedboard/diana/pulp-sdk-diana/pkg/sdk/dev/install/rules -Tpulpissimo/link.ld -L/mnt/c/zedboard/diana/pulp-sdk-diana/pkg/sdk/dev/install/lib/pulpissimo -L/mnt/c/zedboard/diana/pulp-sdk-diana/pkg/sdk/dev/install/lib/pulpissimo/pulpissimo -lrt -lrtio -lrt -lgcc
PULP_OMP_LDFLAGS_hwme = -lomp
pulpRunOpt        += --dir=/mnt/c/zedboard/Resnet20/C_program/build/hwme.c/pulpissimo --binary=hwme/hwme
