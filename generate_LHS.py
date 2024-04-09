import numpy as np
import matplotlib.pylab as plt
import scipy.stats.qmc as qmc

def log_scale(sample, y_min, y_max):
  nsample, dimensions = sample.shape
  sample_scaled = np.zeros((nsample,dimensions))
  for j in range(dimensions):
    b = np.log10(y_max[j]/y_min[j])
    a = y_min[j]
    sample_scaled[:,j] = a*10**(b*sample[:,j])
  return sample_scaled 

seed = 2001
dimensions = 5
n_simulations = 50
sampler = qmc.LatinHypercube(d=dimensions, scramble = True, seed=seed)
sample  = sampler.random(n=n_simulations)

l_bounds = [1e2, 0.1 , 1 , 0.01 , 20]
u_bounds = [3e3, 3.0 , 30, 1., 200]


nsample, dimensions = sample.shape
sample_scaled = np.zeros((nsample,dimensions))

# scale the sample
sample_scaled = log_scale(sample, l_bounds, u_bounds)

fig = plt.figure(figsize=(10,10))

labels = ['l','k','MR', 'r', r'$r_{scale}$']

axs = fig.subplots(nrows=5, ncols=5)

# plot sample
for j in range(dimensions):
  for i in range(j):
    axs[j,i].scatter(sample.T[i], sample.T[j])

# plot scaled sample 
for j in range(dimensions):
  for i in range(j):
    axs[i,j].scatter(sample_scaled.T[j], sample_scaled.T[i], color='orange')
    axs[i,j].set_yscale('log')
    axs[i,j].set_xscale('log')

for i in range(dimensions):
  axs[4,i].set_xlabel(labels[i])
  axs[i,0].set_ylabel(labels[i])

fig.savefig('Ltest_LHS.png')

with open('LHS_cube.txt', 'w') as f:
  np.savetxt(f, sample_scaled)