import os
import time
import numpy as np
import optimization.quasi_newton as qn
import optimization.nconj_grad as ncg
import matplotlib.pyplot as plot
from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

def f1(x):
    n = x.shape[0]
    return (np.sum(x**2), 2*x, 2*np.eye(n))

def f2(x):
    return (np.sum(x**4), 4*x**3, 12*np.diag(x**2))

def g(x,alpha):
    (v, gradv, Hv) = f1(x)
    (u, gradu, Hu) = f2(x)
    return (alpha*u + (1-alpha)*v,
            alpha*gradu + (1-alpha)*gradv,
            alpha*Hu + (1-alpha)*Hv
    )

def f1_noH(x):
    n = x.shape[0]
    return (np.sum(x**2), 2*x)

def f2_noH(x):
    return (np.sum(x**4), 4*x**3)
 
def g_noH(x,alpha):
    (v, gradv) = f1_noH(x)
    (u, gradu) = f2_noH(x)
    return (alpha*u + (1-alpha)*v,
            alpha*gradu + (1-alpha)*gradv
    )

def main_analysis(gfunc, alpha_range, dim_range, x_scalar0, optimizer, print_progress=False, epsilon=1e-12):
    out_size = (len(alpha_range), len(dim_range))
    iteration_mat = np.zeros(out_size) # store number of iterations
    runtime_mat   = np.zeros(out_size) # store runtime of optimizations
    memory_mat    = np.zeros(out_size) # store memory used

    for ia in range(0,len(alpha_range)):
        # define func to be solved
        def func(x):
            return gfunc(x, alpha_range[ia])

        for id in range(0,len(dim_range)):

            # construct initial guess
            x0 = x_scalar0 * np.ones((dim_range[id],))

            # perform test
            start = time.time()
            (soln, niters) = optimizer(func, x0, epsilon=epsilon)
            end = time.time()

            # set data that matters
            iteration_mat[ia, id] = niters
            runtime_mat[ia, id] = end - start

            # print progress
            print("Completed alpha={0} and d={1}".format(alpha_range[ia],dim_range[id]))

    # return the result
    return (iteration_mat, runtime_mat)

# run the main analysis
if  __name__ == "__main__":
    alpha_values = [0, 0.25, 0.5, 0.75, 1]
    low_dims   = [10, 50, 100]
    high_dims  = [1000, 2000, 3000]
    xscalar0   = 2
    counter    = 0

    # compute low dimensional data
    def analysis_func(method, dimensions, title_str, counter):
        (imat, rmat) = main_analysis(g, alpha_values, dimensions, xscalar0, 
                                method, print_progress=True, epsilon=1e-3)
        (na, nd) = imat.shape
        legend_strings = []

        # plot the number of iterations
        plot.figure(counter)
        for id in range(0,len(dimensions)):
            plot.plot(alpha_values, imat[:,id])
            legend_strings.append('d={0}'.format(dimensions[id]))
        plot.legend(legend_strings, loc='upper left')
        plot.title(title_str)
        plot.xlabel(r'$\alpha$')
        plot.ylabel('Number of Iterations until Method Converged')
        counter = counter + 1

        # plot the runtime
        plot.figure(counter)
        for id in range(0,len(dimensions)):
            plot.plot(alpha_values, rmat[:,id])
        plot.legend(legend_strings, loc='upper left')
        plot.title(title_str)
        plot.xlabel(r'$\alpha$')
        plot.ylabel('Runtime until convergence (seconds)')
        counter = counter + 1

        return counter

    # perform tests for quasi-newton
    counter = analysis_func(qn.quasi_newton_cg, low_dims, 'Quasi-Newton | Low-Dim', counter)
    counter = analysis_func(qn.quasi_newton_cg, high_dims, 'Quasi-Newton | High-Dim', counter)

    # perform tests for nonlinear conjugate gradient
    counter = analysis_func(ncg.nonlinear_conjugate_gradient, 
                            low_dims, 'Polak-Ribiere | Low-Dim', counter)
    counter = analysis_func(ncg.nonlinear_conjugate_gradient, 
                            high_dims, 'Polak-Ribiere | High-Dim', counter)

    # plot the results
    file_path = os.path.dirname(os.path.realpath(__file__))
    dir=file_path + '/analysis/simple_convex'
    plot_names = ['qn_low_iter.png', 'qn_low_rt.png',
    'qn_high_iter.png', 'qn_high_rt.png', 
    'pr_low_iter.png', 'pr_low_rt.png',
    'pr_high_iter.png', 'pr_high_rt.png']
    for k in range(0,counter):
        plot.figure(k)
        filename = dir + '/' + plot_names[k]
        plot.savefig(filename, dpi=90)

    # make the plots show
    #plot.show()
