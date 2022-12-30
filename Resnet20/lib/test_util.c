uint32_t* pad_out = (uint32_t*)0x1a10100c;
uint32_t* pad_in  = (uint32_t*)0x1a101008;

static inline void init_gpio(){
    int i;
    for(i = 0; i < 32; i = i + 1) {
        rt_pad_set_function(i, 1);
        rt_gpio_init(0, i);
        rt_gpio_set_dir(0, 1 << i, RT_GPIO_IS_OUT);
    }
    rt_gpio_set_dir(0, 1 << 24, RT_GPIO_IS_IN);
    int j = 0;
    while (j < 25000) {
        j++;
    }
}


static inline void send_instruction(uint8_t e2r_r2e_n, uint16_t address, uint16_t number_transactions){
    int i;
    for(i = 0; i < 16; i = i + 1) {
        rt_gpio_set_dir(0, 1 << i, RT_GPIO_IS_OUT); //set 16 GPIO out
    }

    ////////////////////////////WAIT A BIT///////////////////////////
    int j = 0;
    while (j < 25000) {
        j++;
    }
    ////////////////////////////////////////////////////////////////

    uint32_t address_instruction = (uint32_t) address << 1 | e2r_r2e_n;     
    address_instruction = (uint32_t) 1 << 25 | address_instruction;         //25th bit has to be 1
    
    *pad_out = (uint32_t) 1 << 25 | address_instruction;
    while((uint32_t)(*pad_in & 0x01000000) >> 24 == 0){
        j++;
    }
    
    *pad_out = (uint32_t) 0 << 25;
    while((uint32_t)(*pad_in & 0x01000000) >> 24 == 1){
        j++;
    }

    *pad_out = (uint32_t) 1 << 25 | number_transactions;
    while((uint32_t)(*pad_in & 0x01000000) >> 24 == 0){
        j++;
    }
    *pad_out = (uint32_t) 0 << 25;
    while((uint32_t)(*pad_in & 0x01000000) >> 24 == 1){
        j++;
    }
}

static inline void send_data(uint32_t* l2_address, uint16_t ext_address, uint16_t number_transactions){
    int i;
    uint16_t num_trans;
    init_gpio();
    num_trans = number_transactions*2;
    send_instruction(0, ext_address, num_trans);
    for(i = 0; i < 16; i = i + 1) {
        rt_gpio_set_dir(0, 1 << i, RT_GPIO_IS_OUT);
    }
    int j = 0;
    while (j < 25000) {
        j++;
    }
    for (i = 0; i < num_trans; i = i + 1) {
        if (i%2 == 0){
           *pad_out = (uint32_t) (1 << 25) | (0x0000ffff & (*(l2_address) >> 16));
            while((uint32_t)(*pad_in & 0x01000000) >> 24 == 0){
                //rt_event_yield(NULL);
                j++;
            }
            *pad_out = (uint32_t) (0 << 25);
             while((uint32_t)(*pad_in & 0x01000000) >> 24 == 1){
              //rt_event_yield(NULL);
              j++;
            }
        } else {
            *pad_out = (uint32_t) (1 << 25) | (0x0000ffff & *l2_address) ;
            while((uint32_t)(*pad_in & 0x01000000) >> 24 == 0){
                //rt_event_yield(NULL);
                j++;
            }
            *pad_out = (uint32_t) (0 << 25);
            while((uint32_t)(*pad_in & 0x01000000) >> 24 == 1){
              //rt_event_yield(NULL);
              j++;
            }
            l2_address += 1;
        }
    }
    *pad_out = 0;
}


static void receive_data(uint32_t* l2_address, uint16_t ext_address, uint16_t number_transactions){
    int i;
    init_gpio();
    send_instruction(1, ext_address, number_transactions);
    for(i = 0; i < 16; i = i + 1) {
        rt_gpio_set_dir(0, 1 << i, RT_GPIO_IS_IN);
    }
    int j = 0;
    while (j < 2500){
        j++;
    }
    j = 0;
    uint32_t rx_data;
    uint32_t tmp_rx_data = 0;
    uint32_t trans_index = 0;
    uint32_t ext_ack = 1;

    while(trans_index < number_transactions){
        *pad_out = (uint32_t) 1<<25;
        while((*pad_in & 0x01000000) >> 24 == 0){
            j++;
        }
        rx_data = *pad_in;
        if (trans_index%2 == 0){
            tmp_rx_data = rx_data << 16;
        } else {
            tmp_rx_data = tmp_rx_data | (0x0000ffff & rx_data);
            *l2_address = tmp_rx_data;
            l2_address += 1;
        }
        *pad_out = (uint32_t) 0<<25;

        while((*pad_in & 0x01000000) >> 24 == 1){
            j++;
        }
        trans_index += 1;
    }
}

static inline void init_boot_gpio(){
    //INIT GPIO
    int i,j;
    for(i = 0; i < 32; i = i + 1) {
        rt_pad_set_function(i, 1);
        rt_gpio_init(0, i);
        if (i==18)
            rt_gpio_set_dir(0, 1 << i, RT_GPIO_IS_IN);
        else
            rt_gpio_set_dir(0, 1 << i, RT_GPIO_IS_OUT);
    }
    //WAIT
    j=0;
    while (j < 25000) {
        j++;
    }
}

static inline void set_pin(int pin){
    uint32_t pval = 0;
    pval = *pad_out;
    *pad_out = (uint32_t) 1 << pin | pval;
}

static inline void reset_pin(int pin){
    uint32_t pval = 0;
    pval = *pad_out;
    *pad_out = (uint32_t) ~(1 << pin) & pval;
}

static inline void wait_pin(int pin, int pol){
    int j=0;
    int mask = 1 << pin;
    while((uint32_t)(*pad_in & mask) >> pin == pol){
        j++;
    }
}