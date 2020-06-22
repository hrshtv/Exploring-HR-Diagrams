"""WORKS ONLY FOR CLUSTERS HAVING A WIKIPEDIA PAGE"""

import numpy as np
import matplotlib.pyplot as plt
import math

# Input from user
clusName = str(5272)#input("Enter the numeric part of the cluster's name: ")
fname = "DATA/NGC"+clusName+".txt"   
    
# Loading data from file
dtype1 = np.dtype(float)
x1 = np.loadtxt(fname, dtype=dtype1, skiprows=52, usecols=(20)) # F606W
x2 = np.loadtxt(fname, dtype=dtype1, skiprows=52, usecols=(26)) # F814W


# The probability correction :
prob = np.loadtxt(fname, dtype=dtype1, skiprows=52, usecols=(32))
# Removing garbage & including only the stars which have more than 90% membership probability
b = (x1 <= 22) & (x2 <= 22) & (x1 > 0) & (x2 > 0) & (prob>90)
y = x1[b]
x = x1[b] - x2[b] 

# The first plot, from which the user guesses the turnoff 
# start
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
ax.set_facecolor('xkcd:black')

factor = 0.0001
area = np.pi * factor # Area of each plotted point
colors = [[1, 1, 1]] # Given white color to each point, black background

plt.scatter(x, y, s = area, c = colors)
plt.title("NGC"+clusName, fontsize = 20, fontweight="bold")
plt.ylabel("Apparent Magnitude", fontsize = 18) 
plt.xlabel("Color Index", fontsize = 18)

# Inverting the y-axis and setting the limits
plt.gca().invert_yaxis()

# This ensures that the aspect ratio is 1:1, as in the archived file, i,e the image looks 'square'

plt.axes().set_aspect(aspect = (abs(np.amax(x)-np.amin(x)))/abs(np.amax(y)-np.amin(y)))

#The limits on the axes
plt.xlim(np.amin(x), np.amax(x)) 
plt.ylim(np.amax(y), np.amin(y)) 
plt.show()
#end

# User's guess values
L = 0.475#float(input("Enter the left limit: "))
R = 0.625#float(input("Enter right limit: "))
mTO = 18.5#float(input("Enter the apparent magnitude at turnoff: "))

"""WEB-SCRAPING"""
#start
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
distance = float((s[start+1:start + 5]))*1000 # As kpc

# Actual age
rage = 0
for i in a:
    if i.find("Gyr") != -1:
        rage = i
        break
rage = rage[:-3]
#end

# The final plot

# The plot customization
factor = 0.0001
area = np.pi * factor # Area of each plotted point
colors = [[1, 1, 1]] # Given white color to each point, black background
# To change background color
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
ax.set_facecolor('xkcd:black')

# The plot 
plt.scatter(x, y, s = area, c = colors)
plt.title("NGC"+clusName, fontsize = 20, fontweight="bold")
plt.ylabel("Apparent Magnitude", fontsize = 18) 
plt.xlabel("Color Index", fontsize = 18)

le = np.full((x.size,), L)
plt.plot(le,y,color = [1,0,0])
ri = np.full((x.size,),R )
plt.plot(ri, y, color = [1,0,0])
m_array = np.full((y.size,),mTO )
plt.plot(x, m_array, color = [1,0,0])

# Inverting the y-axis and setting the limits
plt.gca().invert_yaxis()

# This ensures that the aspect ratio is 1:1, as in the archived file, i,e the image looks 'square'

plt.axes().set_aspect(aspect = (abs(np.amax(x)-np.amin(x)))/abs(np.amax(y)-np.amin(y)))

#The limits on the axes
plt.xlim(np.amin(x), np.amax(x)) 
plt.ylim(np.amax(y), np.amin(y)) 
plt.show()

bn = (x > L) & (x < R)
na = x[bn]
N = na.size
print("The number of stars in the subgiant phase is: ",N)

epsilon0 = 39498.100525424656 # from previous program, for NGC5272

LbyL0 = pow(10, 0.4*(4.66 + 5*math.log(1040) - mTO)) # For NGC5272 only

t_sg = (10) * (2.8) * (N/epsilon0) * pow((LbyL0), -0.39) # In Gyr

print("Lifetime in subgiant phase is: ", t_sg, "Gyr")



