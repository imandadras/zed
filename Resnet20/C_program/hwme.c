#include "pulp.h"
#include <stdint.h>
#include <math.h>
#include "archi/hwme/hwme_v1.h"
#include "hal/hwme/hwme_v1.h"

#include "test_util.h"
#include "ips_util.h"
#include "data.h"
#include "boot_diana.h"
#include "gdb_anchor.h"
#define ABORT_ADDRESS 0x1c02c000 //to be checkd in disassembly file
#define RES_ADDRESS   4096 //4096

int main() {

  plp_hwme_enable();  //ENABLE RISC-V TO ACCELERATORS INTERACTION THROUGH INTERRUPT
  boot_diana((unsigned int*) ABORT_ADDRESS); //BOOT PROCEDURE
//-----------SIZE OF .H FILE DATA----------------------------------
  volatile int size_array_crf_ania=sizeof(cr_ania)/sizeof(cr_ania[0]);
  volatile int size_array_im_ania=sizeof(im_ania)/sizeof(im_ania[0]); 
  volatile int size_array_w_ania=sizeof(w_cnn_ania)/sizeof(w_cnn_ania[0]);
  volatile int size_array_bn_ania=sizeof(bn_cnn_ania)/sizeof(bn_cnn_ania[0]);
  volatile int size_array_act_ania=sizeof(input_ania)/sizeof(input_ania[0]);
  volatile int size_array_res_ania=4096;//4096 --> 32*32*16/4 (4=byte of int)

//-----------ASSIGN SPACE IN MEMORY STARTING FROM ABORT ADDRESS----
  uint32_t *crf_ania = (uint32_t *) ABORT_ADDRESS;
  uint32_t *ims_ania = (uint32_t *) (crf_ania + size_array_crf_ania);
  uint32_t *wt_bn_ania = (uint32_t *) (ims_ania+size_array_im_ania); 
  uint32_t *wt_conv_ania = (uint32_t *) (wt_bn_ania+size_array_bn_ania); 
  uint32_t *act = (uint32_t *) (wt_conv_ania+size_array_w_ania);
  uint32_t *res = (uint32_t *) (act+size_array_act_ania);

//----------MOVING DATA TO PUBLIC L2 BANKS-------------------------
  if(get_core_id() == 0) {
    for(int i=0; i<size_array_crf_ania; i++) {
      ((uint32_t *) crf_ania)[i] = cr_ania[i];
    }
    for(int i=0; i<size_array_im_ania; i++) {
      ((uint32_t *) ims_ania)[i] = im_ania[i];
    }
    for(int i=0; i<size_array_w_ania; i++) {
      ((uint32_t *) wt_conv_ania)[i] = (signed int)w_cnn_ania[i];
    }
    for(int i=0; i<size_array_bn_ania; i++) {
      ((uint32_t *) wt_bn_ania)[i] = bn_cnn_ania[i];
    }
    for(int i=0; i<size_array_act_ania; i++) {
      ((uint32_t *) act)[i] = (signed int)input_ania[i];
    }
  }
  
  memcpy_to_L1_ana( (unsigned int*) act, 0, (unsigned int) size_array_act_ania, 4); //COPY INPUT TO L1, BankNum=C/16
  global_sync();
  I_LOOP = 10;
  for(int i=0; i<I_LOOP; i++){
    ims_ania[10] = 0x100ffff+i*0x10000;
    kickoff_ana((unsigned int) crf_ania,
                size_array_crf_ania,
                ims_ania,
                2,
                wt_conv_ania,
                wt_bn_ania
              );
    global_sync();

  //-------COPY BACK RESULTS TO MEMORY-------------------------------
    memcpy_to_L2_ana( (unsigned int*) res, RES_ADDRESS, (unsigned int) size_array_res_ania, 1);
    global_sync();

    gdb_anchor();
    //--send_data((uint32_t*) res, 0,  size_array_res_ania);
  }
//-------END PROCEDURE---------------------------------------------
  plp_hwme_disable();
  printf("Workload Done.\n");
  synch_barrier();
  
  return 0;
}