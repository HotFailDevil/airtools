#!/usr/bin/env python
"""selftest"""
import logging
from numpy.linalg import svd
from numpy import array,mat,squeeze
from scipy import sparse
from numpy.testing import assert_array_almost_equal, assert_allclose,run_module_suite
"""
generate test problems from Julia by

using MatrixDepot
matrixdepot("deriv2",3,false)
"""
A = array([[-0.0277778, -0.0277778, -0.00925926],
           [-0.0277778, -0.0648148, -0.0277778],
           [-0.00925926,-0.0277778, -0.0277778 ]])
b = array([-0.01514653483985129,
            -0.03474793286789414,
            -0.022274315940957783])
x_true = array([0.09622504486493762,
                0.28867513459481287,
                0.48112522432468807])

def test_kaczmarz():
    from airtools.kaczmarz import kaczmarz
    x = kaczmarz(A,b,200,lamb=1.)[0]
    assert_array_almost_equal(x,x_true)

def test_maxent():
    from airtools.maxent import maxent

    x = maxent(A,b,lamb=.000025)[0]
    assert_array_almost_equal(x,x_true)

def test_rzr():
    from airtools.rzr import rzr
    A = array([[1,2,3],
               [0,0,0],
               [4,5,6]])
    b = array([1,2,3])
    Ar,br,g = rzr(A,b)
    assert_array_almost_equal(Ar,array([[1,2,3],
                                        [4,5,6]]))
    assert_array_almost_equal(br,array([1,3]))

def test_picard():
    from airtools.picard import picard
    U,s,V = svd(array([[3,2,2],
                       [2,3,-2],
                       [2,3,4]]))
    eta = picard(U,s,V)[0]
    assert_array_almost_equal(eta,[ 0.02132175, 0.00238076, 0.04433971])

def test_lsqlin():
    try:
        from cvxopt import matrix
    except (ImportError,RuntimeError):
        logging.error('skipped LSQ test due to missing CVXOPT library')
        return

    import airtools.lsqlin as lsqlin
    # simple Testing routines
    C = array(mat('''0.9501,0.7620,0.6153,0.4057;
    0.2311,0.4564,0.7919,0.9354;
    0.6068,0.0185,0.9218,0.9169;
    0.4859,0.8214,0.7382,0.4102;
    0.8912,0.4447,0.1762,0.8936'''))
    sC = sparse.coo_matrix(C)
    csC = lsqlin.scipy_sparse_to_spmatrix(sC)

    A = array(mat('''0.2027,0.2721,0.7467,0.4659;
    0.1987,0.1988,0.4450,0.4186;
    0.6037,0.0152,0.9318,0.8462'''))
    sA = sparse.coo_matrix(A)
    csA = lsqlin.scipy_sparse_to_spmatrix(sA)

    d = array([0.0578, 0.3528, 0.8131, 0.0098, 0.1388])
    md = matrix(d)

    b =  array([0.5251, 0.2026, 0.6721])
    mb = matrix(b)

    lb = array([-0.1] * 4)
    mlb = matrix(lb)
    mmlb = -0.1

    ub = array([2] * 4)
    mub = matrix(ub)
    mmub = 2


    opts = {'show_progress': False}

    for iC in [C, sC, csC]:
        for iA in [A, sA, csA]:
            for iD in [d, md]:
                for ilb in [lb, mlb, mmlb]:
                    for iub in [ub, mub, mmub]:
                        for ib in [b, mb]:
                            ret = lsqlin.lsqlin(iC, iD, 0, iA, ib, None, None, ilb, iub, None, opts)
                            assert_allclose(squeeze(ret['x']),[-1.00e-01, -1.00e-01,  2.15e-01,  3.50e-01],rtol=1e-2)


    #test lsqnonneg
    C = array([[0.0372, 0.2869], [0.6861, 0.7071], [0.6233, 0.6245], [0.6344, 0.6170]]);
    d = array([0.8587, 0.1781, 0.0747, 0.8405]);
    ret = lsqlin.lsqnonneg(C, d, {'show_progress': False})
    assert_allclose(squeeze(ret['x']),[2.5e-7,6.93e-1],rtol=1e-2)

if __name__ == '__main__':
#    test_kaczmarz()
    #test_maxent()
    run_module_suite()
