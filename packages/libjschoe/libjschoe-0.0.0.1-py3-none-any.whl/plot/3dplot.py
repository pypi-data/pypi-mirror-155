from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas

points = pandas.read_csv('res.csv')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = points['electric power1(mW)'].values
y = points['electric power2(mW)'].values
z = points['transmitted power(dBm)'].values

#  x   y   z  
# 1.1,1.2,1.3
# 2.1,2.2,2.3
# 3.1,3.2,3.3
# 4.1,4.2,4.3

ax.scatter(x, y, z, c='r', marker='o')

plt.show()