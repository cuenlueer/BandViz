# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 14:36:33 2021

@author: CU
"""

import Bandplotter_BV as bp
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import ast

def PureBundler1_0(bondtype = '',
            stoff = '',
            buildplot = True,
            fitrange = 10,
            bandcheck = True,
            write_csv_data = False,):
    
    path = './{0}'.format(bondtype)

    print('_______________________________________________') 

    file = open("{0}/{1}/.burai.path".format(path, stoff), "r")
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    
    k_sym = []
    sympoints = []
    for dicts in dictionary["points"]:
        k_sym.append(dicts["coord"])
        sympoints.append(dicts["label"].replace("??",r"$\Gamma$"))

    file.close()

    
    i = 0
    
    bands = np.loadtxt("{0}/{1}/espresso.band1.gnu".format(path, stoff))
    
    K = bands[:,0]

    Range = K.tolist().index(max(k_sym))+1
    bandno = len(bands[:,1])/Range
    k = bands[i*Range:Range*(i+1),0]
    
    

    
    file = open("{0}/{1}/.burai.fermi".format(path, stoff), "r")
    contents = file.read().replace('false', 'False')
    fermdict = ast.literal_eval(contents)
    E_fermi = fermdict["energies"][0] 
    file.close()
    
    if buildplot == True:
        ax = bp.bandploter_ver1_0(workpath = path, solid = '{}'.format(stoff), fermiE = E_fermi, textsize = 16)
    
    
    if bondtype == 'covalent':
        bonding = 0
    elif bondtype == 'ionic':
        bonding = 1
    elif bondtype == 'metallic':
        bonding = 2
    elif bondtype == 'metavalent':
        bonding = 3
    
    baender = []
    label = []
    
    conduction = []
    label_cond = []
    
    valence = []
    label_val = []
    
    
    while i < bandno:
            
        E = bands[i*Range:Range*(i+1),1]-E_fermi
        label.append(str(i+1)), baender.append(E)
        
        i += 1
        
    
    
    j = 0
    l = 0
    
    lowerbounds=[]
    LowerBundles=[]
    
    while j < bandno:
        
        Bj = baender[j]
        Bj_1 = baender[j+1]
        
        under_E_f_ratio = sum((Bj < 0))/len(Bj)
        #print("Under:",under_E_f_ratio)
        if under_E_f_ratio > 0.92:                 #<---- Hier sollte geprüft werden ob das Probleme für Metalle gibt!

            if min(Bj_1) >= max(Bj):
                lowerbounds.append(Bj)
                LowerBundles.append(lowerbounds)
                lowerbounds=[]
                j+=1
                #print('ich funze')
            else:
                lowerbounds.append(Bj)
                j+=1
                #print('ich funze netso')
        
        elif min(Bj) < 0:
            
            if under_E_f_ratio < 0.08: 
                if len(lowerbounds)>0:
                    LowerBundles.append(lowerbounds)
                
                
                
                LowerBundles.append([Bj])
                print('BandNo {0} {1} is quite sus. Metal-like behaviour due to minimum of VB below fermi energy. Will be treated as covalent due to threshold.'.format(stoff,j+1))
                print("minimum Bj:",min(Bj))
                break
            
            else:
                if len(lowerbounds)>0:
                    LowerBundles.append(lowerbounds)
                
                
                LowerBundles.append([Bj])
                print('{0} at band {1}: might be metal if k-point-grid sufficiently dense (?)'.format(stoff,j+1))
                break
        else:
            
            if len(lowerbounds)>0:
                LowerBundles.append(lowerbounds)
            
            
            LowerBundles.append([Bj])
            print('BandNo above E_fermi for {}:'.format(stoff),j+1)
            break
    #____________________________________________________
    if stoff == 'C':
        bogged = LowerBundles             #DEBUGGING ZONE
    #____________________________________________________
    
    LB_len = len(LowerBundles)
    
    
    CB_bundle = LowerBundles[LB_len-1]
    CB_band   = CB_bundle[len(CB_bundle)-1]
    
    for i in LowerBundles:
        DeltaE = max(i[len(i)-1])-min(i[0])
        if buildplot == True and sum(i[-1]) != sum(LowerBundles[-1][-1]):
           ax.annotate(r'$E_\mathrm{b}$'+r'$ = {}$'.format(round(DeltaE,11)), xy = (1,max(i[len(i)-1])-(DeltaE/2)), color='#C00000', size = 'xx-large')
    
    #if buildplot == True:
    #    ax.plot(k, CB_band, 'b') <------------- BLUE BAND ENABLE HERE!
    
    CB_max = max(CB_band)
    CB_min = min(CB_band)
    
    E_k_min_index = CB_band.tolist().index(min(CB_band),10)
    k_0_CB = k[E_k_min_index]
    E_0_CB = CB_band[E_k_min_index]
    
    def func_CB(x, a_CB):

        return a_CB * (x-k_0_CB)**2 + E_0_CB
    
    E_FitMe_CB = CB_band[E_k_min_index-fitrange:E_k_min_index+fitrange]
    k_fit_CB   = k[E_k_min_index-fitrange:E_k_min_index+fitrange]
    
    popt_CB, pcov_CB = curve_fit(func_CB, k_fit_CB, E_FitMe_CB)
    a_CB = popt_CB[0]
    a_cov_CB = pcov_CB[0][0]
    
    #if buildplot == True:
    #    ax.plot(k_fit_CB, func_CB(k_fit_CB, *popt_CB), 'g--',
    #         label=r'fit: $a_\mathrm{CB}$=%5.3f' % tuple(popt_CB))
    
    
    if sum(sum(CB_bundle)) != sum(sum(LowerBundles[LB_len-2])):
        b_bundle  = LowerBundles[LB_len-2]
        b_band    = b_bundle[len(b_bundle)-1]
        b_band_width = max(b_band)-min(b_band)
        
        #if buildplot == True:
        #    ax.plot(k, b_band, 'r') <------------- RED BAND ENABLE HERE!
    
        b_count = len(b_bundle)
        b_width_max = max(b_band)
        b_width_min = min(b_bundle[0])
        
        E_k_max_index = b_band.tolist().index(max(b_band),10)
        k_0_b = k[E_k_max_index]
        E_0_b = b_band[E_k_max_index]
        
        def func_VB(x, a_b):

            return a_b * (x-k_0_b)**2 + E_0_b
        
        E_FitMe_b = b_band[E_k_max_index-fitrange:E_k_max_index+fitrange]
        k_fit_b   = k[E_k_max_index-fitrange:E_k_max_index+fitrange]
        
        popt_b, pcov_b = curve_fit(func_VB, k_fit_b, E_FitMe_b)
        a_b = popt_b[0]
        a_cov_b = pcov_b[0][0]
        
        #if buildplot == True:
        #    ax.plot(k_fit_b, func_VB(k_fit_b, *popt_b), 'g--',
        #         label=r'fit: $a_\mathrm{b}$=%5.3f' % tuple(popt_b))
        
    else:
        print("CB and b equal for {}.".format(stoff))
        
        b_count = 1
        b_width_max = max(CB_band)
        b_width_min = min(CB_band)
        b_band_width = max(b_band)-min(b_band)
    
    if sum(sum(LowerBundles[LB_len-1])) != sum(sum(LowerBundles[LB_len-3])):
        f_bundle  = LowerBundles[LB_len-3]
        f_band    = f_bundle[len(f_bundle)-1]
        
        #if buildplot == True:
        #    ax.plot(k, f_band, 'g')
        
        f_count = len(LowerBundles[len(LowerBundles)-3])
        f_width_max = max(f_band)
        f_width_min = min(f_bundle[0])
        
    else:
        print("b and f equal for {}.".format(stoff))
        
        f_count = b_count
        f_width_max = max(b_band)
        f_width_min = min(b_bundle[0])
    
    
    
    E_BG = CB_min-b_width_max
    E_FG = b_width_min-f_width_max
    
    if buildplot == True:
        ax.annotate(r'$E_\mathrm{g} = $'+'{}'.format(round(E_BG,11)), xy = (1,b_width_max+(E_BG/3)), color = '#203864', size = 'xx-large')
        #ax.annotate(r'$E_\mathrm{FG} = $'+'{}'.format(round(E_FG,11)), xy = (1,f_width_max+(E_FG/3)))
        
    
    if min(CB_band) >= max(b_band) or 0.1 > sum((CB_band < 0))/len(CB_band):
        if k_0_b == k_0_CB:
            direct = 1
        else:
            direct = 0
    else:
        direct = -1
        print('ALERT: CONDUCTION DETECTED! Material: {}'.format(stoff))
    
    
    
    
    ls_hlines = "solid"
    hlines_color_CB = '#203864'
    hlines_color_b = '#C00000'
    hlines_color_f = 'green'
    
    if bandcheck and buildplot == True:
        #ax.hlines(f_width_max, xmin = k[0], xmax = k[len(k)-1], linestyle =  ls_hlines, colors = hlines_color_f)
        #ax.hlines(f_width_min, xmin = k[0], xmax = k[len(k)-1], linestyle =  ls_hlines, colors = hlines_color_f)
        ax.hlines(b_width_max, xmin = k[0], xmax = k[len(k)-1], linestyle =  ls_hlines, colors = hlines_color_b)
        ax.hlines(b_width_min, xmin = k[0], xmax = k[len(k)-1], linestyle =  ls_hlines, colors = hlines_color_b)
        #ax.hlines(CB_max, xmin = k[0], xmax = k[len(k)-1], linestyle =  ls_hlines, colors = hlines_color)
        ax.hlines(CB_min, xmin = k[0], xmax = k[len(k)-1], linestyle =  ls_hlines, colors = hlines_color_CB)
    
    print('_______________________________________________')  
    
    if buildplot == True:
        plt.legend(fontsize = 'large')
        #plt.tight_layout() <- das bringt nichts.
        plt.show(block=False)