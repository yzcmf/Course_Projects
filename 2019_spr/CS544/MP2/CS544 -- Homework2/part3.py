import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.sparse import csr_matrix, eye
from scipy.optimize import minimize
from time import time

GRID_SIZE = 256

def getIndex(x, y):
    return GRID_SIZE * x + y

def interpolant(t, start, end, range_):
    return start + t * float(end - start) / range_
    

mid = GRID_SIZE // 2
cols = []
b = []

for y in range(GRID_SIZE):
    # first append is the first column
    # second append is the middle column
    # third append is the last column
    cols.append(getIndex(0,y))
    cols.append(getIndex(mid,y))
    cols.append(getIndex(GRID_SIZE - 1, y))
    if y <= mid:
        b.append(interpolant(y, 1, 0, mid))
        b.append(interpolant(y, 0, 1, mid))
        b.append(interpolant(y, 1, 0, mid))
    else:
        b.append(interpolant(y - mid, 0, 1, mid))
        b.append(interpolant(y - mid, 1, 0, mid))
        b.append(interpolant(y - mid, 0, 1, mid))

for x in range(GRID_SIZE):
    # first append is the first row
    # second append is the middle row
    # third append is the last row
    cols.append(getIndex(x,0))
    cols.append(getIndex(x,mid))
    cols.append(getIndex(x,GRID_SIZE - 1))
    if x <= mid:
        b.append(interpolant(x, 1, 0, mid))
        b.append(interpolant(x, 0, 1, mid))
        b.append(interpolant(x, 1, 0, mid))
    else:
        b.append(interpolant(x - mid, 0, 1, mid))
        b.append(interpolant(x - mid, 1, 0, mid))
        b.append(interpolant(x - mid, 0, 1, mid))

cols = np.array(cols)
rows = np.arange(len(cols))
data = np.ones(len(cols))

A = csr_matrix((data, (rows, cols)), shape=(len(cols), GRID_SIZE**2))
b = np.array(b)

# Set up Ay for cost func
Ay = -1 * eye(GRID_SIZE**2, GRID_SIZE**2, k=0)
Ay += eye(GRID_SIZE**2, GRID_SIZE**2, k=1)
# need to remove entries where it tries to compare
# h(x,255) to h(x+1,0)
for i in range(GRID_SIZE-1, GRID_SIZE**2, GRID_SIZE):
    Ay[i,i] = 0
    if (i+1 < GRID_SIZE**2):
        Ay[i,i+1] = 0

# Set up Ax for cost func
Ax = -1 * eye(GRID_SIZE**2, GRID_SIZE**2, k=0)
Ax += eye(GRID_SIZE**2, GRID_SIZE**2, k=GRID_SIZE)
# need to remove entries where it tries to compare
# h(255,y) to h(0,y+1)
lastValidEntry = GRID_SIZE**2 - GRID_SIZE
for i in range(lastValidEntry, GRID_SIZE**2):
    Ax[i,i] = 0

def f(x):
    return x.T @ Ax.T @ Ax @ x \
           + x.T @ Ay.T @ Ay @ x

def df(x):
    return 2 * Ax.T @ Ax @ x \
           + 2 * Ay.T @ Ay @ x

def g(x):
    return A @ x - b

def dg(x):
    return A

def ALM(x, lmbda, c):
    s = 0
    hx = Ax @ x
    hy = Ay @ x
    #'''
    h = x.reshape((GRID_SIZE, GRID_SIZE), order='F')
    areas = 0.5 * np.sqrt(1 + (h[:GRID_SIZE-1,1:] - h[:GRID_SIZE-1,:GRID_SIZE-1])**2 + (h[1:,:GRID_SIZE-1] - h[:GRID_SIZE-1,:GRID_SIZE-1])**2)
    areas+= 0.5 * np.sqrt(1 + (h[:GRID_SIZE-1,1:] - h[1:,1:])**2 + (h[1:,:GRID_SIZE-1] - h[1:,1:])**2)
    s = np.sum(areas)
    #'''
    '''
    for i in range(GRID_SIZE**2):
        for j in range(GRID_SIZE**2):
            s += np.sqrt(1 + hx[i] ** 2 + hy[i] ** 2)
    '''
    '''
    hx, hy = np.meshgrid(hx, hy, sparse=True)
    hx = hx ** 2
    hy = hy ** 2
    s = np.sum(np.sqrt(1 + hx + hy))
    '''
    #s = objective(hx, hy, GRID_SIZE)
    return s - np.inner(lmbda,g(x)) + 0.5 * c * la.norm(g(x))**2
    #return f(x) - np.inner(lmbda,g(x)) + 0.5 * c * la.norm(g(x))**2

def dALM(x, lmbda, c):
    return
    #return df(x) - lmbda @ dg(x) + c * g(x) @ dg(x) 

# intial values for algorithm
c = 1.0
lmbda = np.ones(len(cols))
Vh = np.zeros(GRID_SIZE**2)

# Algorithm
start = time()
for i in range(10):
    print(f'Iteration {i+1}')
    res = minimize(ALM, Vh, args=(lmbda, c), method='L-BFGS-B')#, jac=dALM, options={'maxiter': 50})
    Vh = res.x
    lmbda = lmbda - 0.5 * c * g(Vh)
    c = 2 * c
end = time()

print(f'Augmented Lagrangian took {end - start} seconds..')

# plot
h = Vh.reshape((GRID_SIZE,GRID_SIZE), order='F')

x = np.linspace(0,1,GRID_SIZE)
y = np.linspace(0,1,GRID_SIZE)
X, Y = np.meshgrid(x,y)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.plot_surface(X, Y, h, rstride=1, cstride=1)
ax.view_init(20,20)

plt.show()
