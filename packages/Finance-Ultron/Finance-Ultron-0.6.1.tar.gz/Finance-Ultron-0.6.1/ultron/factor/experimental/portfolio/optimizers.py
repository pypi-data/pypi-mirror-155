# -*- coding: utf-8 -*-
from cmath import cos
import numpy as np
from .quadratic import TargetVarianceOptimizer as _TargetVarianceOptimizer

class TargetVarianceOptimizer:
    def __init__(self, 
                objective: np.array,
                current_pos: np.array,
                target_turn_over: float,
                target_vol: float,
                cov: np.ndarray,
                lbound: np.ndarray,
                ubound: np.ndarray) -> None:
        self._optimizer = _TargetVarianceOptimizer(cost=objective,
                benchmark=current_pos, l1norm=target_turn_over,
                variance_target=target_vol*target_vol, variance=cov,
                lower_bound=lbound,upper_bound=ubound)
        self._x, self._f_val,self._status = self._optimizer.solver()

    def status(self):
        return self._status
    
    def feval(self):
        return self._f_val
    
    def x_value(self):
        return self._x