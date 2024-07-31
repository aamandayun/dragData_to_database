#this will pota 1 dimensional feature and target for linear regression

from sklearn.datasets import make_regression
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math
import psycopg2
import time
import socket

conn = psycopg2.connect(
	database = "postgres", user = 'postgres', password='temppwd', host='localhost', port = '5432'
)

conn.autocommit =True
cursor = conn.cursor()

# Generate data

def generate_increasing_data(n):
	x = np.cumsum(np.random.rand(n))
	y = np.cumsum(np.random.rand(n)) + 20 #starts at y=20
	return x, y

	#sorted = np.argsort(x)
	#x_sorted = x[sorted]
	#y_sorted = y[sorted]

	#return x_sorted, y_sorted



def generate_quadratic_data(n):
	x = np.linspace(0, 50, n)
	y = 0.1* x**2+np.cumsum(np.random.rand(n)*3)
	#return x, y

	sorted_indices = np.argsort(x)

	return x[sorted_indices], y[sorted_indices]




def generate_cosine_data(n):
	x = np.linspace(0, 50, n)
	y = 20 *np.cos(0.2*x)+np.cumsum(np.random.rand(n)*5)+30
	return x, y
	#sorted_indices = np.argsort(x)
	#return x[sorted_indices], y[sorted_indices]

def generate_cosine2(n):
	x = np.linspace(0, 50, n)
	y = 35*np.cos(0.1*x)+np.cumsum(np.random.rand(n)*5)
	return x,y


def line_function(x):
	return x+20

def quad_function(x):
	return 0.1*x**2

def cosine_function(x):
	return 20* np.cos(0.2*x) + 30

def cosine2_function(x):
	return 35*np.cos(0.1*x)

X, y = generate_increasing_data(50)

X_quad, y_quad = generate_quadratic_data(50)

X_cos, y_cos = generate_cosine_data(50)

X_cos2, y_cos2 = generate_cosine2(50)
# Create the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(np.min(X)-0.5, np.max(X)+10)
ax.set_ylim(np.min(y)-10, np.max(y)+100)
ax.set_facecolor("black")

# Create empty scatter plot
scat_red = ax.scatter([], [], color='red', label='Deviations')
scat_red2 = ax.scatter([], [], color='red')
scat_red3 = ax.scatter([], [], color = 'red')
scat_red4 = ax.scatter([], [], color = 'red')

scat = ax.scatter([], [], color='blue', label='Profile Drag')
scat_quad = ax.scatter([],[], color='green', label='Parasite drag')
#scat_quad, = ax.plot([], [], 'green', label='Parasite Drag')
scat_cos, = ax.plot([],[], color='yellow', label='Total Drag')
scat_cos2, = ax.plot([], [], color='pink', label='Induced Drag')

# Initialization function: plot the background of each frame
def init():
	scat.set_offsets(np.empty((0,2)))
	scat_red.set_offsets(np.empty((0,2)))
	scat_red2.set_offsets(np.empty((0,2)))
	scat_red3.set_offsets(np.empty((0,2)))
	scat_red4.set_offsets(np.empty((0,2)))

	scat_quad.set_offsets(np.empty((0,2)))
	scat_cos.set_data([], [])
	scat_cos2.set_data([], [])
	return scat, scat_quad, scat_cos, scat_cos2, scat_red2, scat_red3, scat_red4


# Animation function: this is called sequentially
def animate(i):
    # Select the subset of data to be plotted
	subset_X = X[:i+1]
	subset_y = y[:i+1]
	scat.set_offsets(np.c_[subset_X, subset_y])

	subset_X_quad = X_quad[:i+1]
	subset_y_quad = y_quad[:i+1]
	scat_quad.set_offsets(np.c_[subset_X_quad, subset_y_quad])


	subset_X_cos = X_cos[:i+1]
	subset_y_cos = y_cos[:i+1]
	scat_cos.set_data(subset_X_cos, subset_y_cos)

	subset_X_cos2 = X_cos2[:i+1]
	subset_y_cos2 = y_cos2[:i+1]
	scat_cos2.set_data(subset_X_cos2, subset_y_cos2)

	######### LINEAR ###################
	threshold = 1

	deviation = np.abs(subset_y - line_function(subset_X))
	deviated_indices = deviation > threshold
	red_dot = subset_X[deviated_indices]
	red_dot_y = subset_y[deviated_indices]
	length = len(red_dot)
	scat_red.set_offsets(np.c_[red_dot, red_dot_y])
	#send to database
	if length>0:
		cursor.execute('''INSERT INTO profile(TIME, ALT) VALUES(%s, %s);''', (int(red_dot[length-1]), int(red_dot_y[length-1])))
		conn.commit()

	############# QUAD #############################

	threshold2 = 15
	num = quad_function(subset_X_quad)
	dev2 = np.abs(subset_y_quad - quad_function(subset_X_quad))
	dev2_indices = dev2 > threshold2
	red_dot2 = subset_X_quad[dev2_indices]
	red_dot_y2 = subset_y_quad[dev2_indices]
	lengthQuad = len(red_dot2)
	scat_red2.set_offsets(np.c_[red_dot2, red_dot_y2])

	if lengthQuad>0:
		cursor.execute('''INSERT INTO parasite(TIME, ALT) VALUES(%s, %s);''', (int(red_dot2[lengthQuad-1]), int(red_dot_y2[lengthQuad-1])))
		conn.commit()

	############# COSINE ###########################
	threshold3 = 30
	dev3 = np.abs(subset_y_cos - cosine_function(subset_X_cos))
	dev3_indices = dev3 > threshold3
	red_dot3 = subset_X_cos[dev3_indices]
	red_dot_y3 = subset_y_cos[dev3_indices]
	scat_red3.set_offsets(np.c_[red_dot3, red_dot_y3])
	lengthCos = len(red_dot3)

	if lengthCos > 0:
		cursor.execute('''INSERT INTO total(TIME, ALT) VALUES(%s, %s);''', (int(red_dot3[lengthCos-1]), int(red_dot_y3[lengthCos-1])))
		conn.commit()


	########### COSINE2 ##################################
	threshold4 = 10
	dev4 = np.abs(subset_y_cos2 - cosine_function(subset_X_cos2))
	dev4_indices = dev4 > threshold4
	red_dot4 = subset_X_cos2[dev4_indices]
	red_dot_y4 = subset_y_cos2[dev4_indices]
	scat_red4.set_offsets(np.c_[red_dot4, red_dot_y4])
	lengthCos2 = len(red_dot4)

	if lengthCos2 > 0:
		cursor.execute('''INSERT INTO induced(TIME, ALT) VALUES(%s, %s);''', (int(red_dot4[lengthCos2-1]), int(red_dot_y4[lengthCos2-1])))



	return scat, scat_red, scat_quad, scat_red2, scat_cos, scat_red3, scat_cos2, scat_red4

# Create the animation
ani = animation.FuncAnimation(
    fig, animate, init_func=init, frames=len(X), interval=200, blit=True
)

# Display the plot
plt.xlabel('Time')
plt.ylabel('Altitude')
plt.title('Slow Plotting of Regression Data Points')
plt.legend()
plt.show()



