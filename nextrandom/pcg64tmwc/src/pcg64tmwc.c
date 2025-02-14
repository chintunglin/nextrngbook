/*
 * PCG64TMWC implementation
 * 
 * Only works on platforms that support __uint128_t data type
 * 
 * 
*/

#include "pcg64tmwc.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>     // uint16_t; uint32_t; uint64_t


void mwc64_set_seed(mwc64_state *state, uint64_t *seed){
    
    state->xx = seed[1];
    
    #if defined(POWER2_ADD)
        uint64_t bb = ((uint64_t) 1 << state->rr) + ((uint64_t) 1 << state->ww);
    #elif defined(POWER2_DED)
        uint64_t bb = ((uint64_t) 1 << state->rr) - ((uint64_t) 1 << state->ww);
    #else
        uint64_t bb = state->bb;
    #endif 
    
    
    // ensure initial cc in {1, 2, ..., bb - 2}
    state->cc = seed[0] % (bb - 2) + 1;
    
    return;
    
}

void mwc64(mwc64_state *state){
    
    __uint128_t xx = state->xx;
    __uint128_t cc = state->cc;
    __uint128_t cx;
    
    #if defined(POWER2_ADD)
        cx = (xx << state->rr) + (xx << state->ww) + cc;
    #elif defined(POWER2_DED)
        cx = (xx << state->rr) - (xx << state->ww) + cc;
    #else
        cx = state->bb * xx + cc;
    #endif 
    
    state->xx = cx & 0xffffffffffffffff;
    state->cc = cx >> 64;
    
    return;
    
}

#if !defined(POWER2_ADD) && !defined(POWER2_DED)
void pcg64tmwc_set_seed(pcg64tmwc_state *state, 
                        uint64_t bb_1, uint64_t bb_2, 
                        uint64_t *seed_1, uint64_t *seed_2){
    
    // set bb_1, bb_2
    state->mwcstate1.bb = bb_1;
    state->mwcstate2.bb = bb_2;
    
    // mwc seeding
    mwc64_set_seed(&state->mwcstate1, seed_1); 
    mwc64_set_seed(&state->mwcstate2, seed_2); 
    
    state->has_uint32 = 0;
    state->uinteger = 0;
    
    return;
}
#else
void pcg64tmwc_set_seed(pcg64tmwc_state *state, 
                        int rr_1, int ww_1, int rr_2, int ww_2, 
                        uint64_t *seed_1, uint64_t *seed_2){
    
    // set rr, ww
    state->mwcstate1.rr = rr_1;
    state->mwcstate1.ww = ww_1;
    state->mwcstate2.rr = rr_2;
    state->mwcstate2.ww = ww_2;
    
    // mwc seeding
    mwc64_set_seed(&state->mwcstate1, seed_1); 
    mwc64_set_seed(&state->mwcstate2, seed_2); 
    
    state->has_uint32 = 0;
    state->uinteger = 0;
    
    return;
}
#endif


extern inline uint32_t pcg64tmwc_next32(pcg64tmwc_state *state);
                                     
extern inline uint64_t pcg64tmwc_next64(pcg64tmwc_state *state);

extern inline double pcg64tmwc_next_double(pcg64tmwc_state *state);
