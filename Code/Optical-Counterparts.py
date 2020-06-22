import numpy as np
import matplotlib.pyplot as plt

"""
The x-rays were found to be emitted from the given coordinates, by some different method. Now, we need to corelate them which the photometric data that we have and find stars in that region which could be the optical counterparts. 
Analogy:
When on the street if your hear the sound of an engine, you look up and see a car making that noise, that's it. You found the optical counterpart of the sound.
"""

fname = "DATA/NGC5272.txt"
# 2 - 20
# 14 -26
# Loading data
ra   = np.loadtxt(fname, usecols=(33)) #RA
dec  = np.loadtxt(fname, usecols=(34)) #dec
idno = np.loadtxt(fname, dtype = str, usecols=(35)) #ID no.
x1   = np.loadtxt(fname, usecols=(2))  #F275W
x2   = np.loadtxt(fname, usecols=(8)) #F336W
prob = np.loadtxt(fname, usecols=(32))

"""
# Considering stars having valid photometric data in all wavebands
i = 2
condition = True
while i < 26:
    a = np.loadtxt(fname, dtype=dtype1, skiprows=52, usecols=(i))
    condition = ( a > 0 ) & condition
    i = i + 6
"""
# The condition of m < 22 creates additional problems, thus removed
condition = (x1 > 0) & (x2 > 0) & (prob > 90) # Given in question <= since lesser the m more the brightness
#condition = (x1 > 0) & (x2 > 0)

ra   = ra[condition]
dec  = dec[condition]
x1   = x1[condition]
x2   = x2[condition]
idno = idno[condition]
prob = prob[condition]
yy   = x1 
xx   = x1 - x2

ra0 = [] #To store RA of 1st region
dec0 = [] #To store dec of first region
ra01 = [] # second region
dec01 = [] # second region
ind1 = [] # To store the index of the stars in the first region
ind2 = [] ## To store the index of the stars in the first region

# Given data
ra1   = 205.5407
dec1  = 28.3798
erad1 = 10**(-4)

ra2   = 205.5729
dec2  = 28.359
erad2 = 4.4*10**(-4)

# Finding the stars in the first region
for i in range(ra.size):
    if (ra[i] - ra1)*(ra[i] - ra1) + (dec[i] - dec1)*(dec[i] - dec1) <= erad1*erad1 :
        dec0.append(dec[i])
        ra0.append(ra[i])
        ind1.append(i)

# Finding the stars in the second region
for i in range(ra.size):
    if (ra[i] - ra2)*(ra[i] - ra2) + (dec[i] - dec2)*(dec[i] - dec2) <= erad2*erad2 :
        dec01.append(dec[i])
        ra01.append(ra[i])
        ind2.append(i)

# Converting to numpy arrays
ra0   = np.asarray(ra0)
dec0  = np.asarray(dec0)
ra01  = np.asarray(ra01)
dec01 = np.asarray(dec01)

# Finding the (x,y) coords in the CMD for the previously found stars
# For region 1
xi1 = []
yi1 = []
for i in ind1:
    xi1.append(xx[i])
    yi1.append(yy[i]) 
xi1 = np.asarray(xi1)
yi1 = np.asarray(yi1)

# For region 2 
xi2 = []
yi2 = []
for i in ind2:
    xi2.append(xx[i])
    yi2.append(yy[i])
xi2 = np.asarray(xi2)
yi2 = np.asarray(yi2)

"""The position on the RA v dec graph"""
# Plot customisation
factor = pow(10,5)
# Area of each plotted point accounted by the magnitude
area = pow(10, -0.4 * x2) * factor
colors = [[1,1,1]]
# The plot (RA vs dec)
x = dec
y = ra
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
ax.set_facecolor('xkcd:black')
# Making the aspect ratio equal
plt.scatter(x, y, s = area, c = colors)
plt.scatter(dec0 , ra0 , marker='o', color=[[0,1,1]])
plt.scatter(dec01, ra01, marker='o', color="red")
plt.gca().set_aspect(aspect = (abs(np.amax(x)-np.amin(x)))/abs(np.amax(y)-np.amin(y)))
plt.title("NGC5272", fontsize = 20, fontweight="bold")
plt.ylabel("RA", fontsize = 18) # The $ sign is used for subscript, {} are used when > 1 character as subscript
plt.xlabel("dec", fontsize = 18)
plt.show()

"""The position on the CMD"""   
# The plot customization
factor = 0.01
area   = np.pi * factor # Area of each plotted point
colors = [[1, 1, 1]] # Given white color to each point, black background
# To change background color
fig = plt.figure()
ax  = fig.add_subplot(1, 1, 1) # nrows, ncols, index
ax.set_facecolor('xkcd:black')
# The plot 
c1 = [[0,1,1]]
plt.scatter(xx, yy, s = area, c = colors)
plt.scatter(xi1, yi1,s = np.pi*20, marker='o', color=c1)
plt.scatter(xi2, yi2,s = np.pi*20, marker='o', color="red")
plt.title("NGC5272", fontsize = 20, fontweight="bold")
plt.ylabel("Apparent Magnitude", fontsize = 18) # The $ sign is used for subscript, {} are used when > 1 character as subscript
plt.xlabel("Color Index", fontsize = 18)
# Inverting the y-axis and setting the limits
plt.gca().invert_yaxis()
# This ensures that the aspect ratio is 1:1, as in the archived file, i,e the image looks 'square'
plt.gca().set_aspect(aspect = (abs(np.amax(xx)-np.amin(xx)))/abs(np.amax(yy)-np.amin(yy)))
#The limits on the axes
plt.xlim(np.amin(xx), np.amax(xx)) 
plt.ylim(np.amax(yy), np.amin(yy)) 
plt.savefig('XR.png', dpi = 500)
plt.show()

print("REGION 1 :")

print("Number of stars in region 1: ",len(ind1))

for i in ind1:
    print("ID: ",idno[i]," ","Prob:",prob[i],"CI, y-mag: ","(",round(xx[i],2),",",round(yy[i],2),")")
    
"""
print("RA and dec are: ")
for i in range(ra0.size):
    print("RA:",ra0[i],"dec:",dec0[i])
"""

print("REGION 2 :")

print("Number of stars in region 2: ",len(ind2))

for i in ind2:
    print("ID: ",idno[i]," ","Prob:",prob[i],"CI, y-mag: ","(",round(xx[i],2),",",round(yy[i],2),")")

"""  
print("RA and dec are: ")
for i in range(ra01.size):
    print("RA:",ra01[i],"dec:",dec01[i])
"""

