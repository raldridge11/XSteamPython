# -*- coding: utf-8 -*-
'''
* Water and steam properties according to IAPWS IF-97
* By Magnus Holmgren, www.x-eng.com
* The steam tables are free and provided as is.
* We take no responsibilities for any errors in the code or damage thereby.
* You are free to use, modify and distribute the code as long as authorship is properly acknowledged.
* Please notify me at magnus@x-eng.com if the code is used in commercial applications
'''
import Constants
import Convert
import Region1
import Region2
import Region3
import Region4
import Region5
import Regions

englishUnits = False

def Tsat_p(pressure):
    '''Returns saturation temperature as a function of pressure'''
    pressureMin, pressureMax = 0.000611657, 22.06395 + 0.001
    pressure = Convert.toSIUnit(float(pressure), 'pressure', englishUnits=englishUnits)

    if pressure >= pressureMin and pressure <= pressureMax:
        return Convert.fromSIUnit(Region4.t4_p(pressure), 'temperature', englishUnits=englishUnits)
    else:
        return Constants._errorValue

def Tsat_s(entropy):
    '''Returns saturation temperature as a function of entropy'''
    if englishUnits: entropy = Convert.toSIUnit(float(entropy), 'entropy')
    entropyMin, entropyMax = -0.0001545495919, 9.155759395

    if entropy > entropyMin and entropy < entropyMax:
        return Convert.fromSIUnit(Region4.t4_p(Region4.p4_s(entropy)), 'temperature', englishUnits=englishUnits)
    else:
        return Constants._errorValue

def T_ph(pressure, enthalpy):
    '''Returns temperature as a function of pressure and enthalpy'''
    pressure = Convert.toSIUnit(float(pressure), 'pressure', englishUnits=englishUnits)
    enthalpy = float(enthalpy)
    if englishUnits: enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')
    temperature = 0.0

    region = Regions.region_ph(pressure, enthalpy)
    if region is None: return Constants._errorValue

    if region is 1:
        temperature = Region1.t1_ph(pressure, enthalpy)
    elif region is 2:
        temperature = Region2.t2_ph(pressure, enthalpy)
    elif region is 3:
        temperature = Region3.t3_ph(pressure, enthalpy)
    elif region is 4:
        temperature = Region4.t4_p(pressure)
    elif region is 5:
        temperature = Region5.t5_ph(pressure, enthalpy)

    return Convert.fromSIUnit(temperature, 'temperature', englishUnits=englishUnits)

def T_ps(pressure, entropy):
    '''Returns temperature as a function of pressure and entropy'''
    pressure = Convert.toSIUnit(float(pressure), 'pressure', englishUnits=englishUnits)
    entropy = float(entropy)
    if englishUnits: entropy = Convert.toSIUnit(entropy, 'entropy')
    temperature = 0

    region = Regions.region_ps(pressure, entropy)
    if region is None: return Constants._errorValue

    if region is 1:
        temperature = Region1.t1_ps(pressure, entropy)
    elif region is 2:
        temperature = Region2.t2_ps(pressure, entropy)
    elif region is 3:
        temperature = Region3.t3_ps(pressure, entropy)
    elif region is 4:
        temperature = Region4.t4_p(pressure)
    elif region is 5:
        temperature = Region5.t5_ps(pressure, entropy)

    return Convert.fromSIUnit(temperature, 'temperature', englishUnits=englishUnits)

def T_hs(enthalpy, entropy):
    enthalpy, entropy = float(enthalpy), float(entropy)
    if englishUnits:
        enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')
        entropy = Convert.toSIUnit(entropy, 'entropy')
    temperature = 0.0

    region = Regions.region_hs(enthalpy, entropy)
    if region is None or region is 5: return Constants._errorValue

    if region is 1:
        temperature = Region1.t1_ph(Region1.p1_hs(enthalpy, entropy), enthalpy)
    elif region is 2:
        temperature = Region2.t2_ph(Region2.p2_hs(enthalpy, entropy), enthalpy)
    elif region is 3:
        temperature = Region3.t3_ph(Region3.p3_hs(enthalpy, entropy), enthalpy)
    elif region is 4:
        temperature = Region4.t4_hs(enthalpy, entropy)

    return Convert.fromSIUnit(temperature, 'temperature', englishUnits=englishUnits)

def Psat_T(temperature):
    '''Saturation Pressure as a function of temperature'''
    temperature = Convert.toSIUnit(float(temperature), 'temperature', englishUnits=englishUnits)
    pressure = 0.0
    if temperature <= 647.096 and temperature > 273.15:
        pressure = Convert.fromSIUnit(Region4.p4_t(temperature), 'pressure', englishUnits=englishUnits)
    else:
        pressure = Constants._errorValue
    return pressure

def Psat_s(entropy):
    entropy = float(entropy)

    if englishUnits:
        entropy = Convert.toSIUnit(entropy, 'entropy')

    if entropy > -0.0001545495919 and entropy < 9.155759395:
        return Convert.fromSIUnit(Region4.p4_s(entropy), 'pressure', englishUnits=englishUnits)
    else:
        return Constants._errorValue

def P_hs(enthalpy, entropy):
    enthalpy, entropy = float(enthalpy), float(entropy)
    if englishUnits:
        enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')
        entropy = Convert.toSIUnit(entropy, 'entropy')
    pressure = 0.0

    region = Regions.region_hs(enthalpy, entropy)
    if region is None or region == 5: return Constants._errorValue

    if region == 1:
        pressure = Region1.p1_hs(enthalpy, entropy)
    elif region == 2:
        pressure = Region2.p2_hs(enthalpy, entropy)
    elif region == 3:
        pressure = Region3.p3_hs(enthalpy, entropy)
    elif region == 4:
        pressure = Region4.p4_t(Region4.t4_hs(enthalpy, entropy))

    return Convert.fromSIUnit(pressure, 'pressure', englishUnits=englishUnits)

#Rem Function p_hrho(ByVal h As Double, ByVal rho As Double) As Double #7 and #18
#Rem   Dim rhos As Double
#Rem   High_Bound = fromSIunit_p(5000)
#Rem   Low_Bound = fromSIunit_p(0.000611657)
#Rem   p = fromSIunit_p(10)
#Rem   rhos = 1 / v_ph(p, h)
#Rem   Do While Abs(rho - rhos) > 0.0000001
#Rem     rhos = 1 / v_ph(p, h)
#Rem     If rhos >= rho Then
#Rem       High_Bound = p
#Rem     Else
#Rem       Low_Bound = p
#Rem     End If
#Rem     p = (Low_Bound + High_Bound) / 2
#Rem     ' MsgBox "low=" + CStr(Low_Bound) + " high=" + CStr(High_Bound)
#Rem
#Rem     Loop
#Rem     p_hrho = p    ' should be kPa
#Rem End Function

