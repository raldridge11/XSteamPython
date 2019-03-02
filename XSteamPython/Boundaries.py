# -*- coding: utf-8 -*-
'''
Module to calculate boundaries between regions
'''
import math

import numpy as np

def b23p_t(temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam 1997
      Section 4 Auxiliary Equation for the Boundary between Regions 2 and 3 Eq 5, Page 5'''
    return 348.05185628969 - 1.1671859879975*temperature + 1.0192970039326E-03*temperature**2

def b23t_p(pressure):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam 1997
        Section 4 Auxiliary Equation for the Boundary between Regions 2 and 3 Eq 6, Page 6'''
    return 572.54459862746 + math.sqrt((pressure - 13.91883977887) / 1.0192970039326E-03)

def hB13_s(entropy):
    ''''Supplementary Release on Backward Equations ( ) , p h s for Region 3, 'Chapter 4.5 page 23.'''
    i = np.array([0, 1, 1, 3, 5, 6])
    j = np.array([0, -2, 2, -12, -4, -3])
    n = np.array([0.913965547600543, -4.30944856041991E-05, 60.3235694765419, .17518273082168E-18, 0.220000904781292, -69.0815545851641])
    sigma = entropy/3.8
    eta = n*(sigma - 0.884)**i*(sigma - 0.864)**j
    return sum(eta)*1700.0

def tB23_hs(enthalpy, entropy):
    '''Supplementary Release on Backward Equations ( ) , p h s for Region 3, Chapter 4.6 page 25.'''
    i = np.array([-12, -10, -8, -4, -3, -2, -2, -2, -2, 0, 1, 1, 1, 3, 3, 5, 6, 6, 8, 8, 8, 12, 12, 14, 14])
    j = np.array([10, 8, 3, 4, 3, -6, 2, 3, 4, 0, -3, -2, 10, -2, -1, -5, -6, -3, -8, -2, -1, -12, -1, -12, 1])
    n = np.array([6.2909626082981E-04, -8.23453502583165E-04, 5.15446951519474E-08, -1.17565945784945, 3.48519684726192, -5.07837382408313E-12, -2.84637670005479, -2.36092263939673, 6.01492324973779, 1.48039650824546, 3.60075182221907E-04, -1.26700045009952E-02, -1221843.32521413, 0.149276502463272, 0.698733471798484, -2.52207040114321E-02, 1.47151930985213E-02, -1.08618917681849, -9.36875039816322E-04, 81.9877897570217, -182.041861521835, 2.61907376402688E-06, -29162.6417025961, 1.40660774926165E-05, 7832370.62349385])
    sigma = entropy/5.3
    eta = enthalpy/3000.0
    teta = n*(eta - 0.727)**i*(sigma - 0.864)**j
    return sum(teta)*900.0
