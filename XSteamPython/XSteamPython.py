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
    pressure = Convert.toSIUnit(float(pressure), 'pressure', englishUnits=englishUnits)

    if pressure >= Constants._pressureMin and pressure <= Constants._pressureMax + 0.001:
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
    if temperature <= Constants._temperatureMax and temperature > Constants._temperatureMin:
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

def hV_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        enthalpy = Region4.h4_p(pressure, 'vap')
        if englishUnits:
            return Convert.fromSIUnit(enthalpy, 'enthalpy')
        else:
            return enthalpy
    else:
        return Constants._errorValue

def hL_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        enthalpy = Region4.h4_p(pressure, 'liq')
        if englishUnits:
            return Convert.fromSIUnit(enthalpy, 'enthalpy')
        else:
            return enthalpy
    else:
        return Constants._errorValue

def hV_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        enthalpy = Region4.h4_p(Region4.p4_t(temperature), 'vap')
        if englishUnits:
            return Convert.fromSIUnit(enthalpy, 'enthalpy')
        return enthalpy
    else:
        return Constants._errorValue

def hL_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        enthalpy = Region4.h4_p(Region4.p4_t(temperature), 'liq')
        if englishUnits:
            return Convert.fromSIUnit(enthalpy, 'enthalpy')
        return enthalpy
    else:
        return Constants._errorValue

def h_pT(pressure, temperature):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    region = Regions.region_pt(pressure, temperature)
    enthalpy = 0.0

    if region is None or region == 4: return Constants._errorValue

    if region == 1:
        enthalpy = Region1.h1_pt(pressure, temperature)
    elif region == 2:
        enthalpy = Region2.h2_pt(pressure, temperature)
    elif region == 3:
        enthalpy = Region3.h3_pt(pressure, temperature)
    elif region == 5:
        enthalpy = Region5.h5_pt(pressure, temperature)

    if englishUnits:
        return Convert.fromSIUnit(enthalpy, 'enthalpy')
    else:
        return enthalpy

def h_ps(pressure, entropy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        entropy = Convert.toSIUnit(entropy, 'entropy')
    enthalpy = 0.0

    region = Regions.region_ps(pressure, entropy)
    if region is None: return Constants._errorValue

    if region == 1:
        enthalpy = Region1.h1_pt(pressure, Region1.t1_ps(pressure, entropy))
    elif region == 2:
        enthalpy = Region2.h2_pt(pressure, Region2.t2_ps(pressure, entropy))
    elif region == 3:
        enthalpy = Region3.h3_rhot(1.0/Region3.v3_ps(pressure, entropy), Region3.t3_ps(pressure, entropy))
    elif region == 4:
        quality = Region4.x4_ps(pressure, entropy)
        enthalpy = quality*Region4.h4_p(pressure, 'vap') + (1.0 - quality)*Region4.h4_p(pressure, 'liq')
        if enthalpy == 0.0:
            return Constants._errorValue
    elif region == 5:
        enthalpy = Region5.h5_pt(pressure, Region5.t5_ps(pressure, entropy))

    if englishUnits:
        return Convert.fromSIUnit(enthalpy, 'enthalpy')
    else:
        return enthalpy

def h_px(pressure, quality):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)

    if quality > 1.0 or quality < 0.0 or pressure >= 22.064:
        return Constants._errorValue

    liquidEnthalpy = Region4.h4_p(pressure, phase='liq')
    vaporEnthalpy = Region4.h4_p(pressure, phase='vap')

    enthalpy = liquidEnthalpy + quality*(vaporEnthalpy - liquidEnthalpy)
    if enthalpy == 0.0:
        return Constants._errorValue
    if englishUnits and enthalpy != Constants._errorValue:
        enthalpy = Convert.fromSIUnit(enthalpy, 'enthalpy')

    return enthalpy

def h_Tx(temperature, quality):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    if quality > 1.0 or quality < 0.0 or temperature >= Constants._temperatureMax:
        return Constants._errorValue

    pressure = Convert.fromSIUnit(Region4.p4_t(temperature), 'pressure', englishUnits=englishUnits)

    return h_px(pressure, quality)

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

def vV_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    specificVolume = Constants._errorValue
    if pressure <= Constants._pressureMin or pressure >= Constants._pressureMax:
        return Constants._errorValue
    if pressure < Constants._pressureSubDomain:
        specificVolume = Region2.v2_pt(pressure, Region4.t4_p(pressure))
    else:
        specificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, phase='vap'))
    if englishUnits:
        specificVolume = Convert.fromSIUnit(specificVolume, 'specific volume')
    return specificVolume

def vL_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    specificVolume = Constants._errorValue
    if pressure <= Constants._pressureMin or pressure >= Constants._pressureMax:
        return Constants._errorValue

    if pressure < Constants._pressureSubDomain:
        specificVolume = Region1.v1_pt(pressure, Region4.t4_p(pressure))
    else:
        specificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, phase='liq'))

    if englishUnits:
        specificVolume = Convert.fromSIUnit(specificVolume, 'specific volume')
    return specificVolume

def vV_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    specificVolume = Constants._errorValue
    if temperature <= Constants._temperatureMin or temperature >= Constants._temperatureMax:
        return Constants._errorValue
    if temperature <= Constants._temperatureSubDomain:
        specificVolume = Region2.v2_pt(Region4.p4_t(temperature), temperature)
    else:
        specificVolume = Region3.v3_ph(Region4.p4_t(temperature), Region4.h4_p(Region4.p4_t(temperature), phase='vap'))
    if englishUnits:
        specificVolume = Convert.fromSIUnit(specificVolume, 'specific volume')
    return specificVolume

