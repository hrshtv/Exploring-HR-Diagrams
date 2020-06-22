import numpy as np
import matplotlib.pyplot as plt

clusName = input("Enter the numeric part of the cluster's name  : ")
name = "NGC"+clusName
fname = "DATA/NGC"+clusName+".txt" 

""" Reconstructing the Image """
# Loading data
y = np.loadtxt(fname, usecols=(33))
x = np.loadtxt(fname, usecols=(34))
m = np.loadtxt(fname, usecols=(20)) #F606W

su= n = 0
for i in m:
    if i > 0:
        su += i
        n  += 1
avg = su/n
# Wherever magnitude isn't available, replace by the average magnitude.
m = np.where(m < 0, avg , m)

# Plot customisation
factor = pow(10,5)
# Area of each plotted point accounted by the magnitude
area = pow(10, -0.4*m) * factor
colors = [[1,1,1]]

# The plot (RA vs dec)
plt.style.use('dark_background')
# Making the aspect ratio equal
plt.scatter(x, y, s = area, c = colors)
plt.gca().set_aspect(aspect = (abs(np.amax(x)-np.amin(x)))/abs(np.amax(y)-np.amin(y)))

plt.title(name, fontsize = 20, fontweight="bold")
plt.ylabel("y", fontsize = 18) 
plt.xlabel("x", fontsize = 18)
plt.show()











