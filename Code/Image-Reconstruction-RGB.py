import numpy as np
import matplotlib.pyplot as plt

# File data
clusName = input("Enter the numeric part of the cluster's name  : ")
name     = "NGC"+clusName
fname    = "DATA/NGC"+clusName+".txt"

""" Reconstructing the Image """
# Loading data
y    = np.loadtxt(fname,  usecols=(33))
x    = np.loadtxt(fname,  usecols=(34))
mr   = np.loadtxt(fname, usecols=(20)) #F606W
mg   = np.loadtxt(fname, usecols=(14)) #438W
mb   = np.loadtxt(fname, usecols=(8)) #F336W
prob = np.loadtxt(fname, usecols=(32))

# For red
su = n = 0
for i in mr:
    if i > 0:
        su = su + i
        n = n + 1
avgr = su/n
mr = np.where(mr < 0, avgr , mr)

# For blue
su = n = 0
for i in mb:
    if i > 0:
        su = su + i
        n = n + 1
avgb = su/n
mb = np.where(mb < 0, avgb , mb)

# For green
su = n = 0
for i in mg:
    if i > 0:
        su = su + i
        n = n + 1
avgg = su/n
mg = np.where(mg < 0, avgg , mg)

# Plot customisation
factor = pow(10,5.5)

# Area of each plotted point accounted by the magnitude
arear = pow(10, -0.4*mr) * factor
colorsR = [[1,0,0]]

# Area of each plotted point accounted by the magnitude
areag = pow(10, -0.4*mg) * factor
colorsG = [[0,1,0]]

# Area of each plotted point accounted by the magnitude
areab = pow(10, -0.4*mb) * factor
colorsB = [[0,0,1]]

# The plot (RA vs dec)
plt.style.use('dark_background')

#plt.scatter(x, y, s = arear, c = colorsR)
#plt.scatter(x, y, s = areag, c = colorsG)
plt.scatter(x, y, s = areab, c = colorsB)

plt.gca().set_aspect(aspect = (abs(np.amax(x)-np.amin(x)))/abs(np.amax(y)-np.amin(y)))
plt.title(name, fontsize = 20, fontweight="bold")
plt.gca().axis('off')
#plt.savefig('blue.png', dpi = 500)
plt.show()











