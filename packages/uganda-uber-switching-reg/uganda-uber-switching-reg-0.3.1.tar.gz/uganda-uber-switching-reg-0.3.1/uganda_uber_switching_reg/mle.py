# %%
import os
os.environ["MKL_NUM_THREADS"] = "4"
os.environ["NUMEXPR_NUM_THREADS"] = "4"
os.environ["OMP_NUM_THREADS"] = "4"
from joblib import delayed, Parallel

import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.base.model import GenericLikelihoodModel
import warnings
np.errstate(all="raise")
import functools

from linearmodels.panel.data import PanelData
from linearmodels import PanelOLS
from linearmodels.panel.model import PanelFormulaParser
from linearmodels.panel.utility import check_absorbed, not_absorbed, AbsorbingEffectError

class UnequalRowException(Exception):
    pass


def get_mle_betas(res, regimes):

    beta0_mle = res.params[0:regimes]

    beta1_mle = res.params[regimes : 2 * regimes]

    return beta0_mle, beta1_mle, np.append(beta0_mle, beta1_mle)


def get_mle_sigmas(res, regimes):
    """
    Get sigmas from MLE estimation, then transform back (take absolute value)
    """

    return np.abs(res.params[2 * regimes : 3 * regimes])

def _reorganize_gaul_ind(ind):
    ind[5], ind[6] = ind[6], ind[5]
    ind[8], ind[9] = ind[9], ind[8]
    return ind
