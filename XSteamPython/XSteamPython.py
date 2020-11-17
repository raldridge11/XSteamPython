# -*- coding: utf-8 -*-
'''
XSteamPython
Steam tables in python
'''
import math

try:
    import Constants
    import Convert
    import Region1
    import Region2
    import Region3
    import Region4
    import Region5
    import Regions
    import Viscosity
except ImportError:
    from . import Constants
    from . import Convert
    from . import Region1
    from . import Region2
    from . import Region3
    from . import Region4
    from . import Region5
    from . import Regions
    from . import Viscosity

englishUnits = False

def switchUnits():
    '''Function to switch between unit systems'''
    global englishUnits
    englishUnits = not englishUnits
    if englishUnits:
        print("Using English units")
    else:
        print("Using SI Units")

def useEnglish():
    '''Set units to use english units'''
    global englishUnits
    print("Using English units")
    englishUnits = True

def useSI():
    '''Set units to use SI units'''
    global englishUnits
    print("Using SI Units")
    englishUnits = False

def Tsat_p(pressure):
    '''
    Saturation temperature given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: Saturation temperature in °C or °F
    '''
    pressure = Convert.toSIUnit(float(pressure), 'pressure', englishUnits=englishUnits)

    if pressure >= Constants._pressureMin and pressure <= Constants._pressureMax + 0.001:
        return Convert.fromSIUnit(Region4.t4_p(pressure), 'temperature', englishUnits=englishUnits)
    else:
        return Constants._errorValue

def Tsat_s(entropy):
    '''
    Saturation temperature given entropy

    Args:
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: Saturation temperature in °C or °F
    '''
    if englishUnits: entropy = Convert.toSIUnit(float(entropy), 'entropy')
    entropyMin, entropyMax = -0.0001545495919, 9.155759395

    if entropy > entropyMin and entropy < entropyMax:
        return Convert.fromSIUnit(Region4.t4_p(Region4.p4_s(entropy)), 'temperature', englishUnits=englishUnits)
    else:
        return Constants._errorValue

def T_ph(pressure, enthalpy):
    '''
    Temperature given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: Temperature in °C or °F
    '''
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
    '''
    Temperature given pressure and entropy

    Args:
        pressure (float): pressure in kPa or psi
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: Temperature in °C or °F
    '''
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
    '''
    Temperature given enthalpy and entropy

    Args:
        enthalpy (float): enthalpy in kJ/kg or Btu/lb
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: Temperature in °C or °F
    '''
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
    '''
    Saturation Pressure given temperature

    Args:
        temperature (float): temperature in °C or °F

    Returns:
        float: pressure in kPa or psi

    '''
    temperature = Convert.toSIUnit(float(temperature), 'temperature', englishUnits=englishUnits)
    pressure = 0.0
    if temperature <= Constants._temperatureMax and temperature > Constants._temperatureMin:
        pressure = Convert.fromSIUnit(Region4.p4_t(temperature), 'pressure', englishUnits=englishUnits)
    else:
        pressure = Constants._errorValue
    return pressure

def Psat_s(entropy):
    '''
    Saturation pressure given entropy

    Args:
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: pressure in kPa or psi
    '''
    entropy = float(entropy)

    if englishUnits:
        entropy = Convert.toSIUnit(entropy, 'entropy')

    if entropy > -0.0001545495919 and entropy < 9.155759395:
        return Convert.fromSIUnit(Region4.p4_s(entropy), 'pressure', englishUnits=englishUnits)
    else:
        return Constants._errorValue

def P_hs(enthalpy, entropy):
    '''
    Pressure given enthalpy and entropy

    Args:
        enthalpy (float): enthalpy in kJ/kg or Btu/lb
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: pressure in kPa or psi
    '''
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

def hV_p(pressure):
    '''
    Vapor enthalpy given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: enthalpy in kJ/kg or Btu/lb
    '''
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
    '''
    Liquid enthalpy given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: enthalpy in kJ/kg or Btu/lb
    '''
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
    '''
    Vapor enthalpy given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: enthalpy in kJ/kg or Btu/lb
    '''
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        enthalpy = Region4.h4_p(Region4.p4_t(temperature), 'vap')
        if englishUnits:
            return Convert.fromSIUnit(enthalpy, 'enthalpy')
        return enthalpy
    else:
        return Constants._errorValue

def hL_T(temperature):
    '''
    Liquid enthalpy given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: enthalpy in kJ/kg or Btu/lb
    '''
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    if temperature > Constants._temperatureMin and temperature < Constants._temperatureMax:
        enthalpy = Region4.h4_p(Region4.p4_t(temperature), 'liq')
        if englishUnits:
            return Convert.fromSIUnit(enthalpy, 'enthalpy')
        return enthalpy
    else:
        return Constants._errorValue

