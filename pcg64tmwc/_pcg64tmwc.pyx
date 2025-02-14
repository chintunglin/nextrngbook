#cython: binding=True


import numpy as np
cimport numpy as np

from libc.stdint cimport uint32_t, uint64_t
from numpy.random cimport BitGenerator

from numbers import Number

__all__ = ["_PCG64TMWC"]


cdef extern from "src/pcg64tmwc.h": 
    
    struct s_mwc64_state:
        uint64_t cc         # states: (c_n)
        uint64_t xx         # states: (x_n)
        uint64_t bb         # multiplier

    ctypedef s_mwc64_state mwc64_state # rename (to match C codes)


    struct s_pcg64tmwc_state:
        mwc64_state mwcstate1            # underlying states 1
        mwc64_state mwcstate2            # underlying states 2
        int has_uint32
        uint32_t uinteger

    ctypedef s_pcg64tmwc_state pcg64tmwc_state # rename (to match C codes)

    # random number generation functions
    uint32_t pcg64tmwc_next32(pcg64tmwc_state *state) noexcept nogil
    uint64_t pcg64tmwc_next64(pcg64tmwc_state *state) noexcept nogil
    double pcg64tmwc_next_double(pcg64tmwc_state *state) noexcept nogil
    
    # seeding function
    void pcg64tmwc_set_seed(pcg64tmwc_state *state, 
                            uint64_t bb_1, uint64_t bb_2, 
                            uint64_t *seed_1, uint64_t *seed_2)
    

# Numpy format
cdef uint32_t pcg64tmwc_uint32(void *st) noexcept nogil:
    return pcg64tmwc_next32(<pcg64tmwc_state *> st)

cdef uint64_t pcg64tmwc_uint64(void *st) noexcept nogil:
    return pcg64tmwc_next64(<pcg64tmwc_state *> st)

cdef double pcg64tmwc_double(void *st) noexcept nogil:
    return pcg64tmwc_next_double(<pcg64tmwc_state *> st)


cdef class _PCG64TMWC(BitGenerator):
    
    cdef pcg64tmwc_state __rng_state
    
    def __init__(self, bb_1, bb_2, seed=None):
        
        # check whether values are valid
        self._inspect_b_x(bb_1), self._inspect_b_x(bb_2)
        
        
        BitGenerator.__init__(self, seed)
        
        # initial seeding and specifying the PCG64TMWC generator 
        val_pt = <uint64_t *>np.PyArray_DATA(self._seed_seq.generate_state(4, np.uint64))

        pcg64tmwc_set_seed(&self.__rng_state, bb_1, bb_2,
                           val_pt, val_pt + 2)

        # Numpy format
        self._bitgen.state = <void *>&self.__rng_state
        self._bitgen.next_uint32 = &pcg64tmwc_uint32
        self._bitgen.next_uint64 = &pcg64tmwc_uint64
        self._bitgen.next_double = &pcg64tmwc_double
        self._bitgen.next_raw = &pcg64tmwc_uint64
        

    @property
    def state(self):
        """
        Get or set the PRNG state

        Returns
        -------
        state : dict
            Dictionary containing the information required to describe the
            state of the PRNG
        """
        
        
        return {"bit_generator": self.__class__.__name__,
                "state": {"cc_1": self.__rng_state.mwcstate1.cc, 
                          "xx_1": self.__rng_state.mwcstate1.xx,
                          "bb_1": self.__rng_state.mwcstate1.bb,
                          "cc_2": self.__rng_state.mwcstate2.cc,
                          "xx_2": self.__rng_state.mwcstate2.xx,
                          "bb_2": self.__rng_state.mwcstate2.bb},
                "has_uint32": self.__rng_state.has_uint32,
                "uinteger": self.__rng_state.uinteger}

    @state.setter
    def state(self, value):

        if not isinstance(value, dict):
            raise TypeError("state must be a dict")
            
        bitgen = value.get("bit_generator", "")
        if bitgen != self.__class__.__name__:
            raise ValueError(f"state must be for a {self.__class__.__name__} RNG")
        
        
        # raise KeyError if lack some keys
        cc_1 = value["state"]["cc_1"]
        xx_1 = value["state"]["xx_1"]
        bb_1 = value["state"]["bb_1"]
        cc_2 = value["state"]["cc_2"]
        xx_2 = value["state"]["xx_2"]
        bb_2 = value["state"]["bb_2"]

        has_uint32 = value["has_uint32"]
        uinteger = value["uinteger"]       
        
        
        # check whether values are valid
        self._inspect_b_x(bb_1), self._inspect_b_x(bb_2)
        self._inspect_b_x(xx_1), self._inspect_b_x(xx_2)
        self._inspect_cc(cc_1, bb_1), self._inspect_cc(cc_2, bb_2)
        
        if has_uint32 not in {0, 1}:
            raise ValueError("has_uint32 must be True or False")
        
        
        # set new values
        self.__rng_state.mwcstate1.cc = cc_1
        self.__rng_state.mwcstate1.xx = xx_1
        self.__rng_state.mwcstate1.bb = bb_1
        self.__rng_state.mwcstate2.cc = cc_2
        self.__rng_state.mwcstate2.xx = xx_2
        self.__rng_state.mwcstate2.bb = bb_2
        
        self.__rng_state.has_uint32 = has_uint32
        self.__rng_state.uinteger = uinteger

    
    @staticmethod
    def _inspect_b_x(value):
        
        two_power_64 = 1 << 64
        
        if not isinstance(value, Number):
            raise TypeError("bb and xx must be numeric")
        
        if int(value) != value or not (0 <= value < two_power_64):
            raise ValueError("bb and xx must be integers in [0, 2^64 - 1]")
    
    @staticmethod
    def _inspect_cc(cc, bb):
        
        if not isinstance(cc, Number):
            raise TypeError("cc must be numeric")
        
        if int(cc) != cc or not (1 <= cc < bb - 1):
            raise ValueError("cc must be an integer in [1, bb - 2]")
    
    
