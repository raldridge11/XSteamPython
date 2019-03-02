# -*- coding: utf-8 -*-
'''
Region 1 functions
'''
import math

import numpy as np
import scipy
from scipy import optimize

try:
    import Constants
except ImportError:
    from . import Constants

i = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 8, 8, 21, 23, 29, 30, 31, 32])
j = np.array([-2, -1, 0, 1, 2, 3, 4, 5, -9, -7, -1, 0, 1, 3, -3, 0, 1, 3, 17, -4, 0, 6, -5, -2, 10, -8, -11, -6, -29, -31, -38, -39, -40, -41])
n = np.array([0.14632971213167, -0.84548187169114, -3.756360367204, 3.3855169168385, -0.95791963387872, 0.15772038513228, -0.016616417199501, 8.1214629983568E-04, 2.8319080123804E-04, -6.0706301565874E-04, -0.018990068218419, -0.032529748770505, -0.021841717175414, -5.283835796993E-05, -4.7184321073267E-04, -3.0001780793026E-04, 4.7661393906987E-05, -4.4141845330846E-06, -7.2694996297594E-16, -3.1679644845054E-05, -2.8270797985312E-06, -8.5205128120103E-10, -2.2425281908E-06, -6.5171222895601E-07, -1.4341729937924E-13, -4.0516996860117E-07, -1.2734301741641E-09, -1.7424871230634E-10, -6.8762131295531E-19, 1.4478307828521E-20, 2.6335781662795E-23, -1.1947622640071E-23, 1.8228094581404E-24, -9.3537087292458E-26])

# IAPWS IF 97 Calling functions
#
# Functions for region 1
def v1_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    5 Equations for Region 1, Section. 5.1 Basic Equation Eqution 7, Table 3, Page 6'''
    ps = pressure/16.53
    tau = 1386.0/temperature
    g_p = -n*i*(7.1 - ps)**(i - 1)*(tau - 1.222)**j
    return Constants._R*temperature*ps*sum(g_p)/(1000.0*pressure)

def h1_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997 5 Equations for Region 1, Section. 5.1 Basic Equation Equation 7, Table 3, Page 6'''
    p = pressure/16.53
    tau = 1386.0/temperature
    g_t = n*j*((7.1 - p)**i)*(tau - 1.222)**(j - 1)

    return Constants._R*temperature*tau*g_t.sum()

def u1_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    5 Equations for Region 1, Section. 5.1 Basic Equation'''
    pressure = pressure/16.53
    tau = 1386.0/temperature
    g_p = -n*i*(7.1 - pressure)**(i - 1)*(tau - 1.222)**j
    g_t = n*(7.1 - pressure)**i*j*(tau - 1.222)**(j - 1)
    return Constants._R*temperature*(tau*sum(g_t) - pressure*sum(g_p))

def s1_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    5 Equations for Region 1, Section. 5.1 Basic Equation Equation 7, Table 3, Page 6'''
    pressure = pressure/16.53
    temperature = 1386.0/temperature
    g_t = n*(7.1 - pressure)**i*j*(temperature - 1.222)**(j - 1)
    g = n*(7.1 - pressure)**i*(temperature - 1.222)**j
    return Constants._R*(temperature*sum(g_t) - sum(g))

def cp1_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    5 Equations for Region 1, Section. 5.1 Basic Equation Equation 7, Table 3, Page 6'''
    pressure = pressure/16.53
    temperature = 1386.0/temperature
    g_tt = n*(7.1 - pressure)**i*j*(j-1)*(temperature - 1.222)**(j - 2)
    return -Constants._R*temperature**2*sum(g_tt)

def cv1_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    5 Equations for Region 1, Section. 5.1 Basic Equation Equation 7, Table 3, Page 6'''
    pressure = pressure/16.53
    temperature = 1386.0/temperature
    g_p = -n*i*(7.1 - pressure)**(i - 1)*(temperature - 1.222)**j
    g_pp = n*i*(i - 1)*(7.1 - pressure)**(i - 2)*(temperature - 1.222)**j
    g_pt = -n*i*(7.1 - pressure)**(i - 1)*j*(temperature - 1.222)**(j - 1)
    g_tt = n*(7.1 - pressure)**i*j*(j - 1)*(temperature - 1.222)**(j - 2)
    return Constants._R*(-1.0*(temperature**2*sum(g_tt)) + (sum(g_p) - temperature*sum(g_pt))**2/sum(g_pp))

