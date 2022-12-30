#include "ips_util.h"
#include "test_util.h"
#include "boot_data.h"

void boot_diana( unsigned int* abort_address){

  //----------------SIZING THE .H DATA--------------------------------
  volatile int size_array_cr_ania=sizeof(cra_boot)/sizeof(cra_boot[0]);
  volatile int size_array_im_ania=sizeof(ima_boot)/sizeof(ima_boot[0]); 
  
  //-----------ASSIGN SPACE IN MEMORY STARTING FROM ABORT ADDRESS-----
  uint32_t *cr_ania = (uint32_t *) abort_address;
  uint32_t *im_ania = (uint32_t *) (cr_ania     + size_array_cr_ania);

  //----------MOVING DATA TO PUBLIC L2 BANKS-------------------------
  if(get_core_id() == 0) {
    for(int i=0; i<size_array_cr_ania; i++) {
      ((uint32_t *) cr_ania)[i] = cra_boot[i];
    }
    for(int i=0; i<size_array_im_ania; i++) {
      ((uint32_t *) im_ania)[i] = ima_boot[i];
    }
  }

  //----------BOOT PROCEDURE------------------------
  init_boot_gpio();
  set_pin(17);
  kickoff_ana( cr_ania, size_array_cr_ania, im_ania, 2, 0, 0); //kick off analog core
  global_sync();
  reset_pin(17);
  wait_pin(18,0);
}