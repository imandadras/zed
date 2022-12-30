#ifndef __TEST_UTILS_H__
#define __TEST_UTILS_H__

#include "test_util.c"

static inline void init_gpio();
static inline void send_instruction(uint8_t e2r_r2e_n, uint16_t address, uint16_t number_transactions);
static inline void send_data(uint32_t* l2_address, uint16_t ext_address, uint16_t number_transactions);
static void receive_data(uint32_t* l2_address, uint16_t ext_address, uint16_t number_transactions);
static inline void init_boot_gpio();
static inline void set_pin(int pin);
static inline void reset_pin(int pin);
static inline void wait_pin(int pin, int pol);

#endif