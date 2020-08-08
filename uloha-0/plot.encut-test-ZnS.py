import os
import numpy as np
from matplotlib import pyplot as plt

for color, folder in [("bs-", "../encut-test-ZnS-RS"), ("ro-", "../encut-test-ZnS-ZB")]:

    results = []

    for root, directories, files in os.walk(folder):
        for directory in sorted(directories):
            if "scf-" in directory:
                try:
                    output = open(root+"/"+directory+"/scf.out").read()

                    start_flag = output.rfind('!')
                    end_flag = output.find('\n',start_flag)
                    E = float(output[start_flag:end_flag].split()[4])

                    results.append([float(directory[4:]),E])
                except:
                    print('error')
                    pass

    results = sorted(results, key=lambda x: x[0])
    results = np.array(results).T

    plt.plot(results[0],results[1],color,linewidth=2, label=folder[-6:])

plt.xlabel('ecutwfc [Ry]')
plt.ylabel('Structure energy [Ry]')
plt.legend()
plt.tight_layout()
plt.savefig("encut-ZnS.png")
