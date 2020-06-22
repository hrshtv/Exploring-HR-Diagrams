"""Works only for clusters having a wikipedia page"""
import numpy as np
# Required for integration
from scipy.integrate import quad
import math

# mass of the sun
m0 = 1.989*10**30 

#Function to be integrated, x = L/L0.
def func(x):
    return ( x**(-1.3421))

# Input from user
clusName = input("Enter the numeric part of the cluster's name  : ")
fname = "DATA/NGC"+clusName+".txt"   
    
# Loading data from file
m = np.loadtxt(fname, usecols=(20)) #F606W 

# The probability correction :
prob = np.loadtxt(fname, usecols=(32))

# Removing garbage & Magnitude correction
b =  (m <= 22) & (m > 0) & (prob>90)
m = m[b]

"""WEB-SCRAPING"""
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
distance = float((s[start+1:start + 5]))*1000 # As kpc
#END

# Calculations
lumrat = pow(10 , 0.4*(4.66 + 5*math.log(distance/10,10) - m))
#The limits of the integration
lmax = np.amax(lumrat)
lmin = np.amin(lumrat)
N = m.size
# The value of the integration
I = quad(func, lmin, lmax)[0] 
# The stellar density constant
epsilon0 = (N*3.8)/I
# Results
print("The total number of stars under consideration :",N)
print("The maximum value of L/L0 is                  :",lmax)
print("The minimum value of L/L0 is                  :",lmin)
print("The Stellar Density Constant is               :",epsilon0)