def vL_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    specificVolume = Constants._errorValue
    if temperature <= Constants._temperatureMin or temperature >= Constants._temperatureMax:
        return Constants._errorValue
    if temperature <= Constants._temperatureSubDomain:
        specificVolume = Region1.v1_pt(Region4.p4_t(temperature), temperature)
    else:
        specificVolume = Region3.v3_ph(Region4.p4_t(temperature), Region4.h4_p(Region4.p4_t(temperature), phase='liq'))
    if englishUnits:
        specificVolume = Convert.fromSIUnit(specificVolume, 'specific volume')
    return specificVolume

def v_pT(pressure, temperature):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    specificVolume = Constants._errorValue

    region = Regions.region_pt(pressure, temperature)
    if region is None or region == 4: return Constants._errorValue

    if region == 1:
        specificVolume = Region1.v1_pt(pressure, temperature)
    elif region == 2:
        specificVolume = Region2.v2_pt(pressure, temperature)
    elif region == 3:
        specificVolume = Region3.v3_ph(pressure, Region3.h3_pt(pressure, temperature))
    elif region == 5:
        specificVolume = Region5.v5_pt(pressure, temperature)

    if englishUnits:
        specificVolume = Convert.fromSIUnit(specificVolume, 'specific volume')

    return specificVolume

