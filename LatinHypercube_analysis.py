import pynbody, h5py, time, lib_readWrite
import matplotlib.pylab as plt
import numpy as np


# OUTPUT
outposition = "LHS_files/"

sim_to_skip = [4, 13,24] # peculiar simulatinos
paths      = lib_readWrite.get_LHS_paths()

# merger params
stellar_mass_threshold = 1e1 # in Msun

# arrays to write
n_simul     = len(paths)
HMR_snap    = np.full(n_simul, 1e-4)
f_5_snap    = np.full(n_simul, 1e-4)
IC_cube     = np.full((5,n_simul), 1e-4)
addit_IC    = np.zeros((1, n_simul))

# plot for visual check
check_with_plot = False

if check_with_plot:
  fig = plt.figure()
  ax  = fig.subplots(nrows = 1,ncols = 1)#, sharex = True,sharey = True )
  ax.set_xlabel('x [pc]')
  ax.set_ylabel('y [pc]')
  ax.set_aspect('equal')


# start of the computing time count
start_time = time.time()

for j,basepath in enumerate(paths):
  # status
  print()
  print('working on', basepath)

  if np.isin(j, sim_to_skip): 
    print('skipped simulation')
    continue

  # read the IC from summary params
  summary_param_file = lib_readWrite.read_summary_params_file(path = basepath)
  IC_cube[0,j] = summary_param_file.getfloat('HypercubeValues',"l")
  IC_cube[1,j] = summary_param_file.getfloat('HypercubeValues',"k")
  IC_cube[2,j] = summary_param_file.getfloat('HypercubeValues',"mass_ratio")
  
  dm_mass_frac_gal_1   = summary_param_file.getfloat('Gal1',"dm_mass_frac")
  star_mass_frac_gal_1 = summary_param_file.getfloat('Gal1',"star_mass_frac")
  IC_cube[3,j]         = dm_mass_frac_gal_1/star_mass_frac_gal_1 # mass to light ratio
  IC_cube[4,j]         = summary_param_file.getfloat('Gal1',"star_rscale")*1.68 *1e3 # HMR in pc
  
  # additional IC values
  stellar_mass_gal1  = star_mass_frac_gal_1 * summary_param_file.getfloat('Gal1',"m_200")*1e10 # in Msun
  addit_IC[0,j]      = 0.5*stellar_mass_gal1/(4/3*np.pi*IC_cube[4,j]**3) # mean density

  # open the snap 
  number_snap    = lib_readWrite.get_number_of_snaps(basepath=basepath)
  print('using snap', number_snap-1)
  snap_path, snap_FoF_path = lib_readWrite.get_name_i_snap_and_FoF(int(number_snap-1),basepath)
  snap = pynbody.load(str(snap_path))
  snap.physical_units(distance='pc', velocity='km s^-1', mass='Msol')

  #mask the bounded stars
  mask_bound_stars = (snap.s['te']< 0.)

  pynbody.analysis.angmom.faceon(snap.s)

  HMR_snap[j] = np.median(snap.s['r'][mask_bound_stars])
  mask_galaxy_stars = (snap.s['r'][mask_bound_stars] < HMR_snap[j]*30)
  mask_f_5_stars    = (snap.s['r'][mask_bound_stars][mask_galaxy_stars]> HMR_snap[j]*5) 
  f_5 = np.sum(mask_f_5_stars)/np.sum(mask_galaxy_stars)

  f_5_snap[j] = max(1e-4,f_5)

  print('f_5\t',f_5_snap[j])
  print('HMR\t',HMR_snap[j])



# write output
hf = h5py.File(outposition + 'parameter_space.h5', 'w')
hf.create_dataset('IC_cube' , data=IC_cube)
hf.create_dataset('addit_IC', data=addit_IC)
hf.create_dataset('f_5_snap', data=f_5_snap)
hf.create_dataset('HMR_snap', data=HMR_snap)
hf.close()


# time took by the analysis
print()
print("--- took %s seconds ---" % (time.time() - start_time))
print()

exit()






