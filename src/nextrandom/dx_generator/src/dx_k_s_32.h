/*
 * DX-k-s 32 bits generator, for k <= KK, s = 1, 2
 * 
 */

#ifndef DX_K_S_32_H
#define DX_K_S_32_H


#include <stdint.h> // uint16_t; uint32_t; uint64_t

#if defined(_WIN32) && !defined (__MINGW32__)
#define inline __forceinline
#endif

#define B_LCG 16807     // LCG for seeding
#define KK 700       // upper limit of kk (num. of terms of the dx_kk_s generator)


// 32-bit rescale
#define NEXT32_RESCALE(s, p) ((uint32_t)((s) * (4294967296.0 / (p))))
//#define NEXT32_ROTATE1(s, r) (((s) >> (r)) | ((s) << (32 - (r))))
//#define NEXT32_ROTATE2_XOR(s, r1, r2) ((NEXT32_ROTATE1(s, r1)) ^ (NEXT32_ROTATE1(s, r2)))
//#define NEXT32_ROTATE2_MOD(s, r1, r2) ((NEXT32_ROTATE1(s, r1)) + (NEXT32_ROTATE1(s, r2)))

// the state information
typedef struct s_dx_k_s_state {
    uint32_t XX[KK];  // states with at most KK terms
    uint16_t II;      // running index
    uint32_t bb;      // multiplier
    uint32_t pp;      // modulo pp
    uint16_t kk;      // num. of terms of the dx_kk_s generator
} dx_k_s_state;


// seeding
void initialize(dx_k_s_state *state, uint32_t seed);

// update functions
void dx_k_1(dx_k_s_state *state);
void dx_k_2(dx_k_s_state *state);


// for dx_k_1 generator family
// generate a 32 bit random number
static inline uint32_t dx_k_1_next32(dx_k_s_state *state) {
                                         
  dx_k_1(state); // update the state
  
  return NEXT32_RESCALE(state->XX[state->II], state->pp);
  
}

// generate a 64 bit random number (combine two 32 bit random numbers)
static inline uint64_t dx_k_1_next64(dx_k_s_state *state) {
  return (uint64_t) dx_k_1_next32(state) << 32 | 
                    dx_k_1_next32(state);
}

// generate a double in [0, 1)
static inline double dx_k_1_next_double(dx_k_s_state *state) {
    
    dx_k_1(state); // update the state
    
    return (double) state->XX[state->II] / state->pp;
  
}



// for dx_k_2 generator family
// generate a 32 bit random number
static inline uint32_t dx_k_2_next32(dx_k_s_state *state) {
                                         
  dx_k_2(state); // update the state
  
  return NEXT32_RESCALE(state->XX[state->II], state->pp);
  
}

// generate a 64 bit random number (combine two 32 bit random numbers)
static inline uint64_t dx_k_2_next64(dx_k_s_state *state) {
  return (uint64_t) dx_k_2_next32(state) << 32 | 
                    dx_k_2_next32(state);
}

// generate a double in [0, 1)
static inline double dx_k_2_next_double(dx_k_s_state *state) {
  
    dx_k_2(state); // update the state
    
    return (double) state->XX[state->II] / state->pp;
  
}






#endif