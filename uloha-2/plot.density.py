import os
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

def calc_fit_rho(p, slope, intercept):
    return slope*p + intercept

def calc_rel_rho(p, line1, line2):
    slope1, inter1, slope2, inter2 = *line1, *line2
    return ((slope1*p + inter1) - (slope2*p + inter2)) / (slope2*p + inter2)

def get_rho_p(folder):
    prho = []
    for root, directories, files in os.walk(folder):
        for directory in sorted(directories):
            if "vc-relax-" in directory:
                try:
                    # open file
                    output = open(root+"/"+directory+"/vc-relax.out").read()
                    
                    # find final pressure (prelast occurance of "P=")
                    last_occurance = output.rfind('P=')
                    start_flag = output.rfind('P=', 0, last_occurance)
                    end_flag = output.find('\n', start_flag)
                    p = float(output[start_flag:end_flag].split()[-1])

                    # find final enthalpy
                    start_flag = output.rfind('density =')
                    end_flag = output.find('\n', start_flag)
                    rho = float(output[start_flag:end_flag].split()[-2])
                    
                    prho.append([p,rho])
                except:
                    print("error: ", directory)
                    pass
    return np.array(sorted(prho, key=lambda x: x[0]))

line_param = []

# plot two lines for each phase
for color_point, color_line, folder in [("bs", "b", "../vc-relax-ZnS-RS"), 
                                        ("ro", "r", "../vc-relax-ZnS-ZB")]:
    label = folder[-6:]
    prho = get_rho_p(folder)
    
    p = prho[:,0]/10    # GPa
    rho = prho[:,1]     # g/cm^3

    # linear fit
    slope, intercept, r_value, p_value, std_err = stats.linregress(p,rho)
    line_param.append((slope, intercept))
    p_calc = np.linspace(p[0],p[-1],101)
    rho_calc = calc_fit_rho(p_calc, slope, intercept)

    # plot points
    plt.plot(   p,rho,
                color_point,
                label="{}".format(label))

    # plot fit
    plt.plot(    p_calc,rho_calc,
                color_line,
                label="{}: rho={}*p+{}".format(label, slope.round(7), intercept.round(4)))
            
plt.xlabel('Pressure [GPa]')
plt.ylabel('Density [g/cm^3]')
plt.legend()
plt.tight_layout()
plt.savefig("density-vs-pressure.png")
plt.clf()

# calculate relative density
# rel_rho = (rho_zb - rho_rs)/rho_zb

p = np.linspace(p[0],p[-1],101)
rho = calc_rel_rho(p, *line_param)
slope, intercept, r_value, p_value, std_err = stats.linregress(p,rho)

p_calc = np.linspace(p[0],p[-1],101)
rho_calc = calc_fit_rho(p_calc, slope, intercept)

# plot fit
plt.plot(   p_calc, rho_calc,
            'blue',
            label="rel_rho={}*p+{}".format(slope.round(8), intercept.round(5)))
            
plt.xlabel('Pressure [GPa]')
plt.ylabel('Relative density')
plt.legend()
plt.tight_layout()
plt.savefig("rel-density-vs-pressure.png")

# relative density at transition pressure p = 17.854624848203475 GPa
p0 = 17.854624848203475
print("Change of density at transition pressure {} GPa is: {}".
        format(p0, (slope*p0 + intercept)))
