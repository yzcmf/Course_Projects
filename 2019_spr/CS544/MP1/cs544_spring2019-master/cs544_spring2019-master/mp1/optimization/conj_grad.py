
import numpy as np

def conjugate_gradient(A, b, use_matvec_op = False, epsilon = 1e-12 ):
    # Author: C. Howard
    # Code used to solve linear systems Ax = b
    # for symmetric matrix A based on algorithm described at:
    # https://en.wikipedia.org/wiki/Conjugate_gradient_method
    #
    # [Inputs]
    # A: expected to either be
    #   1) A numpy matrix of dimension n by n for some integer n
    #   2) Some functor/function that takes two input vectors (x, o)
    #      where x is the numpy vector that will have a matvec performed
    #      on it and o is the output numpy vector with the result
    #
    # b: numpy vector
    #
    # use_matvec_op: True if A input is a functor/function representing
    #   matrix-vector multiplications, False if A is a numpy matrix
    #
    # epsilon: Tolerance to check for convergence of algorithm
    #
    # [Outputs]
    # Returns a tuple (x, n) where x is the solution to the system
    # and n is the number of iterations it took to get to that solution

    # define a temporary vector for matvecs
    q = np.zeros(b.shape)

    # define approximate solution
    x = np.zeros(b.shape)

    # construct matvec operator if the one passed
    # in is not a matvec
    if type(A) == np.ndarray:
        def matvec_op(xx, yy):
            np.matmul(A, xx, out=yy)
    else:
        matvec_op = A

    # start the conjugate gradient work
    # by computing initial residual
    matvec_op(x, q)
    r = b - q

    # define function to compute residual error
    def error(r):
        return np.linalg.norm(r, np.inf)

    # check if the solution is good enough
    # with the initial guess and return if so
    resid_err = error(r)
    if resid_err < epsilon:
        return (x,0, resid_err)
    
    # initialize a few useful variables for algo
    max_iters = b.shape[0]
    num_iter = 0
    p = np.copy(r)
    beta = 0.0
    alpha = 0.0

    # loop computing the estimate for the solution
    # until tolerance or max iterations is met
    while (resid_err > epsilon) and (num_iter < max_iters):
        # compute the matvec of A(x) and
        # store in temporary vector
        matvec_op(p,q)

        # compute alpha_{k}
        rmag2 = np.dot(r,r)
        denom = np.dot(p,q)
        if denom > 0: # if this is <= 0, it is not a descent dir
            alpha = rmag2/np.dot(p,q)

            # compute updated solution and residual
            x = x + alpha*p
            r = r - alpha*q
        else:
            print('problem with bad direction!')
            break

        # update the residual error
        resid_err = error(r)

        # compute conjugate direction param
        # and new conjugate direction
        beta = np.dot(r,r) / rmag2
        p = r + beta*p
        num_iter = num_iter + 1

    # return the solution
    return (x, num_iter, resid_err)

def Aop(x, o):
    o[:] = x[:]

if __name__ == "__main__":
    n = 2
    b = np.random.uniform(size=(2,))
    A = np.eye(N=2)
    (x1, n1, err1) = conjugate_gradient(A, b)
    print("Error:", err1, "| b:", b,  "| Soln:", x1)

    (x2, n2, err2) = conjugate_gradient(Aop, b)
    print("Error:", err2, "| b:", b,  "| Soln:", x2)



