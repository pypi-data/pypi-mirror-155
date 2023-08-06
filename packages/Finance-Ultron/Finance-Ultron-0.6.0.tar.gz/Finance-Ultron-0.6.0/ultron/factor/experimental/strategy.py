# -*- coding: utf-8 -*-

class RunningSetting(object):
    def __init__(self,
                 lbound=None,
                 ubound=None,
                 weights_bandwidth=None,
                 rebalance_method='risk_neutral',
                 bounds=None,
                 **kwargs):
        self.lbound = lbound
        self.ubound = ubound
        self.weights_bandwidth = weights_bandwidth
        self.rebalance_method = rebalance_method
        self.bounds = bounds
        self.more_opts = kwargs

class Strategy(object):
    def __init__(self,
                 alpha_model,
                 data_meta,
                 universe,
                 start_date,
                 end_date,
                 freq,
                 benchmark=905,
                 industry_cat='sw_adj',
                 industry_level=1,
                 dask_client=None):