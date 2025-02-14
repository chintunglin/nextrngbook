# -*- coding: utf-8 -*-


from ._pcg64tmwc import _PCG64TMWC

__all__ = ["custom_pcg64tmwc", "default_pcg64tmwc", "get_default_pcg64tmwc_args"]


# Default pcg64tmwc setting
_bb_1 = 18446744073709550874
_bb_2 = 18446744073709471449


def custom_pcg64tmwc(bb_1=_bb_1, bb_2=_bb_2, seed=None):
    
    return _PCG64TMWC(bb_1, bb_2, seed)


def default_pcg64tmwc(seed=None):
    
    return _PCG64TMWC(_bb_1, _bb_2, seed)
    

def get_default_pcg64tmwc_args():
    
    return {"bb_1": _bb_1, 
            "bb_2": _bb_2}