#Rem 'Function p_Tv(ByVal T As Double, ByVal v As Double) As Double #19
#Rem 'Dim p_max As Double
#Rem 'Dim p_min As Double
#Rem 'Dim p_mid As Double
#Rem 'Dim T_search As Double
#Rem 'p_max = 30000
#Rem 'p_min = 0
#Rem 'T_search = 0
#Rem 'Do While (T - T_search) > 0.00001
#Rem ' p_mid = (p_max + p_min) / 2
#Rem ' T_search = T_pv(p_mid, v)
#Rem ' If T_search < T Then
#Rem '  p_min = p_mid
#Rem ' End If
#Rem ' If T_search > T Then
#Rem '  p_max = p_mid
#Rem ' End If
#Rem 'Loop
#Rem 'p_Tv = p_mid * 100
#Rem 'End Function
#Rem
#Rem '***********************************************************************************************************
#Rem '*1.4 Enthalpy (h)
#Rem Function hV_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem    hV_p = fromSIunit_h(h4V_p(p))
#Rem  Else
#Rem    hV_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function hL_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem    hL_p = fromSIunit_h(h4L_p(p))
#Rem  Else
#Rem    hL_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function hV_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   hV_T = fromSIunit_h(h4V_p(p4_T(T)))
#Rem  Else
#Rem   hV_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function hL_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   hL_T = fromSIunit_h(h4L_p(p4_T(T)))
#Rem Else
#Rem   hL_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function h_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  T = toSIunit_T(T)
#Rem  Select Case region_pT(p, T)
#Rem  Case 1
#Rem    h_pT = fromSIunit_h(h1_pT(p, T))
#Rem  Case 2
#Rem    h_pT = fromSIunit_h(h2_pT(p, T))
#Rem  Case 3
#Rem    h_pT = fromSIunit_h(h3_pT(p, T))
#Rem  Case 4
#Rem    h_pT = CVErr(xlErrValue)
#Rem  Case 5
#Rem    h_pT = fromSIunit_h(h5_pT(p, T))
#Rem  Case Else
#Rem   h_pT = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function h_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem  Dim xs As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  s = toSIunit_s(s)
#Rem  Select Case region_ps(p, s)
#Rem  Case 1
#Rem    h_ps = fromSIunit_h(h1_pT(p, T1_ps(p, s)))
#Rem  Case 2
#Rem    h_ps = fromSIunit_h(h2_pT(p, T2_ps(p, s)))
#Rem  Case 3
#Rem    h_ps = fromSIunit_h(h3_rhoT(1 / v3_ps(p, s), T3_ps(p, s)))
#Rem  Case 4
#Rem    xs = x4_ps(p, s)
#Rem    h_ps = fromSIunit_h(xs * h4V_p(p) + (1 - xs) * h4L_p(p))
#Rem  Case 5
#Rem    h_ps = fromSIunit_h(h5_pT(p, T5_ps(p, s)))
#Rem  Case Else
#Rem   h_ps = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function h_px(ByVal p As Double, ByVal x As Double) As Double
#Rem  Dim hL As Double
#Rem  Dim hV As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  x = toSIunit_x(x)
#Rem  If x > 1 Or x < 0 Or p >= 22.064 Then
#Rem    h_px = CVErr(xlErrValue)
#Rem    Exit Function
#Rem  End If
#Rem  hL = h4L_p(p)
#Rem  hV = h4V_p(p)
#Rem  h_px = fromSIunit_h(hL + x * (hV - hL))
#Rem End Function
#Rem Function h_Tx(ByVal T As Double, ByVal x As Double) As Double
#Rem  Dim hL As Double
#Rem  Dim hV As Double
#Rem  Dim p As Double
#Rem  T = toSIunit_T(T)
#Rem  x = toSIunit_x(x)
#Rem  If x > 1 Or x < 0 Or T >= 647.096 Then
#Rem    h_Tx = CVErr(xlErrValue)
#Rem    Exit Function
#Rem  End If
#Rem  p = p4_T(T)
#Rem  hL = h4L_p(p)
#Rem  hV = h4V_p(p)
#Rem  h_Tx = fromSIunit_h(hL + x * (hV - hL))
#Rem End Function
#Rem Function h_prho(ByVal p As Double, ByVal rho As Double) As Double
#Rem   Dim hL, hV, vL, vV, x As Double
#Rem   p = p / 100
#Rem   p = toSIunit_p(p)
#Rem   rho = 1 / toSIunit_v(1 / rho)
#Rem   Select Case Region_prho(p, rho)
#Rem   Case 1
#Rem     h_prho = fromSIunit_h(h1_pT(p, T1_prho(p, rho)))
#Rem   Case 2
#Rem     h_prho = fromSIunit_h(h2_pT(p, T2_prho(p, rho)))
#Rem   Case 3
#Rem     h_prho = fromSIunit_h(h3_rhoT(rho, T3_prho(p, rho)))
#Rem   Case 4
#Rem    If p < 16.529 Then
#Rem      vV = v2_pT(p, T4_p(p))
#Rem      vL = v1_pT(p, T4_p(p))
#Rem    Else
#Rem      vV = v3_ph(p, h4V_p(p))
#Rem      vL = v3_ph(p, h4L_p(p))
#Rem     End If
#Rem     hV = h4V_p(p)
#Rem     hL = h4L_p(p)
#Rem   x = (1 / rho - vL) / (vV - vL)
#Rem   h_prho = fromSIunit_h((1 - x) * hL + x * hV)
#Rem  Case 5
#Rem    h_prho = fromSIunit_h(h5_pT(p, T5_prho(p, rho)))
#Rem  Case Else
#Rem    h_prho = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function h_pv(ByVal p As Double, ByVal v As Double) As Double
#Rem  Dim rho As Double
#Rem  rho = 1 / v
#Rem  h_pv = h_prho(p, rho)
#Rem End Function
#Rem 'Function h_Tv(ByVal T As Double, ByVal v As Double) As Double
#Rem 'Dim p As Double
#Rem 'p = p_Tv(T, v)
#Rem 'h_Tv = h_pv(p, v)
#Rem 'End Function
#Rem '***********************************************************************************************************
#Rem '*1.5 Specific Volume (v)
#Rem Function vV_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   If p < 16.529 Then
#Rem    vV_p = fromSIunit_v(v2_pT(p, T4_p(p)))
#Rem   Else
#Rem    vV_p = fromSIunit_v(v3_ph(p, h4V_p(p)))
#Rem   End If
#Rem  Else
#Rem    vV_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function vL_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   If p < 16.529 Then
#Rem    vL_p = fromSIunit_v(v1_pT(p, T4_p(p)))
#Rem   Else
#Rem    vL_p = fromSIunit_v(v3_ph(p, h4L_p(p)))
#Rem   End If
#Rem  Else
#Rem    vL_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function vV_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   If T <= 623.15 Then
#Rem    vV_T = fromSIunit_v(v2_pT(p4_T(T), T))
#Rem   Else
#Rem    vV_T = fromSIunit_v(v3_ph(p4_T(T), h4V_p(p4_T(T))))
#Rem   End If
#Rem  Else
#Rem    vV_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function vL_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   If T <= 623.15 Then
#Rem    vL_T = fromSIunit_v(v1_pT(p4_T(T), T))
#Rem   Else
#Rem    vL_T = fromSIunit_v(v3_ph(p4_T(T), h4L_p(p4_T(T))))
#Rem   End If
#Rem  Else
#Rem    vL_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function v_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  T = toSIunit_T(T)
#Rem  Select Case region_pT(p, T)
#Rem  Case 1
#Rem    v_pT = fromSIunit_v(v1_pT(p, T))
#Rem  Case 2
#Rem    v_pT = fromSIunit_v(v2_pT(p, T))
#Rem  Case 3
#Rem    v_pT = fromSIunit_v(v3_ph(p, h3_pT(p, T)))
#Rem  Case 4
#Rem    v_pT = CVErr(xlErrValue)
#Rem  Case 5
#Rem    v_pT = fromSIunit_v(v5_pT(p, T))
#Rem  Case Else
#Rem   v_pT = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem
#Rem Function v_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem  Dim xs As Double
#Rem  Dim v4V As Double
#Rem  Dim v4L As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  h = toSIunit_h(h)
#Rem  Select Case region_ph(p, h)
#Rem  Case 1
#Rem    v_ph = fromSIunit_v(v1_pT(p, T1_ph(p, h)))
#Rem  Case 2
#Rem    v_ph = fromSIunit_v(v2_pT(p, T2_ph(p, h)))
#Rem  Case 3
#Rem    v_ph = fromSIunit_v(v3_ph(p, h))
#Rem  Case 4
#Rem    xs = x4_ph(p, h)
#Rem    If p < 16.529 Then
#Rem      v4V = v2_pT(p, T4_p(p))
#Rem      v4L = v1_pT(p, T4_p(p))
#Rem    Else
#Rem      v4V = v3_ph(p, h4V_p(p))
#Rem      v4L = v3_ph(p, h4L_p(p))
#Rem     End If
#Rem     v_ph = fromSIunit_v((xs * v4V + (1 - xs) * v4L))
#Rem  Case 5
#Rem    v_ph = fromSIunit_v(v5_pT(p, T5_ph(p, h)))
#Rem  Case Else
#Rem   v_ph = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function v_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem  Dim xs As Double
#Rem  Dim v4V As Double
#Rem  Dim v4L As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  s = toSIunit_s(s)
#Rem  Select Case region_ps(p, s)
#Rem  Case 1
#Rem    v_ps = fromSIunit_v(v1_pT(p, T1_ps(p, s)))
#Rem  Case 2
#Rem    v_ps = fromSIunit_v(v2_pT(p, T2_ps(p, s)))
#Rem  Case 3
#Rem    v_ps = fromSIunit_v(v3_ps(p, s))
#Rem  Case 4
#Rem    xs = x4_ps(p, s)
#Rem    If p < 16.529 Then
#Rem      v4V = v2_pT(p, T4_p(p))
#Rem      v4L = v1_pT(p, T4_p(p))
#Rem    Else
#Rem      v4V = v3_ph(p, h4V_p(p))
#Rem      v4L = v3_ph(p, h4L_p(p))
#Rem     End If
#Rem     v_ps = fromSIunit_v((xs * v4V + (1 - xs) * v4L))
#Rem  Case 5
#Rem    v_ps = fromSIunit_v(v5_pT(p, T5_ps(p, s)))
#Rem  Case Else
#Rem    v_ps = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem
#Rem '***********************************************************************************************************
#Rem '*1.6 Density (rho)
#Rem ' Density is calculated as 1/v
#Rem Function rhoV_p(ByVal p As Double) As Double
#Rem   rhoV_p = 1 / vV_p(p)
#Rem End Function
#Rem Function rhoL_p(ByVal p As Double) As Double
#Rem   rhoL_p = 1 / vL_p(p)
#Rem End Function
#Rem Function rhoL_T(ByVal T As Double) As Double
#Rem   rhoL_T = 1 / vL_T(T)
#Rem End Function
#Rem Function rhoV_T(ByVal T As Double) As Double
#Rem   rhoV_T = 1 / vV_T(T)
#Rem End Function
#Rem Function rho_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem   rho_pT = 1 / v_pT(p, T)
#Rem End Function
#Rem Function rho_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem   rho_ph = 1 / v_ph(p, h)
#Rem End Function
#Rem Function rho_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem   rho_ps = 1 / v_ps(p, s)
#Rem End Function
#Rem
#Rem '***********************************************************************************************************
#Rem '*1.7 Specific entropy (s)
#Rem Function sV_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   If p < 16.529 Then
#Rem    sV_p = fromSIunit_s(s2_pT(p, T4_p(p)))
#Rem   Else
#Rem    sV_p = fromSIunit_s(s3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p)))
#Rem   End If
#Rem  Else
#Rem    sV_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function sL_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   If p < 16.529 Then
#Rem    sL_p = fromSIunit_s(s1_pT(p, T4_p(p)))
#Rem   Else
#Rem    sL_p = fromSIunit_s(s3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p)))
#Rem   End If
#Rem  Else
#Rem    sL_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function sV_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   If T <= 623.15 Then
#Rem    sV_T = fromSIunit_s(s2_pT(p4_T(T), T))
#Rem   Else
#Rem    sV_T = fromSIunit_s(s3_rhoT(1 / (v3_ph(p4_T(T), h4V_p(p4_T(T)))), T))
#Rem   End If
#Rem  Else
#Rem    sV_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function sL_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   If T <= 623.15 Then
#Rem    sL_T = fromSIunit_s(s1_pT(p4_T(T), T))
#Rem   Else
#Rem    sL_T = fromSIunit_s(s3_rhoT(1 / (v3_ph(p4_T(T), h4L_p(p4_T(T)))), T))
#Rem   End If
#Rem  Else
#Rem    sL_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function s_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  T = toSIunit_T(T)
#Rem  Select Case region_pT(p, T)
#Rem  Case 1
#Rem    s_pT = fromSIunit_s(s1_pT(p, T))
#Rem  Case 2
#Rem    s_pT = fromSIunit_s(s2_pT(p, T))
#Rem  Case 3
#Rem    s_pT = fromSIunit_s(s3_rhoT(1 / v3_ph(p, h3_pT(p, T)), T))
#Rem  Case 4
#Rem    s_pT = CVErr(xlErrValue)
#Rem  Case 5
#Rem    s_pT = fromSIunit_s(s5_pT(p, T))
#Rem  Case Else
#Rem   s_pT = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function s_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem  Dim Ts As Double
#Rem  Dim xs As Double
#Rem  Dim s4V As Double
#Rem  Dim s4L As Double
#Rem  Dim v4V As Double
#Rem  Dim v4L As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  h = toSIunit_h(h)
#Rem  Select Case region_ph(p, h)
#Rem  Case 1
#Rem    s_ph = fromSIunit_s(s1_pT(p, T1_ph(p, h)))
#Rem  Case 2
#Rem    s_ph = fromSIunit_s(s2_pT(p, T2_ph(p, h)))
#Rem  Case 3
#Rem    s_ph = fromSIunit_s(s3_rhoT(1 / v3_ph(p, h), T3_ph(p, h)))
#Rem  Case 4
#Rem    Ts = T4_p(p)
#Rem    xs = x4_ph(p, h)
#Rem    If p < 16.529 Then
#Rem      s4V = s2_pT(p, Ts)
#Rem      s4L = s1_pT(p, Ts)
#Rem    Else
#Rem      v4V = v3_ph(p, h4V_p(p))
#Rem      s4V = s3_rhoT(1 / v4V, Ts)
#Rem      v4L = v3_ph(p, h4L_p(p))
#Rem      s4L = s3_rhoT(1 / v4L, Ts)
#Rem     End If
#Rem    s_ph = fromSIunit_s((xs * s4V + (1 - xs) * s4L))
#Rem  Case 5
#Rem    s_ph = fromSIunit_s(s5_pT(p, T5_ph(p, h)))
#Rem  Case Else
#Rem   s_ph = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function s_pv(ByVal p As Double, ByVal v As Double) As Double
#Rem Dim rho As Double
#Rem Dim h As Double
#Rem rho = 1 / v
#Rem h = h_prho(p, rho)
#Rem s_pv = s_ph(p, h)
#Rem End Function
#Rem 'Function s_Tv(ByVal T As Double, ByVal v As Double) As Double
#Rem 'Dim p As Double
#Rem 'p = p_Tv(T, v)
#Rem 's_Tv = s_pv(p, v)
#Rem 'End Function
#Rem '***********************************************************************************************************
#Rem '*1.8 Specific internal energy (u)
#Rem Function uV_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   If p < 16.529 Then
#Rem    uV_p = fromSIunit_u(u2_pT(p, T4_p(p)))
#Rem   Else
#Rem    uV_p = fromSIunit_u(u3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p)))
#Rem   End If
#Rem  Else
#Rem    uV_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function uL_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   If p < 16.529 Then
#Rem    uL_p = fromSIunit_u(u1_pT(p, T4_p(p)))
#Rem   Else
#Rem    uL_p = fromSIunit_u(u3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p)))
#Rem   End If
#Rem  Else
#Rem    uL_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function uV_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   If T <= 623.15 Then
#Rem    uV_T = fromSIunit_u(u2_pT(p4_T(T), T))
#Rem   Else
#Rem    uV_T = fromSIunit_u(u3_rhoT(1 / (v3_ph(p4_T(T), h4V_p(p4_T(T)))), T))
#Rem   End If
#Rem  Else
#Rem    uV_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function uL_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   If T <= 623.15 Then
#Rem    uL_T = fromSIunit_u(u1_pT(p4_T(T), T))
#Rem   Else
#Rem    uL_T = fromSIunit_u(u3_rhoT(1 / (v3_ph(p4_T(T), h4L_p(p4_T(T)))), T))
#Rem   End If
#Rem  Else
#Rem    uL_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function u_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  T = toSIunit_T(T)
#Rem  Select Case region_pT(p, T)
#Rem  Case 1
#Rem    u_pT = fromSIunit_u(u1_pT(p, T))
#Rem  Case 2
#Rem    u_pT = fromSIunit_u(u2_pT(p, T))
#Rem  Case 3
#Rem    u_pT = fromSIunit_u(u3_rhoT(1 / v3_ph(p, h3_pT(p, T)), T))
#Rem  Case 4
#Rem    u_pT = CVErr(xlErrValue)
#Rem  Case 5
#Rem    u_pT = fromSIunit_u(u5_pT(p, T))
#Rem  Case Else
#Rem   u_pT = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function u_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem  Dim Ts As Double
#Rem  Dim xs As Double
#Rem  Dim u4v As Double
#Rem  Dim u4L As Double
#Rem  Dim v4V As Double
#Rem  Dim v4L As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  h = toSIunit_h(h)
#Rem  Select Case region_ph(p, h)
#Rem  Case 1
#Rem    u_ph = fromSIunit_u(u1_pT(p, T1_ph(p, h)))
#Rem  Case 2
#Rem    u_ph = fromSIunit_u(u2_pT(p, T2_ph(p, h)))
#Rem  Case 3
#Rem    u_ph = fromSIunit_u(u3_rhoT(1 / v3_ph(p, h), T3_ph(p, h)))
#Rem  Case 4
#Rem    Ts = T4_p(p)
#Rem    xs = x4_ph(p, h)
#Rem    If p < 16.529 Then
#Rem      u4v = u2_pT(p, Ts)
#Rem      u4L = u1_pT(p, Ts)
#Rem    Else
#Rem      v4V = v3_ph(p, h4V_p(p))
#Rem      u4v = u3_rhoT(1 / v4V, Ts)
#Rem      v4L = v3_ph(p, h4L_p(p))
#Rem      u4L = u3_rhoT(1 / v4L, Ts)
#Rem    End If
#Rem    u_ph = fromSIunit_u((xs * u4v + (1 - xs) * u4L))
#Rem  Case 5
#Rem    Ts = T5_ph(p, h)
#Rem    u_ph = fromSIunit_u(u5_pT(p, Ts))
#Rem  Case Else
#Rem   u_ph = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function u_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem  Dim x As Double
#Rem  Dim u4v, uLp, uVp, u4L As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  s = toSIunit_s(s)
#Rem  Select Case region_ps(p, s)
#Rem  Case 1
#Rem    u_ps = fromSIunit_u(u1_pT(p, T1_ps(p, s)))
#Rem  Case 2
#Rem    u_ps = fromSIunit_u(u2_pT(p, T2_ps(p, s)))
#Rem  Case 3
#Rem    u_ps = fromSIunit_u(u3_rhoT(1 / v3_ps(p, s), T3_ps(p, s)))
#Rem  Case 4
#Rem    If p < 16.529 Then
#Rem      uLp = u1_pT(p, T4_p(p))
#Rem      uVp = u2_pT(p, T4_p(p))
#Rem    Else
#Rem      uLp = u3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p))
#Rem      uVp = u3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p))
#Rem    End If
#Rem    x = x4_ps(p, s)
#Rem    u_ps = fromSIunit_u((x * uVp + (1 - x) * uLp))
#Rem  Case 5
#Rem    u_ps = fromSIunit_u(u5_pT(p, T5_ps(p, s)))
#Rem  Case Else
#Rem   u_ps = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function u_pv(ByVal p As Double, ByVal v As Double) As Double
#Rem Dim rho As Double
#Rem Dim h As Double
#Rem rho = 1 / v
#Rem h = h_prho(p, rho)
#Rem u_pv = u_ph(p, h)
#Rem End Function
#Rem 'Function u_Tv(ByVal T As Double, ByVal v As Double) As Double
#Rem 'Dim p As Double
#Rem 'p = p_Tv(T, v)
#Rem 'u_Tv = u_pv(p, v)
#Rem 'End Function
#Rem '***********************************************************************************************************
#Rem '*1.9 Specific isobaric heat capacity (Cp)
#Rem Function CpV_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   If p < 16.529 Then
#Rem    CpV_p = fromSIunit_Cp(Cp2_pT(p, T4_p(p)))
#Rem   Else
#Rem    CpV_p = fromSIunit_Cp(Cp3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p)))
#Rem   End If
#Rem  Else
#Rem    CpV_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function CpL_p(ByVal p As Double) As Double
#Rem  Dim T, h, v As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   If p < 16.529 Then
#Rem    CpL_p = fromSIunit_Cp(Cp1_pT(p, T4_p(p)))
#Rem   Else
#Rem   T = T4_p(p)
#Rem   h = h4L_p(p)
#Rem   v = v3_ph(p, h4L_p(p))
#Rem
#Rem    CpL_p = fromSIunit_Cp(Cp3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p)))
#Rem   End If
#Rem  Else
#Rem    CpL_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function CpV_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   If T <= 623.15 Then
#Rem    CpV_T = fromSIunit_Cp(Cp2_pT(p4_T(T), T))
#Rem   Else
#Rem    CpV_T = fromSIunit_Cp(Cp3_rhoT(1 / (v3_ph(p4_T(T), h4V_p(p4_T(T)))), T))
#Rem   End If
#Rem  Else
#Rem    CpV_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function CpL_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   If T <= 623.15 Then
#Rem    CpL_T = fromSIunit_Cp(Cp1_pT(p4_T(T), T))
#Rem   Else
#Rem    CpL_T = fromSIunit_Cp(Cp3_rhoT(1 / (v3_ph(p4_T(T), h4L_p(p4_T(T)))), T))
#Rem   End If
#Rem  Else
#Rem    CpL_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function Cp_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  T = toSIunit_T(T)
#Rem  Select Case region_pT(p, T)
#Rem  Case 1
#Rem    Cp_pT = fromSIunit_Cp(Cp1_pT(p, T))
#Rem  Case 2
#Rem    Cp_pT = fromSIunit_Cp(Cp2_pT(p, T))
#Rem  Case 3
#Rem    Cp_pT = fromSIunit_Cp(Cp3_rhoT(1 / v3_ph(p, h3_pT(p, T)), T))
#Rem  Case 4
#Rem    Cp_pT = CVErr(xlErrValue)
#Rem  Case 5
#Rem    Cp_pT = fromSIunit_Cp(Cp5_pT(p, T))
#Rem  Case Else
#Rem   Cp_pT = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function Cp_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  h = toSIunit_h(h)
#Rem  Select Case region_ph(p, h)
#Rem  Case 1
#Rem    Cp_ph = fromSIunit_Cp(Cp1_pT(p, T1_ph(p, h)))
#Rem  Case 2
#Rem    Cp_ph = fromSIunit_Cp(Cp2_pT(p, T2_ph(p, h)))
#Rem  Case 3
#Rem    Cp_ph = fromSIunit_Cp(Cp3_rhoT(1 / v3_ph(p, h), T3_ph(p, h)))
#Rem  Case 4
#Rem    Cp_ph = CVErr(xlErrValue) '#Not def. for mixture"
#Rem  Case 5
#Rem    Cp_ph = fromSIunit_Cp(Cp5_pT(p, T5_ph(p, h)))
#Rem  Case Else
#Rem   Cp_ph = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function Cp_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  s = toSIunit_s(s)
#Rem  Select Case region_ps(p, s)
#Rem  Case 1
#Rem    Cp_ps = fromSIunit_Cp(Cp1_pT(p, T1_ps(p, s)))
#Rem  Case 2
#Rem    Cp_ps = fromSIunit_Cp(Cp2_pT(p, T2_ps(p, s)))
#Rem  Case 3
#Rem    Cp_ps = fromSIunit_Cp(Cp3_rhoT(1 / v3_ps(p, s), T3_ps(p, s)))
#Rem  Case 4
#Rem    Cp_ps = CVErr(xlErrValue) '#Not def. for mixture"
#Rem  Case 5
#Rem    Cp_ps = fromSIunit_Cp(Cp5_pT(p, T5_ps(p, s)))
#Rem  Case Else
#Rem   Cp_ps = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*1.10 Specific isochoric heat capacity (Cv)
#Rem Function CvV_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   If p < 16.529 Then
#Rem    CvV_p = fromSIunit_Cv(Cv2_pT(p, T4_p(p)))
#Rem   Else
#Rem    CvV_p = fromSIunit_Cv(Cv3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p)))
#Rem   End If
#Rem  Else
#Rem    CvV_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function CvL_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   If p < 16.529 Then
#Rem    CvL_p = fromSIunit_Cv(Cv1_pT(p, T4_p(p)))
#Rem   Else
#Rem    CvL_p = fromSIunit_Cv(Cv3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p)))
#Rem   End If
#Rem  Else
#Rem    CvL_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function CvV_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   If T <= 623.15 Then
#Rem    CvV_T = fromSIunit_Cv(Cv2_pT(p4_T(T), T))
#Rem   Else
#Rem    CvV_T = fromSIunit_Cv(Cv3_rhoT(1 / (v3_ph(p4_T(T), h4V_p(p4_T(T)))), T))
#Rem   End If
#Rem  Else
#Rem    CvV_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function CvL_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   If T <= 623.15 Then
#Rem    CvL_T = fromSIunit_Cv(Cv1_pT(p4_T(T), T))
#Rem   Else
#Rem    CvL_T = fromSIunit_Cv(Cv3_rhoT(1 / (v3_ph(p4_T(T), h4L_p(p4_T(T)))), T))
#Rem   End If
#Rem  Else
#Rem    CvL_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function Cv_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  T = toSIunit_T(T)
#Rem  Select Case region_pT(p, T)
#Rem  Case 1
#Rem    Cv_pT = fromSIunit_Cv(Cv1_pT(p, T))
#Rem  Case 2
#Rem    Cv_pT = fromSIunit_Cv(Cv2_pT(p, T))
#Rem  Case 3
#Rem    Cv_pT = fromSIunit_Cv(Cv3_rhoT(1 / v3_ph(p, h3_pT(p, T)), T))
#Rem  Case 4
#Rem    Cv_pT = CVErr(xlErrValue)
#Rem  Case 5
#Rem    Cv_pT = fromSIunit_Cv(Cv5_pT(p, T))
#Rem  Case Else
#Rem   Cv_pT = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function Cv_ph(ByVal p, ByVal h) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  h = toSIunit_h(h)
#Rem  Select Case region_ph(p, h)
#Rem  Case 1
#Rem    Cv_ph = fromSIunit_Cv(Cv1_pT(p, T1_ph(p, h)))
#Rem  Case 2
#Rem    Cv_ph = fromSIunit_Cv(Cv2_pT(p, T2_ph(p, h)))
#Rem  Case 3
#Rem    Cv_ph = fromSIunit_Cv(Cv3_rhoT(1 / v3_ph(p, h), T3_ph(p, h)))
#Rem  Case 4
#Rem    Cv_ph = CVErr(xlErrValue) '#Not def. for mixture"
#Rem  Case 5
#Rem    Cv_ph = fromSIunit_Cv(Cv5_pT(p, T5_ph(p, h)))
#Rem  Case Else
#Rem   Cv_ph = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem
#Rem Function Cv_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  s = toSIunit_s(s)
#Rem  Select Case region_ps(p, s)
#Rem  Case 1
#Rem    Cv_ps = fromSIunit_Cv(Cv1_pT(p, T1_ps(p, s)))
#Rem  Case 2
#Rem    Cv_ps = fromSIunit_Cv(Cv2_pT(p, T2_ps(p, s)))
#Rem  Case 3
#Rem    Cv_ps = fromSIunit_Cv(Cv3_rhoT(1 / v3_ps(p, s), T3_ps(p, s)))
#Rem  Case 4
#Rem    Cv_ps = CVErr(xlErrValue) '#Not def. for mixture
#Rem  Case 5
#Rem    Cv_ps = fromSIunit_Cv(Cv5_pT(p, T5_ps(p, s)))
#Rem  Case Else
#Rem   Cv_ps = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem
#Rem
#Rem '***********************************************************************************************************
#Rem '*1.11 Speed of sound
#Rem Function wV_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   If p < 16.529 Then
#Rem    wV_p = fromSIunit_w(w2_pT(p, T4_p(p)))
#Rem   Else
#Rem    wV_p = fromSIunit_w(w3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p)))
#Rem   End If
#Rem  Else
#Rem    wV_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function wL_p(ByVal p As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   If p < 16.529 Then
#Rem    wL_p = fromSIunit_w(w1_pT(p, T4_p(p)))
#Rem   Else
#Rem    wL_p = fromSIunit_w(w3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p)))
#Rem   End If
#Rem  Else
#Rem    wL_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function wV_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   If T <= 623.15 Then
#Rem    wV_T = fromSIunit_w(w2_pT(p4_T(T), T))
#Rem   Else
#Rem    wV_T = fromSIunit_w(w3_rhoT(1 / (v3_ph(p4_T(T), h4V_p(p4_T(T)))), T))
#Rem   End If
#Rem  Else
#Rem    wV_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function wL_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T > 273.15 And T < 647.096 Then
#Rem   If T <= 623.15 Then
#Rem    wL_T = fromSIunit_w(w1_pT(p4_T(T), T))
#Rem   Else
#Rem    wL_T = fromSIunit_w(w3_rhoT(1 / (v3_ph(p4_T(T), h4L_p(p4_T(T)))), T))
#Rem   End If
#Rem  Else
#Rem    wL_T = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Function w_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  T = toSIunit_T(T)
#Rem  Select Case region_pT(p, T)
#Rem  Case 1
#Rem    w_pT = fromSIunit_w(w1_pT(p, T))
#Rem  Case 2
#Rem    w_pT = fromSIunit_w(w2_pT(p, T))
#Rem  Case 3
#Rem    w_pT = fromSIunit_w(w3_rhoT(1 / v3_ph(p, h3_pT(p, T)), T))
#Rem  Case 4
#Rem    w_pT = CVErr(xlErrValue)
#Rem  Case 5
#Rem    w_pT = fromSIunit_w(w5_pT(p, T))
#Rem  Case Else
#Rem   w_pT = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem
#Rem Function w_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  h = toSIunit_h(h)
#Rem  Select Case region_ph(p, h)
#Rem  Case 1
#Rem    w_ph = fromSIunit_w(w1_pT(p, T1_ph(p, h)))
#Rem  Case 2
#Rem    w_ph = fromSIunit_w(w2_pT(p, T2_ph(p, h)))
#Rem  Case 3
#Rem    w_ph = fromSIunit_w(w3_rhoT(1 / v3_ph(p, h), T3_ph(p, h)))
#Rem  Case 4
#Rem    w_ph = CVErr(xlErrValue) '#Not def. for mixture
#Rem  Case 5
#Rem    w_ph = fromSIunit_w(w5_pT(p, T5_ph(p, h)))
#Rem  Case Else
#Rem   w_ph = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem
#Rem Function w_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  s = toSIunit_s(s)
#Rem  Select Case region_ps(p, s)
#Rem  Case 1
#Rem    w_ps = fromSIunit_w(w1_pT(p, T1_ps(p, s)))
#Rem  Case 2
#Rem    w_ps = fromSIunit_w(w2_pT(p, T2_ps(p, s)))
#Rem  Case 3
#Rem    w_ps = fromSIunit_w(w3_rhoT(1 / v3_ps(p, s), T3_ps(p, s)))
#Rem  Case 4
#Rem    w_ps = CVErr(xlErrValue) '#Not def. for mixture
#Rem  Case 5
#Rem    w_ps = fromSIunit_w(w5_pT(p, T5_ps(p, s)))
#Rem  Case Else
#Rem   w_ps = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*1.12 Viscosity
#Rem Function my_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  T = toSIunit_T(T)
#Rem  Select Case region_pT(p, T)
#Rem  Case 4
#Rem    my_pT = CVErr(xlErrValue)
#Rem  Case 1, 2, 3, 5
#Rem    my_pT = fromSIunit_my(my_AllRegions_pT(p, T))
#Rem  Case Else
#Rem    my_pT = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function my_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  h = toSIunit_h(h)
#Rem  Select Case region_ph(p, h)
#Rem  Case 1, 2, 3, 5
#Rem    my_ph = fromSIunit_my(my_AllRegions_ph(p, h))
#Rem  Case 4
#Rem   my_ph = CVErr(xlErrValue)
#Rem  Case Else
#Rem   my_ph = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function my_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem  my_ps = my_ph(p, h_ps(p, s))
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*1.13 Prandtl
#Rem Function Pr_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem   Dim Cp As Double
#Rem   Dim my As Double
#Rem   Dim tc As Double
#Rem   Cp = toSIunit_Cp(Cp_pT(p, T))
#Rem   my = toSIunit_my(my_pT(p, T))
#Rem   tc = toSIunit_tc(tc_pT(p, T))
#Rem   Pr_pT = Cp * 1000 * my / tc
#Rem End Function
#Rem Function Pr_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem   Dim Cp As Double
#Rem   Dim my As Double
#Rem   Dim tc As Double
#Rem   Cp = toSIunit_Cp(Cp_ph(p, h))
#Rem   my = toSIunit_my(my_ph(p, h))
#Rem   tc = toSIunit_tc(tc_ph(p, h))
#Rem   Pr_ph = Cp * 1000 * my / tc
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*1.14 Kappa
#Rem Private Function Kappa_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem   Dim Cp As Double
#Rem   Dim Cv As Double
#Rem   Cp = Cp_pT(p, T)
#Rem   Cv = Cv_pT(p, T)
#Rem   Kappa_pT = Cp / Cv
#Rem End Function
#Rem Private Function Kappa_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem   Dim Cp As Double
#Rem   Dim Cv As Double
#Rem   Cv = Cv_ph(p, h)
#Rem   Cp = Cp_ph(p, h)
#Rem   Kappa_ph = Cp / Cv
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*1.15 Surface tension
#Rem Function st_t(ByVal T As Double) As Double
#Rem   T = toSIunit_T(T)
#Rem   st_t = fromSIunit_st(Surface_Tension_T(T))
#Rem End Function
#Rem Function st_p(ByVal p As Double) As Double
#Rem    Dim T As Double
#Rem    T = Tsat_p(p)
#Rem    T = toSIunit_T(T)
#Rem    st_p = fromSIunit_st(Surface_Tension_T(T))
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*1.16 Thermal conductivity
#Rem Function tcL_p(ByVal p As Double) As Double
#Rem   Dim T As Double
#Rem   Dim v As Double
#Rem   T = Tsat_p(p)
#Rem   v = vL_p(p)
#Rem   p = p / 100
#Rem   p = toSIunit_p(p)
#Rem   T = toSIunit_T(T)
#Rem   v = toSIunit_v(v)
#Rem   tcL_p = fromSIunit_tc(tc_ptrho(p, T, 1 / v))
#Rem End Function
#Rem Function tcV_p(ByVal p As Double) As Double
#Rem   Dim T As Double
#Rem   Dim v As Double
#Rem   T = Tsat_p(p)
#Rem   v = vV_p(p)
#Rem   p = p / 100
#Rem   p = toSIunit_p(p)
#Rem   T = toSIunit_T(T)
#Rem   v = toSIunit_v(v)
#Rem   tcV_p = fromSIunit_tc(tc_ptrho(p, T, 1 / v))
#Rem End Function
#Rem Function tcL_T(ByVal T As Double) As Double
#Rem   Dim p, v As Double
#Rem   p = psat_T(T)
#Rem   v = vL_T(T)
#Rem   p = p / 100
#Rem   p = toSIunit_p(p)
#Rem   T = toSIunit_T(T)
#Rem   v = toSIunit_v(v)
#Rem   tcL_T = fromSIunit_tc(tc_ptrho(p, T, 1 / v))
#Rem End Function
#Rem Function tcV_T(ByVal T As Double) As Double
#Rem   Dim p, v As Double
#Rem   p = psat_T(T)
#Rem   v = vV_T(T)
#Rem   p = p / 100
#Rem   p = toSIunit_p(p)
#Rem   T = toSIunit_T(T)
#Rem   v = toSIunit_v(v)
#Rem   tcV_T = fromSIunit_tc(tc_ptrho(p, T, 1 / v))
#Rem End Function
#Rem Function tc_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem   Dim v As Double
#Rem   v = v_pT(p, T)
#Rem   p = p / 100
#Rem   p = toSIunit_p(p)
#Rem   T = toSIunit_T(T)
#Rem   v = toSIunit_v(v)
#Rem   tc_pT = fromSIunit_tc(tc_ptrho(p, T, 1 / v))
#Rem End Function
#Rem Function tc_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem   Dim v As Double
#Rem   Dim T As Double
#Rem   v = v_ph(p, h)
#Rem   T = T_ph(p, h)
#Rem   p = p / 100
#Rem   p = toSIunit_p(p)
#Rem   T = toSIunit_T(T)
#Rem   v = toSIunit_v(v)
#Rem   tc_ph = fromSIunit_tc(tc_ptrho(p, T, 1 / v))
#Rem End Function
#Rem Function tc_hs(ByVal h As Double, ByVal s As Double) As Double
#Rem   Dim p As Double
#Rem   Dim v As Double
#Rem   Dim T As Double
#Rem   p = p_hs(h, s)
#Rem   v = v_ph(p, h)
#Rem   T = T_ph(p, h)
#Rem   p = p / 100
#Rem   p = toSIunit_p(p)
#Rem   T = toSIunit_T(T)
#Rem   v = toSIunit_v(v)
#Rem   tc_hs = fromSIunit_tc(tc_ptrho(p, T, 1 / v))
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*1.17 Vapour fraction
#Rem Function x_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  h = toSIunit_h(h)
#Rem   If p > 0.000611657 And p < 22.06395 Then
#Rem     x_ph = fromSIunit_x(x4_ph(p, h))
#Rem   Else
#Rem     x_ph = CVErr(xlErrValue)
#Rem   End If
#Rem End Function
#Rem Function x_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  s = toSIunit_s(s)
#Rem   If p > 0.000611657 And p < 22.06395 Then
#Rem     x_ps = fromSIunit_x(x4_ps(p, s))
#Rem   Else
#Rem     x_ps = CVErr(xlErrValue)
#Rem   End If
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*1.18 Vapour Volume Fraction
#Rem Function vx_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem  Dim vL As Double
#Rem  Dim vV As Double
#Rem  Dim xs As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  h = toSIunit_h(h)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem     If p < 16.529 Then
#Rem       vL = v1_pT(p, T4_p(p))
#Rem       vV = v2_pT(p, T4_p(p))
#Rem     Else
#Rem       vL = v3_ph(p, h4L_p(p))
#Rem       vV = v3_ph(p, h4V_p(p))
#Rem     End If
#Rem     xs = x4_ph(p, h)
#Rem     vx_ph = fromSIunit_vx((xs * vV / (xs * vV + (1 - xs) * vL)))
#Rem   Else
#Rem     vx_ph = CVErr(xlErrValue)
#Rem   End If
#Rem End Function
#Rem Function vx_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem  Dim vL As Double
#Rem  Dim vV As Double
#Rem  Dim xs As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  s = toSIunit_s(s)
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem     If p < 16.529 Then
#Rem       vL = v1_pT(p, T4_p(p))
#Rem       vV = v2_pT(p, T4_p(p))
#Rem     Else
#Rem       vL = v3_ph(p, h4L_p(p))
#Rem       vV = v3_ph(p, h4V_p(p))
#Rem     End If
#Rem     xs = x4_ps(p, s)
#Rem     vx_ps = fromSIunit_vx((xs * vV / (xs * vV + (1 - xs) * vL)))
#Rem   Else
#Rem     vx_ps = CVErr(xlErrValue)
#Rem   End If
#Rem End Function
#Rem

