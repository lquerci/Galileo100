import os
import numpy as np
import configparser, datetime
from astropy import units as u
import matplotlib.pyplot as plt


fig = plt.figure()
axs  = fig.add_subplot()

# computational time from test
CPUlimit_array = np.loadtxt('LHS_files/optimized_timelimitCPU.txt')

# actual computational time
CPUhr_used = np.array([558, # 0
                       91,  # 1
                       573,   # 2
                       94,  # 3
                       0,   # 4
                       278, # 5
                       973, # 6
                       164, # 7
                       211, # 8
                       99,  # 9
                       228, # 10
                       232, # 11
                       114, # 12
                       0,   # 13
                       124, # 14
                       118, # 15
                       576, # 16
                       186, # 17
                       160, # 18
                       197, # 19
                       107, # 20
                       278, # 21
                       259, # 22
                       1066, # 23
                       0,   # 24
                       82, # 25
                       622,  # 26
                       1024,   # 27
                       294,  # 28
                       229,   # 29
                       384, # 30
                       486,   # 31
                       85, # 32
                       0, # 33
                       0,  # 34
                       217, # 35
                       147, # 36
                       654, # 37
                       376,   # 38
                       134, # 39
                       374, # 40
                       106, # 41
                       131, # 42
                       171, # 43
                       412, # 44
                       344, # 45
                       331, # 46
                       165, # 47
                       1019, # 48
                       0,   # 49
                       ])

mask_simul = CPUhr_used > 10

n_simul = len(CPUlimit_array)

ratio = np.zeros(n_simul)

j = 0

for i in range(n_simul):
    if mask_simul[i]:
        ratio[i] = CPUlimit_array[i]*10/ CPUhr_used[i]
        print(ratio[j])
        j = j + 1
    else: print(i)

axs.scatter(CPUhr_used[mask_simul] ,ratio[mask_simul] )

fig.savefig('figures/Ltest_computational_time_saving.png',bbox_inches='tight')
