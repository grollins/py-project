from numpy import percentile
import pandas as pd
import pymc3 as pm

def binomial():
    with pm.Model() as model:
        # parameter
        theta = pm.Beta('theta', 1, 1)
        # observed data
        A = pm.Binomial('A', n=100, p=theta, observed=20)
        # run sampling
        trace = pm.sample(1000, tune=500)
    return model, trace

def binomial_ab():
    with pm.Model() as model:
        # parameter
        theta_A = pm.Beta('theta_A', 1, 1)
        theta_B = pm.Beta('theta_B', 1, 1)
        # observed data
        x_A = pm.Binomial('x_A', n=100, p=theta_A, observed=20)
        x_B = pm.Binomial('x_B', n=100, p=theta_B, observed=30)
        delta_theta = \
          pm.Deterministic('delta_theta',
                           theta_B - theta_A)
        # run sampling
        trace = pm.sample(1000, tune=500)
    return model, trace

def compute_ci(trace, params):
    # compute median and 95% for each posterior marginal distribution
    pct = [50.0, 2.5, 97.5]
    pct_labels = ['median', 'lower', 'upper']
    ci_list = [percentile(trace[p], pct) for p in params]
    df = pd.DataFrame(ci_list, index=params, columns=pct_labels)
    return df

def run_ppc(model, trace):
    # posterior predictive checks
    ppc = pm.sample_ppc(trace, samples=200, model=model, size=30)
    return ppc
