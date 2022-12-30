#include "test_util.h"

void memcpy_to_L1_dig(
                        unsigned int* L2_Addr_Byte,
                        unsigned int L1_Addr_16Byte,
                        unsigned int Lenth_4Byte,
                        unsigned int BankNum
                        ){
    /* memcpy write (DIGITAL)*/
    if (BankNum==1){
        hwme_memcpy_op((unsigned int) 2);
        hwme_memcpy_addr_set(L2_Addr_Byte);
        hwme_l1addr_set(L1_Addr_16Byte); // absolute address of L1 (128b / address)
        hwme_memcpy_n_set(Lenth_4Byte);
    }
    else {
        hwme_memcpy_op((unsigned int) 4);
        hwme_memcpy_addr_set(L2_Addr_Byte);
        hwme_l1addr_set(L1_Addr_16Byte); // absolute address of L1 (128b / address)
        hwme_memcpy_bank_length_set(BankNum); // number of bank
        unsigned int row_size;
        row_size = 4*Lenth_4Byte/(BankNum*16);
        hwme_memcpy_row_length_set(row_size);
    }
    // start HWME operation
    hwme_trigger_job();

}

void memcpy_to_L2_dig(
                        unsigned int* L2_Addr_Byte,
                        unsigned int L1_Addr_16Byte,
                        unsigned int Lenth_4Byte,
                        unsigned int BankNum
                        ){
    /* memcpy READ (DIGITAL)*/
    if (BankNum == 1){
        hwme_memcpy_op((unsigned int) 1);
        hwme_memcpy_addr_set(L2_Addr_Byte);
        hwme_l1addr_set(L1_Addr_16Byte); // absolute address of L1 (128b / address)
        hwme_memcpy_n_set(Lenth_4Byte);
    }
    else{
        hwme_memcpy_op((unsigned int) 3);
        hwme_memcpy_addr_set(L2_Addr_Byte);
        hwme_l1addr_set(L1_Addr_16Byte); // absolute address of L1 (128b / address)
        hwme_memcpy_bank_length_set(BankNum); // number of bank
        unsigned int row_size;
        row_size = 4*Lenth_4Byte/(BankNum*16);
        hwme_memcpy_row_length_set(row_size); // number of row (128b)
    }
    hwme_trigger_job();
}

void memcpy_to_L1_ana(
                        unsigned int* L2_Addr_Byte,
                        unsigned int L1_Addr_16Byte,
                        unsigned int Lenth_4Byte,
                        unsigned int BankNum
                        ){
    /* memcpy WRITE (ANALOG)*/
    if (BankNum == 1){
        hwme_ana_memcpy_op((unsigned int) 2);
        hwme_ana_memcpy_addr_set(L2_Addr_Byte);
        hwme_ana_l1addr_set(L1_Addr_16Byte); // absolute address of L1 (128b / address)
        hwme_ana_memcpy_n_set(Lenth_4Byte);
    }
    else{
        hwme_ana_memcpy_op((unsigned int) 4);
        hwme_ana_memcpy_addr_set(L2_Addr_Byte);
        hwme_ana_l1addr_set(L1_Addr_16Byte); // absolute address of L1 (128b / address)
        hwme_ana_memcpy_bank_length_set(BankNum); // number of bank
        unsigned int row_size;
        row_size = 4*Lenth_4Byte/(BankNum*16);

        hwme_ana_memcpy_row_length_set(row_size); // number of row (128b)
    }
    hwme_ana_trigger_job();
}

void memcpy_to_L2_ana(
                        unsigned int* L2_Addr_Byte,
                        unsigned int L1_Addr_16Byte,
                        unsigned int Lenth_4Byte,
                        unsigned int BankNum
                        ){
    /* memcpy READ (ANALOG)*/
    if (BankNum == 1){
        hwme_ana_memcpy_op((unsigned int) 1);
        hwme_ana_memcpy_addr_set(L2_Addr_Byte);
        hwme_ana_l1addr_set(L1_Addr_16Byte); // absolute address of L1 (128b / address)
        hwme_ana_memcpy_n_set(Lenth_4Byte);
    }
    else{
        hwme_ana_memcpy_op((unsigned int) 3);
        hwme_ana_memcpy_addr_set(L2_Addr_Byte);
        hwme_ana_l1addr_set(L1_Addr_16Byte); // absolute address of L1 (128b / address)
        hwme_ana_memcpy_bank_length_set(BankNum); // number of bank
        unsigned int row_size;
        row_size = 4*Lenth_4Byte/(BankNum*16);
        hwme_ana_memcpy_row_length_set(row_size); // number of row (128b)
    }
    hwme_ana_trigger_job();
}

void global_sync(){
    while (hwme_ana_get_status() != 0);
}

void kickoff_dig(
                        unsigned int* crf_adr,
                        unsigned int crf_size,
                        unsigned int* im_adr,
                        unsigned int im_num,
                        unsigned int* wt_conv_adr,
                        unsigned int wt_conv_size                     
                        ){
    hwme_memcpy_op((unsigned int) 0);
    // set up addresses
    hwme_conf_addr_set(crf_adr);
    hwme_conf_n_set(crf_size);
    hwme_im_addr_set(im_adr);
    unsigned int imSizeIn32Bit;
    imSizeIn32Bit = im_num*32;
    hwme_im_n_set(imSizeIn32Bit);
    hwme_wt_conv_addr_set(wt_conv_adr);
    hwme_wt_conv_n_set(wt_conv_size);
    hwme_act_n_set(0);
    hwme_nb_tile_set(0);
    hwme_trigger_job();
}

void kickoff_ana(
                        unsigned int* crf_adr,
                        unsigned int crf_size,
                        unsigned int* im_adr,
                        unsigned int im_num,
                        unsigned int* wt_conv_adr,
                        unsigned int* wt_bn_adr                    
                        ){
    hwme_ana_memcpy_op((unsigned int) 0);
    // set up addresses
    hwme_ana_conf_addr_set(crf_adr);
    hwme_ana_conf_n_set(crf_size);
    hwme_ana_im_addr_set( im_adr);
    unsigned int imSizeIn32Bit;
    imSizeIn32Bit = im_num*16;
    hwme_ana_im_n_set(imSizeIn32Bit);
    hwme_ana_wt_addr_set(wt_conv_adr);
    hwme_ana_simd_addr_set(wt_bn_adr);
    hwme_ana_act_n_set(0);
    hwme_ana_nb_tile_set(0);
    hwme_ana_trigger_job();
}