def v_ph(pressure, enthalpy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')
    specificVolume = Constants._errorValue
    region = Regions.region_ph(pressure, enthalpy)

    if region == 1:
        specificVolume = Region1.v1_pt(pressure, Region1.t1_ph(pressure, enthalpy))
    elif region == 2:
        specificVolume = Region2.v2_pt(pressure, Region2.t2_ph(pressure, enthalpy))
    elif region == 3:
        specificVolume = Region3.v3_ph(pressure, enthalpy)
    elif region == 4:
        quality = Region4.x4_ph(pressure, enthalpy)
        vaporSpecificVolume = 0.0
        liquidSpecificVolume = 0.0
        if pressure < Constants._pressureSubDomain:
            vaporSpecificVolume = Region2.v2_pt(pressure, Region4.t4_p(pressure))
            liquidSpecificVolume = Region1.v1_pt(pressure, Region4.t4_p(pressure))
        else:
            vaporSpecificVolume = Region3.v3_ph(pressure,Region4.h4_p(pressure, phase='vap'))
            liquidSpecificVolume = Region3.v3_ph(pressure,Region4.h4_p(pressure, phase='liq'))
        specificVolume = quality*vaporSpecificVolume + (1.0 - quality)*liquidSpecificVolume
    elif region == 5:
        specificVolume = Region5.v5_pt(pressure, Region5.t5_ph(pressure, enthalpy))

    if englishUnits and specificVolume != Constants._errorValue:
        specificVolume = Convert.fromSIUnit(specificVolume, 'specific volume')

    return specificVolume

def v_ps(pressure, entropy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        entropy = Convert.toSIUnit(entropy, 'entropy')
    specificVolume = Constants._errorValue
    region = Regions.region_ps(pressure, entropy)

    if region == 1:
        specificVolume = Region1.v1_pt(pressure, Region1.t1_ps(pressure, entropy))
    elif region == 2:
        specificVolume = Region2.v2_pt(pressure, Region2.t2_ps(pressure, entropy))
    elif region == 3:
        specificVolume = Region3.v3_ps(pressure, entropy)
    elif region == 4:
        quality = Region4.x4_ps(pressure, entropy)
        vaporSpecificVolume = 0.0
        liquidSpecificVolume = 0.0
        if pressure < Constants._pressureSubDomain:
            vaporSpecificVolume = Region2.v2_pt(pressure, Region4.t4_p(pressure))
            liquidSpecificVolume = Region1.v1_pt(pressure, Region4.t4_p(pressure))
        else:
            vaporSpecificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap'))
            liquidSpecificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq'))
        specificVolume = quality*vaporSpecificVolume + (1.0 - quality)*liquidSpecificVolume
    elif region == 5:
        specificVolume = Region5.v5_pt(pressure, Region5.t5_ps(pressure, entropy))

    if englishUnits and specificVolume != Constants._errorValue:
        specificVolume = Convert.fromSIUnit(specificVolume, 'specific volume')

    return specificVolume

def rhoV_p(pressure):
    return 1.0/vV_p(pressure)

def rhoL_p(pressure):
    return 1.0/vL_p(pressure)

def rhoL_T(temperature):
    return 1.0/vL_T(temperature)

def rhoV_T(temperature):
    return 1.0/vV_T(temperature)

def rho_pT(pressure, temperature):
    return 1.0/v_pT(pressure, temperature)

def rho_ph(pressure, enthalpy):
    return 1.0/v_ph(pressure, enthalpy)

def rho_ps(pressure, entropy):
    return 1.0/v_ps(pressure, entropy)

def sV_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    entropy = Constants._errorValue

    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        if pressure < Constants._pressureSubDomain:
            entropy = Region2.s2_pt(pressure, Region4.t4_p(pressure))
        else:
            specificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap'))
            tsatt = Region4.t4_p(pressure)
            entropy = Region3.s3_rhot(1.0/specificVolume, tsatt)
        if englishUnits:
            entropy = Convert.fromSIUnit(entropy, 'entropy')
        return entropy
    else:
        return Constants._errorValue

def sL_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    entropy = Constants._errorValue

    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        if pressure < Constants._pressureSubDomain:
            entropy = Region1.s1_pt(pressure, Region4.t4_p(pressure))
        else:
            specificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq'))
            tsatt = Region4.t4_p(pressure)
            entropy = Region3.s3_rhot(1.0/specificVolume, tsatt)
        if englishUnits:
            entropy = Convert.fromSIUnit(entropy, 'entropy')
        return entropy
    else:
        return Constants._errorValue

def sV_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    entropy = Constants._errorValue

    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        if temperature <= Constants._temperatureSubDomain:
            entropy = Region2.s2_pt(Region4.p4_t(temperature), temperature)
        else:
            psatt = Region4.p4_t(temperature)
            specificVolume = Region3.v3_ph(psatt, Region4.h4_p(psatt, 'vap'))
            entropy = Region3.s3_rhot(1.0/specificVolume, temperature)

        if englishUnits:
            entropy = Convert.fromSIUnit(entropy, 'entropy')
        return entropy
    else:
        return Constants._errorValue

def sL_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    entropy = Constants._errorValue

    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        if temperature <= Constants._temperatureSubDomain:
            entropy = Region1.s1_pt(Region4.p4_t(temperature), temperature)
        else:
            psatt = Region4.p4_t(temperature)
            specificVolume = Region3.v3_ph(psatt, Region4.h4_p(psatt, 'liq'))
            entropy = Region3.s3_rhot(1.0/specificVolume, temperature)

        if englishUnits:
            entropy = Convert.fromSIUnit(entropy, 'entropy')
        return entropy
    else:
        return Constants._errorValue

def s_pT(pressure, temperature):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    region = Regions.region_pt(pressure, temperature)
    if region is None or region == 4:
        return Constants._errorValue

    entropy = Constants._errorValue
    if region == 1:
        entropy = Region1.s1_pt(pressure, temperature)
    elif region == 2:
        entropy = Region2.s2_pt(pressure, temperature)
    elif region == 3:
        specificVolume = Region3.v3_ph(pressure, Region3.h3_pt(pressure, temperature))
        entropy = Region3.s3_rhot(1.0/specificVolume, temperature)
    elif region == 5:
        entropy = Region5.s5_pt(pressure, temperature)

    if englishUnits:
        entropy = Convert.fromSIUnit(entropy, 'entropy')
    return entropy

def s_ph(pressure, enthalpy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')

    region = Regions.region_ph(pressure, enthalpy)
    if region is None: return Constants._errorValue

    entropy = Constants._errorValue
    if region == 1:
        entropy = Region1.s1_pt(pressure, Region1.t1_ph(pressure, enthalpy))
    elif region == 2:
        entropy = Region2.s2_pt(pressure, Region2.t2_ph(pressure, enthalpy))
    elif region == 3:
        entropy = Region3.s3_rhot(1.0/Region3.v3_ph(pressure, enthalpy), Region3.t3_ph(pressure, enthalpy))
    elif region == 4:
        tsatt = Region4.t4_p(pressure)
        quality = Region4.x4_ph(pressure, enthalpy)
        entropyVapor, entropyLiquid = 0.0, 0.0
        if pressure < Constants._pressureSubDomain:
            entropyVapor = Region2.s2_pt(pressure, tsatt)
            entropyLiquid = Region1.s1_pt(pressure, tsatt)
        else:
            specificVolumeVapor = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap'))
            entropyVapor = Region3.s3_rhot(1.0/specificVolumeVapor, tsatt)
            specificVolumeLiq = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq'))
            entropyLiquid = Region3.s3_rhot(1.0/specificVolumeLiq, tsatt)
        entropy = quality*entropyVapor + (1.0 - quality)*entropyLiquid
    elif region == 5:
        entropy = Region5.s5_pt(pressure, Region5.t5_ph(pressure, enthalpy))

    if englishUnits:
        entropy = Convert.fromSIUnit(entropy, 'entropy')
    return entropy

#Rem Function s_pv(ByVal p As Double, ByVal v As Double) As Double #51
#Rem Dim rho As Double
#Rem Dim h As Double
#Rem rho = 1 / v
#Rem h = h_prho(p, rho)
#Rem s_pv = s_ph(p, h)
#Rem End Function

#Rem 'Function s_Tv(ByVal T As Double, ByVal v As Double) As Double #52
#Rem 'Dim p As Double
#Rem 'p = p_Tv(T, v)
#Rem 's_Tv = s_pv(p, v)
#Rem 'End Function

def uV_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)

    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        internalEnergy = Constants._errorValue
        tsatt = Region4.t4_p(pressure)
        if pressure < Constants._pressureSubDomain:
            internalEnergy = Region2.u2_pt(pressure, tsatt)
        else:
            specificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap'))
            internalEnergy = Region3.u3_rhot(1.0/specificVolume, tsatt)
        if englishUnits:
            internalEnergy = Convert.fromSIUnit(internalEnergy, 'enthalpy')
        return internalEnergy
    else:
        return Constants._errorValue

def uL_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)

    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        internalEnergy = Constants._errorValue
        tsatt = Region4.t4_p(pressure)
        if pressure < Constants._pressureSubDomain:
            internalEnergy = Region1.u1_pt(pressure, tsatt)
        else:
            specificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq'))
            internalEnergy = Region3.u3_rhot(1.0/specificVolume, tsatt)
        if englishUnits:
            internalEnergy = Convert.fromSIUnit(internalEnergy, 'enthalpy')
        return internalEnergy
    else:
        return Constants._errorValue

def uV_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        internalEnergy = Constants._errorValue
        psatt = Region4.p4_t(temperature)
        if temperature <= Constants._temperatureSubDomain:
            internalEnergy = Region2.u2_pt(psatt, temperature)
        else:
            specificVolume = Region3.v3_ph(psatt, Region4.h4_p(psatt, 'vap'))
            internalEnergy = Region3.u3_rhot(1.0/specificVolume, temperature)
        if englishUnits:
            internalEnergy = Convert.fromSIUnit(internalEnergy, 'enthalpy')
        return internalEnergy
    else:
        return Constants._errorValue

def uL_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        internalEnergy = Constants._errorValue
        psatt = Region4.p4_t(temperature)
        if temperature <= Constants._temperatureSubDomain:
            internalEnergy = Region1.u1_pt(psatt, temperature)
        else:
            specificVolume = Region3.v3_ph(psatt, Region4.h4_p(psatt, 'liq'))
            internalEnergy = Region3.u3_rhot(1.0/specificVolume, temperature)
        if englishUnits:
            internalEnergy = Convert.fromSIUnit(internalEnergy, 'enthalpy')
        return internalEnergy
    else:
        return Constants._errorValue

def u_pT(pressure, temperature):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    region = Regions.region_pt(pressure, temperature)
    if region is None or region == 4: return Constants._errorValue

    internalEnergy = Constants._errorValue

    if region == 1:
        internalEnergy = Region1.u1_pt(pressure, temperature)
    elif region == 2:
        internalEnergy = Region2.u2_pt(pressure, temperature)
    elif region == 3:
        specificVolume = Region3.v3_ph(pressure, Region3.h3_pt(pressure, temperature))
        internalEnergy = Region3.u3_rhot(1.0/specificVolume, temperature)
    elif region == 5:
        internalEnergy = Region5.u5_pt(pressure, temperature)

    if englishUnits:
        internalEnergy = Convert.fromSIUnit(internalEnergy, 'enthalpy')

    return internalEnergy

def u_ph(pressure, enthalpy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')

    region = Regions.region_ph(pressure, enthalpy)
    if region is None: return Constants._errorValue

    internalEnergy = Constants._errorValue
    if region == 1:
        internalEnergy = Region1.u1_pt(pressure, Region1.t1_ph(pressure, enthalpy))
    elif region == 2:
        internalEnergy = Region2.u2_pt(pressure, Region2.t2_ph(pressure, enthalpy))
    elif region == 3:
        specificVolume = Region3.v3_ph(pressure, enthalpy)
        internalEnergy = Region3.u3_rhot(1.0/specificVolume, Region3.t3_ph(pressure, enthalpy))
    elif region == 4:
        tsatt = Region4.t4_p(pressure)
        quality = Region4.x4_ph(pressure, enthalpy)
        vaporEnergy, liquidEnergy = 0.0, 0.0
        if pressure < Constants._pressureSubDomain:
            vaporEnergy = Region2.u2_pt(pressure, tsatt)
            liquidEnergy = Region1.u1_pt(pressure, tsatt)
        else:
            vaporSpecificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap'))
            vaporEnergy = Region3.u3_rhot(1.0/vaporSpecificVolume, tsatt)
            liquidSpecificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq'))
            liquidEnergy = Region3.u3_rhot(1.0/liquidSpecificVolume, tsatt)
        internalEnergy = quality*vaporEnergy + (1.0 - quality)*liquidEnergy
    elif region == 5:
        tsatt = Region5.t5_ph(pressure, enthalpy)
        internalEnergy = Region5.u5_pt(pressure, tsatt)

    if englishUnits:
        internalEnergy = Convert.fromSIUnit(internalEnergy, 'enthalpy')
    return internalEnergy

def u_ps(pressure, entropy):
    pressure, entropy = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits), float(entropy)
    if englishUnits:
        entropy = Convert.toSIUnit(entropy, 'entropy')

    region = Regions.region_ps(pressure, entropy)
    if region is None: return Constants._errorValue

    internalEnergy = Constants._errorValue
    if region == 1:
        internalEnergy = Region1.u1_pt(pressure, Region1.t1_ps(pressure, entropy))
    elif region == 2:
        internalEnergy = Region2.u2_pt(pressure, Region2.t2_ps(pressure, entropy))
    elif region == 3:
        specificVolume = Region3.v3_ps(pressure, entropy)
        internalEnergy = Region3.u3_rhot(1.0/specificVolume, Region3.t3_ps(pressure, entropy))
    elif region == 4:
        tsatt = Region4.t4_p(pressure)
        quality = Region4.x4_ps(pressure, entropy)
        vaporEnergy, liquidEnergy = 0.0, 0.0
        if pressure < Constants._pressureSubDomain:
            liquidEnergy = Region1.u1_pt(pressure, tsatt)
            vaporEnergy = Region2.u2_pt(pressure, tsatt)
        else:
            vaporSpecificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap'))
            vaporEnergy = Region3.u3_rhot(1.0/vaporSpecificVolume, tsatt)
            liquidSpecificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq'))
            liquidEnergy = Region3.u3_rhot(1.0/liquidSpecificVolume, tsatt)
        internalEnergy = quality*vaporEnergy + (1.0 - quality)*liquidEnergy
    elif region == 5:
        internalEnergy = Region5.u5_pt(pressure, Region5.t5_ps(pressure, entropy))

    if englishUnits:
        internalEnergy = Convert.fromSIUnit(internalEnergy, 'enthalpy')
    return internalEnergy

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

def cpV_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)

    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        specificHeat = Constants._errorValue
        tsatt = Region4.t4_p(pressure)
        if pressure < Constants._pressureSubDomain:
            specificHeat = Region2.cp2_pt(pressure, tsatt)
        else:
            specificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap'))
            specificHeat = Region3.cp3_rhot(1.0/specificVolume, tsatt)
        if englishUnits:
            specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
        return specificHeat
    else:
        return Constants._errorValue

