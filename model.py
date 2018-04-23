from numpy import percentile
import pandas as pd
import pymc3 as pm


with pm.Model() as model:
    # parameters
    alpha = pm.Uniform('alpha', 0, 100)
    beta = pm.Uniform('beta', 0, 1)
    # observed data
    p = pm.Gamma('p', alpha=alpha, beta=beta, observed=df['price'])
    # posterior sampling
    trace = pm.sample(2000, tune=1000)

# posterior predictive checks
ppc = pm.sample_ppc(trace, samples=200, model=model, size=30)

num_bins = 30
plt.figure()
ax = df['price'].hist(bins=num_bins, cumulative=True, normed=1, histtype='step',
                      color='k')

for i in range(ppc['p'].shape[0]):
    sA = pd.Series(ppc['p'][i,:])
    sA.hist(bins=num_bins, cumulative=True, normed=1, histtype='step', ax=ax,
            color='r', alpha=0.1)
plt.savefig('test.png')
