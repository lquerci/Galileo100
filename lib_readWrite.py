# LIBRARY for reading and writing with my data structures
import os, configparser

def get_LHS_paths(skip = []):
  """
  finds all the paths of the Latin Hypercube Sampling simulations in $SCRATCH

  Args:
    skip (list) if not len 0, the elements in skip are removed from the output list
  Outs:
    paths (arr(str))  
  """
  
  parent_dir = '/g100_scratch/userexternal/lquerci0/LatinHypercubeSampling/mdm_100'
  
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
