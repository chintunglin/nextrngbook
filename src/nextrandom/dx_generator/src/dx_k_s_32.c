/*
 * DX-k-s 32 bits generator
 * 
 */

#include "dx_k_s_32.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>     // uint16_t; uint32_t; uint64_t


void initialize(dx_k_s_state *state, uint32_t seed){
               

    // reset the first seed to be non-zero (seed can't be all zero)
    if (seed == 0) {
        
        seed = 11111;   // seed <= pp - 1
        
    }
    
    // set initial seeds
    state->XX[0] = seed; 
    for (unsigned int i = 1; i < state->kk; i++){

        state->XX[i] = (uint32_t) ((B_LCG *  (uint64_t) state->XX[i - 1]) % state->pp);
    }
    
    
    // initialize index
    state->II = state->kk - 1;            // running index
    
}

void dx_k_1(dx_k_s_state *state){
    
    uint16_t II0 = state->II;
    
    // wrap around running index
    if (++state->II == state->kk) {
        state->II = 0; 
    }
    
    state->XX[state->II] = (uint32_t)((state->bb * (uint64_t) state->XX[state->II] + 
                                                       state->XX[II0]) % state->pp);
    
    return;
    
}


void dx_k_2(dx_k_s_state *state){
    
    uint16_t II0 = state->II;
    
    // wrap around running index
    if (++state->II == state->kk) {
        state->II = 0; 
    }
    
    state->XX[state->II] = (uint32_t)((state->bb * (state->XX[state->II] + 
                                        (uint64_t) state->XX[II0])) % state->pp);
    
    return;
    
}



extern inline uint32_t dx_k_1_next32(dx_k_s_state *state);
                                     
extern inline uint64_t dx_k_1_next64(dx_k_s_state *state);

extern inline double dx_k_1_next_double(dx_k_s_state *state);
                                        
extern inline uint32_t dx_k_2_next32(dx_k_s_state *state);
                                     
extern inline uint64_t dx_k_2_next64(dx_k_s_state *state);

extern inline double dx_k_2_next_double(dx_k_s_state *state);




