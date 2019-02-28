# -*- coding: utf-8 -*-
'''
Region 4 functions
'''
import math

import numpy as np
import scipy
from scipy import optimize

try:
    import Constants
    import Region1
    import Region2
    import Region3
except ImportError:
    from . import Constants
    from . import Region1
    from . import Region2
    from . import Region3

def p4_t(temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    Section 8.1 The Saturation-Pressure Equation Eq 30, Page 33'''
    teta = temperature - 0.23855557567849/(temperature - 650.17534844798)
    a = teta**2 + 1167.0521452767*teta - 724213.16703206
    b = -17.073846940092*teta**2 + 12020.82470247*teta - 3232555.0322333
    c = 14.91510861353*teta**2 - 4823.2657361591*teta + 405113.40542057
    return (2.0*c/(-b + math.sqrt(b**2 - 4*a*c)))**4

def t4_p(pressure):
    ''' Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    Section 8.2 The Saturation-Temperature Equation
    Eq 31, Page 34 '''
    beta = pressure**0.25
    e = beta**2 - 17.073846940092*beta + 14.91510861353
    f = 1167.0521452767*beta**2 + 12020.82470247*beta - 4823.2657361591
    g = -724213.16703206*beta**2 - 3232555.0322333*beta + 405113.40542057
    d = 2*g/(-f - (f**2 - 4*e*g)**0.5)
    return (650.17534844798 + d - ((650.17534844798 + d)**2 - 4*(-0.23855557567849 + 650.17534844798*d))**0.5)/2

def h4_s(entropy):
    ''' Supplementary Release on Backward Equations ( ) , p h s for Region 3,Equations as a Function of h and s for the Region Boundaries, and an Equation( ) sat , T hs for Region 4 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam
    4 Equations for Region Boundaries Given Enthalpy and Entropy See picture page 14'''
    enthalpy = 0.0
    if entropy > -0.0001545495919 and entropy <= 3.77828134:
        # hL1_s Eq 3,Table 9,Page 16
        i = np.array([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 7, 8, 12, 12, 14, 14, 16, 20, 20, 22, 24, 28, 32, 32])
        j = np.array([14, 36, 3, 16, 0, 5, 4, 36, 4, 16, 24, 18, 24, 1, 4, 2, 4, 1, 22, 10, 12, 28, 8, 3, 0, 6, 8])
        n = np.array([0.332171191705237, 6.11217706323496E-04, -8.82092478906822, -0.45562819254325, -2.63483840850452E-05, -22.3949661148062, -4.28398660164013, -0.616679338856916, -14.682303110404, 284.523138727299, -113.398503195444, 1156.71380760859, 395.551267359325, -1.54891257229285, 19.4486637751291, -3.57915139457043, -3.35369414148819, -0.66442679633246, 32332.1885383934, 3317.66744667084, -22350.1257931087, 5739538.75852936, 173.226193407919, -3.63968822121321E-02, 8.34596332878346E-07, 5.03611916682674, 65.5444787064505])
        sigma = entropy/3.8
        eta = sum(n*(sigma - 1.09)**i*(sigma + 0.0000366)**j)
        enthalpy = eta*1700.0
    elif entropy > 3.77828134 and entropy <= 4.41202148223476:
        # hL3_s Eq 4,Table 10,Page 16
        i = np.array([0, 0, 0, 0, 2, 3, 4, 4, 5, 5, 6, 7, 7, 7, 10, 10, 10, 32, 32])
        j = np.array([1, 4, 10, 16, 1, 36, 3, 16, 20, 36, 4, 2, 28, 32, 14, 32, 36, 0, 6])
        n = np.array([0.822673364673336, 0.181977213534479, -0.011200026031362, -7.46778287048033E-04, -0.179046263257381, 4.24220110836657E-02, -0.341355823438768, -2.09881740853565, -8.22477343323596, -4.99684082076008, 0.191413958471069, 5.81062241093136E-02, -1655.05498701029, 1588.70443421201, -85.0623535172818, -31771.4386511207, -94589.0406632871, -1.3927384708869E-06, 0.63105253224098])
        sigma = entropy/3.8
        eta = sum(n*(sigma - 1.09)**i*(sigma + 0.0000366)**j)
        enthalpy = eta*1700.0
    elif entropy > 4.41202148223476 and entropy <= 5.85:
        # Section 4.4 Equations ( ) 2ab " h s and ( ) 2c3b "h s for the Saturated Vapor Line Page 19, Eq 5 hV2c3b_s(s)
        i = np.array([0, 0, 0, 1, 1, 5, 6, 7, 8, 8, 12, 16, 22, 22, 24, 36])
        j = np.array([0, 3, 4, 0, 12, 36, 12, 16, 2, 20, 32, 36, 2, 32, 7, 20])
        n = np.array([1.04351280732769, -2.27807912708513, 1.80535256723202, 0.420440834792042, -105721.24483466, 4.36911607493884E+24, -328032702839.753, -6.7868676080427E+15, 7439.57464645363, -3.56896445355761E+19, 1.67590585186801E+31, -3.55028625419105E+37, 396611982166.538, -4.14716268484468E+40, 3.59080103867382E+18, -1.16994334851995E+40])
        sigma = entropy/5.9
        eta = sum(n*(sigma - 1.02)**i*(sigma - 0.726)**j)
        enthalpy = 2800.0*eta**4
    elif entropy > 5.85 and entropy <= 9.155759395:
        # Section 4.4 Equations ( ) 2ab " h s and ( ) 2c3b "h s for the Saturated Vapor Line Page 20, Eq 6
        i = np.array([1, 1, 2, 2, 4, 4, 7, 8, 8, 10, 12, 12, 18, 20, 24, 28, 28, 28, 28, 28, 32, 32, 32, 32, 32, 36, 36, 36, 36, 36])
        j = np.array([8, 24, 4, 32, 1, 2, 7, 5, 12, 1, 0, 7, 10, 12, 32, 8, 12, 20, 22, 24, 2, 7, 12, 14, 24, 10, 12, 20, 22, 28])
        n = np.array([-524.581170928788, -9269472.18142218, -237.385107491666, 21077015581.2776, -23.9494562010986, 221.802480294197, -5104725.33393438, 1249813.96109147, 2000084369.96201, -815.158509791035, -157.612685637523, -11420042233.2791, 6.62364680776872E+15, -2.27622818296144E+18, -1.71048081348406E+31, 6.60788766938091E+15, 1.66320055886021E+22, -2.18003784381501E+29, -7.87276140295618E+29, 1.51062329700346E+31, 7957321.70300541, 1.31957647355347E+15, -3.2509706829914E+23, -4.18600611419248E+25, 2.97478906557467E+34, -9.53588761745473E+19, 1.66957699620939E+24, -1.75407764869978E+32, 3.47581490626396E+34, -7.10971318427851E+38])
        sigma = entropy/5.21, entropy/9.2
        eta = sum(n*(1.0/sigma[0] - 0.513)**i*(sigma[1] - 0.524)**j)
        enthalpy = 2800.0*math.exp(eta)
    else:
        raise ArithmeticError('Entropy needs to be between {} and {} J/kgK'.format(-0.0001545495919, 9.155759395))

    return enthalpy

def h4_p(pressure, phase):
    pressureMin, pressureMax = 0.000611657, 22.06395
    enthalpy = Constants._errorValue
    if phase not in ['liq', 'vap']:
        raise AttributeError('phase argument needs to be \'liq\' or \'vap\'')

    if pressure > pressureMin and pressure <= pressureMax:
        ts = t4_p(pressure)
        if pressure < 16.529:
            if phase is 'liq':
                enthalpy = Region1.h1_pt(pressure, ts)
            else:
                enthalpy = Region2.h2_pt(pressure, ts)
        else:
            # Solve with Secant Method
            if phase is 'liq':
                start = 1670.858218
            else:
                start =2563.592004 + 5.0 # 5 added to extrapolate to ensure even the border ==350°C solved.
            f = lambda enthalpy: Region3.p3sat_h(enthalpy) - pressure
            enthalpy = optimize.newton(f, start, tol=1e-5)

    return enthalpy

def p4_s(entropy):
    '''Uses h4_s and p_hs for the different regions to determine p4_s'''
    saturationEnthalpy = h4_s(entropy)
    pressure = 0.0
    if entropy > -0.0001545495919 and entropy <= 3.77828134:
        pressure = Region1.p1_hs(saturationEnthalpy, entropy)
    elif entropy > 3.77828134 and entropy <= 5.210887663:
        pressure = Region3.p3_hs(saturationEnthalpy, entropy)
    elif entropy > 5.210887663 and entropy < 9.155759395:
        pressure = Region2.p2_hs(saturationEnthalpy, entropy)
    else:
        raise ArithmeticError('Entropy needs to be between {} and {} J/kgK'.format(-0.0001545495919, 9.155759395))

    return pressure

def x4_ph(pressure, enthalpy):
    ''' Calculate vapor fraction from enthalpy for given pressure'''
    enthalpyVapor = h4_p(pressure, 'vap')
    enthalpyLiquid = h4_p(pressure, 'liq')
    quality = -1.0
    if enthalpy > enthalpyVapor:
        quality = 1.0
    elif enthalpy < enthalpyLiquid:
        quality = 0.0
    else:
        quality = (enthalpy - enthalpyLiquid)/(enthalpyVapor - enthalpyLiquid)

    return quality

def x4_ps(pressure, entropy):

    quality = -1.0
    if pressure < 16.529:
        entropyVapor = Region2.s2_pt(pressure, t4_p(pressure))
        entropyLiquid = Region1.s1_pt(pressure, t4_p(pressure))
    else:
        entropyVapor = Region3.s3_rhot(1.0/(Region3.v3_ph(pressure, h4_p(pressure, 'vap'))), t4_p(pressure))
        entropyLiquid = Region3.s3_rhot(1.0/(Region3.v3_ph(pressure, h4_p(pressure, 'liq'))), t4_p(pressure))

    if entropy < entropyLiquid:
        quality = 0.0
    elif entropy > entropyVapor:
        quality = 1.0
    else:
        quality = (entropy - entropyLiquid)/(entropyVapor - entropyLiquid)

    return quality

def t4_hs(enthalpy, entropy):
    ''' Supplementary Release on Backward Equations ( ) , p h s for Region 3, Chapter 5.3 page 30.
    The if 97 function is only valid for part of region4. Use iteration outside.'''
    if entropy < -0.0001545495919 or entropy >= 9.15546555571324:
        raise ArithmeticError('Entropy needs to be between {} and {} kJ/kgK'.format(-0.0001545495919, 9.15546555571324))
    temperature = 0.0
    i = np.array([0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 5, 6, 6, 6, 8, 10, 10, 12, 14, 14, 16, 16, 18, 18, 18, 20, 28])
    j = np.array([0, 3, 12, 0, 1, 2, 5, 0, 5, 8, 0, 2, 3, 4, 0, 1, 1, 2, 4, 16, 6, 8, 22, 1, 20, 36, 24, 1, 28, 12, 32, 14, 22, 36, 24, 36])
    n = np.array([0.179882673606601, -0.267507455199603, 1.162767226126, 0.147545428713616, -0.512871635973248, 0.421333567697984, 0.56374952218987, 0.429274443819153, -3.3570455214214, 10.8890916499278, -0.248483390456012, 0.30415322190639, -0.494819763939905, 1.07551674933261, 7.33888415457688E-02, 1.40170545411085E-02, -0.106110975998808, 1.68324361811875E-02, 1.25028363714877, 1013.16840309509, -1.51791558000712, 52.4277865990866, 23049.5545563912, 2.49459806365456E-02, 2107964.67412137, 366836848.613065, -144814105.365163, -1.7927637300359E-03, 4899556021.00459, 471.262212070518, -82929439019.8652, -1715.45662263191, 3557776.82973575, 586062760258.436, -12988763.5078195, 31724744937.1057])
    if entropy > 5.210887825 and entropy < 9.15546555571324:
        sigma = entropy/9.2
        eta = enthalpy/2800.0
        teta = sum(n*(eta - 0.119)**i*(sigma - 1.07)**j)
        temperature = teta*550.0
    else:
        if entropy > -0.0001545495919 and entropy <= 3.77828134:
            lowBound, highBound = 0.000611, 165.291642526045
            liquidEnthalpy, pressureL = 0.0, 0.0
            tolerance = (0.00001, 0.0001)
            while abs(liquidEnthalpy - enthalpy) > tolerance[0] and abs(highBound - lowBound) > tolerance[1]:
                pressureL = (highBound + lowBound)/2.0
                temperature = t4_p(pressureL)
                liquidEnthalpy = Region1.h1_pt(pressureL, temperature)
                if liquidEnthalpy > enthalpy:
                    highBound = pressureL
                else:
                    lowBound = pressureL
        elif entropy > 3.77828134 and entropy <= 5.210887663:
            pressureL = Region3.p3sat_h(enthalpy)

        lowBound, highBound = 0.000611, pressureL
        entropyS = 0.0
        tolerance = (0.000001, 0.0000001)
        while abs(entropy - entropyS) > tolerance[0] and abs(highBound - lowBound) > tolerance[1]:
            pressure = (lowBound + highBound)/2.0
            temperature = t4_p(pressure)
            quality = x4_ph(pressure, enthalpy)
            if pressure < 16.529:
                entropyVapor = Region2.s2_pt(pressure, temperature)
                entropyLiquid =Region1.s1_pt(pressure, temperature)
            else:
                specificVolume = Region3.v3_ph(pressure, h4_p(pressure, 'vap'))
                entropyVapor = Region3.s3_rhot(1.0/specificVolume, temperature)
                specificVolume = Region3.v3_ph(pressure, h4_p(pressure, 'liq'))
                entropyLiquid = Region3.s3_rhot(1.0/specificVolume, temperature)
            entropyS = (quality*entropyVapor + (1.0 - quality)*entropyLiquid)
            if entropyS < entropy:
                highBound = pressure
            else:
                lowBound = pressure

    return temperature
