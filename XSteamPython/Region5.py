# -*- coding: utf-8 -*-
'''
Region 5 functions
'''
import math

import numpy as np
import scipy
from scipy import optimize

try:
    import Constants
    import Region2
except ImportError:
    from . import Constants
    from . import Region2

j0 = np.array([0, 1, -3, -2, -1, 2])
n0 = np.array([-13.179983674201, 6.8540841634434, -0.024805148933466, 0.36901534980333, -3.1161318213925, -0.32961626538917])
ir = np.array([1, 1, 1, 2, 3])
jr = np.array([0, 1, 3, 9, 3])
nr = np.array([-1.2563183589592E-04, 2.1774678714571E-03, -0.004594282089991, -3.9724828359569E-06, 1.2919228289784E-07])

def h5_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam September 1997
        Basic Equation for Region 5
        Eq 32,33, Page 36, Tables 37-41'''
    tau = 1000.0/temperature
    gamma0_tau = n0*j0*tau**(j0 - 1)
    gammar_tau = nr*jr*pressure**ir*tau**(jr - 1)
    return Constants._R*temperature*tau*(gamma0_tau.sum() + gammar_tau.sum())

def v5_pt(pressure, temperature):
    ''' Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997 Basic Equation for Region 5
    Eq 32,33, Page 36, Tables 37-41'''
    tau = 1000.0/temperature
    gamma0_pi = 1.0/pressure
    gammar_pi = sum(nr*ir*pressure**(ir - 1)*tau**jr)
    return Constants._R*temperature*(gamma0_pi + gammar_pi)/1000.0

def u5_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997 Basic Equation for Region 5
    Eq 32,33, Page 36, Tables 37-41'''
    tau = 1000.0/temperature
    gamma0_pi = 1.0/pressure
    gamma0_tau = sum(n0*j0*tau**(j0 - 1))
    gammar_pi = sum(nr*ir*pressure**(ir - 1)*tau**jr)
    gammar_tau = sum(nr*pressure**ir*jr*tau**(jr - 1))
    return Constants._R*temperature*(tau*(gamma0_tau + gammar_tau) - pressure*(gamma0_pi + gammar_pi))

def cp5_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997 Basic Equation for Region 5
    Eq 32,33, Page 36, Tables 37-41'''
    tau = 1000.0/temperature
    gamma0_tautau = sum(n0*j0*(j0 - 1)*tau**(j0 - 2))
    gammar_tautau = sum(nr*pressure**ir*jr*(jr - 1)*tau**(jr - 2))
    return -Constants._R*tau**2*(gamma0_tautau + gammar_tautau)

def s5_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997 Basic Equation for Region 5
    Eq 32,33, Page 36, Tables 37-41'''
    tau = 1000.0/temperature
    gamma0_tau = sum(n0*j0*tau**(j0 - 1))
    gamma0 = sum(n0*tau**j0) + math.log(pressure)
    gammar = sum(nr*pressure**ir*tau**jr)
    gammar_tau = sum(nr*pressure**ir*jr*tau**(jr - 1))
    return Constants._R*(tau*(gamma0_tau + gammar_tau) - (gamma0 + gammar))

def cv5_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997 Basic Equation for Region 5
    Eq 32,33, Page 36, Tables 37-41'''
    tau = 1000.0/temperature
    gamma0_tautau = sum(n0*(j0 - 1)*j0*tau**(j0 - 2))
    gammar_pi = sum(nr*ir*pressure**(ir - 1)*tau**jr)
    gammar_pitau = sum(nr*ir*pressure**(ir - 1)*jr*tau**(jr - 1))
    gammar_pipi = sum(nr*ir*(ir - 1)*pressure**(ir - 2)*tau**jr)
    gammar_tautau = sum(nr*pressure**ir*jr*(jr - 1)*tau**(jr - 2))
    return Constants._R*(-(tau**2*(gamma0_tautau + gammar_tautau)) - (1.0 + pressure*gammar_pi - tau*pressure*gammar_pitau)**2 / (1.0 - pressure**2*gammar_pipi))

def w5_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997 Basic Equation for Region 5
    Eq 32,33, Page 36, Tables 37-41'''
    tau = 1000.0/temperature
    gamma0_tautau = sum(n0*(j0 - 1)*j0*tau**(j0 - 2))
    gammar_pi = sum(nr*ir*pressure**(ir - 1)*tau**jr)
    gammar_pitau = sum(nr*ir*pressure**(ir - 1)*jr*tau**(jr - 1))
    gammar_pipi = sum(nr*ir*(ir - 1)*pressure**(ir - 2)*tau**jr)
    gammar_tautau = sum(nr*pressure**ir*jr*(jr - 1)*tau**(jr - 2))
    return math.sqrt(1000.0*Constants._R*temperature*(1.0 + 2.0*pressure*gammar_pi + pressure**2*gammar_pi**2) / ((1.0 - pressure**2*gammar_pipi) + (1.0 + pressure*gammar_pi - tau*pressure*gammar_pitau)**2 / (tau**2*(gamma0_tautau + gammar_tautau))))

def t5_ph(pressure, enthalpy):
    '''Solve with Secant Method'''
    f = lambda temperature: h5_pt(pressure, temperature) - enthalpy
    return optimize.newton(f, 1073.15, tol=1e-5)

def t5_ps(pressure, entropy):
    '''Solve with Secant Method'''
    f = lambda temperature: s5_pt(pressure, temperature) - entropy
    return optimize.newton(f, 1073.15, tol=1e-6)

def t5_prho(pressure, density):
    '''Solve with Secant Method'''
    f = lambda temperature: 1.0/Region2.v2_pt(pressure, temperature) - density
    return optimize.newton(f, 1073.15, tol=1e-6)