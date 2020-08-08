import os
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

def calc_fit_H(p, slope, intercept):
    return slope*p + intercept

def get_H_p(folder):
    pH = []
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
                    start_flag = output.rfind('Final enthalpy =')
                    end_flag = output.find('\n', start_flag)
                    H = float(output[start_flag:end_flag].split()[-2])
                    
                    print((p, H))
                    pH.append([p,H])
                except:
                    print("error: ", directory)
                    pass
    return np.array(sorted(pH, key=lambda x: x[0]))

# save parameters of lines for calculating intersection
line_param = []

# plot two lines for each phase
#for color_point, color_line, folder in [("bs", "b", "../vc-relax-ZnS-RS-around-trans"), 
#										("ro", "r", "../vc-relax-ZnS-ZB-around-trans")]:
for color_point, color_line, folder in [("bs", "b", "../vc-relax-ZnS-RS"), 
										("ro", "r", "../vc-relax-ZnS-ZB")]:
	label = folder[12:18]
	print(label)
	pH = get_H_p(folder)
	
	# points
	p = pH[:,0]/10	# GPa
	H = pH[:,1]		# Ry
	
	# linear fit
	slope, intercept, r_value, p_value, std_err = stats.linregress(p,H)
	line_param.append((slope, intercept))
	p_calc = np.linspace(p[0],p[-1],101)
	H_calc = calc_fit_H(p_calc, slope, intercept)

	# plot points
	plt.plot(	p,H,
				color_point,
				label="{}".format(label))
	
	# plot fit
	plt.plot(	p_calc,H_calc,
				color_line,
				label="{}: H={}*p{}".format(label, slope.round(7), intercept.round(4)))

plt.xlabel('Pressure [GPa]')
plt.ylabel('Enthalpy [Ry]')
plt.legend()
plt.tight_layout()
plt.savefig("enthalpy-vs-pressure.png")

# calculate intersection of two fitting lines
print(line_param)
inter = (line_param[0][1] - line_param[1][1]) / (line_param[1][0] - line_param[0][0])
print("Interception at {} GPa".format(inter))
