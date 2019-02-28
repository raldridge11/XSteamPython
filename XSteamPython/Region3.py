# -*- coding: utf-8 -*-
'''
Region 3 functions
'''
import math

import numpy as np
import scipy
from scipy import optimize

try:
    import Boundaries
    import Constants
    import Region1
    import Region2
except ImportError:
    from . import Boundaries
    from . import Constants
    from . import Region1
    from . import Region2

i = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9, 9, 10, 10, 11])
j = np.array([0, 0, 1, 2, 7, 10, 12, 23, 2, 6, 15, 17, 0, 2, 6, 7, 22, 26, 0, 2, 4, 16, 26, 0, 2, 4, 26, 1, 3, 26, 0, 2, 26, 2, 26, 2, 26, 0, 1, 26])
n = np.array([1.0658070028513, -15.732845290239, 20.944396974307, -7.6867707878716, 2.6185947787954, -2.808078114862, 1.2053369696517, -8.4566812812502E-03, -1.2654315477714, -1.1524407806681, 0.88521043984318, -0.64207765181607, 0.38493460186671, -0.85214708824206, 4.8972281541877, -3.0502617256965, 0.039420536879154, 0.12558408424308, -0.2799932969871, 1.389979956946, -2.018991502357, -8.2147637173963E-03, -0.47596035734923, 0.0439840744735, -0.44476435428739, 0.90572070719733, 0.70522450087967, 0.10770512626332, -0.32913623258954, -0.50871062041158, -0.022175400873096, 0.094260751665092, 0.16436278447961, -0.013503372241348, -0.014834345352472, 5.7922953628084E-04, 3.2308904703711E-03, 8.0964802996215E-05, -1.6557679795037E-04, -4.4923899061815E-05])

