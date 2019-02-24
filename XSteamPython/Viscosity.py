# -*- coding: utf-8 -*-
'''
* Water and steam properties according to IAPWS IF-97
* By Magnus Holmgren, www.x-eng.com
* The steam tables are free and provided as is.
* We take no responsibilities for any errors in the code or damage thereby.
* You are free to use, modify and distribute the code as long as authorship is properly acknowledged.
* Please notify me at magnus@x-eng.com if the code is used in commercial applications
'''
import math

import numpy as np

import Constants
import Regions
import Region1
import Region2
import Region3
import Region5

h0 = np.array([0.5132047, 0.3205656, 0.0, 0.0, -0.7782567, 0.1885447])
h1 = np.array([0.2151778, 0.7317883, 1.241044, 1.476783, 0.0, 0.0])
h2 = np.array([-0.2818107, -1.070786, -1.263184, 0.0, 0.0, 0.0])
h3 = np.array([0.1778064, 0.460504, 0.2340379, -0.4924179, 0.0, 0.0])
h4 = np.array([-0.0417661, 0.0, 0.0, 0.1600435, 0.0, 0.0])
h5 = np.array([0.0, -0.01578386, 0.0, 0.0, 0.0, 0.0])
h6 = np.array([0.0, 0.0, 0.0, -0.003629481, 0.0, 0.0])

def my_allregions_pT(pressure, temperature):
    '''Viscosity (IAPWS formulation 1985, Revised 2003)'''

    # Check valid area
    if temperature > 900.0 + 273.15 or \
       (temperature > 600.0 + 273.15 and pressure > 300.0) or \
       (temperature > 150.0 + 273.15 and pressure > 350.0) or \
       pressure > 500.0:
       return Constants._errorValue

    region = Regions.region_pt(pressure, temperature)
    if region is None: return Constants._errorValue
    
    density = Constants._errorValue
    if region == 1:
        density = 1.0/Region1.v1_pt(pressure, temperature)
    elif region == 2:
        density = 1.0/Region2.v2_pt(pressure, temperature)
    elif region == 3:
        density = 1.0/Region3.v3_ph(pressure, Region3.h3_pt(pressure, temperature))
    elif region == 4:
        density = Constants._errorValue
    elif region == 5:
        density = 1.0/Region5.v5_pt(pressure, temperature)

    rhos = density/317.63
    ts = temperature/647.226
    ps = pressure/22.115

    my_0 = ts**0.5/(1.0 + 0.978197/ts + 0.579829/(ts**2.0) - 0.202354/(ts**3.0))
    total = 0.0
    a, b = 1.0/ts - 1.0, rhos - 1.0
    for i in range(6):
        total += h0[i]*a**i + h1[i]*a**i*b + h2[i]*a**i*b**2 + h3[i]*a**i*b**3 + h4[i]*a**i*b**4 + h5[i]*a**i*b**5 + h6[i]*a**i*b**6

    my_1 = math.exp(rhos*total)
    return my_0*my_1*0.000055071

#Rem
#Rem Private Function my_AllRegions_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem   Dim h0, h1, h2, h3, h4, h5, h6 As Variant, rho, T, Ts, ps, my0, sum, my1, rhos, v4V, v4L, xs As Double, i As Integer
#Rem   h0 = Array(0.5132047, 0.3205656, 0, 0, -0.7782567, 0.1885447)
#Rem   h1 = Array(0.2151778, 0.7317883, 1.241044, 1.476783, 0, 0)
#Rem   h2 = Array(-0.2818107, -1.070786, -1.263184, 0, 0, 0)
#Rem   h3 = Array(0.1778064, 0.460504, 0.2340379, -0.4924179, 0, 0)
#Rem   h4 = Array(-0.0417661, 0, 0, 0.1600435, 0, 0)
#Rem   h5 = Array(0, -0.01578386, 0, 0, 0, 0)
#Rem   h6 = Array(0, 0, 0, -0.003629481, 0, 0)
#Rem
#Rem   'Calcualte density.
#Rem  Select Case region_ph(p, h)
#Rem  Case 1
#Rem    Ts = T1_ph(p, h)
#Rem    T = Ts
#Rem    rho = 1 / v1_pT(p, Ts)
#Rem  Case 2
#Rem    Ts = T2_ph(p, h)
#Rem    T = Ts
#Rem    rho = 1 / v2_pT(p, Ts)
#Rem  Case 3
#Rem    rho = 1 / v3_ph(p, h)
#Rem    T = T3_ph(p, h)
#Rem  Case 4
#Rem    xs = x4_ph(p, h)
#Rem    If p < 16.529 Then
#Rem      v4V = v2_pT(p, T4_p(p))
#Rem      v4L = v1_pT(p, T4_p(p))
#Rem    Else
#Rem      v4V = v3_ph(p, h4V_p(p))
#Rem      v4L = v3_ph(p, h4L_p(p))
#Rem     End If
#Rem     rho = 1 / (xs * v4V + (1 - xs) * v4L)
#Rem     T = T4_p(p)
#Rem  Case 5
#Rem    Ts = T5_ph(p, h)
#Rem    T = Ts
#Rem    rho = 1 / v5_pT(p, Ts)
#Rem  Case Else
#Rem   my_AllRegions_ph = CVErr(xlErrValue)
#Rem   Exit Function
#Rem  End Select
#Rem   rhos = rho / 317.763
#Rem   Ts = T / 647.226
#Rem   ps = p / 22.115
#Rem   'Check valid area
#Rem   If T > 900 + 273.15 Or (T > 600 + 273.15 And p > 300) Or (T > 150 + 273.15 And p > 350) Or p > 500 Then
#Rem     my_AllRegions_ph = CVErr(xlErrValue)
#Rem     Exit Function
#Rem   End If
#Rem   my0 = Ts ^ 0.5 / (1 + 0.978197 / Ts + 0.579829 / (Ts ^ 2) - 0.202354 / (Ts ^ 3))
#Rem
#Rem   sum = 0
#Rem   For i = 0 To 5
#Rem       sum = sum + h0(i) * (1 / Ts - 1) ^ i + h1(i) * (1 / Ts - 1) ^ i * (rhos - 1) ^ 1 + h2(i) * (1 / Ts - 1) ^ i * (rhos - 1) ^ 2 + h3(i) * (1 / Ts - 1) ^ i * (rhos - 1) ^ 3 + h4(i) * (1 / Ts - 1) ^ i * (rhos - 1) ^ 4 + h5(i) * (1 / Ts - 1) ^ i * (rhos - 1) ^ 5 + h6(i) * (1 / Ts - 1) ^ i * (rhos - 1) ^ 6
#Rem   Next i
#Rem   my1 = Exp(rhos * sum)
#Rem   my_AllRegions_ph = my0 * my1 * 0.000055071
#Rem End Function