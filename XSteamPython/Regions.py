# -*- coding: utf-8 -*-
'''
Region determinations
'''
try:
    import Region1
    import Region2
    import Region3
    import Region4
    import Region5
    import Boundaries
except ImportError:
    from . import Region1
    from . import Region2
    from . import Region3
    from . import Region4
    from . import Region5
    from . import Boundaries

def region_pt(pressure, temperature):
    ''' Regions as a function of pressure and temperature '''
    region = 0
    if (temperature > 1073.15 and temperature < 2273.15) and (pressure < 10.0  and pressure > 0.000611):
        region = 5
    elif (temperature <= 1073.15 and temperature > 273.15) and (pressure <= 100 and pressure > 0.000611):
        if temperature > 623.15:
            if pressure > Boundaries.b23p_t(temperature):
                region = 3
                if temperature < 647.096:
                    ps = Region4.p4_t(temperature)
                    if abs(pressure - ps) < 0.00001:
                        region = 4
            else:
                region = 2
        else:
            ps = Region4.p4_t(temperature)
            if abs(pressure - ps) < 0.00001:
                region = 4
            elif pressure > ps:
                region = 1
            else:
                region = 2
    else:
        region = None

    return region

def region_ph(pressure, enthalpy):
    ''' Regions as a function of pressure and enthalpy '''
    pressureMin, pressureMax = 0.000611657, 100.0
    enthalpyMin = 0.963 * pressure + 2.2 # Linear adaption to Region1.h1_pt()+2 to speed up calcualations.

    if pressure < pressureMin or pressure > pressureMax:
        return None

    if enthalpy < enthalpyMin:
        if enthalpy < Region1.h1_pt(pressure, 273.150):
            return None

    if pressure < 16.5292: #Bellow region 3, check region 1,4,2,5

        tsatt = Region4.t4_p(pressure)
        if enthalpy <= Region1.h1_pt(pressure, tsatt):

            return 1
        elif enthalpy < Region2.h2_pt(pressure, tsatt):

            return 4
        elif enthalpy < 4000:
            return 2
        elif enthalpy <= Region2.h2_pt(pressure, 1073.15):

            return 2
        elif enthalpy < Region5.h5_pt(pressure, 2273.15) and pressure <= 10.0:

            return 5
    else:

        if enthalpy < Region1.h1_pt(pressure, 623.15):

            return 1
        elif enthalpy < Region2.h2_pt(pressure, Boundaries.b23t_p(pressure)):

            if pressure > Region3.p3sat_h(enthalpy):

                return 3
            else:

                return 4
        elif enthalpy < Region2.h2_pt(pressure, 1073.15):

            return 2

def region_ps(pressure, entropy):
    ''' Regions as a function of pressure and enthalpy '''
    if pressure < 0.000611657 or pressure > 100.0 or entropy < 0.0 or entropy > Region5.s5_pt(pressure, 2273.15):
        return None

    # Check region 5
    if entropy > Region2.s2_pt(pressure, 1073.15):
        if pressure <= 10.0:
            return 5
        else:
            return None
    # Check region 2
    if pressure > 16.529:
        entropyS = Region2.s2_pt(pressure, Boundaries.b23t_p(pressure)) # Between 5.047 and 5.261. Use to speed up!
    else:
        entropyS = Region2.s2_pt(pressure, Region4.t4_p(pressure))
    if entropy > entropyS:
        return 2
    # Check region 3
    entropyS = Region1.s1_pt(pressure, 623.15)
    if pressure > 16.529 and entropy > entropyS:
        if pressure > Region3.p3sat_s(entropy):
            return 3
        else:
            return 4
    # Check region 4
    if pressure < 16.529 and entropy > Region1.s1_pt(pressure, Region4.t4_p(pressure)):
        return 4
    # If it hasn't reached this point then return region 1
    return 1

