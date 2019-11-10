
import numpy as np
from optimization.line_search import wc_line_search as lsearch

def nonlinear_conjugate_gradient(f, x0, alpha0=1e-6, max_iters=100000, epsilon=1e-12, reset=False, print_progress=False, f_noH = None):
    # Author: C. Howard
    # This function minimizes the input function f(x)
    # using Nonlinear Conjugate Gradient using the
    # Polak–Ribière update for the conjugate direction.
    x = np.copy(x0)
    out = f(x)
    s = -out[1]
    dx1 = np.copy(s)
    dx2 = np.copy(s)

    # print function value at beginning if desired
    if print_progress:
        print("f(x_0):", out[0])

    # define error measure
    def error(u):
        return np.linalg.norm(u,ord=np.inf)

    # do a first step
    alpha = lsearch(f, x, p=s, alpha_guess=alpha0)
    x = x + alpha*s

    # compute current gradient
    outk = f(x)

    # update history of dx variables
    dx1 = dx2
    dx2 = -outk[1]

    # print current function value if desired
    if print_progress:
        print("f(x_{0}):".format(1), outk[0])

    # perform the nonlinear conjugate gradient iteration
    num_iters=1
    fo = 1e100
    fn = outk[0]
    rel_fchng = 10*epsilon
    while(num_iters < max_iters and rel_fchng > epsilon):

        # compute beta using Polak–Ribière method
        beta = np.dot(dx2,dx2-dx1)/np.dot(dx1,dx1)

        # perform reset if necessary
        if reset:
            if beta < 0:
                beta = 0.0

        # update conjugate direction
        s = dx2 + beta*s

        # compute stepsize
        alpha = lsearch(f, x, p=s, alpha_guess=alpha0)

        # update estimate
        x = x + alpha*s

        # compute current gradient
        outk = f(x)
        fo = fn
        fn = outk[0]

        # update history of dx variables
        dx1 = dx2
        dx2 = -outk[1]
        rel_fchng = fo - fn

        # update iteration counter
        num_iters = num_iters + 1

        # print current function value if desired
        if print_progress:
            print("f(x_{0}):".format(num_iters), outk[0])
            #print("error: ",rel_fchng)


    # return the answer
    return (x, num_iters)

def quadratic(x):
    gradf = np.array([2.0*x[0]])
    return (x[0]**2, gradf)

if __name__ == "__main__":
    x0 = np.array([10.0])
    (x,n) = nonlinear_conjugate_gradient(quadratic, x0, reset=True)
    print("Soln:", x ,"| Num Iterations:", n)