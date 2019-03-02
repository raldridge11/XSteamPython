# -*- coding: utf-8 -*-
'''
Conversion functions between SI and English units
'''
conversionFactors = { 'enthalpy': 2.326, #[btu/lb]/[kJ/kg]
                      'specific volume': 0.0624279606, #[ft**3/lb]/[m**3/kg]
                      'entropy': 1.0/0.238845896627, #[btu/(lb*degF)]/[kJ/(kg*K)]
                      'velocity': 0.3048, #[ft/m]
                      'thermal conductivity': 1.0/0.577789, #[btu/lb*ft*hr]/[W/m*K]
                      'surface tension': 1.0/0.068521766, #[lb/ft]/[N/m]
                      'viscosity': 1.0/2419.088311 #[lb/ft*hr]/[Pa*s]
    }

def toSIUnit(value, quantity, englishUnits=False):
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

def fromSIUnit(value, quantity, englishUnits=False):
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