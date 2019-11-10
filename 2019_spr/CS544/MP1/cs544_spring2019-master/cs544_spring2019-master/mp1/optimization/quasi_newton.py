
import numpy as np 
from optimization.conj_grad import conjugate_gradient
from optimization.line_search import surrogate_line_search

def quasi_newton_cg(f, x0, max_iters=100000, epsilon=1e-12, print_progress=False, f_noH = None):
    # Author: C. Howard
    # Function to implement a Quasi-Newton method that uses
    # Conjugate Gradient to solve the system of equations
    # that comes about from the Quasi-Newton method

    # init solution estimate
    x = np.copy(x0)
    n = x.shape[0]

    if f_noH is None:
        f_noH = f

    # define the error measure
    def error(u):
        return np.linalg.norm(u,ord=np.inf)

    # compute the current gradient norm
    rel_fchng = epsilon*10

    # compute function value and gradient
    (fk, gradk, Hk) = f(x)

    # update the number of iterations
    num_iters = 0
    if print_progress:
        print("f(x_{0}):".format(num_iters), fk)

    # loop until convergence or end of iterations
    fo = 1e100
    fn = fk
    while (rel_fchng > epsilon) and (num_iters < max_iters):

        # compute quasi-newton matrix to solve
        (pk, nk, errk) = conjugate_gradient(Hk, -gradk)

        # update the estimate of minimum
        xp = x + pk

        # evaluate and see that the solution isn't too bad
        (fp, gradp) = f_noH(xp)
        if fp < fk:
            x[:] = xp[:]
        else:
            alpha = surrogate_line_search(f_noH, x, pk, alpha_guess=1.0, beta=0.8)
            x = x + alpha*pk

        # compute function value and gradient
        (fk, gradk, Hk) = f(x)
        fo = fn
        fn = fk

        # update the number of iterations
        num_iters = num_iters + 1

        # update the change in function
        rel_fchng = fo - fn

        # print progress if desired
        if print_progress:
            print("f(x_{0}):".format(num_iters), fn)
            #print("df: ", rel_fchng)
    
    # return the result
    return (x, num_iters)

def quadratic(x):
    return (x[0]**2, np.array([2.0*x[0]]), np.array([[2.0]]))

def lin_exp_func(x):
    return (np.exp(x[0] + x[1]) - x[0] - x[1], 
    np.exp(x[0] + x[1]) + np.array([-1, -1]), 
    np.exp(x[0] + x[1]) + np.array([[0, 0], [0, 0]]))

def saddle(x):
    return (x[0]**2 - 1e-5*x[1]**2, np.array([2.0*x[0], -2e-5*x[1]]), np.array([[2.0, 0],[0, -2e-5]]))

def approx_quad(x):
    def f(x):
        return np.sum(np.power(x,2.0))
    def gradf(x):
        return np.array([2.0*x[0], 2.0*x[1]])
    def H(inp, out):
        eps = 1e-5
        out[:] = ((gradf(x + eps*inp) - gradf(x))/eps)[:]
    return (f(x), gradf(x), H)

if __name__ == "__main__":
    x0 = np.array([2, 3])
    (x, n) = quasi_newton_cg(approx_quad, x0)
    print("Soln:", x, "| Num Iterations:", n)