def w1_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    5 Equations for Region 1, Section. 5.1 Basic Equation Equation 7, Table 3, Page 6'''
    pressure = pressure/16.53
    tau = 1386.0/temperature
    g_p = -n*i*(7.1 - pressure)**(i - 1)*(tau - 1.222)**j
    g_pp = n*i*(i - 1)*(7.1 - pressure)**(i - 2)*(tau - 1.222)**j
    g_pt = -n*i*(7.1 - pressure)**(i - 1)*j*(tau - 1.222)**(j - 1)
    g_tt = n*(7.1 - pressure)**i*j*(j - 1)*(tau - 1.222)**(j - 2)
    a = 1000.0*Constants._R*temperature*sum(g_p)**2
    b = (sum(g_p) - tau*sum(g_pt))**2
    c = tau**2*sum(g_tt)
    d = b/c - sum(g_pp)
    return math.sqrt(a/d)

def t1_ph(pressure, enthalpy):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    5 Equations for Region 1, Section. 5.1 Basic Equation, 5.2.1 The Backward Equation T ( p,h )
    Eqution 11, Table 6, Page 10'''
    i = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 5, 6])
    j = np.array([0, 1, 2, 6, 22, 32, 0, 1, 2, 3, 4, 10, 32, 10, 32, 10, 32, 32, 32, 32])
    n = np.array([-238.72489924521, 404.21188637945, 113.49746881718, -5.8457616048039, -1.528548241314E-04, -1.0866707695377E-06, -13.391744872602, 43.211039183559, -54.010067170506, 30.535892203916, -6.5964749423638, 9.3965400878363E-03, 1.157364750534E-07, -2.5858641282073E-05, -4.0644363084799E-09, 6.6456186191635E-08, 8.0670734103027E-11, -9.3477771213947E-13, 5.8265442020601E-15, -1.5020185953503E-17])

    h = enthalpy/2500.0
    T = n*pressure**i*(h + 1)**j
    return T.sum()

def t1_ps(pressure, entropy):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    5 Equations for Region 1, Section. 5.1 Basic Equation, 5.2.2 The Backward Equation T(p, s)Equation 13, Table 8, Page 11'''
    i = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 4])
    j = np.array([0, 1, 2, 3, 11, 31, 0, 1, 2, 3, 12, 31, 0, 1, 2, 9, 31, 10, 32, 32])
    n = np.array([174.78268058307, 34.806930892873, 6.5292584978455, 0.33039981775489, -1.9281382923196E-07, -2.4909197244573E-23, -0.26107636489332, 0.22592965981586, -0.064256463395226, 7.8876289270526E-03, 3.5672110607366E-10, 1.7332496994895E-24, 5.6608900654837E-04, -3.2635483139717E-04, 4.4778286690632E-05, -5.1322156908507E-10, -4.2522657042207E-26, 2.6400441360689E-13, 7.8124600459723E-29, -3.0732199903668E-31])
    return sum(n*pressure**i*(entropy + 2)**j)

def p1_hs(enthalpy, entropy):
    '''Supplementary Release on Backward Equations for Pressure as a Function of Enthalpy and Entropy p(h,s) to the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam
    5 Backward Equation p(h,s) for Region 1'''
    i = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 5])
    j = np.array([0, 1, 2, 4, 5, 6, 8, 14, 0, 1, 4, 6, 0, 1, 10, 4, 1, 4, 0])
    n = np.array([-0.691997014660582, -18.361254878756, -9.28332409297335, 65.9639569909906, -16.2060388912024, 450.620017338667, 854.68067822417, 6075.23214001162, 32.6487682621856, -26.9408844582931, -319.9478483343, -928.35430704332, 30.3634537455249, -65.0540422444146, -4309.9131651613, -747.512324096068, 730.000345529245, 1142.84032569021, -436.407041874559])
    enthalpy = enthalpy/3400.0
    entropy = entropy/7.6
    p = n*(enthalpy + 0.05)**i*(entropy + 0.05)**j
    return sum(p)*100.0

def t1_prho(pressure, density):
    '''Solve with Secant Method'''
    f = lambda temperature: 1.0/v1_pt(pressure, temperature) - density
    return scipy.optimize.newton(f, 273.15, tol=1e-6)
