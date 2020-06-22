"""Metallicity and distance values taken from wikipedia."""
import numpy as np
import matplotlib.pyplot as plt
import math

clusName = input("Numeric part of the cluster's name          : ")
# start
import xlrd as xl
loc = ("DATA/miscellenous.xlsx")
wbook = xl.open_workbook(loc)
sheet = wbook.sheet_by_index(0)
dist  = []
names = []
red   = []
for i in range(sheet.nrows):
    red.append(sheet.cell_value(i,2))
    dist.append(sheet.cell_value(i,1))
    names.append(sheet.cell_value(i,0))
red   = np.asarray(red)
dist  = np.asarray(dist)
names = np.asarray(names)

n = "NGC "+ clusName
i = np.where(names == n)

distance = float(dist[i])
red      = float(red[i])

dmod = 5 * math.log(distance * 100,10)
print("The distance modulus is                     :", round(dmod,2))
# end

fname = "DATA/NGC" + clusName + ".txt"
x1   = np.loadtxt(fname, usecols=(14)) #F438W = B
x2   = np.loadtxt(fname, usecols=(20)) #F606W = V
prob = np.loadtxt(fname, usecols=(32))
b   = (x1 > 0) & (x2 > 0) & (prob>90)
ysc = x1[b]
xsc = x1[b] - x2[b]
while(True):
    fname2 = "DATA/isoc" + clusName + ".txt"
    loga  = np.loadtxt(fname2,usecols = (2)) # Age
    logL  = np.loadtxt(fname2,usecols = (6)) # Luminosity
    logTe = np.loadtxt(fname2,usecols = (7)) # Effective temperature
    M438  = np.loadtxt(fname2,usecols = (33)) # Absolute
    M606  = np.loadtxt(fname2,usecols = (38)) # Absolute

    #b1 = (np.amin(xsc)<=(m275 - m336)) & (np.amax(xsc)>=(m275 - m336)) & (m275 >= np.amin(ysc)) & (m275 <= np.amax(ysc))

    age       = float(input("Enter the expected age of the cluster (Gyr) : "))
    lgage     = math.log(age*10**9,10)
    #  Additional correction value which may be due to extinction/reddening
    # Strictly speaking, we also need to consider reddening and add the appropriate value to the x values.
    c         = float(input("Enter the extra correction factor           : "))
    redden    = float(input("Enter the reddening value                   : "))
    b = (abs(loga - lgage) <= 1.0*10**(-3) )
    loga  = loga[b]
    logL  = logL[b]
    logTe = logTe[b]
    M438  = M438[b]
    M606  = M606[b]
    #
    msc  = np.percentile(xsc, 4)
    m    = np.percentile(M438 - M606, 4)
    redd = abs(m- msc)
    #
    
    # To change background color
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
    ax.set_facecolor('xkcd:black')
    # Theoretical CMD

    plt.plot(M438 - M606 + redden, M438 + dmod + c, color = [1,0,0])
    plt.scatter(xsc, ysc, s = np.pi*0.005, c = [[1,1,1]] )
    plt.gca().invert_yaxis()
    plt.ylim(np.amax(ysc),np.percentile(ysc,(1)))
    plt.xlim(np.percentile(xsc,(1)),np.percentile(xsc,(95)))
    plt.gca().set_aspect(aspect = (abs(np.percentile(xsc,(95))-np.percentile(xsc,(1))))/abs(np.amax(ysc)-np.percentile(ysc,(1))))
    plt.show()
    print("The reddening is :", redden)
    print("The y - shift is :", round(dmod + c,2))
    print("The age is       :", round(age,2),"Gyr")
    print(" ")
    print(("Is this fit good enough? Yes: 1, No: 0 "))
    flag = float(input())
    if flag == 1 :
        break
