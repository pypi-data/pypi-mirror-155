# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from ultron.factor.analysis.factor_analysis import er_portfolio_analysis
from ultron.optimize.model.linearmodel import ConstLinearModel
from ultron.optimize.constraints import LinearConstraints, \
    create_box_bounds, BoundaryType
from ultron.tradingday import *
from kdutils.logger import kd_logger

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
                 start_date,
                 end_date,
                 total_data=None):
        self.alpha_model = alpha_model
        self.dates = [
            d.strftime('%Y-%m-%d') for d in makeSchedule(
                start_date, end_date, '1b', 'china.sse')]
        
        self.total_data = total_data
    
    def prepare_backtest_data(self):
        pass

    def prepare_backtest_models(self, factor_name='factor'):
        models = {}
        total_data_groups = self.total_data.groupby('trade_date')
        alpha_model = ConstLinearModel(features=[factor_name], 
                                weights={factor_name: 1.0})
        for ref_date, _ in total_data_groups:
            models[ref_date] = alpha_model
        self.alpha_models = models
        kd_logger.info("alpha models training finished ...")



    @staticmethod
    def _create_lu_bounds(running_setting, codes, benchmark_w):

        codes = np.array(codes)

        if running_setting.weights_bandwidth:
            lbound = np.maximum(0., benchmark_w - running_setting.weights_bandwidth)
            ubound = running_setting.weights_bandwidth + benchmark_w

        lb = running_setting.lbound
        ub = running_setting.ubound

        if lb or ub:
            if not isinstance(lb, dict):
                lbound = np.ones_like(benchmark_w) * lb
            else:
                lbound = np.zeros_like(benchmark_w)
                for c in lb:
                    lbound[codes == c] = lb[c]

                if 'other' in lb:
                    for i, c in enumerate(codes):
                        if c not in lb:
                            lbound[i] = lb['other']
            if not isinstance(ub, dict):
                ubound = np.ones_like(benchmark_w) * ub
            else:
                ubound = np.ones_like(benchmark_w)
                for c in ub:
                    ubound[codes == c] = ub[c]

                if 'other' in ub:
                    for i, c in enumerate(codes):
                        if c not in ub:
                            ubound[i] = ub['other']
        return lbound, ubound

    def _calculate_pos(self, running_setting, er, data, constraints, benchmark_w, lbound, ubound,
                       risk_model,
                       current_position):
        more_opts = running_setting.more_opts
        try:
            target_pos, _ = er_portfolio_analysis(
                er=er,industry=data.industry_code.values,
                dx_return=None,constraints=constraints,
                detail_analysis=False, benchmark=benchmark_w,
                method=running_setting.rebalance_method,
                lbound=lbound,ubound=ubound,
                current_position=current_position,
                target_vol=more_opts.get('target_vol'),
                turn_over_target=more_opts.get('turn_over_target'),
                risk_model=risk_model)
        except Exception:
            kd_logger.error('{0} rebalance error'.format(data.trade_date.values[0]))
            target_pos = benchmark_w
        




    def run(self, running_setting):
        kd_logger.info("starting backting ...")
        total_data_groups = self.total_data.groupby('trade_date')
        rets = []
        turn_overs = []
        leverags = []
        previous_pos = pd.DataFrame()
        positions = pd.DataFrame()

        if self.alpha_models is None:
            self.prepare_backtest_models()
        
        for ref_date, this_data in total_data_groups:
            new_model = self.alpha_models[ref_date]
            codes = this_data.code.values.tolist()

            if previous_pos.empty:
                current_position = None
            else:
                previous_pos.set_index('code', inplace=True)
                remained_pos = previous_pos.reindex(codes)
                remained_pos.fillna(0., inplace=True)
                current_position = remained_pos.weight.values
            benchmark_w = this_data.weight.values
            constraints = LinearConstraints(running_setting.bounds,
                                            this_data,
                                            benchmark_w)
            lbound, ubound = self._create_lu_bounds(running_setting, codes, benchmark_w)
            this_data.fillna(0, inplace=True)
            ###是否标准化
            new_factors = this_data[new_model.features].values
            new_factors = pd.DataFrame(new_factors, columns=['factor'], index=codes)
            er = new_model.predict(new_factors).astype(float)

            kd_logger.info('{0} re-balance: {1} codes'.format(ref_date, len(er)))
            target_pos = self._calculate_pos(
                running_setting=running_setting, er=er, 
                data=this_data, constraints=constraints, 
                benchmark_w=benchmark_w, lbound=lbound, 
                ubound=ubound,risk_model=risk_model.get_risk_profile(codes),
                current_position=current_position)
            target_pos['code'] = codes
            target_pos['trade_date'] = ref_date
            positions = positions.append(target_pos)
        previous_pos = target_pos