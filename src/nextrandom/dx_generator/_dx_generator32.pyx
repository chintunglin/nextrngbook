#cython: binding=True


import numpy as np
cimport numpy as np

from libc.stdint cimport uint16_t, uint32_t, uint64_t
from numpy.random cimport BitGenerator

__all__ = ["_DXGenerator32"]

_ss_support = {1, 2} # supported ss arguments in dx_kk_ss

np.import_array()


cdef extern from "src/dx_k_s_32.h":
    
    enum: KK

    struct s_dx_k_s_state:
        uint32_t XX[KK]   # states with at most KK terms (KK was defined in the C header)
        uint16_t II       # running index
        uint32_t bb       # multiplier
        uint32_t pp       # modulo pp
        uint16_t kk       # num. of terms of the dx_kk_s generator

    ctypedef s_dx_k_s_state dx_k_s_state # rename (to match C codes)

    # random number generation functions
    ## dx_k_1 generators
    uint32_t dx_k_1_next32(dx_k_s_state *state)  nogil
    
    uint64_t dx_k_1_next64(dx_k_s_state *state)  nogil
    
    double dx_k_1_next_double(dx_k_s_state *state)  nogil
    
    ## dx_k_2 generators
    uint32_t dx_k_2_next32(dx_k_s_state *state)  nogil
    
    uint64_t dx_k_2_next64(dx_k_s_state *state)  nogil
    
    double dx_k_2_next_double(dx_k_s_state *state)  nogil
    
    

# Numpy format
## dx_k_1 generators

cdef uint32_t dx_k_1_uint32(void *st) noexcept nogil:
    return dx_k_1_next32(<dx_k_s_state *> st)

cdef uint64_t dx_k_1_uint64(void *st) noexcept nogil:
    return dx_k_1_next64(<dx_k_s_state *> st)

cdef double dx_k_1_double(void *st) noexcept nogil:
    return dx_k_1_next_double(<dx_k_s_state *> st)

cdef uint64_t dx_k_1_raw(void *st) noexcept nogil:
    return <uint64_t>dx_k_1_next32(<dx_k_s_state *> st)


## dx_k_2 generators
cdef uint32_t dx_k_2_uint32(void *st) noexcept nogil:
    return dx_k_2_next32(<dx_k_s_state *> st)

cdef uint64_t dx_k_2_uint64(void *st) noexcept nogil:
    return dx_k_2_next64(<dx_k_s_state *> st)

cdef double dx_k_2_double(void *st) noexcept nogil:
    return dx_k_2_next_double(<dx_k_s_state *> st)

cdef uint64_t dx_k_2_raw(void *st) noexcept nogil:
    return <uint64_t>dx_k_2_next32(<dx_k_s_state *> st)


cdef class _DXGenerator32(BitGenerator):
    
    cdef int _ss
    cdef dx_k_s_state _rng_state

    def __init__(self, _bb, _pp, _kk, _ss, seed=None):
        
        BitGenerator.__init__(self, seed)
        
        # specify the dx_k_s generator
        self._rng_state.bb = _bb
        self._rng_state.pp = _pp
        self._rng_state.kk = _kk
        self._ss = _ss
        
        # initial seeding
        val = self._seed_seq.generate_state(self._rng_state.kk, np.uint32)
        
        self._rng_state.XX[0] = 0x80000000UL # avoid all-zeros
        for i in range(1, self._rng_state.kk):
            self._rng_state.XX[i] = val[i]
        
        # initialize running index
        self._rng_state.II = i

        # Numpy format
        self._bitgen.state = &self._rng_state
        self._specify_s()
        

    @property
    def state(self):
        """
        Get the PRNG state

        Returns
        -------
        state : dict
            Dictionary containing the information required to describe the
            state of the PRNG
        """
        
        
        XX = np.zeros(self._rng_state.kk, dtype=np.uint32)
        
        for i in range(self._rng_state.kk):
            XX[i] = self._rng_state.XX[i]

        return {"bit_generator": self.__class__.__name__,
                "state": {"XX": XX, "II": self._rng_state.II,
                          "bb": self._rng_state.bb,
                          "pp": self._rng_state.pp,
                          "kk": self._rng_state.kk,
                          "ss": self._ss}}

    @state.setter
    def state(self, value):

        if not isinstance(value, dict):
            raise TypeError("State must be a dict.")
            
        bitgen = value.get('bit_generator', '')
        if bitgen != self.__class__.__name__:
            raise ValueError('state must be for a {0} '
                             'PRNG'.format(self.__class__.__name__))
            
        if value["state"]["ss"] not in _ss_support:
            raise ValueError(f"ss must be in {_ss_support}.")
            
        XX = value["state"]["XX"]
        for i in range(self._rng_state.kk):
            self._rng_state.XX[i] = XX[i]
            
        self._rng_state.II = value["state"]["II"]
        self._rng_state.bb = value["state"]["bb"]
        self._rng_state.pp = value["state"]["pp"]
        self._rng_state.kk = value["state"]["kk"]
        
        self._ss = value["state"]["ss"]
        self._specify_s()

    
    def _specify_s(self):
        
        
        if self._ss == 1: # dx_k_1
            self._bitgen.next_uint32 = &dx_k_1_uint32
            self._bitgen.next_uint64 = &dx_k_1_uint64
            self._bitgen.next_double = &dx_k_1_double
            self._bitgen.next_raw = &dx_k_1_raw
            
        elif self._ss == 2: #dx_k_2
            self._bitgen.next_uint32 = &dx_k_2_uint32
            self._bitgen.next_uint64 = &dx_k_2_uint64
            self._bitgen.next_double = &dx_k_2_double
            self._bitgen.next_raw = &dx_k_2_raw
    
        else:
            raise ValueError(f"_ss must be in {_ss_support}.")

