from scipy.io import loadmat
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from os import path

MINI = 1e-12

def sigmoid(z):
    return 1/(1+np.exp(-z))
'''
def costFunctionReg(theta, X, y, lmbda):
    m = len(y)
    temp0 = sigmoid(np.dot(X, theta))
    temp1 = np.multiply(y, np.log(temp0))
    temp2 = np.multiply(1-y, np.log(1-temp0))
    return np.sum(temp1 + temp2) / (-m) + np.sum(theta[1:]**2) * lmbda / (2*m)
'''

def costFunctionReg(theta, X, y, lmbda):
    m = len(y)
    interm = sigmoid(np.dot(X, theta))
    interm = np.clip(interm,MINI,1-MINI)
    temp1 = np.multiply(y, np.log(interm))
    temp2 = np.multiply(1-y, np.log(1-interm))
    return np.sum(temp1 + temp2) / (-m) + np.sum(theta[1:]**2) * lmbda / (2*m)

def gradRegularization(theta, X, y, lmbda):
    m = len(y)
    temp = sigmoid(np.dot(X, theta)) - y
    temp = np.dot(temp.T, X).T / m + theta * lmbda / m
    temp[0] = temp[0] - theta[0] * lmbda / m
    return temp

def Hessian(theta, X, y, lmbda):
    m = len(y)
    vals = np.multiply(sigmoid(np.dot(X, theta)),(1-sigmoid(np.dot(X, theta))))/m
    diag = np.diag(vals)

	#hessian for Negative LL
    hess_nll = np.matmul(np.matmul(np.transpose(X),diag),X)
    (nr, nc) = hess_nll.shape
    use_reg = np.ones((nr,))
    use_reg[0] = 0.0
    reg_term = np.diag(lmbda/m * use_reg)
    return hess_nll + reg_term

class Hmatvec:
    def __init__(self, theta, X, Y, lmbda):
        m = len(Y)
        tmp = np.dot(X,theta)
        self.X = X
        self.vals = np.multiply(sigmoid(tmp),(1-sigmoid(tmp)))/m
        (nr,nc) = X.shape
        self.use_reg = np.ones((nc,))*(lmbda/m)
        self.use_reg[0] = 0.0
    def __call__(self, inp, out):
        H1 = np.matmul(np.multiply(self.vals, np.matmul(self.X,inp)),self.X)
        out[:] = (H1 + np.multiply(self.use_reg,inp))[:]

def Hessian_matvec(inp, out, theta, X, y, lmbda):
    m = len(y)
    tmp = np.dot(X, theta)
    vals = np.multiply(sigmoid(tmp),(1-sigmoid(tmp)))/m

	#hessian for Negative LL
    H1 = np.matmul(np.multiply(vals, np.matmul(X,inp)),X)
    (nr,) = H1.shape
    use_reg = np.ones((nr,))*(lmbda/m)
    use_reg[0] = 0.0
    out[:] = (H1 + np.multiply(use_reg,inp))[:]

def build_classifier():
    data = loadmat('mnist.mat')
    #mnist.mat has 5000 examples
    #we are dividing them into train and test sets with 4500 and 500 examples, respectively.
    X = data['X']
    y = data['y']
    p = np.random.permutation(len(X))
    X = X[p]
    y = y[p]
    X_train = X[0:4500]
    y_train = y[0:4500]
    X_test = X[4501:4999]
    y_test= y[4501:4999]

    m = len(y)
    print("num of examples: ", m)
    m_train = len(y_train)
    m_test = len(y_test)
    print("num of examples in training set: ", m_train)
    print("num of examples in test set: ", m_test)

    ones_train = np.ones((m_train,1))
    X_train = np.hstack((ones_train, X_train)) #add the intercept
    (m_train,n_train) = X_train.shape

    ones_test = np.ones((m_test,1))
    X_test = np.hstack((ones_test, X_test)) #add the intercept
    (m_test,n_test) = X_test.shape

    lmbda = 0.1
    k = 10 #10 models, one for each one-vs-all classifer
    theta = np.zeros((k,n_train)) #inital parameters
    for i in range(k):
        digit_class = i if i else 10 #because class 0 is denoted as 10 in the dataset. classes 1 to 9 are denoted by the corresponding number.
        theta[i] = opt.fmin_cg(f = costFunctionReg, x0 = theta[i],  fprime = gradRegularization, args = (X_train, (y_train == digit_class).flatten(), lmbda), maxiter = 100)
        print("hessian shape: ",np.shape(Hessian(theta[i], X_train,y_train, lmbda)))

    pred = np.argmax(X_train @ theta.T, axis = 1)
    pred = [e if e else 10 for e in pred]
    print("train accuracy: ", np.mean(pred == y_train.flatten()) * 100)


    pred_test = np.argmax(X_test @ theta.T, axis = 1)
    pred_test = [e if e else 10 for e in pred_test]
    print("test accuracy: ", np.mean(pred_test == y_test.flatten()) * 100)

def load_MNST_data():
    data = loadmat(path.join(path.dirname(path.abspath(__file__)),'./mnist.mat'))
    X = data['X']
    Y = data['y']
    p = np.random.permutation(len(X))
    return (X[p], Y[p])

def finite_diff(func, x0, dim, h = 1e-5):
    f0 = func(x0)
    x0_dim = x0[dim]
    x0[dim] = x0_dim + h
    fn = func(x0)
    x0[dim] = x0_dim
    deriv = (fn - f0)/h
    return deriv

def derivative_checks():

    # obtain the data
    (X,Y) = load_MNST_data()

    # make small subset
    Xsub = X[:1000]
    Ysub = Y[:1000]

    # define functions that will have derivatives taken
    def f(theta):
        return costFunctionReg(theta, Xsub, (Ysub==1).flatten(), 1.0)
    
    def gradf(theta):
        return gradRegularization(theta, Xsub, (Ysub==1).flatten(), 1.0)

    def hessianf(theta):
        return Hessian(theta, Xsub, (Ysub==1).flatten(), 1.0)

    # choose random theta vector
    (m_train,n_train) = X.shape
    theta = np.random.uniform(low=-1.0, high=0.0, size=(n_train,))

    # check the gradient accuracy
    grad_analyt = gradf(theta)
    grad_approx = np.zeros(grad_analyt.shape)
    for k in range(n_train):
        grad_approx[k] = finite_diff(f,theta,k)
    
    # compute gradient error in infinity-norm and print results
    grad_err = np.linalg.norm(grad_analyt - grad_approx, np.inf)
    print('Gradient difference: {0} in infinity norm'.format(grad_err))

    # check the hessian accuracy
    H_analyt = hessianf(theta)
    H_approx = np.zeros(H_analyt.shape)
    for k in range(n_train):
        H_approx[k,:] = finite_diff(gradf, theta, k)

    # compute hessian error in infinity-norm and print results
    hessian_err = np.linalg.norm(H_analyt - H_approx, np.inf)
    print('Hessian difference: {0} in infinity norm'.format(hessian_err))




if __name__ == "__main__":
    derivative_checks()
    #build_classifier()
    #import sys
    #if len(sys.argv) > 1:
    #    exec(sys.argv[1])
    #else:
    #    build_classifier()

