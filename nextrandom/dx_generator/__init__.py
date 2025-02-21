# -*- coding: utf-8 -*-


from ._dx_generator32 import _DXGenerator32

__all__ = ["custom_dx32", "default_dx32", "get_default_dx32_args"]


# Default dx_generator setting
# 32-bits: dx_643_1
_bb32 = 42720
_pp32 = 2147483647  # 2 ** 31 - 1
_kk32 = 643
_ss32 = 1


def custom_dx32(bb=_bb32, pp=_pp32, kk=_kk32, ss=_ss32, seed=None):
    
    return _DXGenerator32(bb, pp, kk, ss, seed)


def default_dx32(seed=None):
    
    return _DXGenerator32(_bb32, _pp32, _kk32, _ss32, seed)
    

def get_default_dx32_args():
    
    return {"bb": _bb32, 
            "pp": _pp32,
            "kk": _kk32,
            "ss": _ss32}






