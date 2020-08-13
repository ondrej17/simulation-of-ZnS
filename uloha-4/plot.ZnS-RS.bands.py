import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import os
import re

def dist(a,b):
    # calculate the distance between vector a and b
    d = ((a[0]-b[0]) ** 2 + (a[1]-b[1]) ** 2 + (a[2]-b[2]) ** 2)**0.5
    return d

def read_fermi(file_name):
    # Read the fermi energy in scf.out
    fermi = 0
    with open(file_name, "r") as f:
        lines = f.readlines()
    for line in lines:
        if "the Fermi energy" in line:
            fermi = float(line.split()[4])
    
    return fermi

def read_bnd(file_name):
    # Read the bands in Band.dat
    coord_regex = r"^\s+(.\d+.\d+)\s+(.\d+.\d+)\s+(.\d+.\d+)$"
    x_coord = []
    x = []
    x_label_pos = []
    bands = dict()

    with open(file_name, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i]
        match = re.match(coord_regex,line)
        if match:
            x_coord.append([float(match.group(1)), float(match.group(2)), float(match.group(3)) ])
            bandddd = lines[i+1] + lines[i+2]
            bandddd = bandddd.split()

            # Which bands do I want?
            bandddd = bandddd[8:]

            for j in range(len(bandddd)):
            	if j > 3:
		            if j not in bands.keys() and j > 3:
		                bands[j] = []
		            bands[j].append(float(bandddd[j]))
    for i in range(len(x_coord)) :
        if i == 0:
            x.append(0)
        else:
            d = dist(x_coord[i], x_coord[i-1])
            if d < 1e-1:
                x.append( x[-1] + d)
            else:
                x.append( x[-1] )
    return bands,x

def plot(bands, x, x_label_pos, fermi):
    # setup plot
    #font = {'family' : 'DejaVu Sans',
    #        'size'   : 12}
    #plt.rc('font', **font)
    plt.figure(num=None, figsize=(6.4, 4.8), dpi=600, facecolor='w', edgecolor='k')

    # calculate plot bounds
    xaxis = [min(x),max(x)]
    yaxis = [1e3,-1e3]
    for i in bands.values(): 
        yaxis = [min([yaxis[0]]+i),max([yaxis[1]]+i)]
        plt.plot(x, np.array(i)-fermi, color='black', lw=0.2)
    yrange = 0.05*(yaxis[1]-yaxis[0])
    yaxis = np.array([yaxis[0]-yrange,yaxis[1]+yrange])-efermi

    # plot bands and vertical lines at special points
    plt.plot(xaxis, [0, 0], color="#66ccff",ls="solid", alpha = 0.5,lw = 1.2)
    plt.vlines(x_label_pos,yaxis[0],yaxis[1],colors='black',linestyles='--',lw = 0.2)
    plt.xticks(x_label_pos,[r'$\Gamma$',r'X',r'W',r'K',r'$\Gamma$',r'L',r'U',r'W',r'L',r'K$|$U',r'X'])

    # add information to graph
    plt.xlim(xaxis)
    plt.ylim(yaxis)
    #plt.xlabel(r'k-path')
    plt.ylabel(r'$E-E_F$ [eV]')
    plt.savefig('bands-ZnS-RS.png')

efermi = read_fermi('../band-ZnS-RS/ZnS-RS.scf.out')
bands, x = read_bnd('../band-ZnS-RS/ZnS-RS.bands')
x_label_pos = [x[i] for i in [0,63,94,116,182,236,274,296,340,378,401]]
plot(bands,x,x_label_pos,efermi)