def cpL_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)

    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        specificHeat = Constants._errorValue
        tsatt = Region4.t4_p(pressure)
        if pressure < Constants._pressureSubDomain:
            specificHeat = Region1.cp1_pt(pressure, tsatt)
        else:
            specificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq'))
            specificHeat = Region3.cp3_rhot(1.0/specificVolume, tsatt)
        if englishUnits:
            specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
        return specificHeat
    else:
        return Constants._errorValue

def cpV_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        specificHeat = Constants._errorValue
        psatt = Region4.p4_t(temperature)
        if temperature <= Constants._temperatureSubDomain:
            specificHeat = Region2.cp2_pt(psatt, temperature)
        else:
            specificVolume = Region3.v3_ph(psatt, Region4.h4_p(psatt, 'vap'))
            specificHeat = Region3.cp3_rhot(1.0/specificVolume, temperature)

        if englishUnits:
            specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
        return specificHeat
    else:
        return Constants._errorValue

def cpL_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        specificHeat = Constants._errorValue
        psatt = Region4.p4_t(temperature)
        if temperature <= Constants._temperatureSubDomain:
            specificHeat = Region1.cp1_pt(psatt, temperature)
        else:
            specificVolume = Region3.v3_ph(psatt, Region4.h4_p(psatt, 'liq'))
            specificHeat = Region3.cp3_rhot(1.0/specificVolume, temperature)

        if englishUnits:
            specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
        return specificHeat
    else:
        return Constants._errorValue

