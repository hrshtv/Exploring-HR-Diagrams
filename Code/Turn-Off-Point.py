import numpy as np
import matplotlib.pyplot as plt

def turnoff(x) :
    for i in range(x.size):
        if i > 0 :
            if abs(x[i]-x[i-1]) == 0 :
                return [x[i],y[i]]

# Input from user
clusName = input("Enter the numeric part of the cluster's name  : ")
name = "NGC"+clusName
fname = "DATA/NGC"+clusName+".txt"

x1   = np.loadtxt(fname, usecols=(2))
x2   = np.loadtxt(fname, usecols=(8))
prob = np.loadtxt(fname, usecols=(32))

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

xT = turnoff(x)[0]
yT = turnoff(x)[1]
xt = np.full((x.size,), xT)
plt.scatter(xt,y,s = 0.0001,c = [[1,0,0]])
yt = np.full((y.size,), yT)
plt.scatter(x,yt,s = 0.0001,c = [[1,0,0]])

# Inverting the y-axis and setting the limits
plt.gca().invert_yaxis()
# This ensures that the aspect ratio is 1:1, as in the archived file, i,e the image looks 'square'
plt.gca().set_aspect(aspect = (abs(np.amax(x)-np.amin(x)))/abs(np.amax(y)-np.amin(y)))
#The limits on the axes
plt.xlim(np.amin(x), np.amax(x))
plt.ylim(np.amax(y), np.amin(y))
plt.show()
print("The estimated turnoff points is x = ",xT)