class DriverSpecificProbUberMLE(GenericLikelihoodModel):
    """An Uber MLE with two things different:
    - Gets rid of lambda as parameters
    - Uses driver-specific probabilities in likelihood
    - Uses bounding and constrained optimization for probabilities
    
    Uses full probabilities in classifier cols, not categoricals
    """
    
    def __init__(self, 
                 endog,
                 exog,
                 classifier_pred, 
                 classifier_ind = None,
                 classifier_ind_name = None,
                 entity_effects = False,
                 time_effects = False,
                 other_effects=None,
                 weights=None,
                 drop_absorbed=False,
                 check_rank=True,
                 singletons = True,
                 **kwargs):
        
        print("Initializing...")    

        if classifier_ind is None:
            self._group = endog.index.get_level_values(2).name
            if self._group == 'gaul':
                self.classifer_ind = _reorganize_gaul_ind(endog.index.get_level_values(2).unique().tolist())
            endog.reset_index(2, inplace=True)
            exog.reset_index(2, inplace=True)
        else:
            self.classifier_ind = classifier_ind
            self._group = classifier_ind_name
    
        if not all([classifier_ind is not None, classifier_ind_name]):
            raise Exception("If either `classifier_ind` or `classifier_ind_name` is defined, the other must be defined as well, but ")
                
        self.classifier_pred = classifier_pred
        self.classifier_map = {k:v for k,v in zip(self.classifier_pred.columns, self.classifier_ind.cat.categories)}
        
        endog_cat = (
            endog
            .assign(gaul_class = self.ind)
            .assign(gaul = self.classifier_ind)
            .query(f"{self._group}==gaul_class")
            .drop(columns=[self._group, 'gaul_class'])
            )
        
        
        exog_cat = (
            exog
            .assign(gaul_class = self.ind)
            .assign(gaul = self.classifier_ind)
            .query(f"{self._group}==gaul_class")
            .drop(columns=[self._group, 'gaul_class'])
            )

        self.p_model = PanelOLS(dependent=endog_cat,
                exog=exog_cat,
                weights=weights,
                entity_effects=entity_effects,
                time_effects=time_effects,
                other_effects=other_effects,
                singletons=singletons,
                drop_absorbed=drop_absorbed,
                check_rank=check_rank)
        
        self.p_model_full = PanelOLS(dependent=endog,
                exog=exog,
                weights=weights,
                entity_effects=entity_effects,
                time_effects=time_effects,
                other_effects=other_effects,
                singletons=singletons,
                drop_absorbed=drop_absorbed,
                check_rank=check_rank)
        
        self.endog_cat = self.p_model.dependent.dataframe
        self.exog_cat = self.p_model.exog.dataframe
        
        self.endog_full = self.p_model_full.dependent.dataframe.assign(**{self._group : self.classifier_ind})
        self.exog_full = self.p_model_full.exog.dataframe.assign(**{self._group : self.classifier_ind})

        super().__init__(endog=self.endog_cat, 
                         exog=self.exog_cat, **kwargs)
    
        self.entity_effects = self.p_model.entity_effects
        self.time_effects = self.p_model.time_effects
        
        if self.entity_effects and self.time_effects:
            self.demean = 'both'
        elif self.entity_effects and not self.time_effects:
            self.demean = 'entity'
        elif not self.entity_effects and self.time_effects:
            self.demean = 'time'
        else:
            self.demean = None
        
        if self.entity_effects or time_effects:    
            # Check for multiindex
            if not isinstance(exog.index, pd.MultiIndex):
                raise Exception("Dataframe not a multi-index")
        
        self.n_regimes = classifier_ind.nunique()
            
        self._drop_absorbed = drop_absorbed
        
        self._equal_regime = True
        if self.endog_full.groupby(self._group)[self.p_model.dependent.vars[0]].count().nunique() > 1:
            warnings.warn("Warning: observations across regimes is not the same, switching to slower method...")
            self._equal_regime=False
            

        
    @classmethod
    def from_formula(
        cls,
        formula,
        data,
        classifier_pred, 
        other_effects=None,
        weights=None,
        drop_absorbed=False,
        check_rank=True,
        singletons = True,
        **kwargs
    ):
        
        data, classifier_ind_name = data.reset_index(2), data.index.get_level_values(2).name
        
        if classifier_ind_name == 'gaul':
            classifier_ind = data[classifier_ind_name].unique().tolist()
            classifier_ind = _reorganize_gaul_ind(classifier_ind)
        
        parser = PanelFormulaParser(formula, data)
        
        endog, exog = parser.data

        mod = cls(
            endog = endog,
            exog = exog,
            classifier_pred=classifier_pred, 
            classifier_ind = data[classifier_ind_name].astype(pd.CategoricalDtype(classifier_ind, ordered=True)),
            classifier_ind_name = classifier_ind_name,
            entity_effects = parser.entity_effect,
            time_effects = parser.time_effect,
            other_effects=other_effects,
            weights=weights,
            drop_absorbed=drop_absorbed,
            check_rank=check_rank,
            singletons = singletons,
            **kwargs
        )
                
        mod.formula=formula
        
        return mod
    
    @functools.lru_cache(maxsize=128)
    def _regime_list(self, lm):            
        
        if self.demean is not None:
            return np.array([PanelData(group.drop(columns=self._group), 
                                       convert_dummies=False).demean(group=self.demean, low_memory=False).values2d \
                for _, group in getattr(self, lm).groupby(self._group)])
        else:
            return np.array([PanelData(group.drop(columns=self._group), convert_dummies=False).values2d \
                for _, group in getattr(self, lm).groupby(self._group)])
              
    @functools.cached_property
    def X(self):
        X = self._regime_list('exog_full')
        
        # if not self._equal_regime:
        #     print("Regimes not equal... Will merge by shortest dataset")
        #     # Get smallest dataset
        #     minidx = np.argmin([i.dataframe.shape[0] for i in X])
        #     index_to_match = X[minidx].index
            
        #     X = np.array([i.dataframe.query("index in @index_to_match") for i in X])
            
        # (regimes, rows, columns)
        for i, regime in enumerate(X):
            # try:
            check_absorbed(regime, self.exog_full.columns.tolist())
            # TODO: figure out a way to drop absorbed variables
            # except AbsorbingEffectError as e:
            #     if self._drop_absorbed:
            #         X[i, :, :] = not_absorbed(regime, self.p_model._constant, 
            #                                   self.p_model._constant_index)
            
        return X
    
    @functools.cached_property
    def y(self):
        # y = np.array([i.values2d for i in self._regime_list('endog_full')])

        return self._regime_list('endog_full')
    
    @functools.cached_property
    def ind(self):
        return self.classifier_pred.idxmax(axis=1).map(self.classifier_map)
    
    @functools.cached_property
    def p(self):
        return self.classifier_pred.values
    
    @functools.cached_property
    def p_slow(self):
        
        entity = self.p_model.dependent.index.names[0]
        time = self.p_model.dependent.index.names[1]
        
        p = (
            self.classifier_pred
            .reset_index([time], drop=True)
            .reset_index()
            .drop_duplicates([entity])
            .set_index([entity])
        )
        
        # merge into y to get dates for each driver
        
        p_list = [
            i.dataframe
            .reset_index(time)
            .merge(p, left_index=True, right_index=True)
            .drop(columns=[time, self.p_model.dependent.vars[0]]) \
                for i in self._regime_list('endog_full')
        ]
        
        return p_list

    def _ll(self, sigma_vec, beta_vec):
                
        
        if self.n_regimes == 4:
            cm = np.array(
                [
                    [0.85400498, 0.17394031, 0.0470923, 0.17593651],
                    [0.07902572, 0.71988785, 0.13576904, 0.04206538],
                    [0.00444184, 0.05345483, 0.7683022, 0.01397825],
                    [0.06252746, 0.05271701, 0.04883646, 0.76801986],
                ]
            )

        elif self.n_regimes == 10:
            cm = np.array(
                [
                    [
                        7.51733523e-01,
                        3.36037080e-02,
                        1.06639147e-02,
                        1.33630290e-02,
                        9.74529347e-02,
                        7.45621493e-02,
                        5.60966108e-03,
                        2.33992767e-03,
                        2.18987342e-02,
                        5.46599963e-03,
                    ],
                    [
                        1.19240490e-02,
                        8.86442642e-01,
                        1.71998624e-03,
                        5.93912398e-04,
                        1.60149928e-02,
                        1.70039109e-03,
                        3.11647838e-04,
                        0.00000000e00,
                        2.53164557e-03,
                        2.77932185e-04,
                    ],
                    [
                        1.15352213e-02,
                        4.05561993e-03,
                        5.24251806e-01,
                        2.87552586e-02,
                        2.17224636e-02,
                        1.30079918e-02,
                        4.37086093e-02,
                        7.53031270e-02,
                        8.17721519e-02,
                        1.17750602e-01,
                    ],
                    [
                        8.73566198e-02,
                        1.62224797e-02,
                        1.24183007e-01,
                        7.07745608e-01,
                        3.45003833e-02,
                        1.86958000e-01,
                        1.97506817e-01,
                        1.21676239e-01,
                        6.70886076e-02,
                        1.13118399e-01,
                    ],
                    [
                        2.98749271e-02,
                        3.36037080e-02,
                        5.84795322e-03,
                        1.68275179e-03,
                        7.81412386e-01,
                        3.65584084e-03,
                        1.63615115e-03,
                        1.27632419e-03,
                        2.83544304e-02,
                        2.03816935e-03,
                    ],
                    [
                        8.38571706e-02,
                        1.50637312e-02,
                        2.20158239e-02,
                        4.91957436e-02,
                        1.95928103e-02,
                        6.75990478e-01,
                        1.19984418e-02,
                        3.40353116e-03,
                        1.75949367e-02,
                        1.29701686e-02,
                    ],
                    [
                        5.05475990e-03,
                        4.05561993e-03,
                        5.02235982e-02,
                        1.68225687e-01,
                        1.44816424e-03,
                        2.27852406e-02,
                        4.15894040e-01,
                        1.66985748e-01,
                        3.79746835e-03,
                        1.37669075e-01,
                    ],
                    [
                        1.68491997e-03,
                        0.00000000e00,
                        1.61678707e-02,
                        7.72086117e-03,
                        1.70372263e-04,
                        3.48580173e-03,
                        1.18426178e-01,
                        4.69049138e-01,
                        1.64556962e-03,
                        6.95756902e-02,
                    ],
                    [
                        1.09519798e-02,
                        5.79374276e-03,
                        2.23598211e-02,
                        3.46448899e-03,
                        2.53002811e-02,
                        3.74086040e-03,
                        1.16867939e-03,
                        2.12720698e-04,
                        7.68481013e-01,
                        4.53955901e-03,
                    ],
                    [
                        6.02682911e-03,
                        1.15874855e-03,
                        2.22566219e-01,
                        1.92526602e-02,
                        2.38521169e-03,
                        1.41132460e-02,
                        2.03739774e-01,
                        1.59753244e-01,
                        6.83544304e-03,
                        5.36594404e-01,
                    ],
                ]
            )
            
        # if self._equal_regime:
        rnl = norm.pdf(np.squeeze(self.y), self.X@beta_vec, scale=sigma_vec).T
        
        # get row_maxes for probabilities
        row_maxes = self.p.max(axis=1, keepdims=True)
        class_ind = np.where(self.p==row_maxes, self.p, 0)
    
        return np.log((rnl*(class_ind@cm.T)).sum(axis=1))
        # else:
        #     likelihood = []
        #     class_ind = [np.where(p.values==p.values.max(axis=1, keepdims=True), p, 0) for p in self.p_slow]
            
        #     def compute_likelihood(z):
        #         i, (x,y,c) = z
        #         r = norm.pdf(np.squeeze(y), np.squeeze(x@beta_vec), scale=sigma_vec)
        #         return r*(c@cm.T)[:, i]  #@cm.T
            
        #     # likelihood = np.array(Parallel(n_jobs=10, verbose=10)(delayed(compute_likelihood)(z) for z in zip(self.X, self.y, self.p_slow)))
        #     likelihood = np.array([compute_likelihood(z) for z in enumerate(zip(self.X, self.y, class_ind))])
            
        #     return np.log(likelihood.sum(axis=1))

    def _params_to_ll(self, params):

        # Since we always put the covariates at the end, take them out from the end
        # regime_params = res.params.values[:-num_covariates]        
        
        beta_vec =params[:-1]
        sigma_vec = params[-1]
            
        return beta_vec, sigma_vec

    def nloglikeobs(self, params):
        """Negative log-likelihood for an observation. The params matrix is the strange thing here
        and needs to be better defined.

        Args:
            params (ndarray): The matrix of parameters to optimize

        """

        beta_vec, sigma_vec = self._params_to_ll(params)

        ll = self._ll(
            beta_vec=beta_vec, sigma_vec=sigma_vec,
        )

        return -ll

    def bounds(self, num_exog, sigma_bound):
        
        # Now set up bounds on variables
        beta_bounds = [(None, None) for i in range(num_exog-1)]
        
        sigma_bounds = [sigma_bound]

        bounds = tuple(beta_bounds + sigma_bounds)

        return bounds
    
    def _start_params(self, show_ols = False):
        """Runs OLS regression to get start params for MLE coefficients
        """
                
        print("Creating starting values...")

        
        res = self.p_model.fit()
        summary = res.summary
        
        # Now get sigma
        sigma = self.endog.std()

        if show_ols:
            print(summary)          
        
        return np.append(res.params.values, sigma)
    
    def fit(
        self,
        method=None,
        start_params=None,
        maxiter=10000,
        maxfun=5000,
        sigma_bound=None,
        cluster_var=None,
        show_ols=True,
        **kwds,
    ):

        # self.apply_exog_names(regime_impact_names=regime_impact_names)


        if start_params is None:
            start_params = self._start_params(show_ols=show_ols)
        
        if kwds.get('cov_type') is None:
            cov_type='cluster'
            cov_kwds = {'groups' : cluster_var,
                        'df_correction' : True,
                        'use_correction' : True}
        else:
            cov_type = kwds.pop('cov_type', None)
            cov_kwds = kwds.pop('cov_kwds', None) 

        print("Optimizing...")
        optimize = super().fit(
            method=method,
            start_params=start_params,
            maxiter=maxiter,
            maxfun=maxfun,
            eps=1e-08,
            ftol=1e-10,
            bounds=self.bounds(num_exog = len(start_params), sigma_bound=sigma_bound),
            cov_type= cov_type,
            cov_kwds = cov_kwds,
            use_t=True,
            **kwds
        )

        return optimize