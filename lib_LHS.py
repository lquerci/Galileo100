# LIBRARY for LA
import numpy as np

def compute_masses_from_LHScube(LHS_cube):
  n_simul = len(LHS_cube)
  Gal1_Mstar = np.zeros(n_simul)
  Gal1_Mdm   = np.zeros(n_simul)
  Gal2_Mstar = np.zeros(n_simul)
  Gal2_Mdm   = np.zeros(n_simul)
  
  Mstar_tot = 6000
  MtoL_min  = 6000
  MtoL_max  = 100000
   
  # stellar mass
  Gal2_Mstar = Mstar_tot /(1+LHS_cube[:,2])
  Gal1_Mstar = Gal2_Mstar * LHS_cube[:,2]
  
  # mass to light ratio
  MtoL = MtoL_min + LHS_cube[:,3]*(MtoL_max - MtoL_min)
  Gal1_Mdm = Gal1_Mstar * MtoL
  Gal2_Mdm = Gal2_Mstar * MtoL
      

  return Gal1_Mstar,Gal1_Mdm , Gal2_Mstar ,Gal2_Mdm

def replace_values_in_template(template_file, output_file, substitutions):
    """
    Replace ${values} in the template file and write the modified content to the output file.
    
    Args:
        template_file (str): Path to the template file.
        output_file (str): Path to the output file.
        substitutions (dict): Dictionary containing key-value pairs for substitutions.
    """
    with open(template_file, 'r') as f:
        template_content = f.read()

    for key, value in substitutions.items():
        template_content = template_content.replace(f'${{{key}}}', value)

    with open(output_file, 'w') as f:
        f.write(template_content)
