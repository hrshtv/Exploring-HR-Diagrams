import numpy as np
import matplotlib.pyplot as plt
# For legend customization
import matplotlib.patches as mpatches
# For curve fitting
from scipy import optimize

# Finding the magnitude limits
def magCutter(y,ep): # Takes the entire y as parameters   
    for i in range(y.size -1):
        if i > 0 :
            d1 = abs(y[i] - y[i-1]) # Difference 1
            d2 = abs(y[i+1] - y[i]) # Difference 2
            if d1 <= ep and d2 <= ep and y[i] < np.median(y) : # Condition for constant y, must lie in upper half
                return y[i] #The constant y

# The curve fitted is a straight line
def func(x, a, b):
    return a*x + b

# Input from user
clusName = input("Enter the numeric part of the cluster's name: ")
name = "NGC"+clusName

# Loading data from file
fname = "DATA/NGC"+clusName+".txt"  

# To ensure same color index, we use columns 8 and 20, ensures horizontal subgiant branch
x1   = np.loadtxt(fname, usecols=(8))
x2   = np.loadtxt(fname, usecols=(20))
prob = np.loadtxt(fname, usecols=(32))
# Removing garbage & including only the stars which have more than 90% membership probability
b = (x1 > 0) & (x2 > 0) & (prob>90)
y = x1[b]
x = x1[b] - x2[b] 

# Reference Data
ref   = "DATA/NGC5272.txt"
xr1   = np.loadtxt(ref, usecols=(8))
xr2   = np.loadtxt(ref, usecols=(20))
probr = np.loadtxt(ref, usecols=(32))
br = (xr1 > 0) & (xr2 > 0) & (probr>90)
yr = xr1[br]
xr = xr1[br] - xr2[br] 

# Can be removed as it works only for clusters having a wikipedia page
"""
#WEB-SCRAPING
#START
import requests
from bs4 import BeautifulSoup
url0 = 'https://en.wikipedia.org/wiki/NGC_' + clusName

url = requests.get(url0).text
soup = BeautifulSoup(url,"lxml")
soup.prettify()

table = soup.find('table',{'class':'infobox'})
tags = table.find_all('tr')

a = []

for tr in tags:
    cols = tr.find_all('td')
    for tds in cols:
        a.append(str('{:1}'.format(str(tds.text))))

s = a[5]
start = s.find('(')
# The blank space after 10.4 isn't ' ' but it's &nbsp 
ActualDistance = float((s[start+1:start + 5])) # As kpc
#END
"""
# Finding the limits of the plot
xmin = max(np.amin(x),np.amin(xr))
ymin = max(np.amin(y),np.amin(yr))
xmax = max(np.amax(x),np.amax(xr))
ymax = max(np.amax(y),np.amax(yr))

"""THE ACTUAL MATCHING LOGIC"""
cutr = 18.735 # Hardcoded the cut of the reference as reference remains the same 
# Value of epsilon, difference parameter

ep = 0
# Finding the cut, if none is returned increase the value of epsilon, and call again
while True: 
    if ep > 0.1:
        cut = cutr
        break
    cut = magCutter(y,ep)
    if type(cut) == type(None):
        ep += 0.01
    else:
        break

xMS = x[(y > cut)]
yMS = y[(y > cut)]
xrMS = xr[(yr > cutr)]
yrMS = yr[(yr > cutr)]

# Calculating the distance between the two lines, rotate about mean, then y distance

p, pcov   = optimize.curve_fit(func, xMS, yMS)
pr, prcov = optimize.curve_fit(func, xrMS, yrMS)

m = p[0]
mr = pr[0]
c = p[1]
cr = pr[1]

slope = (m + mr)/2 #The slope of the new line , assumed to be the average of both slopes

# The points about which rotation is to be done
Yr = Y0 = (ymin + ymax)/2 # Lines are bound by these 2 horizontal line
Xr = (Yr - cr)/mr
X0 = (Y0 - c)/m

# The new lines
p[0]  = slope
pr[0] = slope
p[1]  = Y0 - slope * X0
pr[1] = Yr - slope * Xr

mew = pr[1] - p[1] # The distance modulus

#Calculations
ratio    = pow(10, -mew/5)
distance = ratio * 10.4

c1 = np.full(xr.shape,cut)
c2 = np.full(xr.shape,cutr)
"""END"""

# The plot customization
factor = 0.00005
area = np.pi * factor # Area of each plotted point
colors = [[1, 0, 0]] # Given red color to each point
# To change background color
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
ax.set_facecolor('xkcd:black')
# Making it look square
plt.gca().set_aspect(aspect = (abs((xmax-xmin))/abs((ymax-ymin))))
# The Scatter Plots
cmdr = plt.scatter(xr, yr, s = area, c = [[1,1,1]], label='Reference')
cmd  = plt.scatter(x, y, s = area, c = colors, label=name)
# The Lines
plt.plot(x , func(x, p[0], p[1])   , c = [0.7,0.7,0])
plt.plot(xr, func(xr, pr[0], pr[1]), c = [1,0.7,0])
# The cut lines
plt.plot(xr,c1,c = [0.5,0.5,0.5])
plt.plot(xr,c2,c = [0.5,0.5,0.5])

plt.title(name, fontsize = 20, fontweight="bold")
plt.ylabel("Apparent Magnitude", fontsize = 18)
plt.xlabel("Color Index", fontsize = 18)

# Inverting the y-axis and setting the limits
plt.gca().invert_yaxis()
#The limits on the axes (kept same as that of the reference)
plt.xlim(xmin,xmax) 
plt.ylim(ymax,ymin) 
# Custom legend
red_patch   = mpatches.Patch(color='red', label=name)
white_patch = mpatches.Patch(color='white', label='Reference')
plt.legend(handles=[red_patch,white_patch])
plt.show()

print("The distance modulus is    : ",mew)
print("The ratio of distances is  : ",ratio)
print("The distance of the cluster: ",distance," kpc")
#print("The % error is             : ",(abs(ActualDistance - distance)/ActualDistance)*100,"%")
print("Magnitude limit is         : ",cut)
print("the difference between the original slopes :",abs(m - mr))