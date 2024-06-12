# LIBRARY for reading and writing with my data structures
import os, configparser, pynbody
import numpy as np
from scipy.spatial.transform import Rotation as R


def get_LHS_paths(skip = []):
  """
  finds all the paths of the Latin Hypercube Sampling simulations in $WORK

  Args:
    skip (list) if not len 0, the elements in skip are removed from the output list
  Outs:
    paths (arr(str))  
  """
  
  parent_dir = '/g100_work/IscrC_UFD-SHF/lquerci0/LatinHypercubeSampling/mdm_100'
  
  path = sorted([f.path for f in os.scandir(parent_dir) if f.is_dir()])
  
  if len(skip) > 0:
    for index in sorted(skip, reverse=True):
      del path[index]

  return path

def read_summary_params_file(path):
  file_path = os.path.join(path,'summary_params.config')
  config = configparser.ConfigParser()
  summary_param = config.read_file(open(file=file_path, mode='r'))
  return config

def get_number_of_snaps(basepath):
  output_dir = "output"
  path = os.path.join(basepath,output_dir)
  snaps_names  = [f_name for f_name in os.listdir(path) if f_name.startswith('snap_')]  
  
  return len(snaps_names)

def get_name_i_snap_and_FoF(i, basepath):
  FoF_file_name  = 'fof_tab_'+str(i).zfill(3)+'.hdf5'
  snap_file_name = 'snap_'+str(i).zfill(3)+'.hdf5'
  output_dir = "output"
  FoF_path_file_name = os.path.join(basepath,output_dir,FoF_file_name)
  snap_path_file_name    = os.path.join(basepath,output_dir,snap_file_name)
  
  return snap_path_file_name,FoF_path_file_name



def compute_HMR_f5(SimSnap):
  # remove unbound stars
  mask_bound_stars = (SimSnap.s['te']< 0.)
  galaxy = SimSnap.s[mask_bound_stars]
  # center on the stellar component
  CM = pynbody.analysis.halo.center_of_mass(galaxy)
  xx = galaxy['x'] - CM[0]
  yy = galaxy['y'] - CM[1]
  zz = galaxy['z'] - CM[2]

  v = np.array([xx,yy,zz])
  

  # parameters of the rotation
  n_rot = 20 # number of rotations per dimension

  # storing arrays
  HMR = np.zeros(n_rot**3)
  f_5 = np.zeros(n_rot**3)
  i = 0

  # output arrays 
  HMR_out = np.zeros(3)
  f_5_out = np.zeros(3)

  #
  # cycle over variuous rotations
  #

  for alpha in np.linspace(0,360, num = n_rot):
    for beta in np.linspace(0,360, num = n_rot):
      for gamma in np.linspace(0,360, num = n_rot):

        # rotation matrix
        r = R.from_euler('xyz', [alpha, beta,gamma],degrees=True)

        
        #print(r.as_euler('xyz', degrees=True))
        
        # apply the rotation
        v_rot = r.apply(v.T).T

        # compute the 2d radius
        r_2d = np.sqrt(v_rot[0]**2+v_rot[1]**2)
        
        # compute the half-mass radius
        HMR[i] = np.median(r_2d)

        # compute f_5
        mask_galaxy_stars = (r_2d < HMR[i]*30)
        mask_f_5_stars    = (r_2d[mask_galaxy_stars]> HMR[i]*5) 
        f_5[i] = np.sum(mask_f_5_stars)/np.sum(mask_galaxy_stars)

        i = i+1

  HMR_out = np.percentile(HMR, [16,50,84])
  f_5_out = np.percentile(f_5, [16,50,84])

  return HMR_out, f_5_out