#'***********************************************************************************************************
#Rem '*5 Transport properties
#Rem '***********************************************************************************************************
#Rem '*5.1 Viscosity (IAPWS formulation 1985, Revised 2003)
#Rem '***********************************************************************************************************
#Rem Private Function my_AllRegions_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem Dim h0, h1, h2, h3, h4, h5, h6 As Variant, rho, Ts, ps, my0, sum, my1, rhos As Double, i As Integer
#Rem   h0 = Array(0.5132047, 0.3205656, 0, 0, -0.7782567, 0.1885447)
#Rem   h1 = Array(0.2151778, 0.7317883, 1.241044, 1.476783, 0, 0)
#Rem   h2 = Array(-0.2818107, -1.070786, -1.263184, 0, 0, 0)
#Rem   h3 = Array(0.1778064, 0.460504, 0.2340379, -0.4924179, 0, 0)
#Rem   h4 = Array(-0.0417661, 0, 0, 0.1600435, 0, 0)
#Rem   h5 = Array(0, -0.01578386, 0, 0, 0, 0)
#Rem   h6 = Array(0, 0, 0, -0.003629481, 0, 0)
#Rem
#Rem   'Calcualte density.
#Rem  Select Case region_pT(p, T)
#Rem  Case 1
#Rem    rho = 1 / v1_pT(p, T)
#Rem  Case 2
#Rem    rho = 1 / v2_pT(p, T)
#Rem  Case 3
#Rem    rho = 1 / v3_ph(p, h3_pT(p, T))
#Rem  Case 4
#Rem    rho = CVErr(xlErrValue)
#Rem  Case 5
#Rem    rho = 1 / v5_pT(p, T)
#Rem  Case Else
#Rem   my_AllRegions_pT = CVErr(xlErrValue)
#Rem   Exit Function
#Rem  End Select
#Rem
#Rem   rhos = rho / 317.763
#Rem   Ts = T / 647.226
#Rem   ps = p / 22.115
#Rem
#Rem   'Check valid area
#Rem   If T > 900 + 273.15 Or (T > 600 + 273.15 And p > 300) Or (T > 150 + 273.15 And p > 350) Or p > 500 Then
#Rem     my_AllRegions_pT = CVErr(xlErrValue)
#Rem     Exit Function
#Rem   End If
#Rem   my0 = Ts ^ 0.5 / (1 + 0.978197 / Ts + 0.579829 / (Ts ^ 2) - 0.202354 / (Ts ^ 3))
#Rem   sum = 0
#Rem   For i = 0 To 5
#Rem       sum = sum + h0(i) * (1 / Ts - 1) ^ i + h1(i) * (1 / Ts - 1) ^ i * (rhos - 1) ^ 1 + h2(i) * (1 / Ts - 1) ^ i * (rhos - 1) ^ 2 + h3(i) * (1 / Ts - 1) ^ i * (rhos - 1) ^ 3 + h4(i) * (1 / Ts - 1) ^ i * (rhos - 1) ^ 4 + h5(i) * (1 / Ts - 1) ^ i * (rhos - 1) ^ 5 + h6(i) * (1 / Ts - 1) ^ i * (rhos - 1) ^ 6
#Rem   Next i
#Rem   my1 = Exp(rhos * sum)
#Rem   my_AllRegions_pT = my0 * my1 * 0.000055071
#Rem End Function
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
#Rem '***********************************************************************************************************
#Rem '*5.2 Thermal Conductivity (IAPWS formulation 1985)
#Rem Function tc_ptrho(ByVal p As Double, ByVal T As Double, ByVal rho As Double) As Double
#Rem 'Revised release on the IAPS Formulation 1985 for the Thermal Conductivity of ordinary water
#Rem 'IAPWS September 1998
#Rem 'Page 8
#Rem  Dim tc0, tc1, dT, Q, s, tc2 As Double
#Rem  If T < 0 Or p < 0.000611657 Or T > 800 Or p > 400 Or Not ((p <= 100 And T <= 100 + 273.15) Or (p <= 150 And T <= 400 + 273.15) Or (p <= 200 And T <= 250 + 273.15) Or (p <= 400 And T <= 125 + 273.15)) Then
#Rem    tc_ptrho = "Out of valid region"
#Rem    Exit Function
#Rem  End If
#Rem   T = T / 647.26
#Rem   rho = rho / 317.7
#Rem   tc0 = T ^ 0.5 * (0.0102811 + 0.0299621 * T + 0.0156146 * T ^ 2 - 0.00422464 * T ^ 3)
#Rem   tc1 = -0.39707 + 0.400302 * rho + 1.06 * Exp(-0.171587 * (rho + 2.39219) ^ 2)
#Rem   dT = Abs(T - 1) + 0.00308976
#Rem   Q = 2 + 0.0822994 / dT ^ (3 / 5)
#Rem   If T >= 1 Then
#Rem    s = 1 / dT
#Rem   Else
#Rem    s = 10.0932 / dT ^ (3 / 5)
#Rem   End If
#Rem   tc2 = (0.0701309 / T ^ 10 + 0.011852) * rho ^ (9 / 5) * Exp(0.642857 * (1 - rho ^ (14 / 5))) + 0.00169937 * s * rho ^ Q * Exp((Q / (1 + Q)) * (1 - rho ^ (1 + Q))) - 1.02 * Exp(-4.11717 * T ^ (3 / 2) - 6.17937 / rho ^ 5)
#Rem   tc_ptrho = tc0 + tc1 + tc2
#Rem End Function

def surfaceTension_T(temperature):
    '''IAPWS Release on Surface Tension of Ordinary Water Substance, September 1994'''
    if temperature < 0.01 or temperature > Constants._tc:
        raise ArithmeticError('Temperature must be between {} and {}'.format(0.01, Constants._tc))
    tau = 1.0 - temperature/Constants._tc
    return 0.2358*tau**1.256*(1.0 - 0.625*tau)