def h_pT(pressure, temperature):
    '''
    Enthalpy given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        temperature (float): Temperature in °C or °F

    Returns:
        float: enthalpy in kJ/kg or Btu/lb
    '''
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
    '''
    Enthalpy given pressure and entropy

    Args:
        pressure (float): pressure in kPa or psi
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: enthalpy in kJ/kg or Btu/lb
    '''
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
    '''
    Enthalpy given pressure and static quality

    Args:
        pressure (float): pressure in kPa or psi
        quality (float): static quality (between 0 and 1)

    Returns:
        float: enthalpy in kJ/kg or Btu/lb
    '''
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
    '''
    Enthalpy given pressure and static quality

    Args:
        temperature (float): Temperature in °C or °F
        quality (float): static quality (between 0 and 1)

    Returns:
        float: enthalpy in kJ/kg or Btu/lb
    '''
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    if quality > 1.0 or quality < 0.0 or temperature >= Constants._temperatureMax:
        return Constants._errorValue

    pressure = Convert.fromSIUnit(Region4.p4_t(temperature), 'pressure', englishUnits=englishUnits)

    return h_px(pressure, quality)

def vV_p(pressure):
    '''
    Vapor specific volume given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: specific volume in m**3/kg or ft**3/lb
    '''
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
    '''
    Liquid specific volume given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: specific volume in m**3/kg or ft**3/lb
    '''
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
    '''
    Vapor specific volume given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: specific volume in m**3/kg or ft**3/lb
    '''
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
    '''
    Liquid specific volume given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: specific volume in m**3/kg or ft**3/lb
    '''
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
    '''
    Specific volume given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        temperature (float): Temperature in °C or °F

    Returns:
        float: specific volume in m**3/kg or ft**3/lb
    '''
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
    '''
    Specific volume given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: specific volume in m**3/kg or ft**3/lb
    '''
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
    '''
    Specific volume given pressure and entropy

    Args:
        pressure (float): pressure in kPa or psi
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: specific volume in m**3/kg or ft**3/lb
    '''
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
    '''
    Vapor density given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: density in kg/m**3 or lb/ft**3
    '''
    return 1.0/vV_p(pressure)

def rhoL_p(pressure):
    '''
    Liquid density given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: density in kg/m**3 or lb/ft**3
    '''
    return 1.0/vL_p(pressure)

def rhoL_T(temperature):
    '''
    Liquid density given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: density in kg/m**3 or lb/ft**3
    '''
    return 1.0/vL_T(temperature)

def rhoV_T(temperature):
    '''
    Vapor density given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: density in kg/m**3 or lb/ft**3
    '''
    return 1.0/vV_T(temperature)

def rho_pT(pressure, temperature):
    '''
    Density given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        temperature (float): Temperature in °C or °F

    Returns:
        float: density in kg/m**3 or lb/ft**3
    '''
    return 1.0/v_pT(pressure, temperature)

def rho_ph(pressure, enthalpy):
    '''
    Density given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: density in kg/m**3 or lb/ft**3
    '''
    return 1.0/v_ph(pressure, enthalpy)

def rho_ps(pressure, entropy):
    '''
    Density given pressure and entropy

    Args:
        pressure (float): pressure in kPa or psi
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: density in kg/m**3 or lb/ft**3
    '''
    return 1.0/v_ps(pressure, entropy)

def sV_p(pressure):
    '''
    Vapor entropy given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: entropy in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Liquid entropy given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: entropy in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Vapor entropy given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: entropy in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Liquid entropy given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: entropy in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Vapor entropy given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        temperature (float): Temperature in °C or °F

    Returns:
        float: entropy in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Vapor entropy given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: entropy in kJ/(kg*K) or btu/(lb*°F)
    '''
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

def uV_p(pressure):
    '''
    Vapor internal energy given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: internal energy in kJ/kg or btu/lb
    '''
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
    '''
    Liquid internal energy given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: internal energy in kJ/kg or btu/lb
    '''
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
    '''
    Vapor internal energy given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: internal energy in kJ/kg or btu/lb
    '''
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
    '''
    Liquid internal energy given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: internal energy in kJ/kg or btu/lb
    '''
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
    '''
    Internal energy given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        temperature (float): Temperature in °C or °F

    Returns:
        float: internal energy in kJ/kg or btu/lb
    '''
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
    '''
    Internal energy given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: internal energy in kJ/kg or btu/lb
    '''
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
    '''
    Internal energy given pressure and entropy

    Args:
        pressure (float): pressure in kPa or psi
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: internal energy in kJ/kg or btu/lb
    '''
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

