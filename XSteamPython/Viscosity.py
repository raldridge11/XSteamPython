# -*- coding: utf-8 -*-
'''
Viscosity functions
'''
import math

import numpy as np

try:
    import Constants
    import Regions
    import Region1
    import Region2
    import Region3
    import Region4
    import Region5
except ImportError:
    from . import Constants
    from . import Regions
    from . import Region1
    from . import Region2
    from . import Region3
    from . import Region4
    from . import Region5

def my_allregions_pT(pressure, temperature):
    '''Viscosity (IAPWS formulation 1985, Revised 2003)'''

    # Check valid area
    if not check_valid_area(pressure, temperature):
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

    return my_rhot(density, temperature)

def my_allregions_ph(pressure, enthalpy):
    '''Viscosity (IAPWS formulation 1985, Revised 2003)'''
    region = Regions.region_ph(pressure, enthalpy)
    if region is None: return Constants._errorValue

    temperature = Constants._errorValue
    density = Constants._errorValue

    if region == 1:
        temperature = Region1.t1_ph(pressure, enthalpy)
        density = 1.0/Region1.v1_pt(pressure, temperature)
    elif region == 2:
        temperature = Region2.t2_ph(pressure, enthalpy)
        density = 1.0/Region2.v2_pt(pressure, temperature)
    elif region == 3:
        temperature = Region3.t3_ph(pressure, enthalpy)
        density = 1.0/Region3.v3_ph(pressure, enthalpy)
    elif region == 4:
        quality = Region4.x4_ph(pressure, enthalpy)
        specificVolumeVapor, specificVolumeLiquid = Constants._errorValue, Constants._errorValue
        temperature = Region4.t4_p(pressure)
        if pressure < Constants._pressureSubDomain:
            specificVolumeVapor = Region2.v2_pt(pressure, temperature)
            specificVolumeLiquid = Region1.v1_pt(pressure, temperature)
        else:
            specificVolumeVapor = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'vap'))
            specificVolumeLiquid = Region3.v3_ph(pressure, Region4.h4_p(pressure, 'liq'))
        density = 1.0/(quality*specificVolumeVapor + (1.0 - quality)*specificVolumeLiquid)
    elif region == 5:
        temperature = Region5.t5_ph(pressure, enthalpy)
        density = 1.0/Region5.v5_pt(pressure, temperature)

    # Check valid area
    if not check_valid_area(pressure, temperature):
       return Constants._errorValue

    return my_rhot(density, temperature)

def check_valid_area(pressure, temperature):
    '''Checks valid area of viscosity functions'''
    # Check valid area
    if temperature > 900.0 + 273.15 or \
       (temperature > 600.0 + 273.15 and pressure > 300.0) or \
       (temperature > 150.0 + 273.15 and pressure > 350.0) or \
       pressure > 500.0:
       return False
    return True

def my_rhot(density, temperature):
    '''Calculates viscosity given density and temperature'''
    h0 = np.array([0.5132047, 0.3205656, 0.0, 0.0, -0.7782567, 0.1885447])
    h1 = np.array([0.2151778, 0.7317883, 1.241044, 1.476783, 0.0, 0.0])
    h2 = np.array([-0.2818107, -1.070786, -1.263184, 0.0, 0.0, 0.0])
    h3 = np.array([0.1778064, 0.460504, 0.2340379, -0.4924179, 0.0, 0.0])
    h4 = np.array([-0.0417661, 0.0, 0.0, 0.1600435, 0.0, 0.0])
    h5 = np.array([0.0, -0.01578386, 0.0, 0.0, 0.0, 0.0])
    h6 = np.array([0.0, 0.0, 0.0, -0.003629481, 0.0, 0.0])

    rhos = density/317.63
    ts = temperature/647.226

    my_0 = ts**0.5/(1.0 + 0.978197/ts + 0.579829/(ts**2.0) - 0.202354/(ts**3.0))
    total = 0.0
    a, b = 1.0/ts - 1.0, rhos - 1.0
    for i in range(6):
        total += h0[i]*a**i + h1[i]*a**i*b + h2[i]*a**i*b**2 + h3[i]*a**i*b**3 + h4[i]*a**i*b**4 + h5[i]*a**i*b**5 + h6[i]*a**i*b**6

    my_1 = math.exp(rhos*total)
    return my_0*my_1*0.000055071