def cp_pT(pressure, temperature):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    region = Regions.region_pt(pressure, temperature)
    if region is None or region == 4: return Constants._errorValue

    specificHeat = Constants._errorValue
    if region == 1:
        specificHeat = Region1.cp1_pt(pressure, temperature)
    elif region == 2:
        specificHeat = Region2.cp2_pt(pressure, temperature)
    elif region == 3:
        specificVolume = Region3.v3_ph(pressure, Region3.h3_pt(pressure, temperature))
        specificHeat = Region3.cp3_rhot(1.0/specificVolume, temperature)
    elif region == 5:
        specificHeat = Region5.cp5_pt(pressure, temperature)

    if englishUnits:
        specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
    return specificHeat

def cp_ph(pressure, enthalpy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')

    region = Regions.region_ph(pressure, enthalpy)
    if region is None or region == 4: return Constants._errorValue

    specificHeat = Constants._errorValue
    if region == 1:
        specificHeat = Region1.cp1_pt(pressure, Region1.t1_ph(pressure, enthalpy))
    elif region == 2:
        specificHeat = Region2.cp2_pt(pressure, Region2.t2_ph(pressure, enthalpy))
    elif region == 3:
        specificVolume = Region3.v3_ph(pressure, enthalpy)
        specificHeat = Region3.cp3_rhot(1.0/specificVolume, Region3.t3_ph(pressure, enthalpy))
    elif region == 5:
        specificHeat = Region5.cp5_pt(pressure, Region5.t5_ph(pressure, enthalpy))

    if englishUnits:
        specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
    return specificHeat

def cp_ps(pressure, entropy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        entropy = Convert.toSIUnit(entropy, 'entropy')

    region = Regions.region_ps(pressure, entropy)
    if region is None or region == 4: return Constants._errorValue

    specificHeat = Constants._errorValue
    if region == 1:
        specificHeat = Region1.cp1_pt(pressure, Region1.t1_ps(pressure, entropy))
    elif region == 2:
        specificHeat = Region2.cp2_pt(pressure, Region2.t2_ps(pressure, entropy))
    elif region == 3:
        specificVolume = Region3.v3_ps(pressure, entropy)
        specificHeat = Region3.cp3_rhot(1.0/specificVolume, Region3.t3_ps(pressure, entropy))
    elif region == 5:
        specificHeat = Region5.cp5_pt(pressure, Region5.t5_ps(pressure, entropy))

    if englishUnits:
        specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
    return specificHeat

def cvV_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)

    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        specificHeat = Constants._errorValue
        tsatt = Region4.t4_p(pressure)
        if pressure < Constants._pressureSubDomain:
            specificHeat = Region2.cv2_pt(pressure, tsatt)
        else:
            specificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap'))
            specificHeat = Region3.cv3_rhot(1.0/specificVolume, tsatt)
        if englishUnits:
            specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
        return specificHeat
    else:
        return Constants._errorValue

def cvL_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)

    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        specificHeat = Constants._errorValue
        tsatt = Region4.t4_p(pressure)
        if pressure < Constants._pressureSubDomain:
            specificHeat = Region1.cv1_pt(pressure, tsatt)
        else:
            specificVolume = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq'))
            specificHeat = Region3.cv3_rhot(1.0/specificVolume, tsatt)
        if englishUnits:
            specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
        return specificHeat
    else:
        return Constants._errorValue