def cpV_p(pressure):
    '''
    Vapor heat capacity at constant pressure given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Liquid heat capacity at constant pressure given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Vapor heat capacity at constant pressure given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Liquid heat capacity at constant pressure given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Heat capacity at constant pressure given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        temperature (float): Temperature in °C or °F

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Heat capacity at constant pressure given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Heat capacity at constant pressure given pressure and entropy

    Args:
        pressure (float): pressure in kPa or psi
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Vapor heat capacity at constant volume given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Liquid heat capacity at constant volume given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Vapor heat capacity at constant volume given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Liquid heat capacity at constant volume given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Heat capacity at constant volume given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        temperature (float): Temperature in °C or °F

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Heat capacity at constant volume given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Heat capacity at constant volume given pressure and entropy

    Args:
        pressure (float): pressure in kPa or psi
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: heat capacity in kJ/(kg*K) or btu/(lb*°F)
    '''
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
    '''
    Vapor speed of sound given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: speed of sound in m/s or ft/s
    '''
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
    '''
    Liquid speed of sound given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: speed of sound in m/s or ft/s
    '''
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
    '''
    Vapor speed of sound given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: speed of sound in m/s or ft/s
    '''
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
    '''
    Liquid speed of sound given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: speed of sound in m/s or ft/s
    '''
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
    '''
    Speed of sound given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        temperature (float): Temperature in °C or °F

    Returns:
        float: speed of sound in m/s or ft/s
    '''
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
    '''
    Speed of sound given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: speed of sound in m/s or ft/s
    '''
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
    '''
    Speed of sound given pressure and entropy

    Args:
        pressure (float): pressure in kPa or psi
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: speed of sound in m/s or ft/s
    '''
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

def my_pT(pressure, temperature):
    '''
    Viscosity given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        temperature (float): Temperature in °C or °F

    Returns:
        float: viscosity in Pa*s or lb/(ft*hr)
    '''
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)

    region = Regions.region_pt(pressure, temperature)
    if region is None or region == 4: return Constants._errorValue

    viscosity = Viscosity.my_allregions_pT(pressure, temperature)

    if englishUnits:
        return Convert.fromSIUnit(viscosity, 'viscosity')
    return viscosity

def my_ph(pressure, enthalpy):
    '''
    Viscosity given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: viscosity in Pa*s or lb/(ft*hr)
    '''
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')

    region = Regions.region_ph(pressure, enthalpy)
    if region is None or region == 4: return Constants._errorValue

    viscosity = Viscosity.my_allregions_ph(pressure, enthalpy)

    if englishUnits:
        return Convert.fromSIUnit(viscosity, 'viscosity')
    return viscosity

def my_ps(pressure, entropy):
    '''
    Viscosity given pressure and entropy

    Args:
        pressure (float): pressure in kPa or psi
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: viscosity in Pa*s or lb/(ft*hr)
    '''
    return my_ph(pressure, h_ps(pressure, entropy))

def Pr_pT(pressure, temperature):
    '''
    Prandtl number given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        temperature (float): Temperature in °C or °F

    Returns:
        float: Prandtl number
    '''
    heatCapacity = cp_pT(pressure, temperature)
    viscosity = my_pT(pressure, temperature)
    thermalConductivity = tc_pT(pressure, temperature)

    if Constants._errorValue in (heatCapacity, viscosity, thermalConductivity):
        return Constants._errorValue

    if englishUnits:
        heatCapacity = Convert.toSIUnit(heatCapacity, 'entropy')
        viscosity = Convert.toSIUnit(viscosity, 'viscosity')
        thermalConductivity = Convert.toSIUnit(thermalConductivity, 'thermal conductivity')

    return heatCapacity*1000.0*viscosity/thermalConductivity

def Pr_ph(pressure, enthalpy):
    '''
    Prandtl number given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: Prandtl number
    '''
    heatCapacity = cp_ph(pressure, enthalpy)
    viscosity = my_ph(pressure, enthalpy)
    thermalConductivity = tc_ph(pressure, enthalpy)

    if Constants._errorValue in (heatCapacity, viscosity, thermalConductivity):
        return Constants._errorValue

    if englishUnits:
        heatCapacity = Convert.toSIUnit(heatCapacity, 'entropy')
        viscosity = Convert.toSIUnit(viscosity, 'viscosity')
        thermalConductivity = Convert.toSIUnit(thermalConductivity, 'thermal conductivity')

    return heatCapacity*1000.0*viscosity/thermalConductivity

def kappa_pT(pressure, temperature):
    '''
    Heat capcity ratio given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        temperature (float): Temperature in °C or °F

    Returns:
        float: Heat capcity ratio
    '''
    cp = cp_pT(pressure, temperature)
    cv = cv_pT(pressure, temperature)
    return cp/cv

def kappa_ph(pressure, enthalpy):
    '''
    Heat capcity ratio given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: Heat capcity ratio
    '''
    cp = cp_ph(pressure, enthalpy)
    cv = cv_ph(pressure, enthalpy)
    return cp/cv

