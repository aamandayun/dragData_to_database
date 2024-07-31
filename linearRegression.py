# utils.py

import numpy as np
import matplotlib.pyplot as plt



#estimate coefficients of linear regression line using least squares
def estimate_coef(time, alt):
	n = np.size(time)

	mean_x = np.mean(time)
	mean_y = np.mean(alt)

        #cross-deviation and deviation about x
	SS_xy = np.sum(time, alt) - n*mean_y*mean_x
	SS_xx = np.sum(time*time) - n*mean_x*mean_x

        #regression coefficient calculations
	b_1 = SS_xy/SS_xx
	b_0 = mean_y - b_1 * mean_x

	return (b_0, b_1)
