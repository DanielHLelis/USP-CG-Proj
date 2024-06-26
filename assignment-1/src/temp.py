import numpy as np

t0 = np.array([[1,0,-4],[0,1,-29],[0,0,1]])
R = np.array([[np.cos(np.deg2rad(45)),-np.sin(np.deg2rad(45)),0],[np.sin(np.deg2rad(45)),np.cos(np.deg2rad(45)),0],[0,0,1]])
t1 = np.array([[1,0,-4],[0,1,-29],[0,0,1]])

r = np.matmul(t1, np.matmul(R,t0))
print(r)

vertices = [[1.5,26.5,1],[6.5,26.5,1],[6.5,31.5,1],[1.5,31.5,1]]

for a in vertices:
    print(a,r@a)