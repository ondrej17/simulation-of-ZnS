#!/usr/bin/env python

# setup backend for matplotlib
import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

# LaTeX text rendering
font = {'family' : 'serif',
        'size'   : 15}
plt.rc('font', **font)
plt.rc('text', usetex=True)
plt.figure(num=None, figsize=(6.4, 4.8), dpi=600, facecolor='w', edgecolor='k')

# load DOS data
data = np.loadtxt('ZnS-RS.dos',skiprows=1)

energy = data[:,0]
dos = data[:,1]
int_dos = data[:,2]

# find Fermi energy in non-selfconsistent calculation
E_Fermi = float(open('ZnS-RS.dos','r').readline().split()[-2])
#lines = open('si.nscf.out','r').readlines()
#for line in lines:
#    if 'Fermi' in line:
#        E_Fermi = float(line.split()[-2])

plt.plot(energy-E_Fermi,dos,color='black',lw=0.2)
ylim = plt.ylim()
plt.vlines(0,ylim[0],ylim[1],colors='#66ccff',linestyles='solid',lw = 0.2)
plt.xlabel(r'$E-E_F$ [eV]')
plt.ylabel(r'density of states')
plt.savefig("dos-ZnS-RS.png")
