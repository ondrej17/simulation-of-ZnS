import os
import numpy as np
from matplotlib import pyplot as plt

results = []

for root, directories, files in os.walk("../kpoints-test-ZnS-RS"):
    for directory in sorted(directories):
        if "scf-" in directory:
            try:
                output = open(root+"/"+directory+"/scf.out").read()

                start_flag = output.rfind('!')
                end_flag = output.find('\n',start_flag)
                E = float(output[start_flag:end_flag].split()[4])

                results.append([int(directory[4]),E])
            except:
                print('error')
                pass

results = sorted(results, key=lambda x: x[0])
results = np.array(results).T

plt.plot(results[0],results[1],'o-',linewidth=2)
plt.xlabel('N v (N,N,N) mriežke')
plt.ylabel('energia [Ry]')
plt.tight_layout()
plt.savefig("kpoints-ZnS-RS.png")