def region_hs(enthalpy, entropy):
    ''' Regions as a function of enthalpy and entropy '''
    enthalpyMin = (((-0.0415878 - 2500.89262) / (-0.00015455 - 9.155759))*entropy)
    if enthalpy < -0.0001545495919 or (entropy < 9.155759395 and enthalpy < enthalpyMin):
        return None
    # Check region 1 or 4 plus a small bit over B13
    if entropy >= -0.0001545495919 and entropy <= 3.77828134:
        if enthalpy < Region4.h4_s(entropy):
            return 4
        elif entropy < 3.397782955: # 100 MPa line is limiting
            temperatureMax = Region1.t1_ps(100.0, entropy)
            enthalpyMax = Region1.h1_pt(100.0, temperatureMax)
            if enthalpy < enthalpyMax:
                return 1
            else:
                return None
        else: # The point is either in region 4, 1, or 3. Check B23
            enthalpyBoundary = Boundaries.hB13_s(entropy)
            if enthalpy < enthalpyBoundary:
                return 1
            temperatureMax = Region3.t3_ps(100.0, entropy)
            specificVolumeMax = Region3.v3_ps(100.0, entropy)
            enthalpyMax = Region3.h3_rhot(1.0/specificVolumeMax, temperatureMax)
            if enthalpy < enthalpyMax:
                return 3
            else:
                return None
    # Check region 2 or 4 upper part of area b23 -> max
    if entropy >= 5.260578707 and entropy <= 11.9212156897728:
        if entropy > 9.155759395: # Above region 4
            temperatureMin = Region2.t2_ps(0.000611, entropy)
            enthalpyMin = Region2.h2_pt(0.000611, temperatureMin)
            enthalpyMax = -0.07554022*entropy**4 + 3.341571*entropy**3 - 55.42151*entropy**2 + 408.515*entropy + 3031.338
            if enthalpy > enthalpyMin and enthalpy < enthalpyMax:
                return 2
            else:
                return None
        vaporEnthalpy = Region4.h4_s(entropy)
        if enthalpy < vaporEnthalpy: # Region 4 under region 3
            return 4
        if entropy < 6.04048367171238:
            temperatureMax = Region2.t2_ps(100.0, entropy)
            enthalpyMax = Region2.h2_pt(100.0, temperatureMax)
        else:
            # Function adapted to h(1073.15,s)
            enthalpyMax = -2.988734*entropy**4 + 121.4015*entropy**3 - 1805.15*entropy**2 + 11720.16*entropy - 23998.33
        if enthalpy < enthalpyMax: # Region 2 over region 3
            return 2
        else:
            return None
    # Check region 3 or 4 below the critical point
    if entropy >= 3.77828134 and entropy <= 4.41202148223476:
        liquidEnthalpy = Region4.h4_s(entropy)
        if enthalpy < liquidEnthalpy:
            return 4
        temperatureMax = Region3.t3_ps(100.0, entropy)
        specificVolumeMax = Region3.v3_ps(100.0, entropy)
        enthalpyMax = Region3.h3_rhot(1.0/specificVolumeMax, temperatureMax)
        if enthalpy < enthalpyMax:
            return 3
        else:
            return None
    # Check region 3 or 4 from critical point to top of b23
    if entropy >= 4.41202148223476 and entropy <= 5.260578707:
        vaporEnthalpy = Region4.h4_s(entropy)
        if enthalpy < vaporEnthalpy:
            return 4
        # Check if under validity of B23
        if entropy <= 5.048096828:
            temperatureMax = Region3.t3_ps(100.0, entropy)
            specificVolumeMax = Region3.v3_ps(100.0, entropy)
            enthalpyMax = Region3.h3_rhot(1.0/specificVolumeMax, temperatureMax)
            if enthalpy < enthalpyMax:
                return 3
            else:
                return None
        else: # In the area of B23
            if enthalpy > 2812.942061: # above b23 in h
                if entropy > 5.09796573397125:
                    temperatureMax = Region2.t2_ps(100.0, entropy)
                    enthalpyMax = Region2.h2_pt(100.0, temperatureMax)
                    if enthalpy < enthalpyMax:
                        return 2
                    else:
                        return None
                else:
                    return None
            if enthalpy < 2563.592004: # Below B23 in h but we have already checked above hV2c3b
                return 3
            # We are within the b23 area in both s and h
            if Region2.p2_hs(enthalpy, entropy) > Boundaries.b23p_t(Boundaries.tB23_hs(enthalpy, entropy)):
                return 3
            else:
                return 2
    return None

def region_prho(pressure, density):
    ''' Regions as a function of pressure and density '''
    specificVolume = 1.0/density
    if pressure < 0.000611657 or pressure > 100.0:
        raise ArithmeticError('Pressure is out of bounds')
    if specificVolume < Region1.v1_pt(pressure, 273.15):
        raise ArithmeticError('Density is out of bounds')
    if pressure < 16.5292: # Below region 3, check region 1, 4, and 2
        if specificVolume < Region1.v1_pt(pressure, Region4.t4_p(pressure)):
            return 1
        if specificVolume < Region2.v2_pt(pressure, Region4.t4_p(pressure)):
            return 4
        if specificVolume < Region2.v2_pt(pressure, 1073.15):
            return 2
        if pressure > 10: # Above region 5
            raise ArithmeticError('Pressure is out of bounds')
        if specificVolume <= Region5.v5_pt(pressure, 2073.15):
            return 5
    else: # Check region 1, 3, 4, 3, 2 (above the lowest point of region 3.)
        if specificVolume < Region1.v1_pt(pressure, 623.15):
            return 1
        # Check if in region 3 or 4 (below region 2)
        if specificVolume < Region2.v2_pt(pressure, Boundaries.b23t_p(pressure)):
            if pressure > 22.064: # Above region 4
                return 3
            if specificVolume < Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq')) or specificVolume > Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap')):
                return 3
            else:
                return 4
        # Check region 2
        if specificVolume < Region2.v2_pt(pressure, 1073.15):
            return 2