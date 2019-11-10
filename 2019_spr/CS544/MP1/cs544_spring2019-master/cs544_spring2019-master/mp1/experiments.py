import os
import time
import numpy as np
import optimization.quasi_newton as qn
import optimization.nconj_grad as ncg
import matplotlib.pyplot as plot
import opt_in_cv.log_reg as lr
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from functools import partial
import pickle
import argparse


# hyper-param
TEST_SIZE = 0.1
LMBDA = 0.1 # regularization parameter
TARGET = 1
PRINT_DETAIL = True
EPS = 1e-8




def load_Cifar():
    file_path = os.path.dirname(os.path.realpath(__file__))
    with open(file_path + "/data/cifar-10-batches-py/data_batch_1","rb") as fo:
        dic = pickle.load(fo,encoding='bytes')
    return (dic[b'data'],np.array(dic[b'labels']))

def load_data(load_ds, ds_name):
    X,y = load_ds()
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=TEST_SIZE)
    # only use to recongnize digit 1
    y_train = (y_train==TARGET).flatten()
    y_test = (y_test==TARGET).flatten()
    train_size, feature_num = X_train.shape

    # init model parameter
    theta = np.zeros(feature_num)
    print("{} data loaded".format(ds_name))
    print("train size: {}".format(len(X_train)))
    print("test size: {}".format(len(X_test)))
    print("number of features: {}".format(len(theta)))
    print("classification target: {}".format(TARGET))

    # bind X_train to loss function, grad, hassian and approx hassian
    f = partial(lr.costFunctionReg, X=X_train, y=y_train, lmbda=LMBDA)
    f_grad = partial(lr.gradRegularization, X=X_train, y=y_train, lmbda=LMBDA)
    f_hassian = partial(lr.Hessian, X=X_train, y=y_train, lmbda=LMBDA)

    def f_h_approx(theta):
        feature_num = len(theta)
        h_approx = np.zeros(feature_num,feature_num)
        for i in range(feature_num):
            h_approx[i] = lr.finite_diff(f_grad,theta,i)
        return h_approx

    # gather it all
    def g(x):
        H = lr.Hmatvec(x,X_train, y_train, LMBDA)
        return (f(x), f_grad(x), f_hassian(x))
    
    def g_noH(x):
        return (f(x), f_grad(x))

    # return train precision and test precision
    def tester(theta):
        train_pred = X_train @ theta
        train_pred = (train_pred > 0.5).flatten()
        test_pred = ((X_test @ theta) > 0.5).flatten()
        #train_prec = precision_score(y_train,train_pred)
        #test_prec = precision_score(y_test,test_pred)
        train_acc = accuracy_score(y_train,train_pred)
        test_acc = accuracy_score(y_test,test_pred)
        return (train_acc, test_acc)

    return (theta,g,g_noH,tester)
'''
given model and optimizer, return wanted stats
@params theta: model parameter, should be a vector of size "feature_num"
@params func: target function, should only take 1 parameter (which should be theta)
@params optimizer: optimizer, should take func and theta as parameters
@params tester: optional tester, if not provided, the precision score will not be reported
return (num_iter, runtime, train_prec, test_prec, final_params)
'''
def train(theta, func, func_noH, optimizer, tester=None, eps=1e-12, print_progress=False):
    start = time.time()
    soln, niters = optimizer(func, theta, max_iters=10000, epsilon=eps, print_progress=print_progress, f_noH=func_noH)
    end = time.time()
    runtime = end - start
    if tester is not None:
        train_score,test_score = tester(soln)
    else:
        train_score,test_score = None, None
    return (niters, runtime, train_score, test_score, soln)

def main(ds):
    if ds != "mnist" and ds != "cifar":
        print("error, dataset should either be \"mnist\" or \"cifar\"")
    elif ds == "mnist":
        theta,g,g_noH, tester = load_data(lr.load_MNST_data,"MNIST")
    else:
        theta,g,g_noH,tester = load_data(load_Cifar,"Cifar")

    print("Quasi-Newton: iterations,runtime,train precision,test precision")
    qn_res = train(theta.copy(), g, g_noH, qn.quasi_newton_cg, tester, eps=EPS, print_progress=PRINT_DETAIL)
    print("              {},{},{},{}".format(*(qn_res[:4])))
    print("Polak-Ribiere: iterations,runtime,train precision,test precision")
    pr_res = train(theta.copy(), g_noH, g_noH, ncg.nonlinear_conjugate_gradient, tester, eps=EPS, print_progress=PRINT_DETAIL)
    print("              {},{},{},{}".format(*(pr_res[:4])))

if __name__ == "__main__":
    # command line argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", default="mnist", 
        help="either mnist or cifar, default to mnist")
    parser.add_argument("-p", "--print", action="store_true",
        help="print details")
    args = parser.parse_args()
    ds = args.data
    PRINT_DETAIL = args.print
    main(ds)
