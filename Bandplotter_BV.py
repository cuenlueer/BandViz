# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 17:16:48 2021

@author: CU
"""
import ast
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from DOSextractor_BV import DOSextractor

import pandas as pd

plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

def bandploter_ver1_0(solid = "", workpath = "", fermiE = 0, textsize = 32):
    font = {'size'   : textsize}
    
    file = open("{0}/{1}/.burai.path".format(workpath, solid), "r")
    
    contents = file.read()
    
    dictionary = ast.literal_eval(contents)
    
    k_sym = []
    sympoints = []
    for dicts in dictionary["points"]:
        k_sym.append(dicts["coord"])
        sympoints.append(dicts["label"].replace("??",r"$\Gamma$"))
    
    file.close()

    i=0
    while i < len(k_sym):
        if '1' in sympoints[i]:
            sympoints[i] = sympoints[i][0]+r'$_{%s}$' % sympoints[i][1]
        if k_sym[i-1] == k_sym[i] and (i-1) != -1:
            sympoints[i] = sympoints[i].replace(sympoints[i],sympoints[i-1]+r"$|$"+sympoints[i])
        i+=1
    
    i = 0
    
    E = np.array([])
    
    #k_sym = [0, 1, 1.5, 1.8536, 2.9142, 3.7802, 4.3926, 4.7462, 5.4533, 6.0656, 6.4192]
    #sympoints = [r'$\Gamma$', 'X','W', 'K', r'$\Gamma$', 'L', 'U', 'W', 'L', r'K$|$U', 'X']
    
    bands = np.loadtxt("{0}/{1}/espresso.band1.gnu".format(workpath, solid))
    K = bands[:,0]
    
    Range = K.tolist().index(max(k_sym))+1
    k = bands[i*Range:Range*(i+1),0]
    bandno = (len(bands[:,1])/Range)
    print('Number of bands plotted:',bandno)
    
    solidlabel_splitted = solid.split('_')
    print(solidlabel_splitted)
    if len(solidlabel_splitted) == 2 and 'U' == solidlabel_splitted[-1][0] or 'R3m' == solidlabel_splitted[-1]:
        solidlabel = solidlabel_splitted[0]+'$_\mathrm{%s}$' % solidlabel_splitted[-1]
    else:
        solidlabel = solidlabel_splitted[0]
    
    fig = plt.figure(figsize = (12.8,7.2))
    
    try:
        df = pd.read_excel('appendix_metadata_BV.xlsx')
        structure = df.loc[df['solid_BV'] == '{}'.format(solid), 'structure_BV'].iloc[0]
        if structure == 'Fm-3m':
            structurelabel = r'Fm$\bar{3}$m'
        elif structure == 'Pnma':
            structurelabel = 'Pnma'
        elif structure == 'R3m':
            structurelabel = 'R3m'
        elif structure == 'P4/nmm':
            structurelabel = 'P4/nmm'
        elif structure == 'Pm-3m':
            structurelabel = r'Pm$\bar{3}$m'
        elif structure == 'Fd-3m':
            structurelabel = r'Fd$\bar{3}$m'
        elif structure == 'F-43m':
            structurelabel = r'F$\bar{4}3$m'
        elif structure == 'P6_3mc':
            structurelabel = 'P6$_3$mc'
        else:
            structurelabel = ''
        
        solidlabel = solidlabel +' ('+structurelabel+') '
    except:
        solidlabel = solidlabel
    
    fig.suptitle(solidlabel+' - Electronic band structure', **font)
    gs = gridspec.GridSpec(1, 3, width_ratios=[3, 1, 1]) 
    gs.update(wspace=0, hspace=0)
    ax0 = fig.add_subplot(gs[0])
    plt.xticks(k_sym, sympoints, rotation='horizontal',**font)
    
    
    while i < bandno:
        Ei = np.append(E,bands[i*Range:Range*(i+1),1])-fermiE
        #Dieses "Ei" ist kein "E" mit index i. Könnte genauso gut alles andere da stehen.
        i = i+1        
        ax0.plot(k, Ei, 'black')
    
    
    ax0.set_xlabel('high symmetry points', **font)
    ax0.set_ylabel(r'$E-E_\mathrm{F}$ (eV)', **font)
    ax0.set_xlim([0,k[len(k)-1]])
    ax0.tick_params(axis='both', labelsize=16)
    ax0.grid()
    
    try:
        DOS,E,s1,p1,d1,s2,p2,d2,spd1,spd2,dos,pdos,totaldos,inttotaldos,E_total,constituent1,constituent2 = DOSextractor(workpath, solid)
        ax0.set_ylim(ymax = max(E)+1)
        
        #DELTE THIS ZONE WHEN DONE__________________________________________
        #ax0.set_ylim(-9, 6)
        #DELTE THIS ZONE WHEN DONE__________________________________________
        
    except:
        DOS,E,s1,p1,d1,s2,p2,d2,spd1,spd2,dos,pdos,totaldos,inttotaldos,E_total = np.zeros(15)
        constituent1 = ''
        constituent2 = ''
        print('DOS-Extractor failed to retrieve DOS-Data.')
    
    ax1 = fig.add_subplot(gs[1], sharey = ax0)
    
    #ax1.plot(pdos,E,label = 'pDOS', color='grey') <------------- GREY DOS ENABLE HERE!
    ax1.plot(dos,E,label = 'DOS', color='black')
    
    ax1.plot(s1,E,linestyle = 'dashed',label = 's - {}'.format(constituent1))
    ax1.plot(p1,E,linestyle = 'dashed',label = 'p - {}'.format(constituent1))
    ax1.plot(d1,E,linestyle = 'dashed',label = 'd - {}'.format(constituent1))
    if constituent2 != '':
        ax1.plot(s2,E,color = '#1f77b4',label = 's - {}'.format(constituent2))
        ax1.plot(p2,E,color = '#ff7f0e',label = 'p - {}'.format(constituent2))
        ax1.plot(d2,E,color = '#2ca02c',label = 'd - {}'.format(constituent2))
    
    ax1.set_xlabel('states/eV', **font)
    ax1.set_xlim(xmin=0)
    ax1.tick_params(axis='both', labelsize=16)
    ax1.xaxis.tick_top()
    ax1.grid()
    plt.setp(ax1.get_yticklabels(), visible=False)
    

    #DELTE THIS ZONE WHEN DONE__________________________________________
    #ax1.set_xlim(0, 2.5)
    #DELTE THIS ZONE WHEN DONE__________________________________________
    
    ax2 = fig.add_subplot(gs[2], sharey = ax0, sharex = ax1)
    
    #ax2.plot(spd1+spd2,E,label = 'sum', color = 'grey') <------------- GREY DOS ENABLE HERE!
    ax2.plot(totaldos,E_total,label = 'total', color = 'black')
    
    ax2.plot(spd1,E,color = '#d62728',linestyle = 'dashed',label = '{}'.format(constituent1))
    if constituent2 != '':
        ax2.plot(spd2,E,color = '#9467bd',label = '{}'.format(constituent2))
        
    ax2.set_xlim(xmin=0)
    ax2.tick_params(axis='both', labelsize=16)
    ax2.grid()
    plt.setp(ax2.get_yticklabels(), visible=False)
    
    
    ax1.legend(fontsize = 'large')
    plt.tight_layout()
    return ax0