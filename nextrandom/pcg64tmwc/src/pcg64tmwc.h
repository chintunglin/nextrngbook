/*
 * PCG64TMWC implementation
 * 
 * Only works on platforms that support __uint128_t data type
 * 
 * Underlying generators: two MWC 64 bits generators
 * 
 *    mm = 2^64 (modulus)
 * 
 *    If not define POWER2_ADD OR POWER2_DED:
 * 
 *      bb_1, bb_2 can be decided by users
 *      e.g., bb = 2^64 − 742 = 18,446,744,073,709,550,874
 *      e.g., bb = 2^64 − 80,167 = 18,446,744,073,709,471,449
 * 
 *    else: use powers-of-two decomposition (efficient implementation)
 *      
 *      rr, ww >= 0,
 *      (rr, ww): bb = 2^rr + 2^ww or (rr, -ww): bb = 2^rr - 2^ww
 *      
 *      (rr_1, ww_1) and (rr_2, ww_2) can be decided by users
 *      e.g., (rr, ww) = (9, 16), (21, 52), (23, 36)
 *      e.g., (rr, -ww) = (37, -19), (54, -34), (57, -25), (61, -37)
 *      
 * Output function: XSL RR 128/64
 * 
*/

#ifndef PCG64TMWC_H
#define PCG64TMWC_H


#include <stdint.h> // uint16_t; uint32_t; uint64_t

#if defined(_WIN32) && !defined (__MINGW32__)
#define inline __forceinline
#endif


// the underlying state information
#if !defined(POWER2_ADD) && !defined(POWER2_DED)
    typedef struct s_mwc64_state {
        uint64_t cc;         // states: (c_n)
        uint64_t xx;         // states: (x_n)
        uint64_t bb;         // multiplier
    } mwc64_state;
#else
    typedef struct s_mwc64_state {
        uint64_t cc;         // states: (c_n)
        uint64_t xx;         // states: (x_n)
        int rr;              // multiplier r part
        int ww;              // multiplier w part
    } mwc64_state;
#endif    


// underlying seeding
void mwc64_set_seed(mwc64_state *state, uint64_t *seed);

// underlying update functions
void mwc64(mwc64_state *state);

// the state information
typedef struct s_pcg64tmwc_state {
    mwc64_state mwcstate1;            // underlying states 1
    mwc64_state mwcstate2;            // underlying states 2
    int has_uint32;
    uint32_t uinteger;
} pcg64tmwc_state;

// seeding
#if !defined(POWER2_ADD) && !defined(POWER2_DED)
    void pcg64tmwc_set_seed(pcg64tmwc_state *state, 
                            uint64_t bb_1, uint64_t bb_2, 
                            uint64_t *seed_1, uint64_t *seed_2);
#else
    void pcg64tmwc_set_seed(pcg64tmwc_state *state, 
                            int rr_1, int ww_1, int rr_2, int ww_2, 
                            uint64_t *seed_1, uint64_t *seed_2);
#endif 

// output function: XSL RR 128/64
static inline uint64_t pcg_rotr_64(uint64_t value, unsigned int rot) {
#ifdef _WIN32
  return _rotr64(value, rot);
#else
  return (value >> rot) | (value << (64 - rot));
#endif
}

static inline uint64_t pcg_output_xsl_rr_128_64(uint64_t upper, uint64_t lower) {
  return pcg_rotr_64(upper ^ lower, upper >> 58);
}


// generate a 64 bit random number
static inline uint64_t pcg64tmwc_next64(pcg64tmwc_state *state) {  

    mwc64(&state->mwcstate1); // update the state
    mwc64(&state->mwcstate2); // update the state
    
    // output transform and return
    return pcg_output_xsl_rr_128_64(state->mwcstate1.xx, state->mwcstate2.xx);

}

// generate a 32 bit random number
static inline uint32_t pcg64tmwc_next32(pcg64tmwc_state *state) {

    uint64_t next;
    
    if (state->has_uint32) {
        
        state->has_uint32 = 0;
        return state->uinteger;
        
    }
    
    next = pcg64tmwc_next64(state);
    
    state->has_uint32 = 1;
    state->uinteger = (uint32_t)(next >> 32);
    
    return (uint32_t)(next & 0xffffffff);    

}

// generate a double in [0, 1)
static inline double pcg64tmwc_next_double(pcg64tmwc_state *state) {
    
    // 2^64 = 18446744073709551616
    return pcg64tmwc_next64(state) / 18446744073709551616.0;
    
}


#endif