import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.sparse import csr_matrix, eye
from scipy.optimize import minimize
from time import time

GRID_SIZE = 256

# Set up constraint
points = np.array([[0,0],[0,.5],[0,1],[.5,0],[.5,.5],[.5,1],[1,0],[1,.5],[1,1]])
cols = np.zeros(9)
for i in range(points.shape[0]):
    x,y = points[i]
    cols[i] = GRID_SIZE * np.floor((GRID_SIZE - 1) * x) + np.floor((GRID_SIZE - 1)  * y)

cols = cols.astype(np.int64)
rows = np.array([0,1,2,3,4,5,6,7,8])
data = np.array([1,1,1,1,1,1,1,1,1])

A = csr_matrix((data, (rows, cols)), shape=(len(cols), GRID_SIZE**2))
b = np.array([1,0,1,0,1,0,1,0,1])

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
    return f(x) - np.inner(lmbda,g(x)) + 0.5 * c * la.norm(g(x))**2

def dALM(x, lmbda, c):
    return df(x) - lmbda @ dg(x) + c * g(x) @ dg(x) 

# intial values for algorithm
c = 1.0
lmbda = np.ones(len(cols))
Vh = np.zeros(GRID_SIZE**2)

# Algorithm
start = time()
for i in range(5):
    print(f'Iteration {i+1}')
    res = minimize(ALM, Vh, args=(lmbda, c), method='L-BFGS-B', jac=dALM) #options={'maxiter': 50})
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