import os
import numpy as np
import configparser, datetime
from astropy import units as u
import matplotlib.pyplot as plt
import lib_LHS as lib_LHS


# directories
template_dir  = '/g100/home/userexternal/lquerci0/codes/Templates'
# $HOME
#output_dir    = '/g100/home/userexternal/lquerci0/codes/Ltest_LatinHypercubeSampling/mdm_100'
# $WORK
#output_dir    = '/g100_work/IscrC_UFD-SHF/Ltest_LatinHypercubeSampling/mdm_100'
# $SCRATCH
output_dir    = '/g100_scratch/userexternal/lquerci0/LatinHypercubeSampling/mdm_100'

try:
    os.makedirs(output_dir)
except FileExistsError:
    print("directory already present")
except Exception as error:
    print('not able to make the directory. Error: ', type(error).__name__)
    exit()

# fixed values
m_dm       = 100.
m_star     = 1.
x_distance = 8 * u.kpc

# read the values from file
LHS_cube = np.loadtxt('LHS_cube.txt')
n_simulations = len(LHS_cube)

# read the optimized end file
end_file_array = np.loadtxt('optimized_end_time.txt')
CPUlimit_array = np.loadtxt('optimized_timelimitCPU.txt')


# galaxies masses 
Gal1_Mstar,Gal1_Mdm , Gal2_Mstar ,Gal2_Mdm = lib_LHS.compute_masses_from_LHScube(LHS_cube)

