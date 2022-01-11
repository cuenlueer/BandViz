# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 12:45:35 2021

@author: CU
"""
import numpy as np
import os
import ast


def DOSextractor(workpath, solid):
    path = '{0}/{1}'.format(workpath,solid)
    
    file = open(path+'/.burai.fermi', "r")
    contents = file.read().replace('false', 'False')
    fermdict = ast.literal_eval(contents)
    E_fermi = fermdict["energies"][0] 
    file.close()
    
    items = os.listdir(path)
    
    yar = []
    
    atm1 = []
    atm2 = []
    
    orbitallist1 = []
    orbitallist2 = []
    
    for i in items:
        
        if i[:18] == 'espresso.pdos_atm#':
           yar.append(i) 
        
        if i == 'espresso.pdos_tot':
            ptotal = np.loadtxt(path+'/'+'espresso.pdos_tot')
        
        if i == 'espresso.dos':
            total = np.loadtxt(path+'/'+'espresso.dos')
    
    print(yar,'\n')
     
    atomname1 = [i for i in yar if i[20:22] == yar[0][20:22]]
    atomname2 = [i for i in yar if i[20:22] != yar[0][20:22] and i[20:22] == yar[len(yar)-1][20:22]]
    print(atomname1,'\n')
    print(atomname2,'\n')
    
    for i in atomname1:
        orbital = i[-2]
        orbitallist1.append(orbital)
        atm1.append(np.loadtxt(path+'/'+i))
        
    for i in atomname2:
        orbital = i[-2]
        orbitallist2.append(orbital)
        atm2.append(np.loadtxt(path+'/'+i))
       
    if len(yar) == len(atomname1)+len(atomname2):
        print('All wfc-files haven been found!')
    else:
        print('ALERT! NOT ALL WFC-FILES USED! PDOS-OUTPUTS CORRUPTED!')
    
    #LABELINGAREA______________________________________________________________
    
    constituent1 = atomname1[0][20:22]
    if constituent1[1] == ')':
        constituent1 = constituent1[0]

    try:
        constituent2 = atomname2[0][20:22]
        if constituent2[1] == ')':
            constituent2 = constituent2[0]
    except:
        constituent2 = ''
        print('No second constituent.')
    #LABELINGAREA______________________________________________________________
    
    DOS = [atm1,atm2,ptotal,total]
    
    s1 = np.zeros(len(atm1[0][:,0]))
    p1 = np.zeros(len(atm1[0][:,0]))
    d1 = np.zeros(len(atm1[0][:,0]))
    i=0
    while i < len(orbitallist1):
        
        if orbitallist1[i] == 's':
           s1 = atm1[i][:,2]+s1
        
        if orbitallist1[i] == 'p':
           p1 = atm1[i][:,2]+atm1[i][:,3]+atm1[i][:,4]+p1
        
        if orbitallist1[i] == 'd':
           d1 = atm1[i][:,2]+atm1[i][:,3]+atm1[i][:,4]+atm1[i][:,5]+atm1[i][:,6]+d1
        
        i+=1
    
    print(orbitallist1)    
    
    try:
        s2 = np.zeros(len(atm2[0][:,0]))
        p2 = np.zeros(len(atm2[0][:,0]))
        d2 = np.zeros(len(atm2[0][:,0]))
    
        i=0
        while i < len(orbitallist2):
            
            if orbitallist2[i] == 's':
               s2 = atm2[i][:,2]+s2
    
            if orbitallist2[i] == 'p':
               p2 = atm2[i][:,2]+atm2[i][:,3]+atm2[i][:,4]+p2
    
            if orbitallist2[i] == 'd':
               d2 = atm2[i][:,2]+atm2[i][:,3]+atm2[i][:,4]+atm2[i][:,5]+atm2[i][:,6]+d2
    
            i+=1   
    
        print(orbitallist2)
    except:
        print('This compound seems to have only one constituent.')
        s2 = np.zeros(len(atm1[0][:,0]))
        p2 = np.zeros(len(atm1[0][:,0]))
        d2 = np.zeros(len(atm1[0][:,0]))
        
    spd1 = s1+p1+d1
    spd2 = s2+p2+d2
    
    E = DOS[2][:,0]-E_fermi
    dos = DOS[2][:,1]
    pdos = DOS[2][:,2]
    
    totaldos = DOS[3][:,1]
    inttotaldos = DOS[3][:,2]
    E_total = DOS[3][:,0]-E_fermi
    return DOS,E,s1,p1,d1,s2,p2,d2,spd1,spd2,dos,pdos,totaldos,inttotaldos,E_total,constituent1,constituent2


'''workpath = './ionic'#
solid = 'CsF'#

DOS,E,s1,p1,d1,s2,p2,d2,spd1,spd2,dos,pdos,totaldos,inttotaldos,E_total,constituent1,constituent2 = DOSextractor(workpath, solid)

for i in DOS,E,s1,p1,d1,s2,p2,d2,spd1,spd2,dos,pdos,totaldos,inttotaldos,E_total:
    i[i==0] = np.nan

plt.figure()
plt.tight_layout()

#plt.plot(E, s1, 'red', label = 'Donor s')
#plt.plot(E, p1, 'green')
#plt.plot(E, d1, 'blue')
#plt.plot(E, s2, 'orange')
#plt.plot(E, p2, 'yellow')
#plt.plot(E, d2, 'purple')
plt.plot(E, dos, 'red')
#plt.plot(E, pdos, 'grey')
#plt.plot(E, spd1, 'pink')
#plt.plot(E, spd2, 'teal')
plt.plot(E_total, totaldos, 'black')
#plt.plot(E_total, inttotaldos, 'black')


plt.legend()
#plt.title(solid+' - Electronic band structure', **font)
plt.ylabel('DOS')
plt.xlabel('Energy/eV')
#annotate('yar', (2,2))
plt.yticks()
#plt.xticks(k_sym, sympoints, rotation='horizontal',**font)
plt.grid()'''