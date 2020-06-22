import numpy as np
import matplotlib.pyplot as plt

# Input from user
clusName = input("Enter the numeric part of the cluster's name  : ")
name = "NGC"+clusName
fname = "../DATA/NGC"+clusName+".txt"

x1 = np.loadtxt(fname, usecols=(2))
x2 = np.loadtxt(fname, usecols=(8))
# The probability correction :
prob = np.loadtxt(fname, usecols=(32))

# Removing garbage & including only the stars which have more than 90% membership probability
b = (x1 > 0) & (x2 > 0) & (prob>90)
y = x1[b]
x = x1[b] - x2[b]

# The plot customization
factor = 0.0001
area = np.pi * factor # Area of each plotted point
colors = [[1, 1, 1]] # Given white color to each point, black background
# To change background color
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
ax.set_facecolor([0,0,0])

# The plot
plt.scatter(x, y, s = area, c = colors)
plt.title(name, fontsize = 20, fontweight="bold")
plt.ylabel("Apparent Magnitude", fontsize = 18)
plt.xlabel("Color Index", fontsize = 18)

# Inverting the y-axis and setting the limits, so that correlation with HRD is easier as HRD plots luminosity increasing along the y - axis
plt.gca().invert_yaxis()
# This ensures that the aspect ratio is 1:1, as in the archived file, i,e the image looks 'square'
plt.gca().set_aspect(aspect = (abs(np.amax(x)-np.amin(x)))/abs(np.amax(y)-np.amin(y)))
#The limits on the axes
plt.xlim(np.amin(x), np.amax(x))
plt.ylim(np.amax(y), np.amin(y))
# plt.savefig('../img/cmd_ngc2808.png', dpi=300)
plt.show()
