__attribute__((aligned(16))) uint32_t ima_boot[] = {
    0x3f,
    0x8000000,
    0x0,
    0x400000,
    0x20200,
    0x70002,
    0x20011,
    0x10002,
    0x1,
    0x20050001,
    0x100ffff,
    0xf000,
    0x9000084,
    0x0,
    0x0,
    0x0,
    0x3f,
    0x0,
    0x0,
    0x0,
    0x0,
    0x70000,
    0x0,
    0x10000,
    0x1,
    0x50001,
    0x10a0001,
    0xf001,
    0x84,
    0x0,
    0x0,
    0x0,
};

__attribute__((aligned(16))) uint32_t cra_boot[] = { 
0x1000000,// cfg.end_time[15:8] cfg.unit_time[7:0] //  cfg.use_blockcolumn[0] // 
0x01010001,// cfg.dac_timing[15:8] cfg.nb_dac_bits[7:0] //  cfg.nb_act_bits[7:0]  // 
0x0,// cfg.csbias_mirror[15:8] cfg.csbias_source[7:0] //  cfg.csbias_observe[2] cfg.csbias_force[1] cfg.force_activation[0] // 
0x0,// dbg.pd_col_c[15:0] //  dbg.pd_col_b[11:4] dbg.pd_col_a[3:0] // 
0x0,// dbg.sw_reset[0] //  dbg.col_connect_min[1] dbg.col_connect_plus[0]  // 
0x0,// empty field //  stp_loop_instr[10:6] str_loop_instr[5:1] inf_loop[0] // 
0x0,// empty field //  empty field // 
0x0,// empty field //  empty field //
0x0,
0x0,
0x0,
0x0,
0x0,
0x0,
0x0,
0x0 
};