# assume the magnitude in F606W band to be its bolometric magnitude
# Due to this assumption, the total luminosity may not match with the actual one
# Ignore the stars fainter than mF606W = 22.
import numpy as np
import matplotlib.pyplot as plt

# Input from user
clusName = input("Enter the numeric part of the cluster's name  : ")
name  = "NGC"+clusName
fname = "DATA/NGC"+clusName+".txt" 

# Loading data
xp   = np.loadtxt(fname, usecols=(34))
yp   = np.loadtxt(fname, usecols=(33))
#F606W Calibrated magnitude
mf   = np.loadtxt(fname, usecols=(20))
# The probability correction :
prob = np.loadtxt(fname, usecols=(32))

condition = (mf <= 22) & (mf > 0) & (prob > 90) # Given in question <= since lesser the mf more the brightness
xp = xp[condition]
yp = yp[condition]
mf = mf[condition]

factor = pow(10,5)
lum    = pow(10, -0.4*mf)
area2  = lum * factor

# Center of cluster at (5000,5000), shift of origin
x = xp - np.median(xp)
y = yp - np.median(yp)

""" Half-Light Radius"""
L = np.sum(lum)
halfL = L / 2
r = halfLum = 0 #Effective / half-light radius

while( r + 0.0001 < np.amax(x)):
    r = r + 0.0001
    halfLum = 0
    for i in range(lum.size) :
        if (x[i]*x[i]+y[i]*y[i]) <= r*r :
            halfLum += lum[i]
    if halfLum > halfL :
        break

theta = np.arange(0,2*3.14,0.01)
xc = r * np.cos(theta)
yc = r * np.sin(theta)

# Plot customisation
factor2 = 0.0001
colors2 = [[1,1,1]]
plt.style.use('dark_background')

#Scatter plot
plt.scatter(x, y, s = area2, c = colors2) 
# The circle
plt.plot(xc, yc, c = [1,0,0])
# Making the aspect ratio equal
plt.gca().set_aspect(aspect = 1)
plt.title(name, fontsize = 20, fontweight="bold")
plt.ylabel("y", fontsize = 18) 
plt.xlabel("x", fontsize = 18)
plt.gca().axis('off')
plt.show()

print("The approximate half-light radius is: ",round(r*3600,4),"arc seconds")
print("or",round(r*60,4),"arc minutes")

#"Beyond the half-light radius (~48′′)" GIVEN AT https://www.aanda.org/articles/aa/full_html/2012/06/aa19375-12/aa19375-12.html