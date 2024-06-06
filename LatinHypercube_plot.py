import pynbody, h5py, time, lib_LHS, lib_readWrite
import matplotlib.pylab as plt
import numpy as np

# File
folder_position = "LHS_files/"
filename        = folder_position +"parameter_space.h5"

hf = h5py.File(str(filename), 'r')
IC_LH  = np.array(hf.get('IC_cube'))
addit_IC = np.array(hf.get('addit_IC'))
f_5_snap = np.array(hf.get('f_5_snap'))
HMR_snap = np.array(hf.get('HMR_snap'))
hf.close()

temp    = IC_LH
temp_f5 = f_5_snap

IC_LH    = np.delete(IC_LH,    [4, 13,24,33,34,49], axis=1) 
addit_IC = np.delete(addit_IC, [4, 13,24,33,34,49], axis=1) 
f_5_snap = np.delete(f_5_snap, [4, 13,24,33,34,49], axis=0) 
HMR_snap = np.delete(HMR_snap, [4, 13,24,33,34,49], axis=0) 

# PLOT
plt.rc('font', family='STIXGeneral',size=15)


if 0:
    # f_5 plot
    fig_f_5 = plt.figure(figsize=(15,5))
    fig_f_5.subplots_adjust(hspace=0.0,wspace=0.1)
    axs_f_5 = fig_f_5.subplots(nrows= 1,ncols= 6, sharey = 'row')

    x_axis = ['L [pc^2 Myr^-1]', 'K [pc^2 Myr^-2]',r'$M_1/M_2$', r'$M_{dm}/M_\star$', r"$R_{1/2} [pc]$",r'$\rho_0$ [$M_\odot$ $pc^{-3}$]']

    for col in range(6):
        if col== 5:
            axs_f_5[col].scatter(addit_IC[0,:], f_5_snap)
        else:    
            axs_f_5[col].scatter(IC_LH[col,:], f_5_snap)
        #axs_f_5[col].scatter(temp[col,[4,13]], temp_f5[[4,13]])
        #axs_f_5[col].scatter(temp[col,[24]], temp_f5[[24]])
        axs_f_5[col].set_xscale('log')
        axs_f_5[col].set_yscale('log')
        #axs_f_5[col].set_ylim(4e-4, 0.11)
        axs_f_5[col].set_xlabel(x_axis[col])
        axs_f_5[col].axhline(0.1, color='red', linestyle='--')
        if col == 2:
            x_min = np.min(IC_LH[col,:])
            pos_text = np.array((x_min*1.01, 0.080))
            axs_f_5[col].text(*pos_text,'Tuc II', fontsize=12, color='red')

        
    axs_f_5[0].set_ylabel(r'$f_5$')

    fig_f_5.savefig(folder_position+"f5.png",bbox_inches='tight')

if 1:
    # f_5 AND HMR plot
    fig_f5HMR = plt.figure(figsize=(15,8))
    fig_f5HMR.subplots_adjust(hspace=0.0,wspace=0.0)
    axs_f5HMR = fig_f5HMR.subplots(nrows= 2,ncols= 6, sharey = 'row', sharex= 'col')

    x_axis = ['L [pc^2 Myr^-1]', 'K [pc^2 Myr^-2]',r'$M_1/M_2$', r'$M_{dm}/M_\star$', r"$R_{1/2} [pc]$",r'$\rho_0$ [$M_\odot$ $pc^{-3}$]']

    for col in range(6):

        if col== 5:
            axs_f5HMR[0,col].scatter(addit_IC[0,:], f_5_snap)
            axs_f5HMR[1,col].scatter(addit_IC[0,:], HMR_snap)
        else:    
            axs_f5HMR[0,col].scatter(IC_LH[col,:], f_5_snap)
            axs_f5HMR[1,col].scatter(IC_LH[col,:], HMR_snap)
        axs_f5HMR[0,col].set_xscale('log')
        axs_f5HMR[1,col].set_xscale('log')
        axs_f5HMR[0,col].set_yscale('log')
        axs_f5HMR[1,col].set_xlabel(x_axis[col])
        axs_f5HMR[0,col].axhline(0.1, color='red', linestyle='--')
        axs_f5HMR[1,col].axhline(140, color='red', linestyle='--')
        if col == 2:
            x_min = np.min(IC_LH[col,:])
            pos_text_f_5 = np.array((x_min*1.01, 0.080))
            pos_text_HMR = np.array((x_min*1.01, 145))
            axs_f5HMR[0,col].text(*pos_text_f_5,'Tuc II', fontsize=12, color='red')
            axs_f5HMR[1,col].text(*pos_text_HMR,'Tuc II', fontsize=12, color='red')

        
    axs_f5HMR[0,0].set_ylabel(r'$f_5$')
    axs_f5HMR[1,0].set_ylabel(r'$R_{1/2} [pc]$')

    fig_f5HMR.savefig(folder_position+"f5_HMR.png",bbox_inches='tight')