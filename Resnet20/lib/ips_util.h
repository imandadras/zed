#ifndef IPS_UTIL_H
#define IPS_UTIL_H

#include "ips_util.c"

void memcpy_to_L1_dig(unsigned int* L2_Addr_Byte, unsigned int L1_Addr_16Byte, unsigned int Lenth_4Byte, unsigned int BankNum);
void memcpy_to_L2_dig(unsigned int* L2_Addr_Byte, unsigned int L1_Addr_16Byte, unsigned int Lenth_4Byte, unsigned int BankNum);
void memcpy_to_L1_ana(unsigned int* L2_Addr_Byte, unsigned int L1_Addr_16Byte, unsigned int Lenth_4Byte, unsigned int BankNum);
void memcpy_to_L2_ana(unsigned int* L2_Addr_Byte, unsigned int L1_Addr_16Byte, unsigned int Lenth_4Byte, unsigned int BankNum);
void global_sync();
void kickoff_dig(unsigned int* crf_adr, unsigned int crf_size, unsigned int* im_adr, unsigned int im_num, unsigned int* wt_conv_adr, unsigned int wt_conv_size);
void kickoff_ana(unsigned int* crf_adr, unsigned int crf_size, unsigned int* im_adr, unsigned int im_num, unsigned int* wt_conv_adr, unsigned int* wt_bn_adr);

#endif