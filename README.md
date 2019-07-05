[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c9ae5f60829541d8b6b2e8962997425d)](https://www.codacy.com/app/aldridge.robert.james/XSteamPython?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=raldridge11/XSteamPython&amp;utm_campaign=Badge_Grade)

[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/c9ae5f60829541d8b6b2e8962997425d)](https://www.codacy.com/app/aldridge.robert.james/XSteamPython?utm_source=github.com&utm_medium=referral&utm_content=raldridge11/XSteamPython&utm_campaign=Badge_Coverage)

[![Build Status](https://travis-ci.org/raldridge11/XSteamPython.svg?branch=master)](https://travis-ci.org/raldridge11/XSteamPython)

# XSteamPython
Port of [XSteam](https://sourceforge.net/projects/xsteam/) tables into Python originally released by Magnus Holmgren.

XSteam provides steam and water properties according to [IAPWS release IF-97](http://www.iapws.org/relguide/IF97-Rev.pdf). The range of applicability is from 0-1000 bar and 0-2000 °C.

Some transport properties (thermal conductivity and viscosity) are also available and based upon [IAPWS 1998](http://www.iapws.org/relguide/ThCond.pdf).

## Installation
Two options are available. The first is to install from PyPI using pip
```sh
pip install XSteamPython
```
Or by cloning and running
```sh
python setup.py install
```
## Requirements
XSteamPython only requires that `SciPy` be installed.

For development, all dependencies are contained in `requirements.txt`.

## Usage
```python
>>> import XSteamPython as stm
>>> enthalpy=stm.h_pT(101.0, 300.0)
>>> print(enthalpy)
3074.515918340631
>>> stm.switchUnits()
Using English units
>>> enthalpy=stm.h_pT(14.7, 70.0)
>>> print(enthalpy)
38.11798524502647
>>> dir(stm)
['Boundaries', 'Constants', 'Convert', 'P_hs', 'Pr_pT', 'Pr_ph', 'Psat_T', 'Psat_s', 'Region1', 'Region2', 'Region3', 'Region4', 'Region5', 'Regions', 'T_hs', 'T_ph', 'T_ps', 'Tsat_p', 'Tsat_s', 'Viscosity', 'XSteamPython', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'cpL_T', 'cpL_p', 'cpV_T', 'cpV_p', 'cp_pT', 'cp_ph', 'cp_ps', 'cvL_T', 'cvL_p', 'cvV_T', 'cvV_p', 'cv_pT', 'cv_ph', 'cv_ps', 'englishUnits', 'hL_T', 'hL_p', 'hV_T', 'hV_p', 'h_Tx', 'h_pT', 'h_ps', 'h_px', 'kappa_pT', 'kappa_ph', 'math', 'my_pT', 'my_ph', 'my_ps', 'rhoL_T', 'rhoL_p', 'rhoV_T', 'rhoV_p', 'rho_pT', 'rho_ph', 'rho_ps', 'sL_T', 'sL_p', 'sV_T', 'sV_p', 's_pT', 's_ph', 'st_p', 'st_t', 'surfaceTension_T', 'switchUnits', 'tcL_T', 'tcL_p', 'tcV_T', 'tcV_p', 'tc_hs', 'tc_pT', 'tc_pTrho', 'tc_ph', 'uL_T', 'uL_p', 'uV_T', 'uV_p', 'u_pT', 'u_ph', 'u_ps', 'vL_T', 'vL_p', 'vV_T', 'vV_p', 'v_pT', 'v_ph', 'v_ps', 'vx_ph', 'vx_ps', 'wL_T', 'wL_p', 'wV_T', 'wV_p', 'w_pT', 'w_ph', 'w_ps', 'x_ph', 'x_ps']
```

Note that calling `stm.switchUnits()` changes from SI to English units and vice versa. Default is SI units.

## Syntax

The syntax for function calling is first the wanted property, followed by an underscore followed by input property(ies). Example:
```
h_pT(101.0, 300.0)
```
The example will return enthalpy given a pressure (101 kPa) and temperature (300 °C).

|Property|Key|
|---|---|
|T| Temperature (°C or °F)|
|p| Pressure (kPa or psi)|
|h| Enthalpy (kJ/kg or btu/lb)|
|v| Specific volume (m\*\*3/kg or ft\*\*3/lb)|
|rho| Density (kg/m\*\*3 or lb/ft\*\*3)|
|s| Specific entropy (kJ/(kg°C) or btu/(lb°F))|
|u| Specific internal energy (kJ/kg or btu/lb)|
|Cp| Specific heat capacity constant pressure (kJ/(kg°C) or btu/(lb°F))|
|Cv| Specific heat capacity constant volume (kJ/(kg°C) or btu/(lb°F))|
|w| Speed of sound (m/s or ft/s)|
|my| Viscosity (N\*s/m\*\*2 or lbm/ft/hr)|
|Pr|Prandtl number|
|kappa|Heat capacity ratio|
|tc| Thermal Conductivity (W/(m\*°C) or btu/(h\*ft\*°F))|
|st| Surface Tension (N/m or lb/ft)|
|x| Vapor fraction (dmnls)|
|vx| Vapor Volume Fraction (dmnls)|

Some functions can have a little extra after the wanted property

|Tag|Key|
|---|---|
|L|Liquid phase|
|V|Vapor phase|
|sat|At saturation|
