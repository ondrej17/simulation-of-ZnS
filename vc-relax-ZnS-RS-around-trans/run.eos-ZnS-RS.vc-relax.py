#!/usr/bin/env python

import os
import numpy as np

calc_script = 'ZnS-RS.vc-relax.in'
pbs_script = 'pbs_Hartree'

# pressure in GPa
min_press = 15
max_press = 20
stp_press = 21

run_cmd = 'qsub pbs_Hartree'

for press in np.linspace(min_press, max_press, stp_press):
    
    press = "{:5.3f}".format(10*press)                     # format pressure string

    print("Calculating {} kBar structure".format(press))
    wd = "vc-relax-" + press

    if not os.path.exists(wd):                          # create directory for calculation
        os.makedirs(wd)

    with open(calc_script) as f:                        # create QE script in final directory
        with open(wd + "/vc-relax.in", "w") as fa:
            for line in f:
                fa.write(line.replace("$PRESS$",press)) # replace $KATOF$ with actual value
    
    with open(pbs_script) as f:                         # create PBS script in final directory
        with open(wd + "/pbs_Hartree", "w") as fa:
            for line in f:
                fa.write(line.replace("$NAME$", press))

    os.system("cd "+wd+";"+run_cmd)                     # run calculation with PBS