for ith_simulation in range(n_simulations):

    #
    # === The 5 parameters to explore ===
    #
    L          = LHS_cube[ith_simulation, 0] * u.pc**2/u.Myr
    K          = LHS_cube[ith_simulation, 1] * u.pc**2 /u.Myr**2
    Mass_Ratio = LHS_cube[ith_simulation, 2]
    r_param    = LHS_cube[ith_simulation, 3]
    HMR_1      = (LHS_cube[ith_simulation, 4] * u.pc).to(u.kpc).value
    
    HypercubeValues = {}
    HypercubeValues['L']          = L.value
    HypercubeValues['K']          = K.value
    HypercubeValues['Mass_Ratio'] = Mass_Ratio
    HypercubeValues['r_param']    = r_param
    HypercubeValues['HMR_1']      = HMR_1

    # unit conversions
    L_kms = L.to(u.km**2/u.s)
    K_kms = K.to(u.km**2/u.s**2)

    # output directory
    simulation_dir = os.path.join(output_dir,str(ith_simulation).zfill(2))
    
    # mkdir output dir
    try:
        os.mkdir(simulation_dir)
    except Exception as error:
        print("\nUnable to create the simulation directory %s. \nIt might already exist, in that case remove the old files before rereunnig\n" % str(simulation_dir))
        print("error type", type(error).__name__)
        exit()
    print("\n\nmoving to", simulation_dir)

    #
    # === Galaxies quantities ===
    #


    #
    # === Galaxy 1 ===
    #
    Gal1 = {}

    # masses
    Gal1_star_mass = Gal1_Mstar[ith_simulation]
    Gal1_DM_mass   = Gal1_Mdm[ith_simulation]
    Gal1_tot_mass = Gal1_star_mass + Gal1_DM_mass

    Gal1['M_200'] = (Gal1_tot_mass)/1e10
    Gal1['DM_MASS_FRAC'] = Gal1_DM_mass/(Gal1_tot_mass)
    Gal1['DM_NPART']     = int(Gal1_DM_mass/m_dm)
    Gal1['DM_NPART_POT'] = Gal1['DM_NPART']*2
    Gal1['STAR_MASS_FRAC'] = Gal1_star_mass/(Gal1_tot_mass)
    Gal1['STAR_NPART']     = int(Gal1_star_mass/m_star)
    Gal1['STAR_NPART_POT'] = Gal1['STAR_NPART']*2
    Gal1['STAR_RSCALE']    = HMR_1/1.68
    Gal1['STAR_RSCALE_CUT']= 3 * Gal1['STAR_RSCALE']

    # convert numbers to strings
    for y in Gal1:
        Gal1[y] = str(Gal1[y])


    # REPLACE GAL1 file
    gal1_template= os.path.join(template_dir, 'Gal.params.template')
    gal1_output  = os.path.join(simulation_dir  , 'Gal1.params')
    lib_LHS.replace_values_in_template(gal1_template, gal1_output, Gal1)
    print("Template file Gal1  has been processed and result written")


    #
    # === Galaxy 2 ===  
    #
    Gal2 = {}

    # masses
    Gal2_star_mass = Gal2_Mstar[ith_simulation]
    Gal2_DM_mass   = Gal2_Mdm[ith_simulation]
    Gal2_tot_mass  = Gal2_star_mass + Gal2_DM_mass

    Gal2['M_200']          = (Gal2_tot_mass)/1e10 
    Gal2['DM_MASS_FRAC']   = Gal2_DM_mass/(Gal2_tot_mass)
    Gal2['DM_NPART']       = int(Gal2_DM_mass/m_dm)
    Gal2['DM_NPART_POT']   = Gal2['DM_NPART']*2
    Gal2['STAR_MASS_FRAC'] = Gal2_star_mass/(Gal2_tot_mass)
    Gal2['STAR_NPART']     = int(Gal2_star_mass/m_star)
    Gal2['STAR_NPART_POT'] = Gal2['STAR_NPART']*2
    Gal2['STAR_RSCALE']    = HMR_1 * Mass_Ratio**(-1/3)/1.68
    Gal2['STAR_RSCALE_CUT']= 3 * Gal2['STAR_RSCALE']

    # convert numbers to strings
    for y in Gal2:
        Gal2[y] = str(Gal2[y])

    # REPLACE GAL2 file
    gal2_template= os.path.join(template_dir, 'Gal.params.template')
    gal2_output  = os.path.join(simulation_dir  , 'Gal2.params')
    lib_LHS.replace_values_in_template(gal2_template, gal2_output, Gal2)
    print("Template file Gal2  has been processed and result written")

    #
    # === DICE params ===
    #
    dice_sub = {}
    merger_Mass_Ratio = Gal2_tot_mass/Gal1_tot_mass

    dice_sub['XX_2'] = x_distance/(1+merger_Mass_Ratio)
    dice_sub['XX_1'] = - dice_sub['XX_2'] * merger_Mass_Ratio

    dice_sub['VX_2'] = - np.sqrt(2*K_kms/merger_Mass_Ratio)
    dice_sub['VX_1'] = - dice_sub['VX_2'] * merger_Mass_Ratio 

    dice_sub['YY_2'] = (L_kms*(Gal1_tot_mass+Gal2_tot_mass)/(Gal2_tot_mass*(np.abs(dice_sub['VX_2'])+ np.abs(dice_sub['VX_1'])))).to(u.kpc)
    dice_sub['YY_1'] = - dice_sub['YY_2'] * merger_Mass_Ratio

    # convert numbers to strings
    for y in dice_sub:
        dice_sub[y] = str(dice_sub[y].value)


    # REPLACE Dice file
    dice_template= os.path.join(template_dir, 'Dice_merger.config.template')
    dice_output  = os.path.join(simulation_dir  , 'Dice_merger.config')
    lib_LHS.replace_values_in_template(dice_template, dice_output, dice_sub)
    print("Template file dice  has been processed and result written")

    #
    # === SLURM job DICE ===
    #
    job_dice_sub = {}
    job_dice_sub['run_name'] = ith_simulation

    # convert numbers to strings
    for y in job_dice_sub:
        job_dice_sub[y] = str(job_dice_sub[y])
    
    job_dice_template= os.path.join(template_dir, 'job_dice.sh.template')
    job_dice_output  = os.path.join(simulation_dir  , 'job_dice.sh')
    lib_LHS.replace_values_in_template(job_dice_template, job_dice_output, job_dice_sub)
    print("Template file job_dice has been processed and result written")


    #
    # === SLURM job Arepo ===
    #

    # set the hardware 
    job_arepo_sub = {}
    job_arepo_sub['run_name'] = ith_simulation
    job_arepo_sub['nodes'] = 2
    job_arepo_sub['ntasks-per-node'] = 48
    job_arepo_sub['cpus-per-task'] = 1
    # set the computational time
    n_cpus         = job_arepo_sub['nodes'] * job_arepo_sub['ntasks-per-node'] * job_arepo_sub['cpus-per-task']
    CPUlimit_hrs   = CPUlimit_array[ith_simulation]/n_cpus * 1000/m_dm
    job_time_limit = datetime.timedelta(seconds=round(CPUlimit_hrs*3600))
    job_arepo_sub['time']   = job_time_limit
    job_arepo_sub['n_proc'] = n_cpus

    # convert numbers to strings
    for y in job_arepo_sub:
        job_arepo_sub[y] = str(job_arepo_sub[y])
    
    job_arepo_template= os.path.join(template_dir, 'job_arepo.sh.template')
    job_arepo_output  = os.path.join(simulation_dir  , 'job_arepo.sh')
    lib_LHS.replace_values_in_template(job_arepo_template, job_arepo_output, job_arepo_sub)
    print("Template file job_arepo has been processed and result written")

    #
    # === Arepo params ===
    #
    CPUlimit_sec  = CPUlimit_hrs*3600 
    arepo_template= os.path.join(template_dir, 'ArepoParam_FOF.txt.template')
    arepo_output  = os.path.join(simulation_dir  , 'ArepoParam_FOF.txt')
    arepo_sub     = {'TIME_END': str(end_file_array[ith_simulation]), 
                     'TimeLimitCPU' : str(round(CPUlimit_sec))}
    lib_LHS.replace_values_in_template(arepo_template, arepo_output, arepo_sub)
    print("Template file Arepo has been processed and result written")



    
    #
    # === summary file ===
    #

    config = configparser.ConfigParser()

    config['HypercubeValues'] = HypercubeValues
    config['Gal1'] = Gal1
    config['Gal2'] = Gal2
    config['dice'] = dice_sub
    config['arepo']= arepo_sub
    config['job_arepo']= job_arepo_sub 
    config['job_dice'] = job_dice_sub 
    #write
    summary_file   = os.path.join(simulation_dir,"summary_params.config")
    with open(summary_file, 'w') as configfile:
        config.write(configfile)

    print(f"Summary of the params has been written.")
