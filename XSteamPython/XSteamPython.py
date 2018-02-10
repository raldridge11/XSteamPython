'''
* Water and steam properties according to IAPWS IF-97
* By Magnus Holmgren, www.x-eng.com
* The steam tables are free and provided as is.
* We take no responsibilities for any errors in the code or damage thereby.
* You are free to use, modify and distribute the code as long as authorship is properly acknowledged.
* Please notify me at magnus@x-eng.com if the code is used in commercial applications
'''
import numpy as np

englishUnits = False
_R = 0.461526 #kJ/(kg K)

def Tsat_p(pressure, units:str='SI'):
    '''Returns saturation temperature given a pressure in kPa'''
    pressureMin, pressureMax = 0.000611657, 22.06395 + 0.001
    pressure = toSIUnit(pressure, 'pressure')

    if pressure >= pressureMin and pressure <= pressureMax:
       return fromSIUnit(T4_p(pressure), 'temperature')
    else:
       raise ArithmeticError('Pressure needs to be between {} and {} kPa'.format(fromSIUnit(pressureMin, 'pressure'), fromSIUnit(pressureMax, 'pressure')))

#Rem Function Tsat_s(ByVal s As Double) As Double
#Rem  s = toSIunit_s(s)
#Rem  If s > -0.0001545495919 And s < 9.155759395 Then
#Rem    Tsat_s = fromSIunit_T(T4_p(p4_s(s)))
#Rem  Else
#Rem    Tsat_s = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem
#Rem Function T_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  h = toSIunit_h(h)
#Rem  Select Case region_ph(p, h)
#Rem  Case 1
#Rem    T_ph = fromSIunit_T(T1_ph(p, h))
#Rem  Case 2
#Rem    T_ph = fromSIunit_T(T2_ph(p, h))
#Rem  Case 3
#Rem    T_ph = fromSIunit_T(T3_ph(p, h))
#Rem  Case 4
#Rem    T_ph = fromSIunit_T(T4_p(p))
#Rem  Case 5
#Rem    T_ph = fromSIunit_T(T5_ph(p, h))
#Rem  Case Else
#Rem   T_ph = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function T_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem  p = p / 100
#Rem  p = toSIunit_p(p)
#Rem  s = toSIunit_s(s)
#Rem  Select Case region_ps(p, s)
#Rem  Case 1
#Rem    T_ps = fromSIunit_T(T1_ps(p, s))
#Rem  Case 2
#Rem    T_ps = fromSIunit_T(T2_ps(p, s))
#Rem  Case 3
#Rem    T_ps = fromSIunit_T(T3_ps(p, s))
#Rem  Case 4
#Rem    T_ps = fromSIunit_T(T4_p(p))
#Rem  Case 5
#Rem    T_ps = fromSIunit_T(T5_ps(p, s))
#Rem  Case Else
#Rem   T_ps = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem Function T_pv(ByVal p As Double, ByVal v As Double) As Double
#Rem Dim rho As Double
#Rem Dim h As Double
#Rem rho = 1 / v
#Rem h = h_prho(p, rho)
#Rem T_pv = T_ph(p, h)
#Rem End Function
#Rem Function T_hs(ByVal h As Double, ByVal s As Double) As Double
#Rem  h = toSIunit_h(h)
#Rem  s = toSIunit_s(s)
#Rem  Select Case Region_hs(h, s)
#Rem  Case 1
#Rem    T_hs = fromSIunit_T(T1_ph(p1_hs(h, s), h))
#Rem  Case 2
#Rem    T_hs = fromSIunit_T(T2_ph(p2_hs(h, s), h))
#Rem  Case 3
#Rem    T_hs = fromSIunit_T(T3_ph(p3_hs(h, s), h))
#Rem  Case 4
#Rem    T_hs = fromSIunit_T(T4_hs(h, s))
#Rem  Case 5
#Rem    T_hs = CVErr(xlErrValue) 'Functions of hs is not implemented in region 5
#Rem  Case Else
#Rem    T_hs = CVErr(xlErrValue)
#Rem  End Select
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*1.3 Pressure (p)
#Rem Function psat_T(ByVal T As Double) As Double
#Rem  T = toSIunit_T(T)
#Rem  If T <= 647.096 And T > 273.15 Then
#Rem    psat_T = fromSIunit_p(p4_T(T))
#Rem
#Rem  Else
#Rem    psat_T = CVErr(xlErrValue)
#Rem  End If
#Rem    psat_T = psat_T * 100
#Rem End Function
#Rem Function psat_s(ByVal s As Double) As Double
#Rem  s = toSIunit_s(s)
#Rem  If s > -0.0001545495919 And s < 9.155759395 Then
#Rem    psat_s = fromSIunit_p(p4_s(s))
#Rem  Else
#Rem    psat_s = CVErr(xlErrValue)
#Rem  End If
#Rem  psat_s = psat_s * 100
#Rem End Function
#Rem Function p_hs(ByVal h As Double, ByVal s As Double) As Double
#Rem  h = toSIunit_h(h)
#Rem  s = toSIunit_s(s)
#Rem  Select Case Region_hs(h, s)
#Rem  Case 1
#Rem    p_hs = fromSIunit_p(p1_hs(h, s))
#Rem  Case 2
#Rem    p_hs = fromSIunit_p(p2_hs(h, s))
#Rem  Case 3
#Rem    p_hs = fromSIunit_p(p3_hs(h, s))
#Rem  Case 4
#Rem    p_hs = fromSIunit_p(p4_T(T4_hs(h, s)))
#Rem  Case 5
#Rem    p_hs = CVErr(xlErrValue) 'Functions of hs is not implemented in region 5
#Rem  Case Else
#Rem   p_hs = CVErr(xlErrValue)
#Rem  End Select
#Rem  p_hs = p_hs * 100
#Rem End Function
#Rem Function p_hrho(ByVal h As Double, ByVal rho As Double) As Double
#Rem '*Not valid for water or sumpercritical since water rho does not change very much with p.
#Rem '*Uses iteration to find p.
#Rem   Dim High_Bound As Double
#Rem   Dim Low_Bound As Double
#Rem   Dim p As Double
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
#Rem 'Function p_Tv(ByVal T As Double, ByVal v As Double) As Double
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
#Rem '***********************************************************************************************************
#Rem '*2 IAPWS IF 97 Calling functions                                                                          *
#Rem '***********************************************************************************************************
#Rem '
#Rem '***********************************************************************************************************
#Rem '*2.1 Functions for region 1
#Rem Private Function v1_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem '5 Equations for Region 1, Section. 5.1 Basic Equation
#Rem 'Eqution 7, Table 3, Page 6
#Rem   Dim i As Integer
#Rem   Dim ps, tau, g_p As Double
#Rem   Dim I1, J1, n1 As Variant
#Rem   Const R As Double = 0.461526 'kJ/(kg K)
#Rem   I1 = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 8, 8, 21, 23, 29, 30, 31, 32)
#Rem   J1 = Array(-2, -1, 0, 1, 2, 3, 4, 5, -9, -7, -1, 0, 1, 3, -3, 0, 1, 3, 17, -4, 0, 6, -5, -2, 10, -8, -11, -6, -29, -31, -38, -39, -40, -41)
#Rem   n1 = Array(0.14632971213167, -0.84548187169114, -3.756360367204, 3.3855169168385, -0.95791963387872, 0.15772038513228, -0.016616417199501, 8.1214629983568E-04, 2.8319080123804E-04, -6.0706301565874E-04, -0.018990068218419, -0.032529748770505, -0.021841717175414, -5.283835796993E-05, -4.7184321073267E-04, -3.0001780793026E-04, 4.7661393906987E-05, -4.4141845330846E-06, -7.2694996297594E-16, -3.1679644845054E-05, -2.8270797985312E-06, -8.5205128120103E-10, -2.2425281908E-06, -6.5171222895601E-07, -1.4341729937924E-13, -4.0516996860117E-07, -1.2734301741641E-09, -1.7424871230634E-10, -6.8762131295531E-19, 1.4478307828521E-20, 2.6335781662795E-23, -1.1947622640071E-23, 1.8228094581404E-24, -9.3537087292458E-26)
#Rem   ps = p / 16.53
#Rem   tau = 1386 / T
#Rem   g_p = 0#
#Rem   For i = 0 To 33
#Rem    g_p = g_p - n1(i) * I1(i) * (7.1 - ps) ^ (I1(i) - 1) * (tau - 1.222) ^ J1(i)
#Rem   Next i
#Rem  v1_pT = R * T / p * ps * g_p / 1000
#Rem End Function
#Rem Private Function h1_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem '5 Equations for Region 1, Section. 5.1 Basic Equation
#Rem 'Eqution 7, Table 3, Page 6
#Rem   Dim i As Integer
#Rem   Dim ps, tau, g_t As Double
#Rem   Dim I1, J1, n1 As Variant
#Rem   Const R As Double = 0.461526 'kJ/(kg K)
#Rem   I1 = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 8, 8, 21, 23, 29, 30, 31, 32)
#Rem   J1 = Array(-2, -1, 0, 1, 2, 3, 4, 5, -9, -7, -1, 0, 1, 3, -3, 0, 1, 3, 17, -4, 0, 6, -5, -2, 10, -8, -11, -6, -29, -31, -38, -39, -40, -41)
#Rem   n1 = Array(0.14632971213167, -0.84548187169114, -3.756360367204, 3.3855169168385, -0.95791963387872, 0.15772038513228, -0.016616417199501, 8.1214629983568E-04, 2.8319080123804E-04, -6.0706301565874E-04, -0.018990068218419, -0.032529748770505, -0.021841717175414, -5.283835796993E-05, -4.7184321073267E-04, -3.0001780793026E-04, 4.7661393906987E-05, -4.4141845330846E-06, -7.2694996297594E-16, -3.1679644845054E-05, -2.8270797985312E-06, -8.5205128120103E-10, -2.2425281908E-06, -6.5171222895601E-07, -1.4341729937924E-13, -4.0516996860117E-07, -1.2734301741641E-09, -1.7424871230634E-10, -6.8762131295531E-19, 1.4478307828521E-20, 2.6335781662795E-23, -1.1947622640071E-23, 1.8228094581404E-24, -9.3537087292458E-26)
#Rem   p = p / 16.53
#Rem   tau = 1386 / T
#Rem   g_t = 0#
#Rem   For i = 0 To 33
#Rem    g_t = g_t + (n1(i) * (7.1 - p) ^ I1(i) * J1(i) * (tau - 1.222) ^ (J1(i) - 1))
#Rem   Next i
#Rem  h1_pT = R * T * tau * g_t
#Rem End Function
def h1_pt(pressure, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997 5 Equations for Region 1, Section. 5.1 Basic Equation Equation 7, Table 3, Page 6'''
    i1 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 8, 8, 21, 23, 29, 30, 31, 32])
    j1 = np.array([-2, -1, 0, 1, 2, 3, 4, 5, -9, -7, -1, 0, 1, 3, -3, 0, 1, 3, 17, -4, 0, 6, -5, -2, 10, -8, -11, -6, -29, -31, -38, -39, -40, -41])
    n1 = np.array([0.14632971213167, -0.84548187169114, -3.756360367204, 3.3855169168385, -0.95791963387872, 0.15772038513228, -0.016616417199501, 8.1214629983568E-04, 2.8319080123804E-04, -6.0706301565874E-04, -0.018990068218419, -0.032529748770505, -0.021841717175414, -5.283835796993E-05, -4.7184321073267E-04, -3.0001780793026E-04, 4.7661393906987E-05, -4.4141845330846E-06, -7.2694996297594E-16, -3.1679644845054E-05, -2.8270797985312E-06, -8.5205128120103E-10, -2.2425281908E-06, -6.5171222895601E-07, -1.4341729937924E-13, -4.0516996860117E-07, -1.2734301741641E-09, -1.7424871230634E-10, -6.8762131295531E-19, 1.4478307828521E-20, 2.6335781662795E-23, -1.1947622640071E-23, 1.8228094581404E-24, -9.3537087292458E-26])

    p = pressure/16.53
    tau = 1386.0/temperature
    g_t =n1*j1*((7.1 - p)**i1)*(tau - 1.222)**(j1 - 1)

    return _R*temperature*g_t.sum()

#Rem Private Function u1_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem '5 Equations for Region 1, Section. 5.1 Basic Equation
#Rem 'Eqution 7, Table 3, Page 6
#Rem   Dim i As Integer
#Rem   Dim tau, g_t, g_p As Double
#Rem   Dim I1, J1, n1 As Variant
#Rem   Const R As Double = 0.461526 'kJ/(kg K)
#Rem   I1 = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 8, 8, 21, 23, 29, 30, 31, 32)
#Rem   J1 = Array(-2, -1, 0, 1, 2, 3, 4, 5, -9, -7, -1, 0, 1, 3, -3, 0, 1, 3, 17, -4, 0, 6, -5, -2, 10, -8, -11, -6, -29, -31, -38, -39, -40, -41)
#Rem   n1 = Array(0.14632971213167, -0.84548187169114, -3.756360367204, 3.3855169168385, -0.95791963387872, 0.15772038513228, -0.016616417199501, 8.1214629983568E-04, 2.8319080123804E-04, -6.0706301565874E-04, -0.018990068218419, -0.032529748770505, -0.021841717175414, -5.283835796993E-05, -4.7184321073267E-04, -3.0001780793026E-04, 4.7661393906987E-05, -4.4141845330846E-06, -7.2694996297594E-16, -3.1679644845054E-05, -2.8270797985312E-06, -8.5205128120103E-10, -2.2425281908E-06, -6.5171222895601E-07, -1.4341729937924E-13, -4.0516996860117E-07, -1.2734301741641E-09, -1.7424871230634E-10, -6.8762131295531E-19, 1.4478307828521E-20, 2.6335781662795E-23, -1.1947622640071E-23, 1.8228094581404E-24, -9.3537087292458E-26)
#Rem   p = p / 16.53
#Rem   tau = 1386 / T
#Rem   g_t = 0#
#Rem   g_p = 0#
#Rem   For i = 0 To 33
#Rem    g_p = g_p - n1(i) * I1(i) * (7.1 - p) ^ (I1(i) - 1) * (tau - 1.222) ^ J1(i)
#Rem    g_t = g_t + (n1(i) * (7.1 - p) ^ I1(i) * J1(i) * (tau - 1.222) ^ (J1(i) - 1))
#Rem   Next i
#Rem   u1_pT = R * T * (tau * g_t - p * g_p)
#Rem End Function
#Rem Private Function s1_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem '5 Equations for Region 1, Section. 5.1 Basic Equation
#Rem 'Eqution 7, Table 3, Page 6
#Rem   Dim i As Integer
#Rem   Dim g, g_t As Double
#Rem   Dim I1, J1, n1 As Variant
#Rem   Const R As Double = 0.461526 'kJ/(kg K)
#Rem   I1 = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 8, 8, 21, 23, 29, 30, 31, 32)
#Rem   J1 = Array(-2, -1, 0, 1, 2, 3, 4, 5, -9, -7, -1, 0, 1, 3, -3, 0, 1, 3, 17, -4, 0, 6, -5, -2, 10, -8, -11, -6, -29, -31, -38, -39, -40, -41)
#Rem   n1 = Array(0.14632971213167, -0.84548187169114, -3.756360367204, 3.3855169168385, -0.95791963387872, 0.15772038513228, -0.016616417199501, 8.1214629983568E-04, 2.8319080123804E-04, -6.0706301565874E-04, -0.018990068218419, -0.032529748770505, -0.021841717175414, -5.283835796993E-05, -4.7184321073267E-04, -3.0001780793026E-04, 4.7661393906987E-05, -4.4141845330846E-06, -7.2694996297594E-16, -3.1679644845054E-05, -2.8270797985312E-06, -8.5205128120103E-10, -2.2425281908E-06, -6.5171222895601E-07, -1.4341729937924E-13, -4.0516996860117E-07, -1.2734301741641E-09, -1.7424871230634E-10, -6.8762131295531E-19, 1.4478307828521E-20, 2.6335781662795E-23, -1.1947622640071E-23, 1.8228094581404E-24, -9.3537087292458E-26)
#Rem   p = p / 16.53
#Rem   T = 1386 / T
#Rem   g = 0#
#Rem   g_t = 0#
#Rem   For i = 0 To 33
#Rem    g_t = g_t + (n1(i) * (7.1 - p) ^ I1(i) * J1(i) * (T - 1.222) ^ (J1(i) - 1))
#Rem    g = g + n1(i) * (7.1 - p) ^ I1(i) * (T - 1.222) ^ J1(i)
#Rem   Next i
#Rem   s1_pT = R * T * g_t - R * g
#Rem End Function
#Rem Private Function Cp1_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem '5 Equations for Region 1, Section. 5.1 Basic Equation
#Rem 'Eqution 7, Table 3, Page 6
#Rem   Dim i As Integer
#Rem   Dim G_tt As Double
#Rem   Dim I1, J1, n1 As Variant
#Rem   Const R As Double = 0.461526 'kJ/(kg K)
#Rem   I1 = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 8, 8, 21, 23, 29, 30, 31, 32)
#Rem   J1 = Array(-2, -1, 0, 1, 2, 3, 4, 5, -9, -7, -1, 0, 1, 3, -3, 0, 1, 3, 17, -4, 0, 6, -5, -2, 10, -8, -11, -6, -29, -31, -38, -39, -40, -41)
#Rem   n1 = Array(0.14632971213167, -0.84548187169114, -3.756360367204, 3.3855169168385, -0.95791963387872, 0.15772038513228, -0.016616417199501, 8.1214629983568E-04, 2.8319080123804E-04, -6.0706301565874E-04, -0.018990068218419, -0.032529748770505, -0.021841717175414, -5.283835796993E-05, -4.7184321073267E-04, -3.0001780793026E-04, 4.7661393906987E-05, -4.4141845330846E-06, -7.2694996297594E-16, -3.1679644845054E-05, -2.8270797985312E-06, -8.5205128120103E-10, -2.2425281908E-06, -6.5171222895601E-07, -1.4341729937924E-13, -4.0516996860117E-07, -1.2734301741641E-09, -1.7424871230634E-10, -6.8762131295531E-19, 1.4478307828521E-20, 2.6335781662795E-23, -1.1947622640071E-23, 1.8228094581404E-24, -9.3537087292458E-26)
#Rem   p = p / 16.53
#Rem   T = 1386 / T
#Rem   G_tt = 0#
#Rem   For i = 0 To 33
#Rem    G_tt = G_tt + (n1(i) * (7.1 - p) ^ I1(i) * J1(i) * (J1(i) - 1) * (T - 1.222) ^ (J1(i) - 2))
#Rem   Next i
#Rem   Cp1_pT = -R * T ^ 2 * G_tt
#Rem End Function
#Rem Private Function Cv1_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem '5 Equations for Region 1, Section. 5.1 Basic Equation
#Rem 'Eqution 7, Table 3, Page 6
#Rem   Dim i As Integer
#Rem   Dim g_p, g_pp, g_pt, G_tt As Double
#Rem   Dim I1, J1, n1 As Variant
#Rem   Const R As Double = 0.461526 'kJ/(kg K)
#Rem   I1 = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 8, 8, 21, 23, 29, 30, 31, 32)
#Rem   J1 = Array(-2, -1, 0, 1, 2, 3, 4, 5, -9, -7, -1, 0, 1, 3, -3, 0, 1, 3, 17, -4, 0, 6, -5, -2, 10, -8, -11, -6, -29, -31, -38, -39, -40, -41)
#Rem   n1 = Array(0.14632971213167, -0.84548187169114, -3.756360367204, 3.3855169168385, -0.95791963387872, 0.15772038513228, -0.016616417199501, 8.1214629983568E-04, 2.8319080123804E-04, -6.0706301565874E-04, -0.018990068218419, -0.032529748770505, -0.021841717175414, -5.283835796993E-05, -4.7184321073267E-04, -3.0001780793026E-04, 4.7661393906987E-05, -4.4141845330846E-06, -7.2694996297594E-16, -3.1679644845054E-05, -2.8270797985312E-06, -8.5205128120103E-10, -2.2425281908E-06, -6.5171222895601E-07, -1.4341729937924E-13, -4.0516996860117E-07, -1.2734301741641E-09, -1.7424871230634E-10, -6.8762131295531E-19, 1.4478307828521E-20, 2.6335781662795E-23, -1.1947622640071E-23, 1.8228094581404E-24, -9.3537087292458E-26)
#Rem   p = p / 16.53
#Rem   T = 1386 / T
#Rem   g_p = 0#
#Rem   g_pp = 0#
#Rem   g_pt = 0#
#Rem   G_tt = 0#
#Rem   For i = 0 To 33
#Rem    g_p = g_p - n1(i) * I1(i) * (7.1 - p) ^ (I1(i) - 1) * (T - 1.222) ^ J1(i)
#Rem    g_pp = g_pp + n1(i) * I1(i) * (I1(i) - 1) * (7.1 - p) ^ (I1(i) - 2) * (T - 1.222) ^ J1(i)
#Rem    g_pt = g_pt - n1(i) * I1(i) * (7.1 - p) ^ (I1(i) - 1) * J1(i) * (T - 1.222) ^ (J1(i) - 1)
#Rem    G_tt = G_tt + n1(i) * (7.1 - p) ^ I1(i) * J1(i) * (J1(i) - 1) * (T - 1.222) ^ (J1(i) - 2)
#Rem   Next i
#Rem   Cv1_pT = R * (-(T ^ 2 * G_tt) + (g_p - T * g_pt) ^ 2 / g_pp)
#Rem End Function
#Rem Private Function w1_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem '5 Equations for Region 1, Section. 5.1 Basic Equation
#Rem 'Eqution 7, Table 3, Page 6
#Rem   Dim i As Integer
#Rem   Dim g_p, g_pp, g_pt, G_tt, tau As Double
#Rem   Dim I1, J1, n1 As Variant
#Rem   Const R As Double = 0.461526 'kJ/(kg K)
#Rem   I1 = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 8, 8, 21, 23, 29, 30, 31, 32)
#Rem   J1 = Array(-2, -1, 0, 1, 2, 3, 4, 5, -9, -7, -1, 0, 1, 3, -3, 0, 1, 3, 17, -4, 0, 6, -5, -2, 10, -8, -11, -6, -29, -31, -38, -39, -40, -41)
#Rem   n1 = Array(0.14632971213167, -0.84548187169114, -3.756360367204, 3.3855169168385, -0.95791963387872, 0.15772038513228, -0.016616417199501, 8.1214629983568E-04, 2.8319080123804E-04, -6.0706301565874E-04, -0.018990068218419, -0.032529748770505, -0.021841717175414, -5.283835796993E-05, -4.7184321073267E-04, -3.0001780793026E-04, 4.7661393906987E-05, -4.4141845330846E-06, -7.2694996297594E-16, -3.1679644845054E-05, -2.8270797985312E-06, -8.5205128120103E-10, -2.2425281908E-06, -6.5171222895601E-07, -1.4341729937924E-13, -4.0516996860117E-07, -1.2734301741641E-09, -1.7424871230634E-10, -6.8762131295531E-19, 1.4478307828521E-20, 2.6335781662795E-23, -1.1947622640071E-23, 1.8228094581404E-24, -9.3537087292458E-26)
#Rem   p = p / 16.53
#Rem   tau = 1386 / T
#Rem   g_p = 0#
#Rem   g_pp = 0#
#Rem   g_pt = 0#
#Rem   G_tt = 0#
#Rem   For i = 0 To 33
#Rem    g_p = g_p - n1(i) * I1(i) * (7.1 - p) ^ (I1(i) - 1) * (tau - 1.222) ^ J1(i)
#Rem    g_pp = g_pp + n1(i) * I1(i) * (I1(i) - 1) * (7.1 - p) ^ (I1(i) - 2) * (tau - 1.222) ^ J1(i)
#Rem    g_pt = g_pt - n1(i) * I1(i) * (7.1 - p) ^ (I1(i) - 1) * J1(i) * (tau - 1.222) ^ (J1(i) - 1)
#Rem    G_tt = G_tt + n1(i) * (7.1 - p) ^ I1(i) * J1(i) * (J1(i) - 1) * (tau - 1.222) ^ (J1(i) - 2)
#Rem   Next i
#Rem   w1_pT = (1000 * R * T * g_p ^ 2 / ((g_p - tau * g_pt) ^ 2 / (tau ^ 2 * G_tt) - g_pp)) ^ 0.5
#Rem End Function
#Rem Private Function T1_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem '5 Equations for Region 1, Section. 5.1 Basic Equation, 5.2.1 The Backward Equation T ( p,h )
#Rem 'Eqution 11, Table 6, Page 10
#Rem   Dim i As Integer
#Rem   Dim T As Double
#Rem   Dim I1, J1, n1 As Variant
#Rem   I1 = Array(0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 5, 6)
#Rem   J1 = Array(0, 1, 2, 6, 22, 32, 0, 1, 2, 3, 4, 10, 32, 10, 32, 10, 32, 32, 32, 32)
#Rem   n1 = Array(-238.72489924521, 404.21188637945, 113.49746881718, -5.8457616048039, -1.528548241314E-04, -1.0866707695377E-06, -13.391744872602, 43.211039183559, -54.010067170506, 30.535892203916, -6.5964749423638, 9.3965400878363E-03, 1.157364750534E-07, -2.5858641282073E-05, -4.0644363084799E-09, 6.6456186191635E-08, 8.0670734103027E-11, -9.3477771213947E-13, 5.8265442020601E-15, -1.5020185953503E-17)
#Rem   h = h / 2500
#Rem   T = 0#
#Rem   For i = 0 To 19
#Rem    T = T + n1(i) * p ^ I1(i) * (h + 1) ^ J1(i)
#Rem   Next i
#Rem   T1_ph = T
#Rem End Function
#Rem Private Function T1_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem '5 Equations for Region 1, Section. 5.1 Basic Equation, 5.2.2 The Backward Equation T ( p, s )
#Rem 'Eqution 13, Table 8, Page 11
#Rem   Dim i As Integer
#Rem   Dim I1, J1, n1 As Variant
#Rem   I1 = Array(0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 4)
#Rem   J1 = Array(0, 1, 2, 3, 11, 31, 0, 1, 2, 3, 12, 31, 0, 1, 2, 9, 31, 10, 32, 32)
#Rem   n1 = Array(174.78268058307, 34.806930892873, 6.5292584978455, 0.33039981775489, -1.9281382923196E-07, -2.4909197244573E-23, -0.26107636489332, 0.22592965981586, -0.064256463395226, 7.8876289270526E-03, 3.5672110607366E-10, 1.7332496994895E-24, 5.6608900654837E-04, -3.2635483139717E-04, 4.4778286690632E-05, -5.1322156908507E-10, -4.2522657042207E-26, 2.6400441360689E-13, 7.8124600459723E-29, -3.0732199903668E-31)
#Rem   T1_ps = 0#
#Rem   For i = 0 To 19
#Rem    T1_ps = T1_ps + n1(i) * p ^ I1(i) * (s + 2) ^ J1(i)
#Rem   Next i
#Rem End Function
#Rem Private Function p1_hs(ByVal h As Double, ByVal s As Double) As Double
#Rem 'Supplementary Release on Backward Equations for Pressure as a Function of Enthalpy and Entropy p(h,s) to the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam
#Rem '5 Backward Equation p(h,s) for Region 1
#Rem 'Eqution 1, Table 2, Page 5
#Rem   Dim i As Integer
#Rem   Dim p As Double
#Rem   Dim I1, J1, n1 As Variant
#Rem   I1 = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 5)
#Rem   J1 = Array(0, 1, 2, 4, 5, 6, 8, 14, 0, 1, 4, 6, 0, 1, 10, 4, 1, 4, 0)
#Rem   n1 = Array(-0.691997014660582, -18.361254878756, -9.28332409297335, 65.9639569909906, -16.2060388912024, 450.620017338667, 854.68067822417, 6075.23214001162, 32.6487682621856, -26.9408844582931, -319.9478483343, -928.35430704332, 30.3634537455249, -65.0540422444146, -4309.9131651613, -747.512324096068, 730.000345529245, 1142.84032569021, -436.407041874559)
#Rem   h = h / 3400
#Rem   s = s / 7.6
#Rem   p = 0#
#Rem   For i = 0 To 18
#Rem    p = p + n1(i) * (h + 0.05) ^ I1(i) * (s + 0.05) ^ J1(i)
#Rem   Next i
#Rem   p1_hs = p * 100
#Rem End Function
#Rem Private Function T1_prho(ByVal p As Double, ByVal rho As Double) As Double
#Rem   'Solve by iteration. Observe that fo low temperatures this equation has 2 solutions.
#Rem   'Solve with half interval method
#Rem   Dim i As Integer
#Rem   Dim Ts, Low_Bound, High_Bound, rhos As Double
#Rem   Low_Bound = 273.15
#Rem   High_Bound = T4_p(p)
#Rem   Do While Abs(rho - rhos) > 0.00001
#Rem     Ts = (Low_Bound + High_Bound) / 2
#Rem     rhos = 1 / v1_pT(p, Ts)
#Rem     If rhos < rho Then
#Rem       High_Bound = Ts
#Rem     Else
#Rem       Low_Bound = Ts
#Rem     End If
#Rem     Loop
#Rem     T1_prho = Ts
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*2.2 Functions for region 2
#Rem
#Rem Private Function v2_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem '6 Equations for Region 2, Section. 6.1 Basic Equation
#Rem 'Table 11 and 12, Page 14 and 15
#Rem   Dim i As Integer
#Rem   Dim tau, g0_pi, gr_pi As Double
#Rem   Dim Ir, Jr, nr, J0, n0 As Variant
#Rem   Const R As Double = 0.461526 'kJ/(kg K)
#Rem   J0 = Array(0, 1, -5, -4, -3, -2, -1, 2, 3)
#Rem   n0 = Array(-9.6927686500217, 10.086655968018, -0.005608791128302, 0.071452738081455, -0.40710498223928, 1.4240819171444, -4.383951131945, -0.28408632460772, 0.021268463753307)
#Rem   Ir = Array(1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9, 10, 10, 10, 16, 16, 18, 20, 20, 20, 21, 22, 23, 24, 24, 24)
#Rem   Jr = Array(0, 1, 2, 3, 6, 1, 2, 4, 7, 36, 0, 1, 3, 6, 35, 1, 2, 3, 7, 3, 16, 35, 0, 11, 25, 8, 36, 13, 4, 10, 14, 29, 50, 57, 20, 35, 48, 21, 53, 39, 26, 40, 58)
#Rem   nr = Array(-1.7731742473213E-03, -0.017834862292358, -0.045996013696365, -0.057581259083432, -0.05032527872793, -3.3032641670203E-05, -1.8948987516315E-04, -3.9392777243355E-03, -0.043797295650573, -2.6674547914087E-05, 2.0481737692309E-08, 4.3870667284435E-07, -3.227767723857E-05, -1.5033924542148E-03, -0.040668253562649, -7.8847309559367E-10, 1.2790717852285E-08, 4.8225372718507E-07, 2.2922076337661E-06, -1.6714766451061E-11, -2.1171472321355E-03, -23.895741934104, -5.905956432427E-18, -1.2621808899101E-06, -0.038946842435739, 1.1256211360459E-11, -8.2311340897998, 1.9809712802088E-08, 1.0406965210174E-19, -1.0234747095929E-13, -1.0018179379511E-09, -8.0882908646985E-11, 0.10693031879409, -0.33662250574171, 8.9185845355421E-25, 3.0629316876232E-13, -4.2002467698208E-06, -5.9056029685639E-26, 3.7826947613457E-06, -1.2768608934681E-15, 7.3087610595061E-29, 5.5414715350778E-17, -9.436970724121E-07)
#Rem   tau = 540 / T
#Rem   g0_pi = 1 / p
#Rem   gr_pi = 0#
#Rem   For i = 0 To 42
#Rem    gr_pi = gr_pi + nr(i) * Ir(i) * p ^ (Ir(i) - 1) * (tau - 0.5) ^ Jr(i)
#Rem   Next i
#Rem   v2_pT = R * T / p * p * (g0_pi + gr_pi) / 1000
#Rem End Function
#Rem Private Function h2_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem '6 Equations for Region 2, Section. 6.1 Basic Equation
#Rem 'Table 11 and 12, Page 14 and 15
#Rem   Dim i As Integer
#Rem   Dim tau, g0_tau, gr_tau As Double
#Rem   Dim Ir, Jr, nr, J0, n0 As Variant
#Rem   Const R As Double = 0.461526 'kJ/(kg K)
#Rem   J0 = Array(0, 1, -5, -4, -3, -2, -1, 2, 3)
#Rem   n0 = Array(-9.6927686500217, 10.086655968018, -0.005608791128302, 0.071452738081455, -0.40710498223928, 1.4240819171444, -4.383951131945, -0.28408632460772, 0.021268463753307)
#Rem   Ir = Array(1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9, 10, 10, 10, 16, 16, 18, 20, 20, 20, 21, 22, 23, 24, 24, 24)
#Rem   Jr = Array(0, 1, 2, 3, 6, 1, 2, 4, 7, 36, 0, 1, 3, 6, 35, 1, 2, 3, 7, 3, 16, 35, 0, 11, 25, 8, 36, 13, 4, 10, 14, 29, 50, 57, 20, 35, 48, 21, 53, 39, 26, 40, 58)
#Rem   nr = Array(-1.7731742473213E-03, -0.017834862292358, -0.045996013696365, -0.057581259083432, -0.05032527872793, -3.3032641670203E-05, -1.8948987516315E-04, -3.9392777243355E-03, -0.043797295650573, -2.6674547914087E-05, 2.0481737692309E-08, 4.3870667284435E-07, -3.227767723857E-05, -1.5033924542148E-03, -0.040668253562649, -7.8847309559367E-10, 1.2790717852285E-08, 4.8225372718507E-07, 2.2922076337661E-06, -1.6714766451061E-11, -2.1171472321355E-03, -23.895741934104, -5.905956432427E-18, -1.2621808899101E-06, -0.038946842435739, 1.1256211360459E-11, -8.2311340897998, 1.9809712802088E-08, 1.0406965210174E-19, -1.0234747095929E-13, -1.0018179379511E-09, -8.0882908646985E-11, 0.10693031879409, -0.33662250574171, 8.9185845355421E-25, 3.0629316876232E-13, -4.2002467698208E-06, -5.9056029685639E-26, 3.7826947613457E-06, -1.2768608934681E-15, 7.3087610595061E-29, 5.5414715350778E-17, -9.436970724121E-07)
#Rem   tau = 540 / T
#Rem   g0_tau = 0#
#Rem   For i = 0 To 8
#Rem     g0_tau = g0_tau + n0(i) * J0(i) * tau ^ (J0(i) - 1)
#Rem   Next i
#Rem   gr_tau = 0#
#Rem   For i = 0 To 42
#Rem    gr_tau = gr_tau + nr(i) * p ^ Ir(i) * Jr(i) * (tau - 0.5) ^ (Jr(i) - 1)
#Rem   Next i
#Rem   h2_pT = R * T * tau * (g0_tau + gr_tau)
#Rem End Function
#Rem Private Function u2_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem '6 Equations for Region 2, Section. 6.1 Basic Equation
#Rem 'Table 11 and 12, Page 14 and 15
#Rem   Dim i As Integer
#Rem   Dim tau, g0_tau, g0_pi, gr_pi, gr_tau As Double
#Rem   Dim Ir, Jr, nr, J0, n0 As Variant
#Rem   Const R As Double = 0.461526 'kJ/(kg K)
#Rem   J0 = Array(0, 1, -5, -4, -3, -2, -1, 2, 3)
#Rem   n0 = Array(-9.6927686500217, 10.086655968018, -0.005608791128302, 0.071452738081455, -0.40710498223928, 1.4240819171444, -4.383951131945, -0.28408632460772, 0.021268463753307)
#Rem   Ir = Array(1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9, 10, 10, 10, 16, 16, 18, 20, 20, 20, 21, 22, 23, 24, 24, 24)
#Rem   Jr = Array(0, 1, 2, 3, 6, 1, 2, 4, 7, 36, 0, 1, 3, 6, 35, 1, 2, 3, 7, 3, 16, 35, 0, 11, 25, 8, 36, 13, 4, 10, 14, 29, 50, 57, 20, 35,
#Rem   nr = Array(-1.7731742473213E-03, -0.017834862292358, -0.045996013696365, -0.057581259083432, -0.05032527872793, -3.3032641670203E-05, -1.8948987516315E-04, -3.9392777243355E-03, -0.043797295650573, -2.6674547914087E-05, 2.0481737692309E-08, 4.3870667284435E-07, -3.227767723857E-05, -1.5033924542148E-03, -0.040668253562649, -7.8847309559367E-10, 1.2790717852285E-08, 4.8225372718507E-07, 2.2922076337661E-06, -1.6714766451061E-11, -2.1171472321355E-03, -23.895741934104, -5.905956432427E-18, -1.2621808899101E-06, -0.038946842435739, 1.1256211360459E-11, -8.2311340897998, 1.9809712802088E-08, 1.0406965210174E-19, -1.0234747095929E-13, -1.0018179379511E-09, -8.0882908646985E-11, 0.10693031879409, -0.33662250574171, 8.9185845355421E-25, 3.0629316876232E-13, -4.2002467698208E-06, -5.9056029685639E-26, 3.7826947613457E-06, -1.2768608934681E-15, 7.3087610595061E-29, 5.5414715350778E-17, -9.436970724121E-07)
#Rem   tau = 540 / T
#Rem   g0_tautau = 0#
#Rem   For i = 0 To 8
#Rem     g0_tautau = g0_tautau + n0(i) * J0(i) * (J0(i) - 1) * tau ^ (J0(i) - 2)
#Rem   Next i
#Rem   gr_pi = 0#
#Rem   gr_pitau = 0#
#Rem   gr_pipi = 0#
#Rem   gr_tautau = 0#
#Rem   For i = 0 To 42
#Rem    gr_pi = gr_pi + nr(i) * Ir(i) * p ^ (Ir(i) - 1) * (tau - 0.5) ^ Jr(i)
#Rem    gr_pipi = gr_pipi + nr(i) * Ir(i) * (Ir(i) - 1) * p ^ (Ir(i) - 2) * (tau - 0.5) ^ Jr(i)
#Rem    gr_pitau = gr_pitau + nr(i) * Ir(i) * p ^ (Ir(i) - 1) * Jr(i) * (tau - 0.5) ^ (Jr(i) - 1)
#Rem    gr_tautau = gr_tautau + nr(i) * p ^ Ir(i) * Jr(i) * (Jr(i) - 1) * (tau - 0.5) ^ (Jr(i) - 2)
#Rem   Next i
#Rem   w2_pT = (1000 * R * T * (1 + 2 * p * gr_pi + p ^ 2 * gr_pi ^ 2) / ((1 - p ^ 2 * gr_pipi) + (1 + p * gr_pi - tau * p * gr_pitau) ^ 2 / (tau ^ 2 * (g0_tautau + gr_tautau)))) ^ 0.5
#Rem End Function
#Rem Private Function T2_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem   'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem   '6 Equations for Region 2,6.3.1 The Backward Equations T( p, h ) for Subregions 2a, 2b, and 2c
#Rem   Dim sub_reg As Integer
#Rem   Dim i As Integer
#Rem   Dim Ts, hs As Double
#Rem   Dim Ji, Ii, ni As Variant
#Rem
#Rem   If p < 4 Then
#Rem    sub_reg = 1
#Rem   Else
#Rem    If p < (905.84278514723 - 0.67955786399241 * h + 1.2809002730136E-04 * h ^ 2) Then
#Rem      sub_reg = 2
#Rem    Else
#Rem      sub_reg = 3
#Rem    End If
#Rem   End If
#Rem
#Rem   Select Case sub_reg
#Rem   Case 1
#Rem     'Subregion A
#Rem     'Table 20, Eq 22, page 22
#Rem     Ji = Array(0, 1, 2, 3, 7, 20, 0, 1, 2, 3, 7, 9, 11, 18, 44, 0, 2, 7, 36, 38, 40, 42, 44, 24, 44, 12, 32, 44, 32, 36, 42, 34, 44, 28)
#Rem     Ii = Array(0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7)
#Rem     ni = Array(1089.8952318288, 849.51654495535, -107.81748091826, 33.153654801263, -7.4232016790248, 11.765048724356, 1.844574935579, -4.1792700549624, 6.2478196935812, -17.344563108114, -200.58176862096, 271.96065473796, -455.11318285818, 3091.9688604755, 252266.40357872, -6.1707422868339E-03, -0.31078046629583, 11.670873077107, 128127984.04046, -985549096.23276, 2822454697.3002, -3594897141.0703, 1722734991.3197, -13551.334240775, 12848734.66465, 1.3865724283226, 235988.32556514, -13105236.545054, 7399.9835474766, -551966.9703006, 3715408.5996233, 19127.72923966, -415351.64835634, -62.459855192507)
#Rem     Ts = 0
#Rem     hs = h / 2000
#Rem     For i = 0 To 33
#Rem       Ts = Ts + ni(i) * p ^ (Ii(i)) * (hs - 2.1) ^ Ji(i)
#Rem     Next i
#Rem     T2_ph = Ts
#Rem   Case 2
#Rem     'Subregion B
#Rem     'Table 21, Eq 23, page 23
#Rem     Ji = Array(0, 1, 2, 12, 18, 24, 28, 40, 0, 2, 6, 12, 18, 24, 28, 40, 2, 8, 18, 40, 1, 2, 12, 24, 2, 12, 18, 24, 28, 40, 18, 24, 40, 28, 2, 28, 1, 40)
#Rem     Ii = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 6, 7, 7, 9, 9)
#Rem     ni = Array(1489.5041079516, 743.07798314034, -97.708318797837, 2.4742464705674, -0.63281320016026, 1.1385952129658, -0.47811863648625, 8.5208123431544E-03, 0.93747147377932, 3.3593118604916, 3.3809355601454, 0.16844539671904, 0.73875745236695, -0.47128737436186, 0.15020273139707, -0.002176411421975, -0.021810755324761, -0.10829784403677, -0.046333324635812, 7.1280351959551E-05, 1.1032831789999E-04, 1.8955248387902E-04, 3.0891541160537E-03, 1.3555504554949E-03, 2.8640237477456E-07, -1.0779857357512E-05, -7.6462712454814E-05, 1.4052392818316E-05, -3.1083814331434E-05, -1.0302738212103E-06, 2.821728163504E-07, 1.2704902271945E-06, 7.3803353468292E-08, -1.1030139238909E-08, -8.1456365207833E-14, -2.5180545682962E-11, -1.7565233969407E-18, 8.6934156344163E-15)
#Rem     Ts = 0
#Rem     hs = h / 2000
#Rem     For i = 0 To 37
#Rem       Ts = Ts + ni(i) * (p - 2) ^ (Ii(i)) * (hs - 2.6) ^ Ji(i)
#Rem     Next i
#Rem     T2_ph = Ts
#Rem   Case Else
#Rem     'Subregion C
#Rem     'Table 22, Eq 24, page 24
#Rem     Ji = Array(0, 4, 0, 2, 0, 2, 0, 1, 0, 2, 0, 1, 4, 8, 4, 0, 1, 4, 10, 12, 16, 20, 22)
#Rem     Ii = Array(-7, -7, -6, -6, -5, -5, -2, -2, -1, -1, 0, 0, 1, 1, 2, 6, 6, 6, 6, 6, 6, 6, 6)
#Rem     ni = Array(-3236839855524.2, 7326335090218.1, 358250899454.47, -583401318515.9, -10783068217.47, 20825544563.171, 610747.83564516, 859777.2253558, -25745.72360417, 31081.088422714, 1208.2315865936, 482.19755109255, 3.7966001272486, -10.842984880077, -0.04536417267666, 1.4559115658698E-13, 1.126159740723E-12, -1.7804982240686E-11, 1.2324579690832E-07, -1.1606921130984E-06, 2.7846367088554E-05, -5.9270038474176E-04, 1.2918582991878E-03)
#Rem     Ts = 0
#Rem     hs = h / 2000
#Rem     For i = 0 To 22
#Rem       Ts = Ts + ni(i) * (p + 25) ^ (Ii(i)) * (hs - 1.8) ^ Ji(i)
#Rem     Next i
#Rem     T2_ph = Ts
#Rem   End Select
#Rem End Function
#Rem Private Function T2_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem   'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem   '6 Equations for Region 2,6.3.2 The Backward Equations T( p, s ) for Subregions 2a, 2b, and 2c
#Rem   'Page 26
#Rem   Dim sub_reg As Integer
#Rem   Dim i As Integer
#Rem   Dim teta, sigma As Double
#Rem   Dim Ji, Ii, ni As Variant
#Rem
#Rem   If p < 4 Then
#Rem      sub_reg = 1
#Rem   Else
#Rem      If s < 5.85 Then
#Rem        sub_reg = 3
#Rem      Else
#Rem        sub_reg = 2
#Rem      End If
#Rem   End If
#Rem   Select Case sub_reg
#Rem   Case 1
#Rem    'Subregion A
#Rem    'Table 25, Eq 25, page 26
#Rem    Ii = Array(-1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.25, -1.25, -1.25, -1, -1, -1, -1, -1, -1, -0.75, -0.75, -0.5, -0.5, -0.5, -0.5, -0.25, -0.25, -0.25, -0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.75, 0.75, 0.75, 0.75, 1, 1, 1.25, 1.25, 1.5, 1.5)
#Rem    Ji = Array(-24, -23, -19, -13, -11, -10, -19, -15, -6, -26, -21, -17, -16, -9, -8, -15, -14, -26, -13, -9, -7, -27, -25, -11, -6, 1, 4, 8, 11, 0, 1, 5, 6, 10, 14, 16, 0, 4, 9, 17, 7, 18, 3, 15, 5, 18)
#Rem    ni = Array(-392359.83861984, 515265.7382727, 40482.443161048, -321.93790923902, 96.961424218694, -22.867846371773, -449429.14124357, -5011.8336020166, 0.35684463560015, 44235.33584819, -13673.388811708, 421632.60207864, 22516.925837475, 474.42144865646, -149.31130797647, -197811.26320452, -23554.39947076, -19070.616302076, 55375.669883164, 3829.3691437363, -603.91860580567, 1936.3102620331, 4266.064369861, -5978.0638872718, -704.01463926862, 338.36784107553, 20.862786635187, 0.033834172656196, -4.3124428414893E-05, 166.53791356412, -139.86292055898, -0.78849547999872, 0.072132411753872, -5.9754839398283E-03, -1.2141358953904E-05, 2.3227096733871E-07, -10.538463566194, 2.0718925496502, -0.072193155260427, 2.074988708112E-07, -0.018340657911379, 2.9036272348696E-07, 0.21037527893619, 2.5681239729999E-04, -0.012799002933781, -8.2198102652018E-06)
#Rem    sigma = s / 2
#Rem    teta = 0
#Rem    For i = 0 To 45
#Rem      teta = teta + ni(i) * p ^ Ii(i) * (sigma - 2) ^ Ji(i)
#Rem    Next i
#Rem    T2_ps = teta
#Rem   Case 2
#Rem     'Subregion B
#Rem     'Table 26, Eq 26, page 27
#Rem     Ii = Array(-6, -6, -5, -5, -4, -4, -4, -3, -3, -3, -3, -2, -2, -2, -2, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5)
#Rem     Ji = Array(0, 11, 0, 11, 0, 1, 11, 0, 1, 11, 12, 0, 1, 6, 10, 0, 1, 5, 8, 9, 0, 1, 2, 4, 5, 6, 9, 0, 1, 2, 3, 7, 8, 0, 1, 5, 0, 1, 3, 0, 1, 0, 1, 2)
#Rem     ni = Array(316876.65083497, 20.864175881858, -398593.99803599, -21.816058518877, 223697.85194242, -2784.1703445817, 9.920743607148, -75197.512299157, 2970.8605951158, -3.4406878548526, 0.38815564249115, 17511.29508575, -1423.7112854449, 1.0943803364167, 0.89971619308495, -3375.9740098958, 471.62885818355, -1.9188241993679, 0.41078580492196, -0.33465378172097, 1387.0034777505, -406.63326195838, 41.72734715961, 2.1932549434532, -1.0320050009077, 0.35882943516703, 5.2511453726066E-03, 12.838916450705, -2.8642437219381, 0.56912683664855, -0.099962954584931, -3.2632037778459E-03, 2.3320922576723E-04, -0.1533480985745, 0.029072288239902, 3.7534702741167E-04, 1.7296691702411E-03, -3.8556050844504E-04, -3.5017712292608E-05, -1.4566393631492E-05, 5.6420857267269E-06, 4.1286150074605E-08, -2.0684671118824E-08, 1.6409393674725E-09)
#Rem     sigma = s / 0.7853
#Rem     teta = 0
#Rem     For i = 0 To 43
#Rem       teta = teta + ni(i) * p ^ Ii(i) * (10 - sigma) ^ Ji(i)
#Rem     Next i
#Rem     T2_ps = teta
#Rem   Case Else
#Rem     'Subregion C
#Rem     'Table 27, Eq 27, page 28
#Rem     Ii = Array(-2, -2, -1, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 7, 7, 7, 7)
#Rem     Ji = Array(0, 1, 0, 0, 1, 2, 3, 0, 1, 3, 4, 0, 1, 2, 0, 1, 5, 0, 1, 4, 0, 1, 2, 0, 1, 0, 1, 3, 4, 5)
#Rem     ni = Array(909.68501005365, 2404.566708842, -591.6232638713, 541.45404128074, -270.98308411192, 979.76525097926, -469.66772959435, 14.399274604723, -19.104204230429, 5.3299167111971, -21.252975375934, -0.3114733441376, 0.60334840894623, -0.042764839702509, 5.8185597255259E-03, -0.014597008284753, 5.6631175631027E-03, -7.6155864584577E-05, 2.2440342919332E-04, -1.2561095013413E-05, 6.3323132660934E-07, -2.0541989675375E-06, 3.6405370390082E-08, -2.9759897789215E-09, 1.0136618529763E-08, 5.9925719692351E-12, -2.0677870105164E-11, -2.0874278181886E-11, 1.0162166825089E-10, -1.6429828281347E-10)
#Rem     sigma = s / 2.9251
#Rem     teta = 0
#Rem     For i = 0 To 29
#Rem       teta = teta + ni(i) * p ^ Ii(i) * (2 - sigma) ^ Ji(i)
#Rem     Next i
#Rem     T2_ps = teta
#Rem     End Select
#Rem End Function
#Rem Private Function p2_hs(ByVal h As Double, ByVal s As Double) As Double
#Rem 'Supplementary Release on Backward Equations for Pressure as a Function of Enthalpy and Entropy p(h,s) to the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam
#Rem 'Chapter 6:Backward Equations p(h,s) for Region 2
#Rem   Dim sub_reg As Integer
#Rem   Dim i As Integer
#Rem   Dim eta, teta, sigma, p As Double
#Rem   Dim Ji, Ii, ni As Variant
#Rem
#Rem   If h < (-3498.98083432139 + 2575.60716905876 * s - 421.073558227969 * s ^ 2 + 27.6349063799944 * s ^ 3) Then
#Rem     sub_reg = 1
#Rem   Else
#Rem    If s < 5.85 Then
#Rem      sub_reg = 3
#Rem    Else
#Rem      sub_reg = 2
#Rem    End If
#Rem   End If
#Rem   Select Case sub_reg
#Rem   Case 1
#Rem     'Subregion A
#Rem     'Table 6, Eq 3, page 8
#Rem     Ii = Array(0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 5, 5, 6, 7)
#Rem     Ji = Array(1, 3, 6, 16, 20, 22, 0, 1, 2, 3, 5, 6, 10, 16, 20, 22, 3, 16, 20, 0, 2, 3, 6, 16, 16, 3, 16, 3, 1)
#Rem     ni = Array(-1.82575361923032E-02, -0.125229548799536, 0.592290437320145, 6.04769706185122, 238.624965444474, -298.639090222922, 0.051225081304075, -0.437266515606486, 0.413336902999504, -5.16468254574773, -5.57014838445711, 12.8555037824478, 11.414410895329, -119.504225652714, -2847.7798596156, 4317.57846408006, 1.1289404080265, 1974.09186206319, 1516.12444706087, 1.41324451421235E-02, 0.585501282219601, -2.97258075863012, 5.94567314847319, -6236.56565798905, 9659.86235133332, 6.81500934948134, -6332.07286824489, -5.5891922446576, 4.00645798472063E-02)
#Rem     eta = h / 4200
#Rem     sigma = s / 12
#Rem     p = 0
#Rem     For i = 0 To 28
#Rem       p = p + ni(i) * (eta - 0.5) ^ Ii(i) * (sigma - 1.2) ^ Ji(i)
#Rem     Next i
#Rem     p2_hs = p ^ 4 * 4
#Rem   Case 2
#Rem     'Subregion B
#Rem     'Table 7, Eq 4, page 9
#Rem     Ii = Array(0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 6, 6, 6, 7, 7, 8, 8, 8, 8, 12, 14)
#Rem     Ji = Array(0, 1, 2, 4, 8, 0, 1, 2, 3, 5, 12, 1, 6, 18, 0, 1, 7, 12, 1, 16, 1, 12, 1, 8, 18, 1, 16, 1, 3, 14, 18, 10, 16)
#Rem     ni = Array(8.01496989929495E-02, -0.543862807146111, 0.337455597421283, 8.9055545115745, 313.840736431485, 0.797367065977789, -1.2161697355624, 8.72803386937477, -16.9769781757602, -186.552827328416, 95115.9274344237, -18.9168510120494, -4334.0703719484, 543212633.012715, 0.144793408386013, 128.024559637516, -67230.9534071268, 33697238.0095287, -586.63419676272, -22140322476.9889, 1716.06668708389, -570817595.806302, -3121.09693178482, -2078413.8463301, 3056059461577.86, 3221.57004314333, 326810259797.295, -1441.04158934487, 410.694867802691, 109077066873.024, -24796465425889.3, 1888019068.65134, -123651009018773#)
#Rem     eta = h / 4100
#Rem     sigma = s / 7.9
#Rem     For i = 0 To 32
#Rem       p = p + ni(i) * (eta - 0.6) ^ Ii(i) * (sigma - 1.01) ^ Ji(i)
#Rem     Next i
#Rem     p2_hs = p ^ 4 * 100
#Rem   Case Else
#Rem     'Subregion C
#Rem     'Table 8, Eq 5, page 10
#Rem     Ii = Array(0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 10, 12, 16)
#Rem     Ji = Array(0, 1, 2, 3, 4, 8, 0, 2, 5, 8, 14, 2, 3, 7, 10, 18, 0, 5, 8, 16, 18, 18, 1, 4, 6, 14, 8, 18, 7, 7, 10)
#Rem     ni = Array(0.112225607199012, -3.39005953606712, -32.0503911730094, -197.5973051049, -407.693861553446, 13294.3775222331, 1.70846839774007, 37.3694198142245, 3581.44365815434, 423014.446424664, -751071025.760063, 52.3446127607898, -228.351290812417, -960652.417056937, -80705929.2526074, 1626980172256.69, 0.772465073604171, 46392.9973837746, -13731788.5134128, 1704703926305.12, -25110462818730.8, 31774883083552#, 53.8685623675312, -55308.9094625169, -1028615.22421405, 2042494187562.34, 273918446.626977, -2.63963146312685E+15, -1078908541.08088, -29649262098.0124, -1.11754907323424E+15)
#Rem     eta = h / 3500
#Rem     sigma = s / 5.9
#Rem     For i = 0 To 30
#Rem       p = p + ni(i) * (eta - 0.7) ^ Ii(i) * (sigma - 1.1) ^ Ji(i)
#Rem     Next i
#Rem     p2_hs = p ^ 4 * 100
#Rem   End Select
#Rem End Function
#Rem Private Function T2_prho(ByVal p As Double, ByVal rho As Double) As Double
#Rem   'Solve by iteration. Observe that fo low temperatures this equation has 2 solutions.
#Rem   'Solve with half interval method
#Rem   Dim Low_Bound, High_Bound, rhos, Ts As Double
#Rem
#Rem   If p < 16.5292 Then
#Rem     Low_Bound = T4_p(p)
#Rem   Else
#Rem     Low_Bound = B23T_p(p)
#Rem   End If
#Rem   High_Bound = 1073.15
#Rem   Do While Abs(rho - rhos) > 0.000001
#Rem     Ts = (Low_Bound + High_Bound) / 2
#Rem     rhos = 1 / v2_pT(p, Ts)
#Rem     If rhos < rho Then
#Rem       High_Bound = Ts
#Rem     Else
#Rem       Low_Bound = Ts
#Rem     End If
#Rem     Loop
#Rem     T2_prho = Ts
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*2.3 Functions for region 3
#Rem
#Rem Private Function p3_rhoT(ByVal rho As Double, ByVal T As Double) As Double
#Rem   'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem   '7 Basic Equation for Region 3, Section. 6.1 Basic Equation
#Rem   'Table 30 and 31, Page 30 and 31
#Rem   Dim i As Integer, Ji, Ii, ni As Variant, delta, tau, fidelta As Double
#Rem   Const R As Double = 0.461526, tc As Double = 647.096, pc As Double = 22.064, rhoc As Double = 322
#Rem   Ii = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9, 9, 10, 10, 11)
#Rem   Ji = Array(0, 0, 1, 2, 7, 10, 12, 23, 2, 6, 15, 17, 0, 2, 6, 7, 22, 26, 0, 2, 4, 16, 26, 0, 2, 4, 26, 1, 3, 26, 0, 2, 26, 2, 26, 2, 26, 0, 1, 26)
#Rem   ni = Array(1.0658070028513, -15.732845290239, 20.944396974307, -7.6867707878716, 2.6185947787954, -2.808078114862, 1.2053369696517, -8.4566812812502E-03, -1.2654315477714, -1.1524407806681, 0.88521043984318, -0.64207765181607, 0.38493460186671, -0.85214708824206, 4.8972281541877, -3.0502617256965, 0.039420536879154, 0.12558408424308, -0.2799932969871, 1.389979956946, -2.018991502357, -8.2147637173963E-03, -0.47596035734923, 0.0439840744735, -0.44476435428739, 0.90572070719733, 0.70522450087967, 0.10770512626332, -0.32913623258954, -0.50871062041158, -0.022175400873096, 0.094260751665092, 0.16436278447961, -0.013503372241348, -0.014834345352472, 5.7922953628084E-04, 3.2308904703711E-03, 8.0964802996215E-05, -1.6557679795037E-04, -4.4923899061815E-05)
#Rem   delta = rho / rhoc
#Rem   tau = tc / T
#Rem   fidelta = 0
#Rem   For i = 1 To 39
#Rem     fidelta = fidelta + ni(i) * Ii(i) * delta ^ (Ii(i) - 1) * tau ^ Ji(i)
#Rem   Next i
#Rem   fidelta = fidelta + ni(0) / delta
#Rem   p3_rhoT = rho * R * T * delta * fidelta / 1000
#Rem End Function
#Rem Private Function u3_rhoT(ByVal rho As Double, ByVal T As Double) As Double
#Rem   'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem   '7 Basic Equation for Region 3, Section. 6.1 Basic Equation
#Rem   'Table 30 and 31, Page 30 and 31
#Rem   Dim i As Integer, Ji, Ii, ni As Variant, delta, tau, fitau As Double
#Rem   Const R As Double = 0.461526, tc As Double = 647.096, pc As Double = 22.064, rhoc As Double = 322
#Rem   Ii = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9, 9, 10, 10, 11)
#Rem   Ji = Array(0, 0, 1, 2, 7, 10, 12, 23, 2, 6, 15, 17, 0, 2, 6, 7, 22, 26, 0, 2, 4, 16, 26, 0, 2, 4, 26, 1, 3, 26, 0, 2, 26, 2, 26, 2, 26, 0, 1, 26)
#Rem   ni = Array(1.0658070028513, -15.732845290239, 20.944396974307, -7.6867707878716, 2.6185947787954, -2.808078114862, 1.2053369696517, -8.4566812812502E-03, -1.2654315477714, -1.1524407806681, 0.88521043984318, -0.64207765181607, 0.38493460186671, -0.85214708824206, 4.8972281541877, -3.0502617256965, 0.039420536879154, 0.12558408424308, -0.2799932969871, 1.389979956946, -2.018991502357, -8.2147637173963E-03, -0.47596035734923, 0.0439840744735, -0.44476435428739, 0.90572070719733, 0.70522450087967, 0.10770512626332, -0.32913623258954, -0.50871062041158, -0.022175400873096, 0.094260751665092, 0.16436278447961, -0.013503372241348, -0.014834345352472, 5.7922953628084E-04, 3.2308904703711E-03, 8.0964802996215E-05, -1.6557679795037E-04, -4.4923899061815E-05)
#Rem   delta = rho / rhoc
#Rem   tau = tc / T
#Rem   fitau = 0
#Rem   For i = 1 To 39
#Rem     fitau = fitau + ni(i) * delta ^ Ii(i) * Ji(i) * tau ^ (Ji(i) - 1)
#Rem   Next i
#Rem   u3_rhoT = R * T * (tau * fitau)
#Rem End Function
#Rem
#Rem Private Function h3_rhoT(ByVal rho As Double, ByVal T As Double) As Double
#Rem   'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem   '7 Basic Equation for Region 3, Section. 6.1 Basic Equation
#Rem   'Table 30 and 31, Page 30 and 31
#Rem   Dim i As Integer, Ji, Ii, ni As Variant, delta, tau, fidelta, fitau As Double
#Rem   Const R As Double = 0.461526, tc As Double = 647.096, pc As Double = 22.064, rhoc As Double = 322
#Rem   Ii = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9, 9, 10, 10, 11)
#Rem   Ji = Array(0, 0, 1, 2, 7, 10, 12, 23, 2, 6, 15, 17, 0, 2, 6, 7, 22, 26, 0, 2, 4, 16, 26, 0, 2, 4, 26, 1, 3, 26, 0, 2, 26, 2, 26, 2, 26, 0, 1, 26)
#Rem   ni = Array(1.0658070028513, -15.732845290239, 20.944396974307, -7.6867707878716, 2.6185947787954, -2.808078114862, 1.2053369696517, -8.4566812812502E-03, -1.2654315477714, -1.1524407806681, 0.88521043984318, -0.64207765181607, 0.38493460186671, -0.85214708824206, 4.8972281541877, -3.0502617256965, 0.039420536879154, 0.12558408424308, -0.2799932969871, 1.389979956946, -2.018991502357, -8.2147637173963E-03, -0.47596035734923, 0.0439840744735, -0.44476435428739, 0.90572070719733, 0.70522450087967, 0.10770512626332, -0.32913623258954, -0.50871062041158, -0.022175400873096, 0.094260751665092, 0.16436278447961, -0.013503372241348, -0.014834345352472, 5.7922953628084E-04, 3.2308904703711E-03, 8.0964802996215E-05, -1.6557679795037E-04, -4.4923899061815E-05)
#Rem   delta = rho / rhoc
#Rem   tau = tc / T
#Rem   fidelta = 0
#Rem   fitau = 0
#Rem   For i = 1 To 39
#Rem     fidelta = fidelta + ni(i) * Ii(i) * delta ^ (Ii(i) - 1) * tau ^ Ji(i)
#Rem     fitau = fitau + ni(i) * delta ^ Ii(i) * Ji(i) * tau ^ (Ji(i) - 1)
#Rem   Next i
#Rem   fidelta = fidelta + ni(0) / delta
#Rem   h3_rhoT = R * T * (tau * fitau + delta * fidelta)
#Rem End Function
#Rem Private Function s3_rhoT(ByVal rho As Double, ByVal T As Double) As Double
#Rem   'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem   '7 Basic Equation for Region 3, Section. 6.1 Basic Equation
#Rem   'Table 30 and 31, Page 30 and 31
#Rem   Dim i As Integer, Ji, Ii, ni As Variant, fi, delta, tau, fitau As Double
#Rem   Const R As Double = 0.461526, tc As Double = 647.096, pc As Double = 22.064, rhoc As Double = 322
#Rem   Ii = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9, 9, 10, 10, 11)
#Rem   Ji = Array(0, 0, 1, 2, 7, 10, 12, 23, 2, 6, 15, 17, 0, 2, 6, 7, 22, 26, 0, 2, 4, 16, 26, 0, 2, 4, 26, 1, 3, 26, 0, 2, 26, 2, 26, 2, 26, 0, 1, 26)
#Rem   ni = Array(1.0658070028513, -15.732845290239, 20.944396974307, -7.6867707878716, 2.6185947787954, -2.808078114862, 1.2053369696517, -8.4566812812502E-03, -1.2654315477714, -1.1524407806681, 0.88521043984318, -0.64207765181607, 0.38493460186671, -0.85214708824206, 4.8972281541877, -3.0502617256965, 0.039420536879154, 0.12558408424308, -0.2799932969871, 1.389979956946, -2.018991502357, -8.2147637173963E-03, -0.47596035734923, 0.0439840744735, -0.44476435428739, 0.90572070719733, 0.70522450087967, 0.10770512626332, -0.32913623258954, -0.50871062041158, -0.022175400873096, 0.094260751665092, 0.16436278447961, -0.013503372241348, -0.014834345352472, 5.7922953628084E-04, 3.2308904703711E-03, 8.0964802996215E-05, -1.6557679795037E-04, -4.4923899061815E-05)
#Rem   delta = rho / rhoc
#Rem   tau = tc / T
#Rem   fi = 0
#Rem   fitau = 0
#Rem   For i = 1 To 39
#Rem     fi = fi + ni(i) * delta ^ Ii(i) * tau ^ Ji(i)
#Rem     fitau = fitau + ni(i) * delta ^ Ii(i) * Ji(i) * tau ^ (Ji(i) - 1)
#Rem   Next i
#Rem   fi = fi + ni(0) * Log(delta)
#Rem   s3_rhoT = R * (tau * fitau - fi)
#Rem End Function
#Rem Private Function Cp3_rhoT(ByVal rho As Double, ByVal T As Double) As Double
#Rem   'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem   '7 Basic Equation for Region 3, Section. 6.1 Basic Equation
#Rem   'Table 30 and 31, Page 30 and 31
#Rem   Dim i As Integer, Ji, Ii, ni As Variant, fideltatau, fi, delta, tau, fitautau, fidelta, fideltatautau, fideltadelta As Double
#Rem   Const R As Double = 0.461526, tc As Double = 647.096, pc As Double = 22.064, rhoc As Double = 322
#Rem   Ii = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9, 9, 10, 10, 11)
#Rem   Ji = Array(0, 0, 1, 2, 7, 10, 12, 23, 2, 6, 15, 17, 0, 2, 6, 7, 22, 26, 0, 2, 4, 16, 26, 0, 2, 4, 26, 1, 3, 26, 0, 2, 26, 2, 26, 2, 26, 0, 1, 26)
#Rem   ni = Array(1.0658070028513, -15.732845290239, 20.944396974307, -7.6867707878716, 2.6185947787954, -2.808078114862, 1.2053369696517, -8.4566812812502E-03, -1.2654315477714, -1.1524407806681, 0.88521043984318, -0.64207765181607, 0.38493460186671, -0.85214708824206, 4.8972281541877, -3.0502617256965, 0.039420536879154, 0.12558408424308, -0.2799932969871, 1.389979956946, -2.018991502357, -8.2147637173963E-03, -0.47596035734923, 0.0439840744735, -0.44476435428739, 0.90572070719733, 0.70522450087967, 0.10770512626332, -0.32913623258954, -0.50871062041158, -0.022175400873096, 0.094260751665092, 0.16436278447961, -0.013503372241348, -0.014834345352472, 5.7922953628084E-04, 3.2308904703711E-03, 8.0964802996215E-05, -1.6557679795037E-04, -4.4923899061815E-05)
#Rem   delta = rho / rhoc
#Rem   tau = tc / T
#Rem   fitautau = 0
#Rem   fidelta = 0
#Rem   fideltatau = 0
#Rem   fideltadelta = 0
#Rem   For i = 1 To 39
#Rem     fitautau = fitautau + ni(i) * delta ^ Ii(i) * Ji(i) * (Ji(i) - 1) * tau ^ (Ji(i) - 2)
#Rem     fidelta = fidelta + ni(i) * Ii(i) * delta ^ (Ii(i) - 1) * tau ^ Ji(i)
#Rem     fideltatau = fideltatau + ni(i) * Ii(i) * delta ^ (Ii(i) - 1) * Ji(i) * tau ^ (Ji(i) - 1)
#Rem     fideltadelta = fideltadelta + ni(i) * Ii(i) * (Ii(i) - 1) * delta ^ (Ii(i) - 2) * tau ^ Ji(i)
#Rem   Next i
#Rem   fidelta = fidelta + ni(0) / delta
#Rem   fideltadelta = fideltadelta - ni(0) / (delta ^ 2)
#Rem   Cp3_rhoT = R * (-(tau ^ 2 * fitautau) + (delta * fidelta - delta * tau * fideltatau) ^ 2 / (2 * delta * fidelta + delta ^ 2 * fideltadelta))
#Rem End Function
#Rem Private Function Cv3_rhoT(ByVal rho As Double, ByVal T As Double) As Double
#Rem   'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem   '7 Basic Equation for Region 3, Section. 6.1 Basic Equation
#Rem   'Table 30 and 31, Page 30 and 31
#Rem   Dim i As Integer, Ji, Ii, ni As Variant, fi, delta, tau, fitautau As Double
#Rem   Const R As Double = 0.461526, tc As Double = 647.096, pc As Double = 22.064, rhoc As Double = 322
#Rem   Ii = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9, 9, 10, 10, 11)
#Rem   Ji = Array(0, 0, 1, 2, 7, 10, 12, 23, 2, 6, 15, 17, 0, 2, 6, 7, 22, 26, 0, 2, 4, 16, 26, 0, 2, 4, 26, 1, 3, 26, 0, 2, 26, 2, 26, 2, 26, 0, 1, 26)
#Rem   ni = Array(1.0658070028513, -15.732845290239, 20.944396974307, -7.6867707878716, 2.6185947787954, -2.808078114862, 1.2053369696517, -8.4566812812502E-03, -1.2654315477714, -1.1524407806681, 0.88521043984318, -0.64207765181607, 0.38493460186671, -0.85214708824206, 4.8972281541877, -3.0502617256965, 0.039420536879154, 0.12558408424308, -0.2799932969871, 1.389979956946, -2.018991502357, -8.2147637173963E-03, -0.47596035734923, 0.0439840744735, -0.44476435428739, 0.90572070719733, 0.70522450087967, 0.10770512626332, -0.32913623258954, -0.50871062041158, -0.022175400873096, 0.094260751665092, 0.16436278447961, -0.013503372241348, -0.014834345352472, 5.7922953628084E-04, 3.2308904703711E-03, 8.0964802996215E-05, -1.6557679795037E-04, -4.4923899061815E-05)
#Rem   delta = rho / rhoc
#Rem   tau = tc / T
#Rem   fitautau = 0
#Rem   For i = 1 To 39
#Rem     fitautau = fitautau + ni(i) * delta ^ Ii(i) * Ji(i) * (Ji(i) - 1) * tau ^ (Ji(i) - 2)
#Rem   Next i
#Rem   Cv3_rhoT = R * -(tau * tau * fitautau)
#Rem End Function
#Rem Private Function w3_rhoT(ByVal rho As Double, ByVal T As Double) As Double
#Rem   'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem   '7 Basic Equation for Region 3, Section. 6.1 Basic Equation
#Rem   'Table 30 and 31, Page 30 and 31
#Rem   Dim i As Integer, Ji, Ii, ni As Variant, fi, delta, tau, fitautau, fidelta, fideltatau, fideltadelta As Double
#Rem   Const R As Double = 0.461526, tc As Double = 647.096, pc As Double = 22.064, rhoc As Double = 322
#Rem   Ii = Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9, 9, 10, 10, 11)
#Rem   Ji = Array(0, 0, 1, 2, 7, 10, 12, 23, 2, 6, 15, 17, 0, 2, 6, 7, 22, 26, 0, 2, 4, 16, 26, 0, 2, 4, 26, 1, 3, 26, 0, 2, 26, 2, 26, 2, 26, 0, 1, 26)
#Rem   ni = Array(1.0658070028513, -15.732845290239, 20.944396974307, -7.6867707878716, 2.6185947787954, -2.808078114862, 1.2053369696517, -8.4566812812502E-03, -1.2654315477714, -1.1524407806681, 0.88521043984318, -0.64207765181607, 0.38493460186671, -0.85214708824206, 4.8972281541877, -3.0502617256965, 0.039420536879154, 0.12558408424308, -0.2799932969871, 1.389979956946, -2.018991502357, -8.2147637173963E-03, -0.47596035734923, 0.0439840744735, -0.44476435428739, 0.90572070719733, 0.70522450087967, 0.10770512626332, -0.32913623258954, -0.50871062041158, -0.022175400873096, 0.094260751665092, 0.16436278447961, -0.013503372241348, -0.014834345352472, 5.7922953628084E-04, 3.2308904703711E-03, 8.0964802996215E-05, -1.6557679795037E-04, -4.4923899061815E-05)
#Rem   delta = rho / rhoc
#Rem   tau = tc / T
#Rem   fitautau = 0
#Rem   fidelta = 0
#Rem   fideltatau = 0
#Rem   fideltadelta = 0
#Rem   For i = 1 To 39
#Rem     fitautau = fitautau + ni(i) * delta ^ Ii(i) * Ji(i) * (Ji(i) - 1) * tau ^ (Ji(i) - 2)
#Rem     fidelta = fidelta + ni(i) * Ii(i) * delta ^ (Ii(i) - 1) * tau ^ Ji(i)
#Rem     fideltatau = fideltatau + ni(i) * Ii(i) * delta ^ (Ii(i) - 1) * Ji(i) * tau ^ (Ji(i) - 1)
#Rem     fideltadelta = fideltadelta + ni(i) * Ii(i) * (Ii(i) - 1) * delta ^ (Ii(i) - 2) * tau ^ Ji(i)
#Rem   Next i
#Rem   fidelta = fidelta + ni(0) / delta
#Rem   fideltadelta = fideltadelta - ni(0) / (delta ^ 2)
#Rem   w3_rhoT = (1000 * R * T * (2 * delta * fidelta + delta ^ 2 * fideltadelta - (delta * fidelta - delta * tau * fideltatau) ^ 2 / (tau ^ 2 * fitautau))) ^ 0.5
#Rem End Function
#Rem Private Function T3_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem 'Revised Supplementary Release on Backward Equations for the Functions T(p,h), v(p,h) and T(p,s), v(p,s) for Region 3 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam
#Rem '2004
#Rem 'Section 3.3 Backward Equations T(p,h) and v(p,h) for Subregions 3a and 3b
#Rem 'Boundary equation, Eq 1 Page 5
#Rem  Dim i As Integer, Ji, Ii, ni As Variant, h3ab, ps, hs, Ts As Double
#Rem  Const R As Double = 0.461526, tc As Double = 647.096, pc As Double = 22.064, rhoc As Double = 322
#Rem  h3ab = (2014.64004206875 + 3.74696550136983 * p - 2.19921901054187E-02 * p ^ 2 + 8.7513168600995E-05 * p ^ 3)
#Rem   If h < h3ab Then
#Rem     'Subregion 3a
#Rem     'Eq 2, Table 3, Page 7
#Rem     Ii = Array(-12, -12, -12, -12, -12, -12, -12, -12, -10, -10, -10, -8, -8, -8, -8, -5, -3, -2, -2, -2, -1, -1, 0, 0, 1, 3, 3, 4, 4, 10, 12)
#Rem     Ji = Array(0, 1, 2, 6, 14, 16, 20, 22, 1, 5, 12, 0, 2, 4, 10, 2, 0, 1, 3, 4, 0, 2, 0, 1, 1, 0, 1, 0, 3, 4, 5)
#Rem     ni = Array(-1.33645667811215E-07, 4.55912656802978E-06, -1.46294640700979E-05, 6.3934131297008E-03, 372.783927268847, -7186.54377460447, 573494.7521034, -2675693.29111439, -3.34066283302614E-05, -2.45479214069597E-02, 47.8087847764996, 7.64664131818904E-06, 1.28350627676972E-03, 1.71219081377331E-02, -8.51007304583213, -1.36513461629781E-02, -3.84460997596657E-06, 3.37423807911655E-03, -0.551624873066791, 0.72920227710747, -9.92522757376041E-03, -0.119308831407288, 0.793929190615421, 0.454270731799386, 0.20999859125991, -6.42109823904738E-03, -0.023515586860454, 2.52233108341612E-03, -7.64885133368119E-03, 1.36176427574291E-02, -1.33027883575669E-02)
#Rem     ps = p / 100
#Rem     hs = h / 2300
#Rem     Ts = 0
#Rem     For i = 0 To 30
#Rem       Ts = Ts + ni(i) * (ps + 0.24) ^ Ii(i) * (hs - 0.615) ^ Ji(i)
#Rem     Next i
#Rem     T3_ph = Ts * 760
#Rem   Else
#Rem     'Subregion 3b
#Rem     'Eq 3, Table 4, Page 7,8
#Rem     Ii = Array(-12, -12, -10, -10, -10, -10, -10, -8, -8, -8, -8, -8, -6, -6, -6, -4, -4, -3, -2, -2, -1, -1, -1, -1, -1, -1, 0, 0, 1, 3, 5, 6, 8)
#Rem     Ji = Array(0, 1, 0, 1, 5, 10, 12, 0, 1, 2, 4, 10, 0, 1, 2, 0, 1, 5, 0, 4, 2, 4, 6, 10, 14, 16, 0, 2, 1, 1, 1, 1, 1)
#Rem     ni = Array(3.2325457364492E-05, -1.27575556587181E-04, -4.75851877356068E-04, 1.56183014181602E-03, 0.105724860113781, -85.8514221132534, 724.140095480911, 2.96475810273257E-03, -5.92721983365988E-03, -1.26305422818666E-02, -0.115716196364853, 84.9000969739595, -1.08602260086615E-02, 1.54304475328851E-02, 7.50455441524466E-02, 2.52520973612982E-02, -6.02507901232996E-02, -3.07622221350501, -5.74011959864879E-02, 5.03471360939849, -0.925081888584834, 3.91733882917546, -77.314600713019, 9493.08762098587, -1410437.19679409, 8491662.30819026, 0.861095729446704, 0.32334644281172, 0.873281936020439, -0.436653048526683, 0.286596714529479, -0.131778331276228, 6.76682064330275E-03)
#Rem     hs = h / 2800
#Rem     ps = p / 100
#Rem     Ts = 0
#Rem     For i = 0 To 32
#Rem       Ts = Ts + ni(i) * (ps + 0.298) ^ Ii(i) * (hs - 0.72) ^ Ji(i)
#Rem     Next i
#Rem     T3_ph = Ts * 860
#Rem   End If
#Rem End Function
#Rem Private Function v3_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem 'Revised Supplementary Release on Backward Equations for the Functions T(p,h), v(p,h) and T(p,s), v(p,s) for Region 3 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam
#Rem '2004
#Rem 'Section 3.3 Backward Equations T(p,h) and v(p,h) for Subregions 3a and 3b
#Rem 'Boundary equation, Eq 1 Page 5
#Rem  Dim i As Integer, Ji, Ii, ni As Variant, h3ab, ps, hs, vs As Double
#Rem  Const R As Double = 0.461526, tc As Double = 647.096, pc As Double = 22.064, rhoc As Double = 322
#Rem   h3ab = (2014.64004206875 + 3.74696550136983 * p - 2.19921901054187E-02 * p ^ 2 + 8.7513168600995E-05 * p ^ 3)
#Rem   If h < h3ab Then
#Rem     'Subregion 3a
#Rem     'Eq 4, Table 6, Page 9
#Rem     Ii = Array(-12, -12, -12, -12, -10, -10, -10, -8, -8, -6, -6, -6, -4, -4, -3, -2, -2, -1, -1, -1, -1, 0, 0, 1, 1, 1, 2, 2, 3, 4, 5, 8)
#Rem     Ji = Array(6, 8, 12, 18, 4, 7, 10, 5, 12, 3, 4, 22, 2, 3, 7, 3, 16, 0, 1, 2, 3, 0, 1, 0, 1, 2, 0, 2, 0, 2, 2, 2)
#Rem     ni = Array(5.29944062966028E-03, -0.170099690234461, 11.1323814312927, -2178.98123145125, -5.06061827980875E-04, 0.556495239685324, -9.43672726094016, -0.297856807561527, 93.9353943717186, 1.92944939465981E-02, 0.421740664704763, -3689141.2628233, -7.37566847600639E-03, -0.354753242424366, -1.99768169338727, 1.15456297059049, 5683.6687581596, 8.08169540124668E-03, 0.172416341519307, 1.04270175292927, -0.297691372792847, 0.560394465163593, 0.275234661176914, -0.148347894866012, -6.51142513478515E-02, -2.92468715386302, 6.64876096952665E-02, 3.52335014263844, -1.46340792313332E-02, -2.24503486668184, 1.10533464706142, -4.08757344495612E-02)
#Rem     ps = p / 100
#Rem     hs = h / 2100
#Rem     vs = 0
#Rem     For i = 0 To 31
#Rem       vs = vs + ni(i) * (ps + 0.128) ^ Ii(i) * (hs - 0.727) ^ Ji(i)
#Rem     Next i
#Rem     v3_ph = vs * 0.0028
#Rem   Else
#Rem     'Subregion 3b
#Rem     'Eq 5, Table 7, Page 9
#Rem     Ii = Array(-12, -12, -8, -8, -8, -8, -8, -8, -6, -6, -6, -6, -6, -6, -4, -4, -4, -3, -3, -2, -2, -1, -1, -1, -1, 0, 1, 1, 2, 2)
#Rem     Ji = Array(0, 1, 0, 1, 3, 6, 7, 8, 0, 1, 2, 5, 6, 10, 3, 6, 10, 0, 2, 1, 2, 0, 1, 4, 5, 0, 0, 1, 2, 6)
#Rem     ni = Array(-2.25196934336318E-09, 1.40674363313486E-08, 2.3378408528056E-06, -3.31833715229001E-05, 1.07956778514318E-03, -0.271382067378863, 1.07202262490333, -0.853821329075382, -2.15214194340526E-05, 7.6965608822273E-04, -4.31136580433864E-03, 0.453342167309331, -0.507749535873652, -100.475154528389, -0.219201924648793, -3.21087965668917, 607.567815637771, 5.57686450685932E-04, 0.18749904002955, 9.05368030448107E-03, 0.285417173048685, 3.29924030996098E-02, 0.239897419685483, 4.82754995951394, -11.8035753702231, 0.169490044091791, -1.79967222507787E-02, 3.71810116332674E-02, -5.36288335065096E-02, 1.6069710109252)
#Rem     ps = p / 100
#Rem     hs = h / 2800
#Rem     vs = 0
#Rem     For i = 0 To 29
#Rem       vs = vs + ni(i) * (ps + 0.0661) ^ Ii(i) * (hs - 0.72) ^ Ji(i)
#Rem     Next i
#Rem     v3_ph = vs * 0.0088
#Rem   End If
#Rem End Function
#Rem Private Function T3_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem 'Revised Supplementary Release on Backward Equations for the Functions T(p,h), v(p,h) and T(p,s), v(p,s) for Region 3 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam
#Rem '2004
#Rem '3.4 Backward Equations T(p,s) and v(p,s) for Subregions 3a and 3b
#Rem 'Boundary equation, Eq 6 Page 11
#Rem  Dim i As Integer, Ji, Ii, ni As Variant, ps, sigma, teta As Double
#Rem  Const R As Double = 0.461526, tc As Double = 647.096, pc As Double = 22.064, rhoc As Double = 322
#Rem
#Rem   If s <= 4.41202148223476 Then
#Rem     'Subregion 3a
#Rem     'Eq 6, Table 10, Page 11
#Rem     Ii = Array(-12, -12, -10, -10, -10, -10, -8, -8, -8, -8, -6, -6, -6, -5, -5, -5, -4, -4, -4, -2, -2, -1, -1, 0, 0, 0, 1, 2, 2, 3, 8, 8, 10)
#Rem     Ji = Array(28, 32, 4, 10, 12, 14, 5, 7, 8, 28, 2, 6, 32, 0, 14, 32, 6, 10, 36, 1, 4, 1, 6, 0, 1, 4, 0, 0, 3, 2, 0, 1, 2)
#Rem     ni = Array(1500420082.63875, -159397258480.424, 5.02181140217975E-04, -67.2057767855466, 1450.58545404456, -8238.8953488889, -0.154852214233853, 11.2305046746695, -29.7000213482822, 43856513263.5495, 1.37837838635464E-03, -2.97478527157462, 9717779473494.13, -5.71527767052398E-05, 28830.794977842, -74442828926270.3, 12.8017324848921, -368.275545889071, 6.64768904779177E+15, 0.044935925195888, -4.22897836099655, -0.240614376434179, -4.74341365254924, 0.72409399912611, 0.923874349695897, 3.99043655281015, 3.84066651868009E-02, -3.59344365571848E-03, -0.735196448821653, 0.188367048396131, 1.41064266818704E-04, -2.57418501496337E-03, 1.23220024851555E-03)
#Rem     sigma = s / 4.4
#Rem     ps = p / 100
#Rem     teta = 0
#Rem     For i = 0 To 32
#Rem       teta = teta + ni(i) * (ps + 0.24) ^ Ii(i) * (sigma - 0.703) ^ Ji(i)
#Rem     Next i
#Rem     T3_ps = teta * 760
#Rem   Else
#Rem     'Subregion 3b
#Rem     'Eq 7, Table 11, Page 11
#Rem     Ii = Array(-12, -12, -12, -12, -8, -8, -8, -6, -6, -6, -5, -5, -5, -5, -5, -4, -3, -3, -2, 0, 2, 3, 4, 5, 6, 8, 12, 14)
#Rem     Ji = Array(1, 3, 4, 7, 0, 1, 3, 0, 2, 4, 0, 1, 2, 4, 6, 12, 1, 6, 2, 0, 1, 1, 0, 24, 0, 3, 1, 2)
#Rem     ni = Array(0.52711170160166, -40.1317830052742, 153.020073134484, -2247.99398218827, -0.193993484669048, -1.40467557893768, 42.6799878114024, 0.752810643416743, 22.6657238616417, -622.873556909932, -0.660823667935396, 0.841267087271658, -25.3717501764397, 485.708963532948, 880.531517490555, 2650155.92794626, -0.359287150025783, -656.991567673753, 2.41768149185367, 0.856873461222588, 0.655143675313458, -0.213535213206406, 5.62974957606348E-03, -316955725450471#, -6.99997000152457E-04, 1.19845803210767E-02, 1.93848122022095E-05, -2.15095749182309E-05)
#Rem     sigma = s / 5.3
#Rem     ps = p / 100
#Rem     teta = 0
#Rem     For i = 0 To 27
#Rem       teta = teta + ni(i) * (ps + 0.76) ^ Ii(i) * (sigma - 0.818) ^ Ji(i)
#Rem     Next i
#Rem     T3_ps = teta * 860
#Rem   End If
#Rem End Function
#Rem Private Function v3_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem 'Revised Supplementary Release on Backward Equations for the Functions T(p,h), v(p,h) and T(p,s), v(p,s) for Region 3 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam
#Rem '2004
#Rem '3.4 Backward Equations T(p,s) and v(p,s) for Subregions 3a and 3b
#Rem 'Boundary equation, Eq 6 Page 11
#Rem  Dim i As Integer, Ji, Ii, ni As Variant, ps, sigma, omega As Double
#Rem  Const R As Double = 0.461526, tc As Double = 647.096, pc As Double = 22.064, rhoc As Double = 322
#Rem   If s <= 4.41202148223476 Then
#Rem     'Subregion 3a
#Rem     'Eq 8, Table 13, Page 14
#Rem     Ii = Array(-12, -12, -12, -10, -10, -10, -10, -8, -8, -8, -8, -6, -5, -4, -3, -3, -2, -2, -1, -1, 0, 0, 0, 1, 2, 4, 5, 6)
#Rem     Ji = Array(10, 12, 14, 4, 8, 10, 20, 5, 6, 14, 16, 28, 1, 5, 2, 4, 3, 8, 1, 2, 0, 1, 3, 0, 0, 2, 2, 0)
#Rem     ni = Array(79.5544074093975, -2382.6124298459, 17681.3100617787, -1.10524727080379E-03, -15.3213833655326, 297.544599376982, -35031520.6871242, 0.277513761062119, -0.523964271036888, -148011.182995403, 1600148.99374266, 1708023226634.27, 2.46866996006494E-04, 1.6532608479798, -0.118008384666987, 2.537986423559, 0.965127704669424, -28.2172420532826, 0.203224612353823, 1.10648186063513, 0.52612794845128, 0.277000018736321, 1.08153340501132, -7.44127885357893E-02, 1.64094443541384E-02, -6.80468275301065E-02, 0.025798857610164, -1.45749861944416E-04)
#Rem     ps = p / 100
#Rem     sigma = s / 4.4
#Rem     omega = 0
#Rem     For i = 0 To 27
#Rem       omega = omega + ni(i) * (ps + 0.187) ^ Ii(i) * (sigma - 0.755) ^ Ji(i)
#Rem     Next i
#Rem     v3_ps = omega * 0.0028
#Rem   Else
#Rem     'Subregion 3b
#Rem     'Eq 9, Table 14, Page 14
#Rem     Ii = Array(-12, -12, -12, -12, -12, -12, -10, -10, -10, -10, -8, -5, -5, -5, -4, -4, -4, -4, -3, -2, -2, -2, -2, -2, -2, 0, 0, 0, 1, 1, 2)
#Rem     Ji = Array(0, 1, 2, 3, 5, 6, 0, 1, 2, 4, 0, 1, 2, 3, 0, 1, 2, 3, 1, 0, 1, 2, 3, 4, 12, 0, 1, 2, 0, 2, 2)
#Rem     ni = Array(5.91599780322238E-05, -1.85465997137856E-03, 1.04190510480013E-02, 5.9864730203859E-03, -0.771391189901699, 1.72549765557036, -4.67076079846526E-04, 1.34533823384439E-02, -8.08094336805495E-02, 0.508139374365767, 1.28584643361683E-03, -1.63899353915435, 5.86938199318063, -2.92466667918613, -6.14076301499537E-03, 5.76199014049172, -12.1613320606788, 1.67637540957944, -7.44135838773463, 3.78168091437659E-02, 4.01432203027688, 16.0279837479185, 3.17848779347728, -3.58362310304853, -1159952.60446827, 0.199256573577909, -0.122270624794624, -19.1449143716586, -1.50448002905284E-02, 14.6407900162154, -3.2747778718823)
#Rem     ps = p / 100
#Rem     sigma = s / 5.3
#Rem     omega = 0
#Rem     For i = 0 To 30
#Rem       omega = omega + ni(i) * (ps + 0.298) ^ Ii(i) * (sigma - 0.816) ^ Ji(i)
#Rem    Next i
#Rem    v3_ps = omega * 0.0088
#Rem   End If
#Rem End Function
#Rem
#Rem Private Function p3_hs(ByVal h As Double, ByVal s As Double) As Double
#Rem 'Supplementary Release on Backward Equations ( ) , p h s for Region 3,
#Rem 'Equations as a Function of h and s for the Region Boundaries, and an Equation
#Rem '( ) sat , T hs for Region 4 of the IAPWS Industrial Formulation 1997 for the
#Rem 'Thermodynamic Properties of Water and Steam
#Rem '2004
#Rem 'Section 3 Backward Functions p(h,s), T(h,s), and v(h,s) for Region 3
#Rem  Dim i As Integer, Ji, Ii, ni As Variant, ps, sigma, eta As Double
#Rem  Const R As Double = 0.461526, tc As Double = 647.096, pc As Double = 22.064, rhoc As Double = 322
#Rem   If s < 4.41202148223476 Then
#Rem     'Subregion 3a
#Rem     'Eq 1, Table 3, Page 8
#Rem     Ii = Array(0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 6, 7, 8, 10, 10, 14, 18, 20, 22, 22, 24, 28, 28, 32, 32)
#Rem     Ji = Array(0, 1, 5, 0, 3, 4, 8, 14, 6, 16, 0, 2, 3, 0, 1, 4, 5, 28, 28, 24, 1, 32, 36, 22, 28, 36, 16, 28, 36, 16, 36, 10, 28)
#Rem     ni = Array(7.70889828326934, -26.0835009128688, 267.416218930389, 17.2221089496844, -293.54233214597, 614.135601882478, -61056.2757725674, -65127225.1118219, 73591.9313521937, -11664650591.4191, 35.5267086434461, -596.144543825955, -475.842430145708, 69.6781965359503, 335.674250377312, 25052.6809130882, 146997.380630766, 5.38069315091534E+19, 1.43619827291346E+21, 3.64985866165994E+19, -2547.41561156775, 2.40120197096563E+27, -3.93847464679496E+29, 1.47073407024852E+24, -4.26391250432059E+31, 1.94509340621077E+38, 6.66212132114896E+23, 7.06777016552858E+33, 1.75563621975576E+41, 1.08408607429124E+28, 7.30872705175151E+43, 1.5914584739887E+24, 3.77121605943324E+40)
#Rem     sigma = s / 4.4
#Rem     eta = h / 2300
#Rem     ps = 0
#Rem     For i = 0 To 32
#Rem       ps = ps + ni(i) * (eta - 1.01) ^ Ii(i) * (sigma - 0.75) ^ Ji(i)
#Rem     Next i
#Rem     p3_hs = ps * 99
#Rem   Else
#Rem     'Subregion 3b
#Rem     'Eq 2, Table 4, Page 8
#Rem     Ii = Array(-12, -12, -12, -12, -12, -10, -10, -10, -10, -8, -8, -6, -6, -6, -6, -5, -4, -4, -4, -3, -3, -3, -3, -2, -2, -1, 0, 2, 2, 5, 6, 8, 10, 14, 14)
#Rem     Ji = Array(2, 10, 12, 14, 20, 2, 10, 14, 18, 2, 8, 2, 6, 7, 8, 10, 4, 5, 8, 1, 3, 5, 6, 0, 1, 0, 3, 0, 1, 0, 1, 1, 1, 3, 7)
#Rem     ni = Array(1.25244360717979E-13, -1.26599322553713E-02, 5.06878030140626, 31.7847171154202, -391041.161399932, -9.75733406392044E-11, -18.6312419488279, 510.973543414101, 373847.005822362, 2.99804024666572E-08, 20.0544393820342, -4.98030487662829E-06, -10.230180636003, 55.2819126990325, -206.211367510878, -7940.12232324823, 7.82248472028153, -58.6544326902468, 3550.73647696481, -1.15303107290162E-04, -1.75092403171802, 257.98168774816, -727.048374179467, 1.21644822609198E-04, 3.93137871762692E-02, 7.04181005909296E-03, -82.910820069811, -0.26517881813125, 13.7531682453991, -52.2394090753046, 2405.56298941048, -22736.1631268929, 89074.6343932567, -23923456.5822486, 5687958081.29714)
#Rem     sigma = s / 5.3
#Rem     eta = h / 2800
#Rem     ps = 0
#Rem     For i = 0 To 34
#Rem       ps = ps + ni(i) * (eta - 0.681) ^ Ii(i) * (sigma - 0.792) ^ Ji(i)
#Rem     Next i
#Rem     p3_hs = 16.6 / ps
#Rem   End If
#Rem End Function
#Rem Private Function h3_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem    'Not avalible with IF 97
#Rem    'Solve function T3_ph-T=0 with half interval method.
#Rem    Dim Ts, Low_Bound, High_Bound, hs As Double
#Rem    Ts = T + 1
#Rem    Low_Bound = h1_pT(p, 623.15)
#Rem    High_Bound = h2_pT(p, B23T_p(p))
#Rem    Do While Abs(T - Ts) > 0.00001
#Rem     hs = (Low_Bound + High_Bound) / 2
#Rem     Ts = T3_ph(p, hs)
#Rem     If Ts > T Then
#Rem       High_Bound = hs
#Rem     Else
#Rem       Low_Bound = hs
#Rem     End If
#Rem    Loop
#Rem    h3_pT = hs
#Rem End Function
#Rem Private Function T3_prho(ByVal p As Double, ByVal rho As Double)
#Rem   'Solve by iteration. Observe that fo low temperatures this equation has 2 solutions.
#Rem   'Solve with half interval method
#Rem   Dim ps, Low_Bound, High_Bound, Ts As Double
#Rem   Low_Bound = 623.15
#Rem   High_Bound = 1073.15
#Rem   Do While Abs(p - ps) > 0.00000001
#Rem     Ts = (Low_Bound + High_Bound) / 2
#Rem     ps = p3_rhoT(rho, Ts)
#Rem     If ps > p Then
#Rem       High_Bound = Ts
#Rem     Else
#Rem       Low_Bound = Ts
#Rem     End If
#Rem     Loop
#Rem     T3_prho = Ts
#Rem End Function
#Rem
#Rem '***********************************************************************************************************
#Rem '*2.4 Functions for region 4
#Rem Private Function p4_T(ByVal T As Double) As Double
#Rem   'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem   'Section 8.1 The Saturation-Pressure Equation
#Rem   'Eq 30, Page 33
#Rem   Dim teta, a, b, c As Double
#Rem   teta = T - 0.23855557567849 / (T - 650.17534844798)
#Rem   a = teta ^ 2 + 1167.0521452767 * teta - 724213.16703206
#Rem   b = -17.073846940092 * teta ^ 2 + 12020.82470247 * teta - 3232555.0322333
#Rem   c = 14.91510861353 * teta ^ 2 - 4823.2657361591 * teta + 405113.40542057
#Rem   p4_T = (2 * c / (-b + (b ^ 2 - 4 * a * c) ^ 0.5)) ^ 4
#Rem End Function
def T4_p(p):
    ''' Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    Section 8.2 The Saturation-Temperature Equation
    Eq 31, Page 34 '''

    beta = p**0.25
    e = beta**2 - 17.073846940092*beta + 14.91510861353
    f = 1167.0521452767*beta**2 + 12020.82470247*beta - 4823.2657361591
    g = -724213.16703206*beta**2 - 3232555.0322333*beta + 405113.40542057
    d = 2*g/(-f - (f**2 - 4*e*g)**0.5)
    return (650.17534844798 + d - ((650.17534844798 + d)**2 - 4*(-0.23855557567849 + 650.17534844798*d))**0.5)/2

#Rem Private Function h4_s(ByVal s As Double) As Double
#Rem 'Supplementary Release on Backward Equations ( ) , p h s for Region 3,Equations as a Function of h and s for the Region Boundaries, and an Equation( ) sat , T hs for Region 4 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam
#Rem '4 Equations for Region Boundaries Given Enthalpy and Entropy
#Rem ' Se picture page 14
#Rem Dim Ii, Ji, ni As Variant, eta, sigma, sigma1, sigma2 As Double, i As Integer
#Rem   If s > -0.0001545495919 And s <= 3.77828134 Then
#Rem     'hL1_s
#Rem     'Eq 3,Table 9,Page 16
#Rem     Ii = Array(0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 7, 8, 12, 12, 14, 14, 16, 20, 20, 22, 24, 28, 32, 32)
#Rem     Ji = Array(14, 36, 3, 16, 0, 5, 4, 36, 4, 16, 24, 18, 24, 1, 4, 2, 4, 1, 22, 10, 12, 28, 8, 3, 0, 6, 8)
#Rem     ni = Array(0.332171191705237, 6.11217706323496E-04, -8.82092478906822, -0.45562819254325, -2.63483840850452E-05, -22.3949661148062, -4.28398660164013, -0.616679338856916, -14.682303110404, 284.523138727299, -113.398503195444, 1156.71380760859, 395.551267359325, -1.54891257229285, 19.4486637751291, -3.57915139457043, -3.35369414148819, -0.66442679633246, 32332.1885383934, 3317.66744667084, -22350.1257931087, 5739538.75852936, 173.226193407919, -3.63968822121321E-02, 8.34596332878346E-07, 5.03611916682674, 65.5444787064505)
#Rem     sigma = s / 3.8
#Rem     eta = 0
#Rem     For i = 0 To 26
#Rem       eta = eta + ni(i) * (sigma - 1.09) ^ Ii(i) * (sigma + 0.0000366) ^ Ji(i)
#Rem     Next i
#Rem     h4_s = eta * 1700
#Rem   ElseIf s > 3.77828134 And s <= 4.41202148223476 Then
#Rem     'hL3_s
#Rem     'Eq 4,Table 10,Page 16
#Rem     Ii = Array(0, 0, 0, 0, 2, 3, 4, 4, 5, 5, 6, 7, 7, 7, 10, 10, 10, 32, 32)
#Rem     Ji = Array(1, 4, 10, 16, 1, 36, 3, 16, 20, 36, 4, 2, 28, 32, 14, 32, 36, 0, 6)
#Rem     ni = Array(0.822673364673336, 0.181977213534479, -0.011200026031362, -7.46778287048033E-04, -0.179046263257381, 4.24220110836657E-02, -0.341355823438768, -2.09881740853565, -8.22477343323596, -4.99684082076008, 0.191413958471069, 5.81062241093136E-02, -1655.05498701029, 1588.70443421201, -85.0623535172818, -31771.4386511207, -94589.0406632871, -1.3927384708869E-06, 0.63105253224098)
#Rem     sigma = s / 3.8
#Rem     eta = 0
#Rem     For i = 0 To 18
#Rem       eta = eta + ni(i) * (sigma - 1.09) ^ Ii(i) * (sigma + 0.0000366) ^ Ji(i)
#Rem     Next i
#Rem     h4_s = eta * 1700
#Rem   ElseIf s > 4.41202148223476 And s <= 5.85 Then
#Rem     'Section 4.4 Equations ( ) 2ab " h s and ( ) 2c3b "h s for the Saturated Vapor Line
#Rem     'Page 19, Eq 5
#Rem     'hV2c3b_s(s)
#Rem     Ii = Array(0, 0, 0, 1, 1, 5, 6, 7, 8, 8, 12, 16, 22, 22, 24, 36)
#Rem     Ji = Array(0, 3, 4, 0, 12, 36, 12, 16, 2, 20, 32, 36, 2, 32, 7, 20)
#Rem     ni = Array(1.04351280732769, -2.27807912708513, 1.80535256723202, 0.420440834792042, -105721.24483466, 4.36911607493884E+24, -328032702839.753, -6.7868676080427E+15, 7439.57464645363, -3.56896445355761E+19, 1.67590585186801E+31, -3.55028625419105E+37, 396611982166.538, -4.14716268484468E+40, 3.59080103867382E+18, -1.16994334851995E+40)
#Rem     sigma = s / 5.9
#Rem     eta = 0
#Rem     For i = 0 To 15
#Rem       eta = eta + ni(i) * (sigma - 1.02) ^ Ii(i) * (sigma - 0.726) ^ Ji(i)
#Rem     Next i
#Rem     h4_s = eta ^ 4 * 2800
#Rem   ElseIf s > 5.85 And s < 9.155759395 Then
#Rem     'Section 4.4 Equations ( ) 2ab " h s and ( ) 2c3b "h s for the Saturated Vapor Line
#Rem     'Page 20, Eq 6
#Rem     Ii = Array(1, 1, 2, 2, 4, 4, 7, 8, 8, 10, 12, 12, 18, 20, 24, 28, 28, 28, 28, 28, 32, 32, 32, 32, 32, 36, 36, 36, 36, 36)
#Rem     Ji = Array(8, 24, 4, 32, 1, 2, 7, 5, 12, 1, 0, 7, 10, 12, 32, 8, 12, 20, 22, 24, 2, 7, 12, 14, 24, 10, 12, 20, 22, 28)
#Rem     ni = Array(-524.581170928788, -9269472.18142218, -237.385107491666, 21077015581.2776, -23.9494562010986, 221.802480294197, -5104725.33393438, 1249813.96109147, 2000084369.96201, -815.158509791035, -157.612685637523, -11420042233.2791, 6.62364680776872E+15, -2.27622818296144E+18, -1.71048081348406E+31, 6.60788766938091E+15, 1.66320055886021E+22, -2.18003784381501E+29, -7.87276140295618E+29, 1.51062329700346E+31, 7957321.70300541, 1.31957647355347E+15, -3.2509706829914E+23, -4.18600611419248E+25, 2.97478906557467E+34, -9.53588761745473E+19, 1.66957699620939E+24, -1.75407764869978E+32, 3.47581490626396E+34, -7.10971318427851E+38)
#Rem     sigma1 = s / 5.21
#Rem     sigma2 = s / 9.2
#Rem     eta = 0
#Rem     For i = 0 To 29
#Rem       eta = eta + ni(i) * (1 / sigma1 - 0.513) ^ Ii(i) * (sigma2 - 0.524) ^ Ji(i)
#Rem     Next i
#Rem     h4_s = Exp(eta) * 2800
#Rem   Else
#Rem     h4_s = CVErr(xlErrValue)
#Rem   End If
#Rem End Function
#Rem Private Function p4_s(ByVal s As Double) As Double
#Rem   'Uses h4_s and p_hs for the diffrent regions to determine p4_s
#Rem   Dim hsat As Double
#Rem   hsat = h4_s(s)
#Rem   If s > -0.0001545495919 And s <= 3.77828134 Then
#Rem     p4_s = p1_hs(hsat, s)
#Rem   ElseIf s > 3.77828134 And s <= 5.210887663 Then
#Rem     p4_s = p3_hs(hsat, s)
#Rem   ElseIf s > 5.210887663 And s < 9.155759395 Then
#Rem     p4_s = p2_hs(hsat, s)
#Rem   Else
#Rem     p4_s = CVErr(xlErrValue)
#Rem   End If
#Rem End Function
#Rem Private Function h4L_p(ByVal p As Double) As Double
#Rem  Dim Low_Bound, High_Bound, hs, ps, Ts As Double
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   Ts = T4_p(p)
#Rem   If p < 16.529 Then
#Rem     h4L_p = h1_pT(p, Ts)
#Rem   Else
#Rem     'Iterate to find the the backward solution of p3sat_h
#Rem     Low_Bound = 1670.858218
#Rem     High_Bound = 2087.23500164864
#Rem     Do While Abs(p - ps) > 0.00001
#Rem       hs = (Low_Bound + High_Bound) / 2
#Rem       ps = p3sat_h(hs)
#Rem       If ps > p Then
#Rem         High_Bound = hs
#Rem       Else
#Rem         Low_Bound = hs
#Rem       End If
#Rem     Loop
#Rem
#Rem     h4L_p = hs
#Rem   End If
#Rem  Else
#Rem   h4L_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Private Function h4V_p(ByVal p As Double) As Double
#Rem  Dim Low_Bound, High_Bound, hs, ps, Ts As Double
#Rem  If p > 0.000611657 And p < 22.06395 Then
#Rem   Ts = T4_p(p)
#Rem   If p < 16.529 Then
#Rem     h4V_p = h2_pT(p, Ts)
#Rem   Else
#Rem     'Iterate to find the the backward solution of p3sat_h
#Rem     Low_Bound = 2087.23500164864
#Rem     High_Bound = 2563.592004 + 5 '5 added to extrapolate to ensure even the border ==350°C solved.
#Rem     Do While Abs(p - ps) > 0.000001
#Rem       hs = (Low_Bound + High_Bound) / 2
#Rem       ps = p3sat_h(hs)
#Rem       If ps < p Then
#Rem         High_Bound = hs
#Rem       Else
#Rem         Low_Bound = hs
#Rem       End If
#Rem     Loop
#Rem     h4V_p = hs
#Rem   End If
#Rem  Else
#Rem   h4V_p = CVErr(xlErrValue)
#Rem  End If
#Rem End Function
#Rem Private Function x4_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem 'Calculate vapour fraction from hL and hV for given p
#Rem  Dim h4v, h4l As Double
#Rem   h4v = h4V_p(p)
#Rem   h4l = h4L_p(p)
#Rem   If h > h4v Then
#Rem     x4_ph = 1
#Rem   ElseIf h < h4l Then
#Rem     x4_ph = 0
#Rem   Else
#Rem     x4_ph = (h - h4l) / (h4v - h4l)
#Rem   End If
#Rem End Function
#Rem Private Function x4_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem  Dim ssV, ssL As Double
#Rem   If p < 16.529 Then
#Rem    ssV = s2_pT(p, T4_p(p))
#Rem    ssL = s1_pT(p, T4_p(p))
#Rem   Else
#Rem    ssV = s3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p))
#Rem    ssL = s3_rhoT(1 / (v3_ph(p, h4L_p(p))), T4_p(p))
#Rem   End If
#Rem   If s < ssL Then
#Rem     x4_ps = 0
#Rem   ElseIf s > ssV Then
#Rem     x4_ps = 1
#Rem   Else
#Rem     x4_ps = (s - ssL) / (ssV - ssL)
#Rem   End If
#Rem End Function
#Rem Private Function T4_hs(ByVal h As Double, ByVal s As Double) As Double
#Rem 'Supplementary Release on Backward Equations ( ) , p h s for Region 3,
#Rem 'Chapter 5.3 page 30.
#Rem 'The if 97 function is only valid for part of region4. Use iteration outsida.
#Rem  Dim Ii, Ji, ni As Variant, hL, Ts, ss, p, sigma, eta, teta, High_Bound, Low_Bound, PL, s4V, v4V, s4L, v4L, xs As Double, i As Integer
#Rem    Ii = Array(0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 5, 6, 6, 6, 8, 10, 10, 12, 14, 14, 16, 16, 18, 18, 18, 20, 28)
#Rem    Ji = Array(0, 3, 12, 0, 1, 2, 5, 0, 5, 8, 0, 2, 3, 4, 0, 1, 1, 2, 4, 16, 6, 8, 22, 1, 20, 36, 24, 1, 28, 12, 32, 14, 22, 36, 24, 36)
#Rem    ni = Array(0.179882673606601, -0.267507455199603, 1.162767226126, 0.147545428713616, -0.512871635973248, 0.421333567697984, 0.56374952218987, 0.429274443819153, -3.3570455214214, 10.8890916499278, -0.248483390456012, 0.30415322190639, -0.494819763939905, 1.07551674933261, 7.33888415457688E-02, 1.40170545411085E-02, -0.106110975998808, 1.68324361811875E-02, 1.25028363714877, 1013.16840309509, -1.51791558000712, 52.4277865990866, 23049.5545563912, 2.49459806365456E-02, 2107964.67412137, 366836848.613065, -144814105.365163, -1.7927637300359E-03, 4899556021.00459, 471.262212070518, -82929439019.8652, -1715.45662263191, 3557776.82973575, 586062760258.436, -12988763.5078195, 31724744937.1057)
#Rem   If (s > 5.210887825 And s < 9.15546555571324) Then
#Rem     sigma = s / 9.2
#Rem     eta = h / 2800
#Rem     teta = 0
#Rem     For i = 0 To 35
#Rem       teta = teta + ni(i) * (eta - 0.119) ^ Ii(i) * (sigma - 1.07) ^ Ji(i)
#Rem     Next i
#Rem     T4_hs = teta * 550
#Rem Else
#Rem     'Function psat_h
#Rem     If s > -0.0001545495919 And s <= 3.77828134 Then
#Rem       Low_Bound = 0.000611
#Rem       High_Bound = 165.291642526045
#Rem       Do While Abs(hL - h) > 0.00001 And Abs(High_Bound - Low_Bound) > 0.0001
#Rem        PL = (Low_Bound + High_Bound) / 2
#Rem        Ts = T4_p(PL)
#Rem        hL = h1_pT(PL, Ts)
#Rem        If hL > h Then
#Rem          High_Bound = PL
#Rem        Else
#Rem          Low_Bound = PL
#Rem        End If
#Rem       Loop
#Rem     ElseIf s > 3.77828134 And s <= 4.41202148223476 Then
#Rem       PL = p3sat_h(h)
#Rem     ElseIf s > 4.41202148223476 And s <= 5.210887663 Then
#Rem       PL = p3sat_h(h)
#Rem     End If
#Rem     Low_Bound = 0.000611
#Rem     High_Bound = PL
#Rem     Do While Abs(s - ss) > 0.000001 And Abs(High_Bound - Low_Bound) > 0.0000001
#Rem       p = (Low_Bound + High_Bound) / 2
#Rem
#Rem       'Calculate s4_ph
#Rem       Ts = T4_p(p)
#Rem       xs = x4_ph(p, h)
#Rem       If p < 16.529 Then
#Rem         s4V = s2_pT(p, Ts)
#Rem         s4L = s1_pT(p, Ts)
#Rem       Else
#Rem         v4V = v3_ph(p, h4V_p(p))
#Rem         s4V = s3_rhoT(1 / v4V, Ts)
#Rem         v4L = v3_ph(p, h4L_p(p))
#Rem         s4L = s3_rhoT(1 / v4L, Ts)
#Rem       End If
#Rem       ss = (xs * s4V + (1 - xs) * s4L)
#Rem
#Rem       If ss < s Then
#Rem         High_Bound = p
#Rem       Else
#Rem         Low_Bound = p
#Rem       End If
#Rem     Loop
#Rem     T4_hs = T4_p(p)
#Rem End If
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*2.5 Functions for region 5
#Rem Private Function h5_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem   'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem   'Basic Equation for Region 5
#Rem   'Eq 32,33, Page 36, Tables 37-41
#Rem    Dim Iir, Jir, nir, ni0, Ji0 As Variant, tau, gamma0_tau, gammar_tau As Double, i As Integer
#Rem    Const R As Double = 0.461526   'kJ/(kg K)
#Rem   Ji0 = Array(0, 1, -3, -2, -1, 2)
#Rem   ni0 = Array(-13.179983674201, 6.8540841634434, -0.024805148933466, 0.36901534980333, -3.1161318213925, -0.32961626538917)
#Rem   Iir = Array(1, 1, 1, 2, 3)
#Rem   Jir = Array(0, 1, 3, 9, 3)
#Rem   nir = Array(-1.2563183589592E-04, 2.1774678714571E-03, -0.004594282089991, -3.9724828359569E-06, 1.2919228289784E-07)
#Rem   tau = 1000 / T
#Rem   gamma0_tau = 0
#Rem   For i = 0 To 5
#Rem     gamma0_tau = gamma0_tau + ni0(i) * Ji0(i) * tau ^ (Ji0(i) - 1)
#Rem   Next i
#Rem   gammar_tau = 0
#Rem   For i = 0 To 4
#Rem     gammar_tau = gammar_tau + nir(i) * p ^ Iir(i) * Jir(i) * tau ^ (Jir(i) - 1)
#Rem   Next i
#Rem   h5_pT = R * T * tau * (gamma0_tau + gammar_tau)
#Rem End Function
#Rem
#Rem
#Rem Private Function v5_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem 'Basic Equation for Region 5
#Rem 'Eq 32,33, Page 36, Tables 37-41
#Rem Dim Iir, Jir, nir, ni0, Ji0 As Variant, tau, gamma0_pi, gammar_pi As Double, i As Integer
#Rem Const R As Double = 0.461526   'kJ/(kg K)
#Rem Ji0 = Array(0, 1, -3, -2, -1, 2)
#Rem ni0 = Array(-13.179983674201, 6.8540841634434, -0.024805148933466, 0.36901534980333, -3.1161318213925, -0.32961626538917)
#Rem Iir = Array(1, 1, 1, 2, 3)
#Rem Jir = Array(0, 1, 3, 9, 3)
#Rem nir = Array(-1.2563183589592E-04, 2.1774678714571E-03, -0.004594282089991, -3.9724828359569E-06, 1.2919228289784E-07)
#Rem tau = 1000 / T
#Rem gamma0_pi = 1 / p
#Rem gammar_pi = 0
#Rem For i = 0 To 4
#Rem   gammar_pi = gammar_pi + nir(i) * Iir(i) * p ^ (Iir(i) - 1) * tau ^ Jir(i)
#Rem Next i
#Rem v5_pT = R * T / p * p * (gamma0_pi + gammar_pi) / 1000
#Rem End Function
#Rem
#Rem Private Function u5_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem 'Basic Equation for Region 5
#Rem 'Eq 32,33, Page 36, Tables 37-41
#Rem Dim Iir, Jir, nir, ni0, Ji0 As Variant, tau, gamma0_pi, gammar_pi, gamma0_tau, gammar_tau As Double, i As Integer
#Rem Const R As Double = 0.461526   'kJ/(kg K)
#Rem Ji0 = Array(0, 1, -3, -2, -1, 2)
#Rem ni0 = Array(-13.179983674201, 6.8540841634434, -0.024805148933466, 0.36901534980333, -3.1161318213925, -0.32961626538917)
#Rem Iir = Array(1, 1, 1, 2, 3)
#Rem Jir = Array(0, 1, 3, 9, 3)
#Rem nir = Array(-1.2563183589592E-04, 2.1774678714571E-03, -0.004594282089991, -3.9724828359569E-06, 1.2919228289784E-07)
#Rem tau = 1000 / T
#Rem gamma0_pi = 1 / p
#Rem gamma0_tau = 0
#Rem For i = 0 To 5
#Rem   gamma0_tau = gamma0_tau + ni0(i) * Ji0(i) * tau ^ (Ji0(i) - 1)
#Rem Next i
#Rem gammar_pi = 0
#Rem gammar_tau = 0
#Rem For i = 0 To 4
#Rem   gammar_pi = gammar_pi + nir(i) * Iir(i) * p ^ (Iir(i) - 1) * tau ^ Jir(i)
#Rem   gammar_tau = gammar_tau + nir(i) * p ^ Iir(i) * Jir(i) * tau ^ (Jir(i) - 1)
#Rem Next i
#Rem u5_pT = R * T * (tau * (gamma0_tau + gammar_tau) - p * (gamma0_pi + gammar_pi))
#Rem End Function
#Rem Private Function Cp5_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem 'Basic Equation for Region 5
#Rem 'Eq 32,33, Page 36, Tables 37-41
#Rem Dim Iir, Jir, nir, ni0, Ji0 As Variant, tau, gamma0_tautau, gammar_tautau As Double, i As Integer
#Rem Const R As Double = 0.461526   'kJ/(kg K)
#Rem Ji0 = Array(0, 1, -3, -2, -1, 2)
#Rem ni0 = Array(-13.179983674201, 6.8540841634434, -0.024805148933466, 0.36901534980333, -3.1161318213925, -0.32961626538917)
#Rem Iir = Array(1, 1, 1, 2, 3)
#Rem Jir = Array(0, 1, 3, 9, 3)
#Rem nir = Array(-1.2563183589592E-04, 2.1774678714571E-03, -0.004594282089991, -3.9724828359569E-06, 1.2919228289784E-07)
#Rem tau = 1000 / T
#Rem gamma0_tautau = 0
#Rem For i = 0 To 5
#Rem   gamma0_tautau = gamma0_tautau + ni0(i) * Ji0(i) * (Ji0(i) - 1) * tau ^ (Ji0(i) - 2)
#Rem Next i
#Rem gammar_tautau = 0
#Rem For i = 0 To 4
#Rem   gammar_tautau = gammar_tautau + nir(i) * p ^ Iir(i) * Jir(i) * (Jir(i) - 1) * tau ^ (Jir(i) - 2)
#Rem Next i
#Rem Cp5_pT = -R * tau ^ 2 * (gamma0_tautau + gammar_tautau)
#Rem End Function
#Rem
#Rem Private Function s5_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem 'Basic Equation for Region 5
#Rem 'Eq 32,33, Page 36, Tables 37-41
#Rem Dim Iir, Jir, nir, ni0, Ji0 As Variant, tau, gamma0, gamma0_tau, gammar, gammar_tau As Double, i As Integer
#Rem Const R As Double = 0.461526   'kJ/(kg K)
#Rem Ji0 = Array(0, 1, -3, -2, -1, 2)
#Rem ni0 = Array(-13.179983674201, 6.8540841634434, -0.024805148933466, 0.36901534980333, -3.1161318213925, -0.32961626538917)
#Rem Iir = Array(1, 1, 1, 2, 3)
#Rem Jir = Array(0, 1, 3, 9, 3)
#Rem nir = Array(-1.2563183589592E-04, 2.1774678714571E-03, -0.004594282089991, -3.9724828359569E-06, 1.2919228289784E-07)
#Rem tau = 1000 / T
#Rem gamma0 = Log(p)
#Rem gamma0_tau = 0
#Rem For i = 0 To 5
#Rem   gamma0_tau = gamma0_tau + ni0(i) * Ji0(i) * tau ^ (Ji0(i) - 1)
#Rem   gamma0 = gamma0 + ni0(i) * tau ^ Ji0(i)
#Rem Next i
#Rem gammar = 0
#Rem gammar_tau = 0
#Rem For i = 0 To 4
#Rem   gammar = gammar + nir(i) * p ^ Iir(i) * tau ^ Jir(i)
#Rem   gammar_tau = gammar_tau + nir(i) * p ^ Iir(i) * Jir(i) * tau ^ (Jir(i) - 1)
#Rem Next i
#Rem s5_pT = R * (tau * (gamma0_tau + gammar_tau) - (gamma0 + gammar))
#Rem End Function
#Rem Private Function Cv5_pT(ByVal p As Double, ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
#Rem 'Basic Equation for Region 5
#Rem 'Eq 32,33, Page 36, Tables 37-41
#Rem Dim Iir, Jir, nir, ni0, Ji0 As Variant, tau, gamma0_tautau, gammar_pi, gammar_pitau, gammar_pipi, gammar_tautau As Double, i As Integer
#Rem Const R As Double = 0.461526   'kJ/(kg K)
#Rem Ji0 = Array(0, 1, -3, -2, -1, 2)
#Rem ni0 = Array(-13.179983674201, 6.8540841634434, -0.024805148933466, 0.36901534980333, -3.1161318213925, -0.32961626538917)
#Rem Iir = Array(1, 1, 1, 2, 3)
#Rem Jir = Array(0, 1, 3, 9, 3)
#Rem nir = Array(-1.2563183589592E-04, 2.1774678714571E-03, -0.004594282089991, -3.9724828359569E-06, 1.2919228289784E-07)
#Rem tau = 1000 / T
#Rem gamma0_tautau = 0
#Rem For i = 0 To 5
#Rem   gamma0_tautau = gamma0_tautau + ni0(i) * (Ji0(i) - 1) * Ji0(i) * tau ^ (Ji0(i) - 2)
#Rem Next i
#Rem gammar_pi = 0
#Rem gammar_pitau = 0
#Rem gammar_pipi = 0
#Rem gammar_tautau = 0
#Rem For i = 0 To 4
#Rem   gammar_pi = gammar_pi + nir(i) * Iir(i) * p ^ (Iir(i) - 1) * tau ^ Jir(i)
#Rem   gammar_pitau = gammar_pitau + nir(i) * Iir(i) * p ^ (Iir(i) - 1) * Jir(i) * tau ^ (Jir(i) - 1)
#Rem   gammar_pipi = gammar_pipi + nir(i) * Iir(i) * (Iir(i) - 1) * p ^ (Iir(i) - 2) * tau ^ Jir(i)
#Rem   gammar_tautau = gammar_tautau + nir(i) * p ^ Iir(i) * Jir(i) * (Jir(i) - 1) * tau ^ (Jir(i) - 2)
#Rem Next i
#Rem w5_pT = (1000 * R * T * (1 + 2 * p * gammar_pi + p ^ 2 * gammar_pi ^ 2) / ((1 - p ^ 2 * gammar_pipi) + (1 + p * gammar_pi - tau * p * gammar_pitau) ^ 2 / (tau ^ 2 * (gamma0_tautau + gammar_tautau)))) ^ 0.5
#Rem End Function
#Rem
#Rem Private Function T5_ph(ByVal p As Double, ByVal h As Double) As Double
#Rem     'Solve with half interval method
#Rem     Dim Low_Bound, High_Bound, Ts, hs As Double
#Rem     Low_Bound = 1073.15
#Rem     High_Bound = 2273.15
#Rem     Do While Abs(h - hs) > 0.00001
#Rem       Ts = (Low_Bound + High_Bound) / 2
#Rem       hs = h5_pT(p, Ts)
#Rem       If hs > h Then
#Rem         High_Bound = Ts
#Rem       Else
#Rem         Low_Bound = Ts
#Rem       End If
#Rem     Loop
#Rem     T5_ph = Ts
#Rem End Function
#Rem
#Rem Private Function T5_ps(ByVal p As Double, ByVal s As Double) As Double
#Rem     'Solve with half interval method
#Rem     Dim Low_Bound, High_Bound, Ts, ss As Double
#Rem     Low_Bound = 1073.15
#Rem     High_Bound = 2273.15
#Rem     Do While Abs(s - ss) > 0.00001
#Rem       Ts = (Low_Bound + High_Bound) / 2
#Rem       ss = s5_pT(p, Ts)
#Rem       If ss > s Then
#Rem         High_Bound = Ts
#Rem       Else
#Rem         Low_Bound = Ts
#Rem       End If
#Rem     Loop
#Rem     T5_ps = Ts
#Rem End Function
#Rem Private Function T5_prho(ByVal p As Double, ByVal rho As Double) As Double
#Rem   'Solve by iteration. Observe that fo low temperatures this equation has 2 solutions.
#Rem   'Solve with half interval method
#Rem   Dim Low_Bound, High_Bound, Ts, rhos As Double
#Rem     Low_Bound = 1073.15
#Rem     High_Bound = 2073.15
#Rem   Do While Abs(rho - rhos) > 0.000001
#Rem     Ts = (Low_Bound + High_Bound) / 2
#Rem     rhos = 1 / v2_pT(p, Ts)
#Rem     If rhos < rho Then
#Rem       High_Bound = Ts
#Rem     Else
#Rem       Low_Bound = Ts
#Rem     End If
#Rem     Loop
#Rem     T5_prho = Ts
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*3 Region Selection
#Rem '***********************************************************************************************************
#Rem '*3.1 Regions as a function of pT
#Rem Private Function region_pT(ByVal p As Double, ByVal T As Double) As Integer
#Rem Dim ps As Double
#Rem If T > 1073.15 And p < 10 And T < 2273.15 And p > 0.000611 Then
#Rem   region_pT = 5
#Rem ElseIf T <= 1073.15 And T > 273.15 And p <= 100 And p > 0.000611 Then
#Rem   If T > 623.15 Then
#Rem     If p > B23p_T(T) Then
#Rem      region_pT = 3
#Rem      If T < 647.096 Then
#Rem         ps = p4_T(T)
#Rem         If Abs(p - ps) < 0.00001 Then
#Rem            region_pT = 4
#Rem         End If
#Rem      End If
#Rem     Else
#Rem      region_pT = 2
#Rem     End If
#Rem    Else
#Rem     ps = p4_T(T)
#Rem     If Abs(p - ps) < 0.00001 Then
#Rem       region_pT = 4
#Rem     ElseIf p > ps Then
#Rem       region_pT = 1
#Rem     Else
#Rem       region_pT = 2
#Rem     End If
#Rem    End If
#Rem   Else
#Rem     region_pT = 0 '**Error, Outside valid area
#Rem   End If
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*3.2 Regions as a function of ph
#Rem Private Function region_ph(ByVal p, ByVal h) As Integer
#Rem Dim hL, hV, h_45, h_5u, Ts As Double
#Rem  'Check if outside pressure limits
#Rem  If p < 0.000611657 Or p > 100 Then
#Rem      region_ph = 0
#Rem      Exit Function
#Rem  End If
#Rem
#Rem  'Check if outside low h.
#Rem  If h < 0.963 * p + 2.2 Then 'Linear adaption to h1_pt()+2 to speed up calcualations.
#Rem     If h < h1_pT(p, 273.15) Then
#Rem       region_ph = 0
#Rem       Exit Function
#Rem     End If
#Rem  End If
#Rem
#Rem  If p < 16.5292 Then 'Bellow region 3,Check  region 1,4,2,5
#Rem    'Check Region 1
#Rem    Ts = T4_p(p)
#Rem    hL = 109.6635 * Log(p) + 40.3481 * p + 734.58 'Approximate function for hL_p
#Rem    If Abs(h - hL) < 100 Then 'If approximate is not god enough use real function
#Rem       hL = h1_pT(p, Ts)
#Rem    End If
#Rem    If h <= hL Then
#Rem      region_ph = 1
#Rem      Exit Function
#Rem    End If
#Rem    'Check Region 4
#Rem    hV = 45.1768 * Log(p) - 20.158 * p + 2804.4 'Approximate function for hV_p
#Rem    If Abs(h - hV) < 50 Then 'If approximate is not god enough use real function
#Rem       hV = h2_pT(p, Ts)
#Rem    End If
#Rem    If h < hV Then
#Rem      region_ph = 4
#Rem      Exit Function
#Rem    End If
#Rem    'Check upper limit of region 2 Quick Test
#Rem    If h < 4000 Then
#Rem      region_ph = 2
#Rem      Exit Function
#Rem    End If
#Rem   'Check region 2 (Real value)
#Rem    h_45 = h2_pT(p, 1073.15)
#Rem    If h <= h_45 Then
#Rem      region_ph = 2
#Rem      Exit Function
#Rem    End If
#Rem   'Check region 5
#Rem    If p > 10 Then
#Rem      region_ph = 0
#Rem      Exit Function
#Rem    End If
#Rem    h_5u = h5_pT(p, 2273.15)
#Rem    If h < h_5u Then
#Rem       region_ph = 5
#Rem       Exit Function
#Rem    End If
#Rem    region_ph = 0
#Rem    Exit Function
#Rem   Else 'For p>16.5292
#Rem    'Check if in region1
#Rem    If h < h1_pT(p, 623.15) Then
#Rem      region_ph = 1
#Rem      Exit Function
#Rem    End If
#Rem    'Check if in region 3 or 4 (Bellow Reg 2)
#Rem    If h < h2_pT(p, B23T_p(p)) Then
#Rem      'Region 3 or 4
#Rem      If p > p3sat_h(h) Then
#Rem        region_ph = 3
#Rem        Exit Function
#Rem      Else
#Rem        region_ph = 4
#Rem        Exit Function
#Rem      End If
#Rem   End If
#Rem   'Check if region 2
#Rem   If h < h2_pT(p, 1073.15) Then
#Rem     region_ph = 2
#Rem     Exit Function
#Rem   End If
#Rem  End If
#Rem  region_ph = 0
#Rem End Function
def region_ph(pressure, enthalpy):

    region = 0
    pressureMin, pressureMax = 0.000611657, 100.0
    enthalpyMin = 0.963 * pressure + 2.2 # Linear adaption to h1_pt()+2 to speed up calcualations.

    if pressure < pressureMin or pressure > pressureMax:
        raise ArithmeticError

    if enthalpy < enthalpyMin:
        if enthalpy < h1_pt(pressure, 273.150):
            raise ArithmeticError

#Rem '***********************************************************************************************************
#Rem '*3.3 Regions as a function of ps
#Rem Private Function region_ps(ByVal p As Double, ByVal s) As Integer
#Rem Dim ss As Double
#Rem   If p < 0.000611657 Or p > 100 Or s < 0 Or s > s5_pT(p, 2273.15) Then
#Rem    region_ps = 0
#Rem    Exit Function
#Rem   End If
#Rem
#Rem   'Check region 5
#Rem   If s > s2_pT(p, 1073.15) Then
#Rem     If p <= 10 Then
#Rem       region_ps = 5
#Rem       Exit Function
#Rem     Else
#Rem       region_ps = 0
#Rem       Exit Function
#Rem     End If
#Rem   End If
#Rem
#Rem   'Check region 2
#Rem   If p > 16.529 Then
#Rem     ss = s2_pT(p, B23T_p(p)) 'Between 5.047 and 5.261. Use to speed up!
#Rem   Else
#Rem     ss = s2_pT(p, T4_p(p))
#Rem   End If
#Rem   If s > ss Then
#Rem       region_ps = 2
#Rem       Exit Function
#Rem   End If
#Rem
#Rem   'Check region 3
#Rem   ss = s1_pT(p, 623.15)
#Rem   If p > 16.529 And s > ss Then
#Rem     If p > p3sat_s(s) Then
#Rem       region_ps = 3
#Rem       Exit Function
#Rem     Else
#Rem       region_ps = 4
#Rem       Exit Function
#Rem     End If
#Rem   End If
#Rem
#Rem   'Check region 4 (Not inside region 3)
#Rem   If p < 16.529 And s > s1_pT(p, T4_p(p)) Then
#Rem     region_ps = 4
#Rem     Exit Function
#Rem   End If
#Rem
#Rem   'Check region 1
#Rem   If p > 0.000611657 And s > s1_pT(p, 273.15) Then
#Rem     region_ps = 1
#Rem     Exit Function
#Rem   End If
#Rem   region_ps = 1
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*3.4 Regions as a function of hs
#Rem Private Function Region_hs(ByVal h, ByVal s) As Integer
#Rem Dim TMax, hMax, hB, hL, hV, vmax, Tmin, hMin As Double
#Rem   If s < -0.0001545495919 Then
#Rem     Region_hs = 0
#Rem     Exit Function
#Rem   End If
#Rem   'Check linear adaption to p=0.000611. If bellow region 4.
#Rem   hMin = (((-0.0415878 - 2500.89262) / (-0.00015455 - 9.155759)) * s)
#Rem   If s < 9.155759395 And h < hMin Then
#Rem     Region_hs = 0
#Rem     Exit Function
#Rem   End If
#Rem
#Rem   '******Kolla 1 eller 4. (+liten bit över B13)
#Rem   If s >= -0.0001545495919 And s <= 3.77828134 Then
#Rem     If h < h4_s(s) Then
#Rem       Region_hs = 4
#Rem       Exit Function
#Rem     ElseIf s < 3.397782955 Then '100MPa line is limiting
#Rem       TMax = T1_ps(100, s)
#Rem       hMax = h1_pT(100, TMax)
#Rem       If h < hMax Then
#Rem        Region_hs = 1
#Rem        Exit Function
#Rem       Else
#Rem        Region_hs = 0
#Rem        Exit Function
#Rem       End If
#Rem      Else 'The point is either in region 4,1,3. Check B23
#Rem       hB = hB13_s(s)
#Rem       If h < hB Then
#Rem         Region_hs = 1
#Rem         Exit Function
#Rem       End If
#Rem       TMax = T3_ps(100, s)
#Rem       vmax = v3_ps(100, s)
#Rem       hMax = h3_rhoT(1 / vmax, TMax)
#Rem       If h < hMax Then
#Rem         Region_hs = 3
#Rem         Exit Function
#Rem       Else
#Rem         Region_hs = 0
#Rem         Exit Function
#Rem       End If
#Rem      End If
#Rem   End If
#Rem
#Rem   '******Kolla region 2 eller 4. (Övre delen av område b23-> max)
#Rem   If s >= 5.260578707 And s <= 11.9212156897728 Then
#Rem     If s > 9.155759395 Then 'Above region 4
#Rem       Tmin = T2_ps(0.000611, s)
#Rem       hMin = h2_pT(0.000611, Tmin)
#Rem       'Function adapted to h(1073.15,s)
#Rem       hMax = -0.07554022 * s ^ 4 + 3.341571 * s ^ 3 - 55.42151 * s ^ 2 + 408.515 * s + 3031.338
#Rem       If h > hMin And h < hMax Then
#Rem         Region_hs = 2
#Rem         Exit Function
#Rem       Else
#Rem         Region_hs = 0
#Rem         Exit Function
#Rem       End If
#Rem     End If
#Rem
#Rem
#Rem       hV = h4_s(s)
#Rem
#Rem     If h < hV Then  'Region 4. Under region 3.
#Rem         Region_hs = 4
#Rem         Exit Function
#Rem     End If
#Rem     If s < 6.04048367171238 Then
#Rem       TMax = T2_ps(100, s)
#Rem       hMax = h2_pT(100, TMax)
#Rem     Else
#Rem      'Function adapted to h(1073.15,s)
#Rem       hMax = -2.988734 * s ^ 4 + 121.4015 * s ^ 3 - 1805.15 * s ^ 2 + 11720.16 * s - 23998.33
#Rem     End If
#Rem      If h < hMax Then  'Region 2. Över region 4.
#Rem         Region_hs = 2
#Rem         Exit Function
#Rem     Else
#Rem         Region_hs = 0
#Rem         Exit Function
#Rem     End If
#Rem    End If
#Rem
#Rem    'Kolla region 3 eller 4. Under kritiska punkten.
#Rem    If s >= 3.77828134 And s <= 4.41202148223476 Then
#Rem      hL = h4_s(s)
#Rem      If h < hL Then
#Rem        Region_hs = 4
#Rem        Exit Function
#Rem      End If
#Rem      TMax = T3_ps(100, s)
#Rem      vmax = v3_ps(100, s)
#Rem      hMax = h3_rhoT(1 / vmax, TMax)
#Rem      If h < hMax Then
#Rem         Region_hs = 3
#Rem         Exit Function
#Rem      Else
#Rem         Region_hs = 0
#Rem         Exit Function
#Rem     End If
#Rem    End If
#Rem
#Rem    'Kolla region 3 eller 4 från kritiska punkten till övre delen av b23
#Rem    If s >= 4.41202148223476 And s <= 5.260578707 Then
#Rem      hV = h4_s(s)
#Rem      If h < hV Then
#Rem         Region_hs = 4
#Rem         Exit Function
#Rem      End If
#Rem      'Kolla om vi är under b23 giltighetsområde.
#Rem      If s <= 5.048096828 Then
#Rem        TMax = T3_ps(100, s)
#Rem        vmax = v3_ps(100, s)
#Rem        hMax = h3_rhoT(1 / vmax, TMax)
#Rem        If h < hMax Then
#Rem          Region_hs = 3
#Rem          Exit Function
#Rem        Else
#Rem          Region_hs = 0
#Rem          Exit Function
#Rem        End If
#Rem      Else 'Inom området för B23 i s led.
#Rem        If (h > 2812.942061) Then 'Ovanför B23 i h_led
#Rem          If s > 5.09796573397125 Then
#Rem            TMax = T2_ps(100, s)
#Rem            hMax = h2_pT(100, TMax)
#Rem            If h < hMax Then
#Rem              Region_hs = 2
#Rem              Exit Function
#Rem            Else
#Rem              Region_hs = 0
#Rem              Exit Function
#Rem            End If
#Rem          Else
#Rem            Region_hs = 0
#Rem            Exit Function
#Rem          End If
#Rem        End If
#Rem        If (h < 2563.592004) Then   'Nedanför B23 i h_led men vi har redan kollat ovanför hV2c3b
#Rem           Region_hs = 3
#Rem           Exit Function
#Rem        End If
#Rem        'Vi är inom b23 området i både s och h led.
#Rem        If p2_hs(h, s) > B23p_T(TB23_hs(h, s)) Then
#Rem          Region_hs = 3
#Rem          Exit Function
#Rem        Else
#Rem          Region_hs = 2
#Rem          Exit Function
#Rem        End If
#Rem      End If
#Rem    End If
#Rem    Region_hs = CVErr(xlErrValue)
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*3.5 Regions as a function of p and rho
#Rem Private Function Region_prho(ByVal p As Double, ByVal rho) As Integer
#Rem   Dim v As Double
#Rem   v = 1 / rho
#Rem   If p < 0.000611657 Or p > 100 Then
#Rem     Region_prho = 0
#Rem     Exit Function
#Rem   End If
#Rem   If p < 16.5292 Then 'Bellow region 3, Check region 1,4,2
#Rem     If v < v1_pT(p, 273.15) Then 'Observe that this is not actually min of v. Not valid Water of 4°C is ligther.
#Rem       Region_prho = 0
#Rem       Exit Function
#Rem     End If
#Rem     If v <= v1_pT(p, T4_p(p)) Then
#Rem       Region_prho = 1
#Rem       Exit Function
#Rem     End If
#Rem     If v < v2_pT(p, T4_p(p)) Then
#Rem       Region_prho = 4
#Rem       Exit Function
#Rem     End If
#Rem     If v <= v2_pT(p, 1073.15) Then
#Rem       Region_prho = 2
#Rem       Exit Function
#Rem     End If
#Rem     If p > 10 Then 'Above region 5
#Rem       Region_prho = 0
#Rem       Exit Function
#Rem     End If
#Rem     If v <= v5_pT(p, 2073.15) Then
#Rem       Region_prho = 5
#Rem       Exit Function
#Rem     End If
#Rem   Else 'Check region 1,3,4,3,2 (Above the lowest point of region 3.)
#Rem     If v < v1_pT(p, 273.15) Then 'Observe that this is not actually min of v. Not valid Water of 4°C is ligther.
#Rem       Region_prho = 0
#Rem       Exit Function
#Rem     End If
#Rem     If v < v1_pT(p, 623.15) Then
#Rem       Region_prho = 1
#Rem       Exit Function
#Rem     End If
#Rem     'Check if in region 3 or 4 (Bellow Reg 2)
#Rem     If v < v2_pT(p, B23T_p(p)) Then
#Rem      'Region 3 or 4
#Rem       If p > 22.064 Then 'Above region 4
#Rem         Region_prho = 3
#Rem         Exit Function
#Rem       End If
#Rem       If v < v3_ph(p, h4L_p(p)) Or v > v3_ph(p, h4V_p(p)) Then 'Uses iteration!!
#Rem         Region_prho = 3
#Rem         Exit Function
#Rem       Else
#Rem         Region_prho = 4
#Rem         Exit Function
#Rem       End If
#Rem     End If
#Rem     'Check if region 2
#Rem     If v < v2_pT(p, 1073.15) Then
#Rem       Region_prho = 2
#Rem       Exit Function
#Rem     End If
#Rem   End If
#Rem
#Rem   Region_prho = 0
#Rem End Function
#Rem
#Rem
#Rem '***********************************************************************************************************
#Rem '*4 Region Borders
#Rem '***********************************************************************************************************
#Rem '***********************************************************************************************************
#Rem '*4.1 Boundary between region 2 and 3.
#Rem Private Function B23p_T(ByVal T As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam
#Rem '1997
#Rem 'Section 4 Auxiliary Equation for the Boundary between Regions 2 and 3
#Rem 'Eq 5, Page 5
#Rem B23p_T = 348.05185628969 - 1.1671859879975 * T + 1.0192970039326E-03 * T ^ 2
#Rem End Function
#Rem Private Function B23T_p(ByVal p As Double) As Double
#Rem 'Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam
#Rem '1997
#Rem 'Section 4 Auxiliary Equation for the Boundary between Regions 2 and 3
#Rem 'Eq 6, Page 6
#Rem B23T_p = 572.54459862746 + ((p - 13.91883977887) / 1.0192970039326E-03) ^ 0.5
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*4.2 Region 3. pSat_h and pSat_s
#Rem Private Function p3sat_h(ByVal h As Double) As Double
#Rem 'Revised Supplementary Release on Backward Equations for the Functions T(p,h), v(p,h) and T(p,s), v(p,s) for Region 3 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam
#Rem '2004
#Rem 'Section 4 Boundary Equations psat(h) and psat(s) for the Saturation Lines of Region 3
#Rem 'Se pictures Page 17, Eq 10, Table 17, Page 18
#Rem Dim Ii, Ji, ni As Variant, ps As Double, i As Integer
#Rem Ii = Array(0, 1, 1, 1, 1, 5, 7, 8, 14, 20, 22, 24, 28, 36)
#Rem Ji = Array(0, 1, 3, 4, 36, 3, 0, 24, 16, 16, 3, 18, 8, 24)
#Rem ni = Array(0.600073641753024, -9.36203654849857, 24.6590798594147, -107.014222858224, -91582131580576.8, -8623.32011700662, -23.5837344740032, 2.52304969384128E+17, -3.89718771997719E+18, -3.33775713645296E+22, 35649946963.6328, -1.48547544720641E+26, 3.30611514838798E+18, 8.13641294467829E+37)
#Rem h = h / 2600
#Rem ps = 0
#Rem For i = 0 To 13
#Rem   ps = ps + ni(i) * (h - 1.02) ^ Ii(i) * (h - 0.608) ^ Ji(i)
#Rem Next i
#Rem p3sat_h = ps * 22
#Rem End Function
#Rem Private Function p3sat_s(ByVal s As Double) As Double
#Rem Dim Ii, Ji, ni As Variant, sigma, p As Double, i As Integer
#Rem Ii = Array(0, 1, 1, 4, 12, 12, 16, 24, 28, 32)
#Rem Ji = Array(0, 1, 32, 7, 4, 14, 36, 10, 0, 18)
#Rem ni = Array(0.639767553612785, -12.9727445396014, -2.24595125848403E+15, 1774667.41801846, 7170793495.71538, -3.78829107169011E+17, -9.55586736431328E+34, 1.87269814676188E+23, 119254746466.473, 1.10649277244882E+36)
#Rem sigma = s / 5.2
#Rem p = 0
#Rem For i = 0 To 9
#Rem   p = p + ni(i) * (sigma - 1.03) ^ Ii(i) * (sigma - 0.699) ^ Ji(i)
#Rem Next i
#Rem p3sat_s = p * 22
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '4.3 Region boundary 1to3 and 3to2 as a functions of s
#Rem Private Function hB13_s(ByVal s As Double) As Double
#Rem 'Supplementary Release on Backward Equations ( ) , p h s for Region 3,
#Rem 'Chapter 4.5 page 23.
#Rem Dim Ii, Ji, ni As Variant, sigma, eta As Double, i As Integer
#Rem   Ii = Array(0, 1, 1, 3, 5, 6)
#Rem   Ji = Array(0, -2, 2, -12, -4, -3)
#Rem   ni = Array(0.913965547600543, -4.30944856041991E-05, 60.3235694765419, 1.17518273082168E-18, 0.220000904781292, -69.0815545851641)
#Rem   sigma = s / 3.8
#Rem   eta = 0
#Rem   For i = 0 To 5
#Rem     eta = eta + ni(i) * (sigma - 0.884) ^ Ii(i) * (sigma - 0.864) ^ Ji(i)
#Rem   Next i
#Rem   hB13_s = eta * 1700
#Rem End Function
#Rem Private Function TB23_hs(ByVal h As Double, ByVal s As Double) As Double
#Rem 'Supplementary Release on Backward Equations ( ) , p h s for Region 3,
#Rem 'Chapter 4.6 page 25.
#Rem Dim Ii, Ji, ni As Variant, sigma, eta, teta As Double, i As Integer
#Rem    Ii = Array(-12, -10, -8, -4, -3, -2, -2, -2, -2, 0, 1, 1, 1, 3, 3, 5, 6, 6, 8, 8, 8, 12, 12, 14, 14)
#Rem    Ji = Array(10, 8, 3, 4, 3, -6, 2, 3, 4, 0, -3, -2, 10, -2, -1, -5, -6, -3, -8, -2, -1, -12, -1, -12, 1)
#Rem    ni = Array(6.2909626082981E-04, -8.23453502583165E-04, 5.15446951519474E-08, -1.17565945784945, 3.48519684726192, -5.07837382408313E-12, -2.84637670005479, -2.36092263939673, 6.01492324973779, 1.48039650824546, 3.60075182221907E-04, -1.26700045009952E-02, -1221843.32521413, 0.149276502463272, 0.698733471798484, -2.52207040114321E-02, 1.47151930985213E-02, -1.08618917681849, -9.36875039816322E-04, 81.9877897570217, -182.041861521835, 2.61907376402688E-06, -29162.6417025961, 1.40660774926165E-05, 7832370.62349385)
#Rem   sigma = s / 5.3
#Rem   eta = h / 3000
#Rem   teta = 0
#Rem   For i = 0 To 24
#Rem     teta = teta + ni(i) * (eta - 0.727) ^ Ii(i) * (sigma - 0.864) ^ Ji(i)
#Rem   Next i
#Rem   TB23_hs = teta * 900
#Rem End Function
#Rem
#Rem '***********************************************************************************************************
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
#Rem '***********************************************************************************************************
#Rem '5.3 Surface Tension
#Rem Private Function Surface_Tension_T(ByVal T As Double)
#Rem 'IAPWS Release on Surface Tension of Ordinary Water Substance,
#Rem 'September 1994
#Rem Dim tau As Double
#Rem Const tc As Double = 647.096, b As Double = 0.2358, bb As Double = -0.625, my As Double = 1.256
#Rem If T < 0.01 Or T > tc Then
#Rem  Surface_Tension_T = "Out of valid region"
#Rem  Exit Function
#Rem End If
#Rem tau = 1 - T / tc
#Rem Surface_Tension_T = b * tau ^ my * (1 + bb * tau)
#Rem End Function
#Rem '***********************************************************************************************************
#Rem '*6 Units                                                                                      *
#Rem '***********************************************************************************************************
conversionFactors = { 'enthalpy': 2.326, #[btu/lb]/[kJ/kg]
                      'specific volume': 0.0624279606, #[ft**3/lb]/[m**3/kg]
                      'entropy': 1.0/0.238845896627, #[btu/(lb*degF)]/[kJ/(kg*K)]
                      'velocity': 0.3048, #[ft/m]
                      'thermal conductivity': 1.0/0.577789, #[btu/lb*ft*hr]/[W/m*K]
                      'surface tension': 1.0/0.068521766, #[lb/ft]/[N/m]
                      'viscosity': 1.0/2419.088311 #[lb/ft*hr]/[Pa*s]
    }

def toSIUnit(value, quantity:str):

    quantity = quantity.lower()

    if quantity == 'pressure':

        if not englishUnits:

            value /= 1000.0
        else:

            value *= 0.00689475729
    elif quantity == 'temperature':

        if not englishUnits:

            value +=  273.15
        else:

            value = (5.0/9.0)*(value - 32.0) + 273.15
    else:

        value *= conversionFactors[quantity]

    return value

def fromSIUnit(value, quantity:str):

    quantity = quantity.lower()

    if quantity == 'pressure':

        if not englishUnits:

            value *= 1000.0
        else:

            value /= 0.00689475729
    elif quantity == 'temperature':

        if not englishUnits:

            value -=  273.15
        else:

            value = (value - 273.15)*(9.0/5.0) + 32.0
    else:

        value /= conversionFactors[quantity]

    return value