def cvV_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        specificHeat = Constants._errorValue
        psatt = Region4.p4_t(temperature)
        if temperature <= Constants._temperatureSubDomain:
            specificHeat = Region2.cv2_pt(psatt, temperature)
        else:
            specificVolume = Region3.v3_ph(psatt, Region4.h4_p(psatt, 'vap'))
            specificHeat = Region3.cv3_rhot(1.0/specificVolume, temperature)

        if englishUnits:
            specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
        return specificHeat
    else:
        return Constants._errorValue

def cvL_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        specificHeat = Constants._errorValue
        psatt = Region4.p4_t(temperature)
        if temperature <= Constants._temperatureSubDomain:
            specificHeat = Region1.cv1_pt(psatt, temperature)
        else:
            specificVolume = Region3.v3_ph(psatt, Region4.h4_p(psatt, 'liq'))
            specificHeat = Region3.cv3_rhot(1.0/specificVolume, temperature)

        if englishUnits:
            specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
        return specificHeat
    else:
        return Constants._errorValue

def cv_pT(pressure, temperature):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    region = Regions.region_pt(pressure, temperature)
    if region is None or region == 4: return Constants._errorValue

    specificHeat = Constants._errorValue
    if region == 1:
        specificHeat = Region1.cv1_pt(pressure, temperature)
    elif region == 2:
        specificHeat = Region2.cv2_pt(pressure, temperature)
    elif region == 3:
        specificVolume = Region3.v3_ph(pressure, Region3.h3_pt(pressure, temperature))
        specificHeat = Region3.cv3_rhot(1.0/specificVolume, temperature)
    elif region == 5:
        specificHeat = Region5.cv5_pt(pressure, temperature)

    if englishUnits:
        specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
    return specificHeat

