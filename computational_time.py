import os
import numpy as np
import configparser, datetime
from astropy import units as u
import matplotlib.pyplot as plt


fig = plt.figure()
axs  = fig.add_subplot()

# computational time from test
CPUlimit_array = np.loadtxt('optimized_timelimitCPU.txt')

# actual computational time
CPUhr_used = np.array([558, # 0
                       91,  # 1
                       0,   # 2
                       94,  # 3
                       0,   # 4
                       278, # 5
                       0,   # 6
                       164, # 7
                       211, # 8
                       99,  # 9
                       228, # 10
                       232, # 11
                       114, # 12
                       0,   # 13
                       124, # 14
                       118, # 15
                       0, # 16
                       0, # 17
                       160, # 18
                       0, # 19
                       107, # 20
                       0, # 21
                       0, # 22
                       0, # 23
                       0,   # 24
                       ])

mask_simul = CPUhr_used > 10

n_simul = len(CPUhr_used[CPUhr_used > 10])

ratio = np.zeros(n_simul)

j = 0

for i in range(25):
    if mask_simul[i]:
        ratio[j] = CPUlimit_array[i]*10/ CPUhr_used[i]*0.7
        j = j + 1

axs.scatter(CPUhr_used[mask_simul] ,ratio )

fig.savefig('figures/Ltest_computational_time_saving.png',bbox_inches='tight')