def p3_rhot(density, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    '7 Basic Equation for Region 3, Section. 6.1 Basic Equation Table 30 and 31, Page 30 and 31'''
    delta = density/Constants._rhoc
    tau = Constants._tc/temperature
    fidelta = sum(n*i*delta**(i - 1.0)*tau**j) + n[0]/delta
    return density*Constants._R*temperature*delta*fidelta/1000.0

def u3_rhot(density, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    7 Basic Equation for Region 3, Section. 6.1 Basic Equation Table 30 and 31, Page 30 and 31'''
    delta = density/Constants._rhoc
    tau = Constants._tc/temperature
    fitau = sum(n*delta**i*j*tau**(j - 1))
    return Constants._R*temperature*tau*fitau

def h3_rhot(density, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    7 Basic Equation for Region 3, Section. 6.1 Basic Equation Table 30 and 31, Page 30 and 31'''
    delta = density/Constants._rhoc
    tau = Constants._tc/temperature
    fidelta = sum(n*i*delta**(i - 1)*tau**j) + n[0]/delta
    fitau = sum(n*delta**i*j*tau**(j - 1))
    return Constants._R*temperature*(tau*fitau + delta*fidelta)

def s3_rhot(density, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    7 Basic Equation for Region 3, Section. 6.1 Basic Equation Table 30 and 31, Page 30 and 31'''
    delta = density/Constants._rhoc
    tau = Constants._tc/temperature
    fi = sum(n*delta**i*tau**j) + n[0]*(math.log(delta) - 1.0)
    fitau = sum(n*delta**i*j*tau**(j - 1))
    return Constants._R*(tau*fitau - fi)

def cp3_rhot(density, temperature):
    '''Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    7 Basic Equation for Region 3, Section. 6.1 Basic Equation Table 30 and 31, Page 30 and 31 '''
    delta = density/Constants._rhoc
    tau = Constants._tc/temperature
    fitautau = sum(n*delta**i*j*(j - 1)*tau**(j - 2))
    fidelta = sum(n*i*delta**(i - 1)*tau**j) + n[0]/delta
    fideltatau = sum(n*i*delta**(i - 1)*j*tau**(j - 1))
    fideltadelta = sum(n*i*(i - 1)*delta**(i - 2)*tau**j) - n[0]/delta**2
    return Constants._R*(-(tau**2*fitautau) + (delta*fidelta - delta*tau*fideltatau)**2 / (2.0*delta*fidelta + delta**2*fideltadelta))

def cv3_rhot(density, temperature):
    ''' Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    7 Basic Equation for Region 3, Section. 6.1 Basic Equation Table 30 and 31, Page 30 and 31'''
    delta = density/Constants._rhoc
    tau = Constants._tc/temperature
    fitautau = sum(n*delta**i*j*(j -1)*tau**(j - 2))
    return -Constants._R*tau**2*fitautau

def w3_rhot(density, temperature):
    ''' Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam, September 1997
    7 Basic Equation for Region 3, Section. 6.1 Basic Equation Table 30 and 31, Page 30 and 31'''
    delta = density/Constants._rhoc
    tau = Constants._tc/temperature
    fitautau = sum(n*delta**i*j*(j - 1)*tau**(j - 2))
    fidelta = sum(n*i*delta**(i - 1)*tau**j) + n[0]/delta
    fideltatau = sum(n*i*delta**(i - 1)*j*tau**(j - 1))
    fideltadelta = sum(n*i*(i - 1)*delta**(i - 2)*tau**j) - n[0]/delta**2
    return math.sqrt(1000.0*Constants._R*temperature*(2.0*delta*fidelta + delta**2*fideltadelta - (delta*fidelta - delta*tau*fideltatau)**2 / (tau**2 * fitautau)))

def t3_ph(pressure, enthalpy):
    '''Revised Supplementary Release on Backward Equations for the Functions T(p,h), v(p,h) and T(p,s), v(p,s) for Region 3 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam 2004
    Section 3.3 Backward Equations T(p,h) and v(p,h) for Subregions 3a and 3b Boundary equation, Eq 1 Page 5'''
    h3ab = 2014.64004206875 + 3.74696550136983*pressure - 2.19921901054187E-02*pressure**2 + 8.7513168600995E-05*pressure**3

    if enthalpy < h3ab:
        ## Subregion 3a Eq 2, Table 3, Page 7
        i = np.array([-12, -12, -12, -12, -12, -12, -12, -12, -10, -10, -10, -8, -8, -8, -8, -5, -3, -2, -2, -2, -1, -1, 0, 0, 1, 3, 3, 4, 4, 10, 12])
        j = np.array([0, 1, 2, 6, 14, 16, 20, 22, 1, 5, 12, 0, 2, 4, 10, 2, 0, 1, 3, 4, 0, 2, 0, 1, 1, 0, 1, 0, 3, 4, 5])
        n = np.array([-1.33645667811215E-07, 4.55912656802978E-06, -1.46294640700979E-05, 6.3934131297008E-03, 372.783927268847, -7186.54377460447, 573494.7521034, -2675693.29111439, -3.34066283302614E-05, -2.45479214069597E-02, 47.8087847764996, 7.64664131818904E-06, 1.28350627676972E-03, 1.71219081377331E-02, -8.51007304583213, -1.36513461629781E-02, -3.84460997596657E-06, 3.37423807911655E-03, -0.551624873066791, 0.72920227710747, -9.92522757376041E-03, -0.119308831407288, 0.793929190615421, 0.454270731799386, 0.20999859125991, -6.42109823904738E-03, -0.023515586860454, 2.52233108341612E-03, -7.64885133368119E-03, 1.36176427574291E-02, -1.33027883575669E-02])

        ps = pressure/100.0
        hs = enthalpy/2300.0
        Ts = n*(ps + 0.24)**i*(hs - 0.615)**j
        return 760.0*Ts.sum()
    else:
        ## Subregion 3b Eq3, Table 4, Page 7,8
        i = np.array([-12, -12, -10, -10, -10, -10, -10, -8, -8, -8, -8, -8, -6, -6, -6, -4, -4, -3, -2, -2, -1, -1, -1, -1, -1, -1, 0, 0, 1, 3, 5, 6, 8])
        j = np.array([0, 1, 0, 1, 5, 10, 12, 0, 1, 2, 4, 10, 0, 1, 2, 0, 1, 5, 0, 4, 2, 4, 6, 10, 14, 16, 0, 2, 1, 1, 1, 1, 1])
        n = np.array([3.2325457364492E-05, -1.27575556587181E-04, -4.75851877356068E-04, 1.56183014181602E-03, 0.105724860113781, -85.8514221132534, 724.140095480911, 2.96475810273257E-03, -5.92721983365988E-03, -1.26305422818666E-02, -0.115716196364853, 84.9000969739595, -1.08602260086615E-02, 1.54304475328851E-02, 7.50455441524466E-02, 2.52520973612982E-02, -6.02507901232996E-02, -3.07622221350501, -5.74011959864879E-02, 5.03471360939849, -0.925081888584834, 3.91733882917546, -77.314600713019, 9493.08762098587, -1410437.19679409, 8491662.30819026, 0.861095729446704, 0.32334644281172, 0.873281936020439, -0.436653048526683, 0.286596714529479, -0.131778331276228, 6.76682064330275E-03])

        ps = pressure/100.0
        hs = enthalpy/2800.0
        Ts = n*(ps + 0.298)**i*(hs - 0.72)**j
        return 860.0*Ts.sum()

def v3_ph(pressure, enthalpy):
    '''Revised Supplementary Release on Backward Equations for the Functions T(p,h), v(p,h) and T(p,s), v(p,s) for Region 3 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam 2004
    Section 3.3 Backward Equations T(p,h) and v(p,h) for Subregions 3a and 3b Boundary equation, Eq 1 Page 5'''
    specificVolume = 0.0
    enthalpyBoundary = 2014.64004206875 + 3.74696550136983*pressure - 2.19921901054187E-02 *pressure**2 + 8.7513168600995E-05*pressure**3

    if enthalpy < enthalpyBoundary:
        # Subregion 3a Eq 4, Table 6, Page 9
        i = np.array([-12, -12, -12, -12, -10, -10, -10, -8, -8, -6, -6, -6, -4, -4, -3, -2, -2, -1, -1, -1, -1, 0, 0, 1, 1, 1, 2, 2, 3, 4, 5, 8])
        j = np.array([6, 8, 12, 18, 4, 7, 10, 5, 12, 3, 4, 22, 2, 3, 7, 3, 16, 0, 1, 2, 3, 0, 1, 0, 1, 2, 0, 2, 0, 2, 2, 2])
        n = np.array([5.29944062966028E-03, -0.170099690234461, 11.1323814312927, -2178.98123145125, -5.06061827980875E-04, 0.556495239685324, -9.43672726094016, -0.297856807561527, 93.9353943717186, 1.92944939465981E-02, 0.421740664704763, -3689141.2628233, -7.37566847600639E-03, -0.354753242424366, -1.99768169338727, 1.15456297059049, 5683.6687581596, 8.08169540124668E-03, 0.172416341519307, 1.04270175292927, -0.297691372792847, 0.560394465163593, 0.275234661176914, -0.148347894866012, -6.51142513478515E-02, -2.92468715386302, 6.64876096952665E-02, 3.52335014263844, -1.46340792313332E-02, -2.24503486668184, 1.10533464706142, -4.08757344495612E-02])
        ps = pressure/100.0
        hs = enthalpy/2100.0
        vs = sum(n*(ps + 0.128)**i*(hs - 0.727)**j)
        specificVolume = vs*0.0028
    else:
        # Subregion 3b Eq 5, Table 7, Page 9
        i = np.array([-12, -12, -8, -8, -8, -8, -8, -8, -6, -6, -6, -6, -6, -6, -4, -4, -4, -3, -3, -2, -2, -1, -1, -1, -1, 0, 1, 1, 2, 2])
        j = np.array([0, 1, 0, 1, 3, 6, 7, 8, 0, 1, 2, 5, 6, 10, 3, 6, 10, 0, 2, 1, 2, 0, 1, 4, 5, 0, 0, 1, 2, 6])
        n = np.array([-2.25196934336318E-09, 1.40674363313486E-08, 2.3378408528056E-06, -3.31833715229001E-05, 1.07956778514318E-03, -0.271382067378863, 1.07202262490333, -0.853821329075382, -2.15214194340526E-05, 7.6965608822273E-04, -4.31136580433864E-03, 0.453342167309331, -0.507749535873652, -100.475154528389, -0.219201924648793, -3.21087965668917, 607.567815637771, 5.57686450685932E-04, 0.18749904002955, 9.05368030448107E-03, 0.285417173048685, 3.29924030996098E-02, 0.239897419685483, 4.82754995951394, -11.8035753702231, 0.169490044091791, -1.79967222507787E-02, 3.71810116332674E-02, -5.36288335065096E-02, 1.6069710109252])
        ps = pressure/100.0
        hs = enthalpy/2800.0
        vs = sum(n*(ps + 0.0661)**i*(hs - 0.72)**j)
        specificVolume = vs*0.0088

    return specificVolume

def t3_ps(pressure, entropy):
    '''Revised Supplementary Release on Backward Equations for the Functions T(p,h), v(p,h) and T(p,s), v(p,s) for Region 3 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam 2004
    3.4 Backward Equations T(p,s) and v(p,s) for Subregions 3a and 3b Boundary equation, Eq 6 Page 11'''
    entropyBoundary = 4.41202148223476
    temperature = 0.0
    if entropy <= entropyBoundary:
        # Subregion 3a Eq 6, Table 10, Page 11
        i = np.array([-12, -12, -10, -10, -10, -10, -8, -8, -8, -8, -6, -6, -6, -5, -5, -5, -4, -4, -4, -2, -2, -1, -1, 0, 0, 0, 1, 2, 2, 3, 8, 8, 10])
        j = np.array([28, 32, 4, 10, 12, 14, 5, 7, 8, 28, 2, 6, 32, 0, 14, 32, 6, 10, 36, 1, 4, 1, 6, 0, 1, 4, 0, 0, 3, 2, 0, 1, 2])
        n = np.array([1500420082.63875, -159397258480.424, 5.02181140217975E-04, -67.2057767855466, 1450.58545404456, -8238.8953488889, -0.154852214233853, 11.2305046746695, -29.7000213482822, 43856513263.5495, 1.37837838635464E-03, -2.97478527157462, 9717779473494.13, -5.71527767052398E-05, 28830.794977842, -74442828926270.3, 12.8017324848921, -368.275545889071, 6.64768904779177E+15, 0.044935925195888, -4.22897836099655, -0.240614376434179, -4.74341365254924, 0.72409399912611, 0.923874349695897, 3.99043655281015, 3.84066651868009E-02, -3.59344365571848E-03, -0.735196448821653, 0.188367048396131, 1.41064266818704E-04, -2.57418501496337E-03, 1.23220024851555E-03])
        sigma = entropy/4.4
        ps = pressure/100.0
        teta = sum(n*(ps + 0.24)**i*(sigma - 0.703)**j)
        temperature = teta*760.0
    else:
        # Subregion 3b Eq 7, Table 11, Page 11
        i = np.array([-12, -12, -12, -12, -8, -8, -8, -6, -6, -6, -5, -5, -5, -5, -5, -4, -3, -3, -2, 0, 2, 3, 4, 5, 6, 8, 12, 14])
        j = np.array([1, 3, 4, 7, 0, 1, 3, 0, 2, 4, 0, 1, 2, 4, 6, 12, 1, 6, 2, 0, 1, 1, 0, 24, 0, 3, 1, 2])
        n = np.array([0.52711170160166, -40.1317830052742, 153.020073134484, -2247.99398218827, -0.193993484669048, -1.40467557893768, 42.6799878114024, 0.752810643416743, 22.6657238616417, -622.873556909932, -0.660823667935396, 0.841267087271658, -25.3717501764397, 485.708963532948, 880.531517490555, 2650155.92794626, -0.359287150025783, -656.991567673753, 2.41768149185367, 0.856873461222588, 0.655143675313458, -0.213535213206406, 5.62974957606348E-03, -316955725450471, -6.99997000152457E-04, 1.19845803210767E-02, 1.93848122022095E-05, -2.15095749182309E-05])
        sigma = entropy/5.3
        ps = pressure/100.0
        teta = sum(n*(ps + 0.76)**i*(sigma - 0.818)**j)
        temperature = teta*860.0

    return temperature

def v3_ps(pressure, entropy):
    '''Revised Supplementary Release on Backward Equations for the Functions T(p,h), v(p,h) and T(p,s), v(p,s) for Region 3 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam 2004
    3.4 Backward Equations T(p,s) and v(p,s) for Subregions 3a and 3b Boundary equation, Eq 6 Page 11'''
    entropyBoundary = 4.41202148223476
    specificVolume = 0.0
    if entropy <= entropyBoundary:
        # Subregion 3a Eq 8, Table 13, Page 14
        i = np.array([-12, -12, -12, -10, -10, -10, -10, -8, -8, -8, -8, -6, -5, -4, -3, -3, -2, -2, -1, -1, 0, 0, 0, 1, 2, 4, 5, 6])
        j = np.array([10, 12, 14, 4, 8, 10, 20, 5, 6, 14, 16, 28, 1, 5, 2, 4, 3, 8, 1, 2, 0, 1, 3, 0, 0, 2, 2, 0])
        n = np.array([79.5544074093975, -2382.6124298459, 17681.3100617787, -1.10524727080379E-03, -15.3213833655326, 297.544599376982, -35031520.6871242, 0.277513761062119, -0.523964271036888, -148011.182995403, 1600148.99374266, 1708023226634.27, 2.46866996006494E-04, 1.6532608479798, -0.118008384666987, 2.537986423559, 0.965127704669424, -28.2172420532826, 0.203224612353823, 1.10648186063513, 0.52612794845128, 0.277000018736321, 1.08153340501132, -7.44127885357893E-02, 1.64094443541384E-02, -6.80468275301065E-02, 0.025798857610164, -1.45749861944416E-04])
        ps = pressure/100.0
        sigma = entropy/4.4
        omega = sum(n*(ps + 0.187)**i*(sigma - 0.755)**j)
        specificVolume = omega*0.0028
    else:
        # Subregion 3b Eq 9, Table 14, Page 14
        i = np.array([-12, -12, -12, -12, -12, -12, -10, -10, -10, -10, -8, -5, -5, -5, -4, -4, -4, -4, -3, -2, -2, -2, -2, -2, -2, 0, 0, 0, 1, 1, 2])
        j = np.array([0, 1, 2, 3, 5, 6, 0, 1, 2, 4, 0, 1, 2, 3, 0, 1, 2, 3, 1, 0, 1, 2, 3, 4, 12, 0, 1, 2, 0, 2, 2])
        n = np.array([5.91599780322238E-05, -1.85465997137856E-03, 1.04190510480013E-02, 5.9864730203859E-03, -0.771391189901699, 1.72549765557036, -4.67076079846526E-04, 1.34533823384439E-02, -8.08094336805495E-02, 0.508139374365767, 1.28584643361683E-03, -1.63899353915435, 5.86938199318063, -2.92466667918613, -6.14076301499537E-03, 5.76199014049172, -12.1613320606788, 1.67637540957944, -7.44135838773463, 3.78168091437659E-02, 4.01432203027688, 16.0279837479185, 3.17848779347728, -3.58362310304853, -1159952.60446827, 0.199256573577909, -0.122270624794624, -19.1449143716586, -1.50448002905284E-02, 14.6407900162154, -3.2747778718823])
        ps = pressure/100.0
        sigma = entropy/5.3
        omega = sum(n*(ps + 0.298)**i*(sigma - 0.816)**j)
        specificVolume = omega*0.0088

    return specificVolume

def p3_hs(enthalpy, entropy):
    '''Supplementary Release on Backward Equations ( ) , p h s for Region 3, Equations as a Function of h and s for the Region Boundaries, and an Equation( ) sat , T hs for Region 4 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam 2004
    Section 3 Backward Functions p(h,s), T(h,s), and v(h,s) for Region 3'''
    entropyBoundary = 4.41202148223476
    pressure = 0.0
    if entropy <= entropyBoundary:
        # Subregion 3a Eq 1, Table 3, Page 8
        i = np.array([0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 6, 7, 8, 10, 10, 14, 18, 20, 22, 22, 24, 28, 28, 32, 32])
        j = np.array([0, 1, 5, 0, 3, 4, 8, 14, 6, 16, 0, 2, 3, 0, 1, 4, 5, 28, 28, 24, 1, 32, 36, 22, 28, 36, 16, 28, 36, 16, 36, 10, 28])
        n = np.array([7.70889828326934, -26.0835009128688, 267.416218930389, 17.2221089496844, -293.54233214597, 614.135601882478, -61056.2757725674, -65127225.1118219, 73591.9313521937, -11664650591.4191, 35.5267086434461, -596.144543825955, -475.842430145708, 69.6781965359503, 335.674250377312, 25052.6809130882, 146997.380630766, 5.38069315091534E+19, 1.43619827291346E+21, 3.64985866165994E+19, -2547.41561156775, 2.40120197096563E+27, -3.93847464679496E+29, 1.47073407024852E+24, -4.26391250432059E+31, 1.94509340621077E+38, 6.66212132114896E+23, 7.06777016552858E+33, 1.75563621975576E+41, 1.08408607429124E+28, 7.30872705175151E+43, 1.5914584739887E+24, 3.77121605943324E+40])
        sigma = entropy/4.4
        eta = enthalpy/2300.0
        ps = sum(n*(eta - 1.01)**i*(sigma - 0.75)**j)
        pressure = ps*99.0
    else:
        # Subregion 3b Eq 2, Table 4, Page 8
        i = np.array([-12, -12, -12, -12, -12, -10, -10, -10, -10, -8, -8, -6, -6, -6, -6, -5, -4, -4, -4, -3, -3, -3, -3, -2, -2, -1, 0, 2, 2, 5, 6, 8, 10, 14, 14])
        j = np.array([2, 10, 12, 14, 20, 2, 10, 14, 18, 2, 8, 2, 6, 7, 8, 10, 4, 5, 8, 1, 3, 5, 6, 0, 1, 0, 3, 0, 1, 0, 1, 1, 1, 3, 7])
        n = np.array([1.25244360717979E-13, -1.26599322553713E-02, 5.06878030140626, 31.7847171154202, -391041.161399932, -9.75733406392044E-11, -18.6312419488279, 510.973543414101, 373847.005822362, 2.99804024666572E-08, 20.0544393820342, -4.98030487662829E-06, -10.230180636003, 55.2819126990325, -206.211367510878, -7940.12232324823, 7.82248472028153, -58.6544326902468, 3550.73647696481, -1.15303107290162E-04, -1.75092403171802, 257.98168774816, -727.048374179467, 1.21644822609198E-04, 3.93137871762692E-02, 7.04181005909296E-03, -82.910820069811, -0.26517881813125, 13.7531682453991, -52.2394090753046, 2405.56298941048, -22736.1631268929, 89074.6343932567, -23923456.5822486, 5687958081.29714])
        sigma = entropy/5.3
        eta = enthalpy/2800.0
        ps = sum(n*(eta - 0.681)**i*(sigma - 0.792)**j)
        pressure = 16.6/ps

    return pressure

def h3_pt(pressure, temperature):
    '''Not avalible with IF 97
    Solve function T3_ph-T=0 with half interval method.'''
    ts = temperature + 1
    lowBound = Region1.h1_pt(pressure, 623.15)
    highBound = Region2.h2_pt(pressure, Boundaries.b23t_p(pressure))
    tolerance = 0.00001
    enthalpy = 0.0
    while abs(temperature - ts) > tolerance:
        enthalpy = (lowBound + highBound)/2.0
        ts = t3_ph(pressure, enthalpy)
        if ts > temperature:
            highBound = enthalpy
        else:
            lowBound = enthalpy

    return enthalpy

def t3_prho(pressure, density):
    '''Solve with Secant Method'''
    f = lambda temperature: p3_rhot(density, temperature) - pressure
    return optimize.newton(f, 623.15, tol=1e-8)

def p3sat_h(enthalpy):
    '''Revised Supplementary Release on Backward Equations for the Functions T(p,h), v(p,h) and T(p,s), v(p,s) for   Region 3 of the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam 2004
       Section 4 Boundary Equations psat(h) and psat(s) for the Saturation Lines of Region 3 see pictures Page 17, Eq 10, Table 17, Page 18'''
    i = np.array([0, 1, 1, 1, 1, 5, 7, 8, 14, 20, 22, 24, 28, 36])
    j = np.array([0, 1, 3, 4, 36, 3, 0, 24, 16, 16, 3, 18, 8, 24])
    n = np.array([0.600073641753024, -9.36203654849857, 24.6590798594147, -107.014222858224, -91582131580576.8, -8623.32011700662, -23.5837344740032, 2.52304969384128E+17, -3.89718771997719E+18, -3.33775713645296E+22, 35649946963.6328, -1.48547544720641E+26, 3.30611514838798E+18, 8.13641294467829E+37])

    h = enthalpy/2600.0
    ps = n*(h - 1.02)**i*(h - 0.608)**j
    return ps.sum()*22.0

def p3sat_s(entropy):
    i = np.array([0, 1, 1, 4, 12, 12, 16, 24, 28, 32])
    j = np.array([0, 1, 32, 7, 4, 14, 36, 10, 0, 18])
    n = np.array([0.639767553612785, -12.9727445396014, -2.24595125848403E+15, 1774667.41801846, 7170793495.71538, -3.78829107169011E+17, -9.55586736431328E+34, 1.87269814676188E+23, 119254746466.473, 1.10649277244882E+36])
    sigma = entropy/5.2
    pressure = sum(n*(sigma - 1.03)**i*(sigma - 0.699)**j)
    return pressure*22.0