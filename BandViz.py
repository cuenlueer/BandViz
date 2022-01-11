# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 17:26:09 2021

@author: CU
"""

from tkinter import *
import Bundler_BV as bndl
import os
import pandas as pd
df = pd.read_excel('appendix_metadata_BV.xlsx')

y = []
root = Tk()
root.title("BandViz")
try:
    root.iconbitmap('icon.ico')
except:
    None




def ionic():
    path = './ionic_appendix'
    solids = os.listdir(path)
    for i in y:
        i.destroy()
    l=1
    n=0
    for i in solids:
        buttonlabel_solid = df.loc[df['solid_BV'] == '{}'.format(i), 'solid_button'].iloc[0]
        buttonlabel_structure = df.loc[df['solid_BV'] == '{}'.format(i), 'structure_BV'].iloc[0]
        buttonlabel = buttonlabel_solid + '\n' + buttonlabel_structure
        
        solidBut = Button(root, text = buttonlabel, fg = 'white', bg = 'black', command =lambda i=i: bndl.PureBundler1_0(bondtype='ionic_appendix', stoff=i))
        solidBut.grid(row=l, column=n)
        n+=1
        if n % 10 == 0:
            l+=1
            n=0
            
        y.append(solidBut)



def cova():
    path = './covalent_appendix'
    solids = os.listdir(path)
    for i in y:
        i.destroy()
    l=1
    n=0
    for i in solids:
        buttonlabel_solid = df.loc[df['solid_BV'] == '{}'.format(i), 'solid_button'].iloc[0]
        buttonlabel_structure = df.loc[df['solid_BV'] == '{}'.format(i), 'structure_BV'].iloc[0]
        buttonlabel = buttonlabel_solid + '\n' + buttonlabel_structure
        
        solidBut = Button(root, text = buttonlabel, fg = 'white', bg = 'red', command =lambda i=i: bndl.PureBundler1_0(bondtype='covalent_appendix', stoff=i))
        solidBut.grid(row=l, column=n)
        n+=1
        if n % 10 == 0:
            l+=1
            n=0
        
        y.append(solidBut)




def mv():
    path = './metavalent_appendix'
    solids = os.listdir(path)
    for i in y:
        i.destroy()
    l=1
    n=0
    for i in solids:
        buttonlabel_solid = df.loc[df['solid_BV'] == '{}'.format(i), 'solid_button'].iloc[0]
        buttonlabel_structure = df.loc[df['solid_BV'] == '{}'.format(i), 'structure_BV'].iloc[0]
        buttonlabel = buttonlabel_solid + '\n' + buttonlabel_structure
        
        solidBut = Button(root, text = buttonlabel, fg = 'white', bg = 'green', command =lambda i=i: bndl.PureBundler1_0(bondtype='metavalent_appendix', stoff=i))
        solidBut.grid(row=l, column=n)
        n+=1
        if n % 10 == 0:
            l+=1
            n=0
        
        y.append(solidBut)
        
        
        
        
ionButton = Button(root, text='Ionic', fg = 'white', bg = 'black', command = ionic)
covButton = Button(root, text='Covalent', fg = 'white', bg = 'red', command = cova)
mvButton = Button(root, text='Metavalent', fg = 'white', bg = 'green', command = mv)




ionButton.grid(row=0, column=0, padx=10)
covButton.grid(row=0, column=1, padx=10)
mvButton.grid(row=0, column=2, padx=10)



root.mainloop()