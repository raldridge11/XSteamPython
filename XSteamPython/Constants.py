# -*- coding: utf-8 -*-
'''
* Water and steam properties according to IAPWS IF-97
* By Magnus Holmgren, www.x-eng.com
* The steam tables are free and provided as is.
* We take no responsibilities for any errors in the code or damage thereby.
* You are free to use, modify and distribute the code as long as authorship is properly acknowledged.
* Please notify me at magnus@x-eng.com if the code is used in commercial applications
'''
_R = 0.461526 # kJ/(kg K)
_tc = 647.096 # K
_tp = 647.26 # K
_pc = 22.064 # MPa
_rhoc = 322.0 # kg/m**3
_rhop = 317.7 # kg/m**3
_errorValue = 2015.0
_pressureMin, _pressureMax, _pressureSubDomain = 0.000611657, 22.06395, 16.529
_temperatureMin, _temperatureMax, _temperatureSubDomain = 273.15, 647.096, 623.15
