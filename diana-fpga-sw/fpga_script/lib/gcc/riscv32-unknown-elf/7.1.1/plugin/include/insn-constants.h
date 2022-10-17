/* Generated automatically by the program `genconstants'
   from the machine description file `md'.  */

#ifndef GCC_INSN_CONSTANTS_H
#define GCC_INSN_CONSTANTS_H

#define REG_LS0 70
#define REG_LS1 71
#define S0_REGNUM 8
#define REG_LE1 69
#define T0_REGNUM 5
#define S1_REGNUM 9
#define T1_REGNUM 6
#define RETURN_ADDR_REGNUM 1
#define REG_LE0 68
#define S2_REGNUM 18
#define REG_LC0 66
#define REG_LC1 67
#define VIT_REG 72

enum unspec_nn {
  UNSPEC_NN_VECTOR = 0,
  UNSPEC_NN_SCALAR = 1,
  UNSPEC_NN_QNT = 2
};
#define NUM_UNSPEC_NN_VALUES 3
extern const char *const unspec_nn_strings[];

enum unspec_nn_v2 {
  UNSPEC_MLSDOT_INIT = 0,
  UNSPEC_MLSDOT = 1
};
#define NUM_UNSPEC_NN_V2_VALUES 2
extern const char *const unspec_nn_v2_strings[];

enum unspec {
  UNSPEC_EH_RETURN = 0,
  UNSPEC_ADDRESS_FIRST = 1,
  UNSPEC_PCREL = 2,
  UNSPEC_LOAD_GOT = 3,
  UNSPEC_TLS = 4,
  UNSPEC_TLS_LE = 5,
  UNSPEC_TLS_IE = 6,
  UNSPEC_TLS_GD = 7,
  UNSPEC_AUIPC = 8,
  UNSPEC_FLT_QUIET = 9,
  UNSPEC_FLE_QUIET = 10,
  UNSPEC_COPYSIGN = 11,
  UNSPEC_LRINT = 12,
  UNSPEC_LROUND = 13,
  UNSPEC_TIE = 14,
  UNSPEC_VEC_PERM1 = 15,
  UNSPEC_VEC_PERM2 = 16,
  UNSPEC_VEC_PERM3 = 17,
  UNSPEC_VEC_PERM4 = 18,
  UNSPEC_VEC_PERM5 = 19,
  UNSPEC_VIT_MAX = 20,
  UNSPEC_VIT_SEL = 21,
  UNSPEC_BINS_REG = 22,
  UNSPEC_BEXTS_REG = 23,
  UNSPEC_BEXTU_REG = 24,
  UNSPEC_READSI = 25,
  UNSPEC_WRITESI = 26,
  UNSPEC_SPR_READ = 27,
  UNSPEC_SPR_WRITE = 28,
  UNSPEC_SPR_BIT_SET = 29,
  UNSPEC_SPR_BIT_CLR = 30,
  UNSPEC_FCSR_READ = 31,
  UNSPEC_FCSR_WRITE = 32,
  UNSPEC_NOP = 33,
  UNSPEC_LSETUP_END = 34,
  UNSPEC_ITU = 35,
  UNSPEC_ITS = 36,
  UNSPEC_ITH = 37,
  UNSPEC_ITM = 38,
  UNSPEC_READSI_NONVOL = 39,
  UNSPEC_MULS = 40,
  UNSPEC_MULU = 41,
  UNSPEC_MULSN = 42,
  UNSPEC_MULSRN = 43,
  UNSPEC_MULUN = 44,
  UNSPEC_MULURN = 45,
  UNSPEC_MACS = 46,
  UNSPEC_MACU = 47,
  UNSPEC_MACSN = 48,
  UNSPEC_MACSRN = 49,
  UNSPEC_MACUN = 50,
  UNSPEC_MACURN = 51,
  UNSPEC_TRUNCSIHI = 52,
  UNSPEC_TRUNCSIQI = 53,
  UNSPEC_BITREV = 54,
  UNSPEC_COMPARE_AND_SWAP = 55,
  UNSPEC_SYNC_OLD_OP = 56,
  UNSPEC_SYNC_EXCHANGE = 57,
  UNSPEC_ATOMIC_STORE = 58,
  UNSPEC_MEMORY_BARRIER = 59
};
#define NUM_UNSPEC_VALUES 60
extern const char *const unspec_strings[];

enum unspecv {
  UNSPECV_GPR_SAVE = 0,
  UNSPECV_GPR_RESTORE = 1,
  UNSPECV_FRFLAGS = 2,
  UNSPECV_FSFLAGS = 3,
  UNSPECV_BLOCKAGE = 4,
  UNSPECV_FENCE = 5,
  UNSPECV_FENCE_I = 6,
  UNSPECV_ALLOC = 7,
  UNSPECV_LC_SET = 8,
  UNSPECV_READ_EVU = 9,
  UNSPECV_OFFSETED_READ = 10,
  UNSPECV_OFFSETED_READ_HALF = 11,
  UNSPECV_OFFSETED_READ_BYTE = 12,
  UNSPECV_OFFSETED_READ_OMP = 13,
  UNSPECV_OFFSETED_WRITE = 14,
  UNSPECV_OFFSETED_WRITE_HALF = 15,
  UNSPECV_OFFSETED_WRITE_BYTE = 16,
  UNSPECV_OMP_PULP_BARRIER = 17,
  UNSPECV_OMP_PULP_CRITICAL_START = 18,
  UNSPECV_OMP_PULP_CRITICAL_END = 19,
  UNSPECV_WRITESI_VOL = 20,
  UNSPECV_READSI_VOL = 21,
  UNSPECV_SPR_READ_VOL = 22
};
#define NUM_UNSPECV_VALUES 23
extern const char *const unspecv_strings[];

#endif /* GCC_INSN_CONSTANTS_H */
