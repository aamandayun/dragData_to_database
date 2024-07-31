from sklearn.datasets import make_moons
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.animation as animation


#estimate coefficients of linear regression line using least squares
def estimate_coef(time, alt):
        n = np.size(time)

        mean_x = np.mean(time)
        mean_y = np.mean(alt)

        #cross-deviation and deviation about x
        SS_xy = np.sum(time*alt) - n*mean_y*mean_x
        SS_xx = np.sum(time*time) - n*mean_x*mean_x

        #regression coefficient calculations
        b_1 = SS_xy/SS_xx
        b_0 = mean_y - b_1 * mean_x

        return (b_0, b_1)

#generate data for plotting
x, y = make_moons(n_samples = 500, shuffle = True, noise = 0.15, random_state=42)

xMin = np.min(x, axis=0)
x_shifted = x-xMin

downward = x_shifted[y==0]
time = downward[:, 0]
alt = downward[:,1]


fig, ax = plt.subplots()
ax.set_xlim(np.min(time), np.max(time))
ax.set_ylim(np.min(alt), np.max(alt))
scat = ax.scatter([], [], color='red', label='Upward-Facing Moon')
line, = ax.plot([], [], color='blue', label='Regression Line')


def init():
	scat.set_offsets([])
	line.set_data([], [])
	return scat, line


def animate(i):
	subset_time = time[:i]
	subset_alt = alt[:i]
	scat.set_offsets(np.c_[subset_time, subset_alt])
	if len(subset_time) > 1:
		b_0, b_1 = estimate_coef(subset_time, subset_alt)
		x_range = np.array([np.min(time), np.max(time)])
		y_range = b_0 + b_1 * x_range
		line.set_data(x_range, y_range)
	return scat, line

# Create the animation
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(time), interval=100, blit=True)

# Display the plot
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Upward-Facing Moon with Updating Regression Line')
plt.legend()
plt.show()

print(f"time: {time} alt:{alt}")
b_0, b_1 = estimate_coef(time, alt)
print(f"b_0  = {b_0}, b_1 = {b_1}")


#plt.plot(time, b_0+b_1 * time, color ='blue', label='Regression Line')

plt.xlabel('Time')
plt.ylabel('Altitude')

#plt.scatter(downward[:, 0], downward[:, 1], c='blue')
plt.show()


