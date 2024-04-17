import pynbody
import matplotlib.pyplot as plt
import numpy as np


snap_path_filename   = '/g100_scratch/userexternal/lquerci0/LatinHypercubeSampling/mdm_100/00/output/snap_023.hdf5' 
out_position         = '/g100/home/userexternal/lquerci0/codes/figures/' 
arepo_snap           = pynbody.load(str(snap_path_filename))
arepo_snap.physical_units(distance='kpc', velocity='km s^-1', mass='Msol')

pynbody.analysis.angmom.faceon(arepo_snap.s)

HMR_snap = np.median(arepo_snap.s['r'])

#mask the bounded stars
mask_bound_stars = (arepo_snap.s['te']< 0.)

mask_galaxy_stars = (arepo_snap.s['r'][mask_bound_stars] < HMR_snap*30)
mask_f_5_stars    = (arepo_snap.s['r'][mask_bound_stars][mask_galaxy_stars]> HMR_snap*5) 
f_5 = np.sum(mask_f_5_stars)/np.sum(mask_galaxy_stars)

print(HMR_snap)
print(f_5)


xx_stars = arepo_snap.s['x']
yy_stars = arepo_snap.s['y']

xx_dm    = arepo_snap.dm['x']
yy_dm    = arepo_snap.dm['y']

fig = plt.figure()
ax  = fig.add_subplot()
ax.set_aspect('equal')

ax.scatter(xx_dm  ,yy_dm  ,color = 'gray', alpha=0.01)
ax.scatter(xx_stars,yy_stars, alpha=0.5)
ax.set_xlim(-10,10)
ax.set_ylim(-10,10)
ax.set_xlabel('x[kpc]')
ax.set_ylabel('y[kpc]')


fig.savefig(out_position+'Ltest_mdm_100_snap'+str(23).zfill(3)+'_2dscatter.png')