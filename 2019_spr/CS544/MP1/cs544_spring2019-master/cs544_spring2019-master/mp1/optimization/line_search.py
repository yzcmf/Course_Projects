import numpy as np

def bt_line_search(f, x, p, alpha_guess=1.0, beta=0.5, c1=1e-4, c2=0.9, maxiter=30):
    # Author: C. Howard
    # This code is doing an approximate line search using
    # backtracking line search

    pmag = np.linalg.norm(p)
    pn = p/pmag
    p[:] = pn[:]

    # compute useful values for when alpha = 0
    out0 = f(x)
    Phi0 = out0[0]
    dPhi0 = np.dot(out0[1],p)

    # if direction is not descent direction
    # then flip the sign of descent dir and slope
    if dPhi0 > 0:
        dPhi0 = -dPhi0
        p[:] = -p[:]

    # define useful functions to compute a good stepsize
    def Phi(alpha):
        return f(x + alpha*p)[0]
    def dPhi_da(alpha):
        return np.dot(f(x + alpha*p)[1],p)
    def condition1(alpha):
        return (Phi(alpha) <= (Phi0 + c1*alpha*dPhi0) )
    def condition2(alpha):
        return (dPhi_da(alpha) >= (c2*dPhi0))
    def scondition2(alpha):
        return (np.abs(dPhi_da(alpha)) <= np.abs(c2*dPhi0))

    # define the initial alpha
    alpha = alpha_guess

    # perform inexact line search with armijo rule loop
    iter = 0
    while(iter < maxiter and (not condition1(alpha)) ):
        alpha = alpha*beta
        iter = iter + 1

    # return the alpha satisfying the conditions
    #print("alpha: ", alpha)
    return alpha

def wc_line_search(f, x, p, alpha_guess=1e-10, beta=10.0, c1=1e-4, c2=0.9, maxiter=30):
    # Author: C. Howard
    # This code is doing an approximate line search using
    # the Wolf Conditions (as seen in class)

    pmag = np.linalg.norm(p)
    pn = p/pmag
    p[:] = pn[:]

    # compute useful values for when alpha = 0
    out0 = f(x)
    Phi0 = out0[0]
    dPhi0 = np.dot(out0[1],p)

    # if direction is not descent direction
    # then flip the sign of descent dir and slope
    if dPhi0 > 0:
        dPhi0 = -dPhi0
        p[:] = -p[:]

    # define useful functions to compute a good stepsize
    def Phi(alpha):
        return f(x + alpha*p)[0]
    def dPhi_da(alpha):
        return np.dot(f(x + alpha*p)[1],p)
    def condition1(alpha, Phi_a):
        return (Phi(alpha) <= (Phi0 + c1*alpha*dPhi0) )
    def condition2(dPhi_a):
        return (dPhi_a >= (c2*dPhi0))
    def scondition2(alpha):
        return (np.abs(dPhi_da(alpha)) <= np.abs(c2*dPhi0))
    '''
    def condition1(alpha):
        return (Phi(alpha) <= (Phi0 + c1*alpha*dPhi0) )
    def condition2(alpha):
        return (dPhi_da(alpha) >= (c2*dPhi0))
    '''

    # define the initial alpha
    alpha = alpha_guess

    # perform inexact line search with armijo rule loop
    iter = 0
    out = f(x + alpha*p)
    check = condition1(alpha,out[0]) and condition2(np.dot(out[1],p))
    while(iter < maxiter and (not check) ):
        alpha = alpha*beta
        out = f(x + alpha*p)
        check = condition1(alpha,out[0]) and condition2(np.dot(out[1],p))
        iter = iter + 1

    # return the alpha satisfying the conditions
    #print("alpha: ", alpha)
    return alpha

def surrogate_line_search(f, x, p, alpha_guess=100.0, beta=0.5, c1=1e-4, c2=0.9, maxiter=3):
    # Author: C. Howard
    # This code is doing an approximate line search using
    # the Wolf Conditions (as seen in class)

    pmag = np.linalg.norm(p)
    pn = p/pmag
    p[:] = pn[:]

    # compute useful values for when alpha = 0
    out0 = f(x)
    Phi0 = out0[0]
    dPhi0 = np.dot(out0[1],p)

    # if direction is not descent direction
    # then flip the sign of descent dir and slope
    if dPhi0 > 0:
        dPhi0 = -dPhi0
        p[:] = -p[:]

    # define useful functions to compute a good stepsize
    def Phi(alpha):
        return f(x + alpha*p)[0]
    def dPhi_da(alpha):
        return np.dot(f(x + alpha*p)[1],p)

    # define the initial alpha
    alpha = alpha_guess

    '''
    A = np.zeros((4,4))
    b = np.zeros((4,))

    # define matrix
    A[0,0:] = [1.0, 0.0, 0.0, 0.0]
    A[1,0:] = [1.0, alpha, alpha**2, alpha**3]
    A[2,0:] = [0, 1.0, 0.0, 0.0]
    A[3,0:] = [0, 1.0, 2*alpha, 3*alpha**2]

    # define the stuff to solve for
    b[:] = [Phi0, outg[0], dPhi0, np.dot(outg[1],p)]

    def surrogate(a):
        return c[0] + a*(c[1] + a*(c[2] + a*c[3]))
    def surrogate_d1(a):
        return (c[1] + a*(2.0*c[2] + 3.0*a*c[3]))
    def surrogate_d2(a):
        return (2.0*c[2] + 6.0*a*c[3])

    '''

    def solve_quadratic(a):
        # compute useful values for alpha_guess
        outg = f(x + a*p)
        A = np.zeros((3,3))
        b = np.zeros((3,))

        # define matrix
        A[0,0:] = [1.0, 0.0, 0.0]
        A[1,0:] = [1.0, a, a**2]
        A[2,0:] = [0, 1.0, 0.0]

        # define the stuff to solve for
        b[:] = [Phi0, outg[0], dPhi0]

        # solve for coefficients
        c = np.linalg.solve(A,b)

        return c

    def surrogate(a, c):
        return c[0] + a*(c[1] + a*c[2])
    def surrogate_d1(a, c):
        return c[1] + a*2.0*c[2]
    def surrogate_d2(a, c):
        return 2.0*c[2]

    # perform minimization using newton
    ag = alpha
    while True:
        c = solve_quadratic(a=ag)
        d1 = surrogate_d1(ag, c)
        d2 = surrogate_d2(ag, c)
        if d2 != 0.0:
            ag = min(ag/10.0, ag - d1/d2)
        else:
            break

        out_t = f(x + ag*p)
        #print("alpha = {0} | {1} vs {2}".format(ag, out_t[0], Phi0))
        if( out_t[0] < Phi0 ):
            alpha = ag
            break
    
    # return the alpha satisfying the conditions
    #print("alpha: ", alpha)
    return alpha