def cv_ph(pressure, enthalpy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')

    region = Regions.region_ph(pressure, enthalpy)
    if region is None or region == 4: return Constants._errorValue

    specificHeat = Constants._errorValue
    if region == 1:
        specificHeat = Region1.cv1_pt(pressure, Region1.t1_ph(pressure, enthalpy))
    elif region == 2:
        specificHeat = Region2.cv2_pt(pressure, Region2.t2_ph(pressure, enthalpy))
    elif region == 3:
        specificVolume = Region3.v3_ph(pressure, enthalpy)
        specificHeat = Region3.cv3_rhot(1.0/specificVolume, Region3.t3_ph(pressure, enthalpy))
    elif region == 5:
        specificHeat = Region5.cv5_pt(pressure, Region5.t5_ph(pressure, enthalpy))

    if englishUnits:
        specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
    return specificHeat

def cv_ps(pressure, entropy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        entropy = Convert.toSIUnit(entropy, 'entropy')

    region = Regions.region_ps(pressure, entropy)
    if region is None or region == 4: return Constants._errorValue

    specificHeat = Constants._errorValue
    if region == 1:
        specificHeat = Region1.cv1_pt(pressure, Region1.t1_ps(pressure, entropy))
    elif region == 2:
        specificHeat = Region2.cv2_pt(pressure, Region2.t2_ps(pressure, entropy))
    elif region == 3:
        specificVolume = Region3.v3_ps(pressure, entropy)
        specificHeat = Region3.cv3_rhot(1.0/specificVolume, Region3.t3_ps(pressure, entropy))
    elif region == 5:
        specificHeat = Region5.cv5_pt(pressure, Region5.t5_ps(pressure, entropy))

    if englishUnits:
        specificHeat = Convert.fromSIUnit(specificHeat, 'entropy')
    return specificHeat

def wV_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)

    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        if pressure < Constants._pressureSubDomain:
            speedOfSound = Region2.w2_pt(pressure, Region4.t4_p(pressure))
        else:
            density = 1.0/Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap'))
            speedOfSound = Region3.w3_rhot(density, Region4.t4_p(pressure))
        if englishUnits:
            speedOfSound = Convert.fromSIUnit(speedOfSound, 'velocity')
        return speedOfSound
    else:
        return Constants._errorValue

def wL_p(pressure):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        if pressure < Constants._pressureSubDomain:
            speedOfSound = Region1.w1_pt(pressure, Region4.t4_p(pressure))
        else:
            density = 1.0/Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq'))
            speedOfSound = Region3.w3_rhot(density, Region4.t4_p(pressure))
        if englishUnits:
            speedOfSound = Convert.fromSIUnit(speedOfSound, 'velocity')
        return speedOfSound
    else:
        return Constants._errorValue

def wV_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        if temperature < Constants._temperatureSubDomain:
            speedOfSound = Region2.w2_pt(Region4.p4_t(temperature), temperature)
        else:
            psatt = Region4.p4_t(temperature)
            density = 1.0/Region3.v3_ph(psatt, Region4.h4_p(psatt, 'vap'))
            speedOfSound = Region3.w3_rhot(density, temperature)
        if englishUnits:
            speedOfSound = Convert.fromSIUnit(speedOfSound, 'velocity')
        return speedOfSound
    else:
        return Constants._errorValue

def wL_T(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        if temperature < Constants._temperatureSubDomain:
            speedOfSound = Region1.w1_pt(Region4.p4_t(temperature), temperature)
        else:
            psatt = Region4.p4_t(temperature)
            density = 1.0/Region3.v3_ph(psatt, Region4.h4_p(psatt, 'liq'))
            speedOfSound = Region3.w3_rhot(density, temperature)
        if englishUnits:
            speedOfSound = Convert.fromSIUnit(speedOfSound, 'velocity')
        return speedOfSound
    else:
        return Constants._errorValue

def w_pT(pressure, temperature):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    region = Regions.region_pt(pressure, temperature)
    if region is None or region == 4: return Constants._errorValue

    if region == 1:
        speedOfSound = Region1.w1_pt(pressure, temperature)
    elif region == 2:
        speedOfSound = Region2.w2_pt(pressure, temperature)
    elif region == 3:
        density = 1.0/Region3.v3_ph(pressure, Region3.h3_pt(pressure, temperature))
        speedOfSound = Region3.w3_rhot(density, temperature)
    elif region == 5:
        speedOfSound = Region5.w5_pt(pressure, temperature)

    if englishUnits:
        speedOfSound = Convert.fromSIUnit(speedOfSound, 'velocity')
    return speedOfSound

def w_ph(pressure, enthalpy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')

    region = Regions.region_ph(pressure, enthalpy)
    if region is None or region == 4: return Constants._errorValue

    if region == 1:
        speedOfSound = Region1.w1_pt(pressure, Region1.t1_ph(pressure, enthalpy))
    elif region == 2:
        speedOfSound = Region2.w2_pt(pressure, Region2.t2_ph(pressure, enthalpy))
    elif region == 3:
        density = 1.0/Region3.v3_ph(pressure, enthalpy)
        speedOfSound = Region3.w3_rhot(density, Region3.t3_ph(pressure, enthalpy))
    elif region == 5:
        speedOfSound = Region5.w5_pt(pressure, Region5.t5_ph(pressure, enthalpy))

    if englishUnits:
        speedOfSound = Convert.fromSIUnit(speedOfSound, 'velocity')
    return speedOfSound

def w_ps(pressure, entropy):
    pressure = Convert.toSIUnit(float(pressure), 'pressure', englishUnits=englishUnits)
    if englishUnits:
        entropy = Convert.toSIUnit(float(entropy), 'entropy')

    region = Regions.region_ps(pressure, entropy)
    if region is None or region == 4: return Constants._errorValue

    if region == 1:
        speedOfSound = Region1.w1_pt(pressure, Region1.t1_ps(pressure, entropy))
    elif region == 2:
        speedOfSound = Region2.w2_pt(pressure, Region2.t2_ps(pressure, entropy))
    elif region == 3:
        density = 1.0/Region3.v3_ps(pressure, entropy)
        speedOfSound = Region3.w3_rhot(density, Region3.t3_ps(pressure, entropy))
    elif region == 5:
        speedOfSound = Region5.w5_pt(pressure, Region5.t5_ps(pressure, entropy))

    if englishUnits:
        speedOfSound = Convert.fromSIUnit(speedOfSound, 'velocity')
    return speedOfSound

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

def kappa_pT(pressure, temperature):
    cp = cp_pT(pressure, temperature)
    cv = cv_pT(pressure, temperature)
    return cp/cv

def kappa_ph(pressure, enthalpy):
    cp = cp_ph(pressure, enthalpy)
    cv = cv_ph(pressure, enthalpy)
    return cp/cv

def st_t(temperature):
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    surfaceTension = surfaceTension_T(temperature)
    if surfaceTension == Constants._errorValue:
        return Constants._errorValue
    if englishUnits:
        surfaceTension = Convert.fromSIUnit(surfaceTension, 'surface tension')
    return surfaceTension

def st_p(pressure):
    temperature = Tsat_p(pressure)
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    if temperature == Constants._errorValue:
        return Constants._errorValue

    surfaceTension = surfaceTension_T(temperature)

    if surfaceTension == Constants._errorValue:
        return Constants._errorValue

    if englishUnits:
        surfaceTension = Convert.fromSIUnit(surfaceTension, 'surface tension')
    return surfaceTension

def tcL_p(pressure):
    tsatt = Tsat_p(pressure)
    specificVolume = vL_p(pressure)

    if Constants._errorValue in (tsatt, specificVolume):
        return Constants._errorValue

    return _tc_pTrho_wrapper(pressure, tsatt, specificVolume)

def tcV_p(pressure):
    tsatt = Tsat_p(pressure)
    specificVolume = vV_p(pressure)

    if Constants._errorValue in (tsatt, specificVolume):
        return Constants._errorValue

    return _tc_pTrho_wrapper(pressure, tsatt, specificVolume)

def tcL_T(temperature):
    psatt = Psat_T(temperature)
    specificVolume = vL_T(temperature)

    if Constants._errorValue in (psatt, specificVolume):
        return Constants._errorValue

    return _tc_pTrho_wrapper(psatt, temperature, specificVolume)

def tcV_T(temperature):
    psatt = Psat_T(temperature)
    specificVolume = vV_T(temperature)

    if Constants._errorValue in (psatt, specificVolume):
        return Constants._errorValue

    return _tc_pTrho_wrapper(psatt, temperature, specificVolume)

def tc_pT(pressure, temperature):
    specificVolume = v_pT(pressure, temperature)
    return _tc_pTrho_wrapper(pressure, temperature, specificVolume)

def tc_ph(pressure, enthalpy):
    specificVolume = v_ph(pressure, enthalpy)
    temperature = T_ph(pressure, enthalpy)
    return _tc_pTrho_wrapper(pressure, temperature, specificVolume)

def tc_hs(enthalpy, entropy):
    enthalpy, entropy = float(enthalpy), float(entropy)
    pressure = P_hs(enthalpy, entropy)
    specificVolume = v_ph(pressure, enthalpy)
    temperature = T_ph(pressure, enthalpy)

    if Constants._errorValue in (pressure, temperature, specificVolume):
        return Constants._errorValue

    return _tc_pTrho_wrapper(pressure, temperature, specificVolume)

def _tc_pTrho_wrapper(pressure, temperature, specificVolume):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    if englishUnits:
        specificVolume = Convert.toSIUnit(specificVolume, 'specific volume')

    thermalConductivity = tc_pTrho(pressure, temperature, 1.0/specificVolume)

    if thermalConductivity == Constants._errorValue:
        return Constants._errorValue

    if englishUnits:
        thermalConductivity = Convert.fromSIUnit(thermalConductivity, 'thermal conductivity')

    return thermalConductivity

def x_ph(pressure, enthalpy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')
    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        return Region4.x4_ph(pressure, enthalpy)
    else:
        return Constants._errorValue

def x_ps(pressure, entropy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        entropy = Convert.toSIUnit(entropy, 'entropy')
    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        return Region4.x4_ps(pressure, entropy)
    else:
        return Constants._errorValue

def vx_ph(pressure, enthalpy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')
    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        quality = Region4.x4_ph(pressure, enthalpy)
        if pressure < Constants._pressureSubDomain:
            tsatt = Region4.t4_p(pressure)
            specificVolumeLiquid = Region1.v1_pt(pressure, tsatt)
            specificVolumeVapor = Region2.v2_pt(pressure, tsatt)
        else:
            specificVolumeLiquid = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq'))
            specificVolumeVapor = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap'))
        return quality*specificVolumeVapor/(quality*specificVolumeVapor + (1.0 - quality)*specificVolumeLiquid)
    else:
        return Constants._errorValue

def vx_ps(pressure, entropy):
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        entropy = Convert.toSIUnit(entropy, 'entropy')
    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        quality = Region4.x4_ps(pressure, entropy)
        if pressure < Constants._pressureSubDomain:
            tsatt = Region4.t4_p(pressure)
            specificVolumeLiquid = Region1.v1_pt(pressure, tsatt)
            specificVolumeVapor = Region2.v2_pt(pressure, tsatt)
        else:
            specificVolumeLiquid = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq'))
            specificVolumeVapor = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap'))
        return quality*specificVolumeVapor/(quality*specificVolumeVapor + (1.0 - quality)*specificVolumeLiquid)
    else:
        return Constants._errorValue

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

def tc_pTrho(pressure, temperature, density):
    '''Revised release on the IAPS Formulation 1985 for the Thermal Conductivity of ordinary water IAPWS September 1998 Page 8'''
    if temperature < 0.0 or pressure < Constants._pressureMin \
        or temperature > 800.0 or pressure > 400.0 \
        or not((pressure <= 100.0 and temperature <= 373.15) \
        or (pressure <= 150.0 and temperature <= 673.15) \
        or (pressure <= 200.0 and temperature <= 523.15) \
        or (pressure <= 400.0 and temperature <= 398.15)):
        return Constants._errorValue
    tPrime = temperature/Constants._tp
    rhoPrime = density/Constants._rhop
    tc0 = tPrime**0.5 * (0.0102811 + 0.0299621*tPrime + 0.0156146*tPrime**2 - 0.00422464*tPrime**3)
    tc1 = -0.39707 + 0.400302*rhoPrime + 1.06 * math.exp(-0.171587*(rhoPrime + 2.39219)**2)
    dT = abs(tPrime - 1.0) + 0.00308976
    Q = 2.0 + 0.0822994/dT**(3.0/5.0)
    if tPrime >= 1.0:
        s = 1.0/tPrime
    else:
        s = 10.0932/dT**(3.0/5.0)
    tc2 = (0.0701309/tPrime**10 + 0.011852)*rhoPrime**(9.0/5.0)*math.exp(0.642857*(1.0-rhoPrime**(14.0/5.0)))\
       + 0.00169937*s*rhoPrime**Q*math.exp((Q/(1.0 + Q))*(1 - rhoPrime**(1.0 + Q)))\
      - 1.02*math.exp(-4.11717*tPrime**(3.0/2.0) - 6.17937/rhoPrime**5)
    return tc0 + tc1 + tc2

def surfaceTension_T(temperature):
    '''IAPWS Release on Surface Tension of Ordinary Water Substance, September 1994'''
    if temperature < 0.01 or temperature > Constants._tc:
        return Constants._errorValue
    tau = 1.0 - temperature/Constants._tc
    return 0.2358*tau**1.256*(1.0 - 0.625*tau)
