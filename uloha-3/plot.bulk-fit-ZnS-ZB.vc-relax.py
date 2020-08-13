#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

def eos(V,b,bd):
    V0_m = V[0]*np.ones(len(V))
    return 3/2*b*(np.power(V0_m/V,7/3)-np.power(V0_m/V,5/3))*(1+3/4*(bd-4)*(np.power(V0_m/V,2/3)-1))

def get_p_V():
    pV = []
    for root, directories, files in os.walk("../vc-relax-ZnS-ZB"):
        for directory in sorted(directories):
            if "vc-relax-" in directory:
                try:
                    p = float(directory[9:])

                    output = open(root+"/"+directory+"/vc-relax.out").read()

                    start_flag = output.rfind('new unit-cell volume')
                    end_flag = output.find('\n',start_flag)
                    V = float(output[start_flag:end_flag].split()[-3])

                    pV.append([p,V])
                except:
                    print('error')
                    pass
    return np.array(sorted(pV, key=lambda x: x[0]))

pV = get_p_V()
p = pV[:,0]/10  # GPa
V = pV[:,1]     # A^3

print("p =", p)
print("V =", V)
popt, pcov = curve_fit(eos,V,p,bounds=(0,[1000.0,100.0]))
print('Bulk modulus:\t{} GPa'.format(popt[0]))
print('Derivation of bulk modulus at p=0:\t{}'.format(popt[1]))

v_calc = np.linspace(V[0],V[-1],101)
p_calc = eos(v_calc,*popt)

plt.plot(p,V,'bo',label='vc-relax-ZnS-ZB data')
plt.plot(p_calc,v_calc,'r-',label='fit: B={:.3f} GPa, B\'={:.3f}'.format(*popt))
plt.xlabel('tlak [GPa]')
plt.ylabel('objem [A^3]')
plt.legend()
plt.tight_layout()
plt.savefig("bulk-fit-ZnS-ZB.png")
