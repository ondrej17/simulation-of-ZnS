#!/usr/bin/env python

import os
import numpy as np

calc_script = 'ZnS-RS.scf.in'
pbs_script = 'pbs_Hartree'

min_kpt = 1
max_kpt = 8

run_cmd = 'qsub pbs_Hartree'

for kpt in np.arange(min_kpt, max_kpt, 1):
    
    K_scf = '{}x{}x{}'.format(kpt,kpt,kpt)                  # format kpoints string

    print("Calculating {} k-point MP grid".format(K_scf))
    wd = "scf-" + str(K_scf)
    print(wd)

    if not os.path.exists(wd):                              # create directory for calculation
        os.makedirs(wd)

    kpoints = '{} {} {} 0 0 0'.format(kpt,kpt,kpt)
    with open(calc_script) as f:                            # create QE script in final directory
        with open(wd + "/scf.in", "w") as fa:
            for line in f:
                fa.write(line.replace("$KPOINTS$",kpoints))   # replace $KPOINTS$ with actual value
    
    with open(pbs_script) as f:                             # create PBS script in final directory
        with open(wd + "/pbs_Hartree", "w") as fa:
            for line in f:
                fa.write(line.replace("$NAME$",'ZnS-RS-'+K_scf))

    os.system("cd "+wd+";"+run_cmd)                         # run calculation with PBS