def st_t(temperature):
    '''
    Surface tension given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: surface tension in N/m or lb/ft
    '''
    temperature = Convert.toSIUnit(temperature, 'temperature', englishUnits=englishUnits)
    surfaceTension = surfaceTension_T(temperature)
    if surfaceTension == Constants._errorValue:
        return Constants._errorValue
    if englishUnits:
        surfaceTension = Convert.fromSIUnit(surfaceTension, 'surface tension')
    return surfaceTension

def st_p(pressure):
    '''
    Surface tension given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: surface tension in N/m or lb/ft
    '''
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
    '''
    Liquid thermal conductivity given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: thermal conductivity in W/(m*K) btu/(lb*ft*hr)
    '''
    tsatt = Tsat_p(pressure)
    specificVolume = vL_p(pressure)

    if Constants._errorValue in (tsatt, specificVolume):
        return Constants._errorValue

    return _tc_pTrho_wrapper(pressure, tsatt, specificVolume)

def tcV_p(pressure):
    '''
    Vapor thermal conductivity given pressure

    Args:
        pressure (float): pressure in kPa or psi

    Returns:
        float: thermal conductivity in W/(m*K) btu/(lb*ft*hr)
    '''
    tsatt = Tsat_p(pressure)
    specificVolume = vV_p(pressure)

    if Constants._errorValue in (tsatt, specificVolume):
        return Constants._errorValue

    return _tc_pTrho_wrapper(pressure, tsatt, specificVolume)

def tcL_T(temperature):
    '''
    Liquid thermal conductivity given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: thermal conductivity in W/(m*K) btu/(lb*ft*hr)
    '''
    psatt = Psat_T(temperature)
    specificVolume = vL_T(temperature)

    if Constants._errorValue in (psatt, specificVolume):
        return Constants._errorValue

    return _tc_pTrho_wrapper(psatt, temperature, specificVolume)

def tcV_T(temperature):
    '''
    Vapor thermal conductivity given temperature

    Args:
        temperature (float): Temperature in °C or °F

    Returns:
        float: thermal conductivity in W/(m*K) btu/(lb*ft*hr)
    '''
    psatt = Psat_T(temperature)
    specificVolume = vV_T(temperature)

    if Constants._errorValue in (psatt, specificVolume):
        return Constants._errorValue

    return _tc_pTrho_wrapper(psatt, temperature, specificVolume)

def tc_pT(pressure, temperature):
    '''
    Liquid thermal conductivity given pressure and temperature

    Args:
        pressure (float): pressure in kPa or psi
        temperature (float): Temperature in °C or °F

    Returns:
        float: thermal conductivity in W/(m*K) btu/(lb*ft*hr)
    '''
    specificVolume = v_pT(pressure, temperature)
    return _tc_pTrho_wrapper(pressure, temperature, specificVolume)

def tc_ph(pressure, enthalpy):
    '''
    Liquid thermal conductivity given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: thermal conductivity in W/(m*K) btu/(lb*ft*hr)
    '''
    specificVolume = v_ph(pressure, enthalpy)
    temperature = T_ph(pressure, enthalpy)
    return _tc_pTrho_wrapper(pressure, temperature, specificVolume)

def tc_hs(enthalpy, entropy):
    '''
    Liquid thermal conductivity given pressure and entropy

    Args:
        pressure (float): pressure in kPa or psi
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: thermal conductivity in W/(m*K) btu/(lb*ft*hr)
    '''
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
    '''
    Static quality given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: static quality
    '''
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        enthalpy = Convert.toSIUnit(enthalpy, 'enthalpy')
    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        return Region4.x4_ph(pressure, enthalpy)
    else:
        return Constants._errorValue

def x_ps(pressure, entropy):
    '''
    Static quality given pressure and entropy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: static quality
    '''
    pressure = Convert.toSIUnit(pressure, 'pressure', englishUnits=englishUnits)
    if englishUnits:
        entropy = Convert.toSIUnit(entropy, 'entropy')
    if pressure > Constants._pressureMin and pressure < Constants._pressureMax:
        return Region4.x4_ps(pressure, entropy)
    else:
        return Constants._errorValue

def vx_ph(pressure, enthalpy):
    '''
    Void fraction given pressure and enthalpy

    Args:
        pressure (float): pressure in kPa or psi
        entropy (float): entropy in kJ/(kg*K) or btu/(lb*°F)

    Returns:
        float: void fraction
    '''
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
    '''
    Void fraction given pressure and entropy

    Args:
        pressure (float): pressure in kPa or psi
        enthalpy (float): enthalpy in kJ/kg or Btu/lb

    Returns:
        float: void fraction
    '''
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
