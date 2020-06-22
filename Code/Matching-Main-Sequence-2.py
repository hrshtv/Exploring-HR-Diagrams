import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def func(x, a, b):
    return a*x + b

""" The CMD """
# Input from user
clusName = input("Enter the numeric part of the cluster's name: ")
# Loading data from file
fname = "DATA/NGC"+clusName+".txt"
dtype1 = np.dtype(float)
x1 = np.loadtxt(fname, dtype=dtype1, skiprows=52, usecols=(2))
x2 = np.loadtxt(fname, dtype=dtype1, skiprows=52, usecols=(20))
# The probability correction :
prob = np.loadtxt(fname, dtype=dtype1, skiprows=52, usecols=(32))

# Reference Data
ref = "DATA/NGC5272.txt"
xr1 = np.loadtxt(ref, dtype=dtype1, skiprows=52, usecols=(2))
xr2 = np.loadtxt(ref, dtype=dtype1, skiprows=52, usecols=(8))
probr = np.loadtxt(ref, dtype=dtype1, skiprows=52, usecols=(32))
br = (xr1 > 19) & (xr2 > 19) & (probr>90)
yr = xr1[br]
xr = xr1[br] - xr2[br]

# Removing garbage & including only the stars which have more than 90% membership probability
b = (x1 > 19) & (x2 > 19) & (prob>90)
y = x1[b]
x = x1[b] - x2[b]

p, pcov = optimize.curve_fit(func, x, y,p0=[2, 2])

# The plot customization
factor = 0.00005
area = np.pi * factor # Area of each plotted point
colors = [[1, 1, 1]] # Given white color to each point, black background
# To change background color
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
ax.set_facecolor('xkcd:black')

xc = x
# The plot
plt.scatter(x, y, s = area, c = colors)
plt.plot(xc,func(xc, p[0], p[1]),c = [1,0,0])
plt.title("NGC"+clusName, fontsize = 20, fontweight="bold")
plt.ylabel("Apparent Magnitude", fontsize = 18) # The $ sign is used for subscript, {} are used when > 1 character as subscript
plt.xlabel("Color Index", fontsize = 18)

# Inverting the y-axis and setting the limits
plt.gca().invert_yaxis()

# This ensures that the aspect ratio is 1:1, as in the archived file, i,e the image looks 'square'
plt.axes().set_aspect(aspect = (abs(np.amax(x)-np.amin(x)))/abs(np.amax(y)-np.amin(y)))

#The limits on the axes
plt.xlim(np.amin(x), np.amax(x))
plt.ylim(np.amax(y), np.amin(y))
plt.show()
