
# this subroutine takes the inputs as provided by the front end of IRI
# and processes them into the format required by the imaz model
# and then makes the imaz prediction and returns it to IRI or the front
# end program as appropriate
#
# inputs in iriinput as follows
#        iriinput(0) == glat
#        iriinput(1) == glon
#        iriinput(2) == year
#        iriinput(3) == day number
#        iriinput(4) == hour in UT
#        iriinput(5) == riometer absorption, Lv in dB
#        iriinput(6) == magnetic Ap index (planetary A index)
#        iriinput(7) == 10.7cm Solar Radio Flux
#        iriinput(8) == altitude
#
# output in imazoutput as follows
#        imazoutput(0,1) == number of results, 59 if alt is -1, else 1
#        imazoutput(1,i), i=1,59, altitude values in km
#        imazoutput(2,i), i=1,59, log of the electron density values in m-3
#        imazoutput(3,i), i=1,59, uncertainty on the log(ne) predicted
#        if altitude is not equal to -1, then imazoutput(0,0)=1 and
#        the rest of the imazoutput array is set to 0.0

import numpy as np
from pyimaz import _pyimaz

class imaz:
    def __init__(self):
        pass

    def get_profile(self, lat, lon, year, day, hour, magAp, f10_7, alt, dtype = np.float32):
        return imaz2007(lat, lon, year, day, hour, magAp, f10_7, alt, dtype = np.float32)


def imaz2007(lat, lon, year, day, hour, magAp, f10_7, alt, dtype = np.float32):
    # Check for input parameters' ranges
    # ? Latitude is in 60 - 80 range

    if (lat < 60) or (lat > 80):
        raise ValueError("Latitude value is outside allowed range (60-80 deg. N or S) "
                            "The value {value} is given."
                            .format(value=lat))
    # ? Altitude is in (50-150 km) range
    if (alt < 50) or (alt > 150):
        raise ValueError("Altitude value is outside allowed range (50-150 km)) "
                            "The value {value} is given."
                            .format(value=alt))
    iriinput = np.zeros(10)
    iriinput[0] = lat
    iriinput[1] = lon
    iriinput[2]= year
    iriinput[3] = day
    iriinput[4] = hour
    iriinput[5] = -1
    iriinput[6] = magAp
    iriinput[7] = f10_7
    iriinput[8] = alt
    inf = np.zeros(8)  # +1 по сравнению с фортран_кодом
    of = np.zeros(3)  # +1 по сравнению с фортран_кодом
    pressure = _pyimaz._get_imaz_pressure()  # местоположение!!
    ninf = np.zeros(7)  # +1 по сравнению с фортран_кодом
    imazoutput = np.zeros((4,60))
    # initialise imazoutput and input arrays

    for i in range(1, 61):
        imazoutput[0, i - 1] = 0.0
        imazoutput[1, i - 1] = 0.0
        imazoutput[2, i - 1] = 0.0
        imazoutput[3, i - 1] = 0.0

    for i in range(0, 8):
        inf[i] = 0.0

    for i in range(0, 7):
        ninf[i] = 0.0

    # determine the solar zenith angle from the given inputs
    # use za to calculate the inverse chapman function
    # call
    # csza(iriinput(4),iriinput(5),iriinput(1),iriinput(2),za)
    # call calcchap(za,chp)
    za = csza(iriinput[3], iriinput[4], iriinput[0], iriinput[1])  # call
    chp = calcchap(za)  # call
    ic = 1 / chp
    # determine the local magnetic time
    LMT = detlmt(iriinput[4], iriinput[0])  # call
    # determine the rest absorption and add it to the given
    # riometer absorption to get integral absorption
    # if the given Lv is equal to -1, then no Lv was available and
    # the network trained with no lv input is used.
    nolv = 1
        # define pi which is needed to determine cyclic components of LMT
    pi = np.float32(np.arctan(1.0) * 4.0)
    # model inputs are read into the inf array
    inf[0] = np.float32(np.sin((2 * pi * LMT) / 24.0))
    inf[1] = np.float32(np.cos((2 * pi * LMT) / 24.0))

    ninf[0] = inf[0]
    ninf[1] = inf[1]
    ninf[2] = iriinput[6]
    ninf[3] = za
    ninf[4] = iriinput[7]

    # if altitude is not equal to -1, then calculate 1 electron density
    # for that altitude
    altitude = iriinput[8]
    if (altitude != -1.0):
        # call
        newpres = atop(iriinput[2], iriinput[3], iriinput[0], altitude)
        if (nolv > 0):
            ninf[5] =  np.log10(newpres)
            # call
            of = nolvcase(ninf)
        else:
            inf[6] =  np.log10(newpres)
            # call
            of = iri_imaz(inf)
            imazoutput[3, 1] = np.float32(np.sqrt(np.abs(of[1])))  # проверить!
        # this is the predicted electron density
        # ne(1)=10**of(0)

        ne = np.array([0.0,0.0])
        ne[0] = of[0]
        imazoutput[0, 0] = 1.0
        imazoutput[1, 1] = altitude
        imazoutput[2, 1] = ne[0]
        #print('imazoutput[2, 1]',imazoutput[2, 1])
    else:
        # if altitude is equal to -1, then determine entire profile at each pressure
        # level from approx. 50 km to 150 km.
        for i in range(0, 60):
            if (nolv > 0):
                ninf[5] =  np.log10(pressure[i])
                of = nolvcase(ninf)
            else:
                inf[6] = np.log10(pressure[i])
                # call
                of = iri_imaz(inf)
                imazoutput[4, i + 1] = np.float32(sqrt(abs(of[1])))
            #  ne(1)=10**of(0)
            ne[0] = of[0]
            # call
            altitude = ptoa(iriinput[2], iriinput[2], iriinput[0], pressure[i])
            imazoutput[2, i + 1] = altitude
            imazoutput[3, i + 1] = ne[0]
        imazoutput[1, 1] = 59.0

    notlog = dtype(np.power(10, imazoutput[2, 1]))  # from log 10 el/(m^3)
    #notlog = notlog * 1000000  # el/(m^3)

    return notlog  # Значение электронной концентрации согласно ориг.модели (в фортране индекс(3,2)


# end of imaz subroutine
def iri_imaz(inputs):
    inputs = np.zeros(7)  # +1 т.к. range исключает последний элемент
    output = np.zeros(2)  # +1 т.к. range исключает последний элемент
    MIN = np.array([-1.0000, -1.0000, 0.0048, 0.0000, 36.0957, 66.2000, -3.2518, 5.5051, 0.0000])
    MAX = np.array([1.0000, 1.0000, 6.9840, 300.0000, 139.4015, 282.6000, 1.7482, 12.1830, 5.7708])
    outnet = np.zeros(3)
    innet = np.zeros(7)

    for col in range(0, 7):
        innet[col] = 2.0 * (inputs[col] - MIN[col]) / (MAX[col] - MIN[col]) - 1.0  # проверить с фортан-версией!

    # make the prediction
    outnet = imaz_network(innet)

    outnet[0] = ((outnet[0] - 0.005) * (MAX[7] - MIN[7]) / 0.99) + MIN[7]
    output[0] = outnet[0]

    # predict the error on the prediction
    outnet = imaz_errnetwork(innet)
    outnet[0] = ((outnet[0] - 0.005) * (MAX[8] - MIN[8]) / 0.99) + MIN[8]
    output[1] = outnet[0]
    # end of imaz_main
    #print("output",output )
    return output


def nolvcase(nolinps):

    innet = np.zeros(6)
    nolout = np.zeros(2)
    MIN = np.array([-1.0000, -1.0000, 0.0000, 36.0957, 66.2000, -3.2518, 6.6748, 0.0000])
    MAX = np.array([1.0000, 1.0000, 300.0000, 139.4015, 282.6000, 1.7482, 12.1830, 0.0000])


    for col in range(0, 6):
        innet[col] = ((2.0 * (nolinps[col] - MIN[col])) / ((MAX[col] - MIN[col]))) - 1.0


    # make the prediction
    # call
    outnet = imaz_nolv_network(innet)
    outnet[0] = ((outnet[0] - .005) * (MAX[6] - MIN[6]) / .99) + MIN[6]
    nolout[0] = outnet[0]

    return nolout


# end of nolvcase
def imaz_network(in_netw):
    #
    # this is the subroutine that contains the neural network parameters
    # the log of the electron density is predicted within this subroutine.
    #
    # version: 25/5/2006 -- 7-40-1 architecture
    # version: 08/8/2006 -- 7-40-1 architecture, IC replaced with ZA,
    #                      kt replaced with Ap
    #
    # Lee-Anne McKinnell, Hermanus Magnetic Observatory, South Africa May 2006
    #

    # Объявление констант
    INPNODES = 7
    HIDNODES = 40
    OUTNODES = 1
    #N = (INPNODES * HIDNODES + (OUTNODES * HIDNODES))
    M = (INPNODES + HIDNODES + OUTNODES)
    out = np.zeros(2)
    act = np.zeros(M)
    weights = np.array([-0.511570, -1.251610, 3.301330, -0.222710, -0.460160, -1.574470,
                            5.091690, -2.342130, -2.593550, -4.813430, -0.762100, 2.666360,
                            0.630720, -0.310980, -2.681070, -0.737950, 5.033210, 0.937530,
                            0.767400, 0.859360, -3.015080, -0.524620, 0.333280, -0.743640,
                            -1.899470, 2.391250, 0.059340, -2.842780, 0.848100, -1.242590,
                            -4.808560, -0.764860, -3.556610, 0.012730, 0.557020, 0.695950,
                            0.201190, 6.583740, 0.433680, -3.384950, -0.397710, 8.962710,
                            2.158410, -2.680740, 3.774620, -3.623000, 5.308870, -1.721990,
                            4.005430, -0.591480, -4.444370, -7.058950, -1.557820, 2.464170,
                            4.966210, -0.341480, -0.250610, 0.041340, -1.464550, -0.227440,
                            -23.201790, -0.108190, -1.163280, -1.034100, 0.537130, 3.527760,
                            -4.759410, -3.133740, 3.095230, 0.393590, -0.227350, 0.146800,
                            -38.901039, 1.128410, 6.125960, 0.070250, 0.618450, -1.180230,
                            -0.192650, 4.940770, -8.061800, -4.242340, 1.575060, -1.266670,
                            -0.426560, 1.396180, -5.914350, -4.586080, -2.984010, 1.828430,
                            0.096170, 2.155150, 0.309260, -5.323400, -0.621880, 2.279130,
                            -1.075580, -0.589050, 0.044360, -0.611130, 0.664060, -0.064770,
                            2.298570, -0.368290, -9.149950, -3.007830, 0.888830, 7.172730,
                            -4.082130, -2.401740, 5.679240, 0.782900, 0.012970, 0.070650,
                            4.836210, -0.326470, -1.017220, -0.263850, -2.572160, 0.140260,
                            -0.036810, 2.737490, -0.260510, 17.605829, -0.311940, 1.565280,
                            -0.587830, -0.098550, 19.483780, 0.932060, 6.657780, -0.193010,
                            2.239600, -0.138820, -0.218960, 16.940889, -17.878370, 0.638280,
                            -0.460000, -0.427660, 0.224430, -0.138390, 55.692890, -0.087020,
                            -0.337600, 0.057740, 0.406320, -0.481530, -0.855320, 2.953560,
                            2.399620, 4.966640, -1.321620, 0.540130, -0.755000, -1.417990,
                            4.464280, 1.126410, -0.230860, 0.026320, -1.879580, -2.356170,
                            2.770840, 3.765690, 5.707590, 3.112980, 0.165670, 2.886470,
                            6.908740, 1.719590, 9.146300, -1.128420, -0.111510, 0.776100,
                            -0.561430, -1.311570, 0.601120, 4.944090, 2.829670, 3.422790,
                            -0.278840, 1.353290, 0.045360, -0.352140, -12.060940, 1.228370,
                            2.882760, -0.583560, 6.192290, 1.761750, 0.700150, 5.726920,
                            5.674780, 0.855320, 0.074920, -0.259380, -2.099010, -0.251940,
                            5.827450, 1.360290, 1.275950, 0.936820, -5.552420, 0.722990,
                            0.214770, -15.307230, 19.372511, -0.003070, -0.129680, 0.259180,
                            -1.358110, -0.955560, -5.033250, 0.982570, -2.095000, 1.680010,
                            -1.126520, 1.470120, -1.488670, -5.321600, -1.115620, -0.077010,
                            1.074060, 1.105090, -0.176950, -1.810810, 1.114580, 3.540570,
                            2.981830, -2.139700, 0.210940, 0.260130, -0.194540, 43.032688,
                            -0.941590, -2.513880, -0.113960, 0.962260, 0.099250, -0.101660,
                            2.922000, -0.080960, 6.040510, 0.367810, 9.650310, -2.142320,
                            0.968310, 1.412210, -4.303680, -1.957810, 0.523280, 5.022570,
                            -0.341070, 0.174050, -10.249500, 0.134370, 1.587480, 0.451220,
                            7.028380, 0.037420, 0.016650, -12.501070, -1.133070, -5.728570,
                            0.360390, -0.943100, -0.065900, 0.096160, 6.637800, -0.102490,
                            21.208851, -0.494320, 2.653950, -3.400010, 4.327080, 9.011000,
                            2.155370, 5.769570, 3.353410, -0.487580, -0.454530, -0.531700,
                            1.565920, -0.827030, 0.757980, 0.529170, -0.155670, -0.221730,
                            -0.779870, 1.418380, -1.353460, -0.835610, -1.204970, -0.686860,
                            0.782460, -0.607430, 1.702250, -1.847990, -0.787880, -1.111860,
                            18.901461, 1.648110, -1.269090, -0.434710, -0.495480, -1.312810,
                            -2.133970, -0.553700, -1.438020, -0.949110, 0.773040, -1.201540,
                            -1.418210, -1.695890, 0.374800, -0.449530, -0.909200, -1.750250,
                            0.904870, 0.589450])

    biases = np.array([1.000000, 0.998030, 0.916740, 0.646710, 0.270800, 0.817340,
                            0.815400, 1.316990, -8.335410, -0.424360, -5.549710, -5.571970,
                            3.087960, -0.183890, -10.389000, -1.371900, -2.343540,
                            -38.701450, -4.895420, -11.445310, -8.381840, 2.087660, 0.075450, 0.368070,
                            1.336170, 17.137079, -1.737150, 58.512260, 0.874180, 3.531080,
                            3.491330, -1.300910, 0.320340, -15.543630, 8.062280, -1.904190,
                            3.360630, -4.841030, -8.483840, -2.210050, 42.191399, 4.970690,
                            -3.511160, -6.771350, -11.545940, 3.613440, -0.731090,
                            -12.939760])



    # input layer
    for member in range(0,(INPNODES)):
        act[member] = in_netw[member]


# hidden layer
    for member in range(0,(HIDNODES)):
        unit=member+INPNODES
        sum=0.0

        for source in range(0,(INPNODES)):

            sum=sum+(act[source]*weights[(member*INPNODES)+source])
            if((sum+biases[unit])< 10000.0):
                act[unit]=1/(1+ np.exp(-sum-biases[unit]))
            else:
                act[unit]=0.0


# output layer
    for member in range(0,(OUTNODES)):
         unit=member+INPNODES+HIDNODES
         sum=0.0

         for source in range(0,(HIDNODES)):
            sum=sum+(act[source+INPNODES]*weights[(INPNODES*HIDNODES)+source])
            if((sum+biases[unit])<10000.0):
                act[unit]=1/(1+ np.exp(-sum-biases[unit]))
            else:
                act[unit]=0.0

# the result

    for member in range (0,(OUTNODES)):
         unit=member+INPNODES+HIDNODES
         out[member] = act[unit]

    return out


def imaz_errnetwork(in_err):
    # this is the subroutine that contains the neural network parameters
    # the uncertainty in the predicted log of the electron density is
    # predicted within this subroutine.


    INPNODES = 7
    HIDNODES = 40
    OUTNODES = 1

    N = (INPNODES * HIDNODES + (OUTNODES * HIDNODES))
    M = (INPNODES + HIDNODES + OUTNODES)

    in_err = np.zeros(INPNODES)
    out = np.zeros(OUTNODES)
    weights = np.zeros(N)
    biases = np.zeros(M)
    act = np.zeros(M)

    weights = np.array([-0.105310, -1.127650, 0.392770, -0.713520, 0.925380, -1.606360,
                              -0.185840, -2.687430, -0.331280, -2.668760, 0.685700, 0.080520,
                              0.290320, -1.758100, -4.222380, -2.819080, -0.272980, 0.656130,
                              -2.918490, 3.083010, -1.115220, -0.594210, 0.539000, 0.532970,
                              0.654520, 1.317070, -0.335230, -5.123020, 2.410500, 0.364150,
                              -1.091370, 0.529740, -0.411480, 0.792080, -1.278130, -0.763840,
                              0.066010, -1.027990, 1.073050, -0.646970, -0.527620, -0.167790,
                              -0.238830, -0.255150, -6.860000, -0.473680, -0.344860, 0.497470,
                              -1.021240, -0.232050, -0.470680, -5.653240, 0.423440, -0.260550,
                              1.793200, -0.321980, 0.476480, -0.707270, 1.358910, -0.367560,
                              -6.428190, -0.625990, -1.006140, 0.856220, -0.789120, -0.760610,
                              -0.538160, -0.641960, 1.497400, 1.129090, 1.375940, 0.407700,
                              0.290040, 3.450290, 5.117750, 5.761180, -2.546970, 1.753940,
                              -0.238730, 0.000570, -3.482250, -0.075710, 0.043220, -0.834340,
                              -0.388200, -0.745690, -1.579420, -0.297170, -0.995950, 1.023240,
                              -2.761320, 1.034540, -0.617020, -2.551870, 0.948890, 2.178500,
                              -0.591860, 3.797240, -0.016980, -0.023830, -15.980340, 0.559820,
                              -0.173800, -0.208790, -0.022000, -2.803690, 0.615610, 3.522490,
                              -1.167470, 1.879290, 1.584760, 0.487610, -0.585090, -0.527860,
                              3.349250, -3.575380, -0.875330, 0.428970, -2.742800, -0.254160,
                              2.556020, 0.871240, -1.830670, -0.482570, -1.491150, -0.549490,
                              2.387760, 1.909200, 3.442310, -0.277560, 1.473900, -0.660990,
                              -0.160740, 0.157010, 2.951870, 0.647280, -1.773040, 0.506610,
                              -0.288830, 0.155560, 0.822180, -3.255350, 1.486360, -1.751770,
                              0.968230, -0.777840, 1.807800, -0.484200, -0.013440, 1.211970,
                              1.309910, -1.919040, -7.844890, 0.191000, -0.641110, -0.046510,
                              -2.685450, -1.719270, 0.196330, -1.877280, -1.459280, -0.745170,
                              4.590540, 4.850230, -2.601460, -2.863660, -0.853890, -0.460120,
                              1.751990, -1.608570, -2.410580, 0.671090, -2.433770, -0.365370,
                              -2.651160, -0.692420, 1.150480, 1.560750, -0.934590, 8.118160,
                              0.020940, 1.000870, 0.421630, 1.260740, 1.250440, -0.734110,
                              -0.962600, -2.869310, 0.086850, 0.211140, -1.379770, -0.436460,
                              0.882940, 0.734310, -0.554430, 0.480130, 0.499690, -0.265170,
                              5.302570, 2.983970, 0.404040, -2.176810, 0.793890, 1.145530,
                              -0.876100, -4.672580, -1.096890, -1.810390, -0.196010, 2.009740,
                              -0.714520, -0.792040, -0.513540, 0.041310, -1.590940, 5.047720,
                              0.962710, -0.273990, 0.384170, -1.574580, -2.426650, 1.102960,
                              4.090620, 0.793280, 2.051070, 0.213290, -0.083290, 2.164570,
                              0.112460, 0.223030, -3.053580, 0.451040, -0.051420, 4.669130,
                              0.521860, 1.037520, -0.311460, -2.624650, -0.882530, 0.225230,
                              5.346270, 1.041920, -0.846060, 1.124440, 0.755260, -1.331540,
                              1.646660, -3.189990, 0.209910, 1.110460, 0.298320, 2.572130,
                              2.564860, 2.866820, -5.234080, 1.022460, -2.706360, 1.793960,
                              0.012040, -0.003550, 0.221290, -11.481430, 1.840110, -0.700490,
                              -0.734690, 0.684000, -0.395550, 1.321550, 0.427310, 1.138070,
                              1.311320, 0.731340, 3.684480, 0.331500, 0.740000, 0.774620,
                              -0.652340, 0.548040, 0.178820, 0.374390, -2.094760, -2.705800,
                              1.884110, -2.058660, 2.280880, -1.139060, 6.632080, -6.404510,
                              -3.182430, 0.577210, -1.565290, -2.050070, -2.439870, -4.304150,
                              8.134030, 2.879330, -3.438850, -2.545030, 3.951750, -2.803160,
                              2.548610, 5.040560, 2.863360, 2.352620, -2.959460, -3.086090,
                              -2.554770, -1.044640, -3.101920, -3.252140, -2.754210, 3.429000,
                              3.347190, -3.825990, 6.269090, -3.424240, -2.066190, -9.193190,
                              7.274360, 0.340360])

    biases = np.array([1.000000, 0.998030, 0.916740, 0.646710, 0.270800, 0.817340,
                             0.815400, -1.612240, -1.289640, 0.392060, 1.705290, 0.369720,
                             -0.561920, -4.445460, -6.266580, 0.655770, -0.339970, -0.923520,
                             -0.235640, -1.877280, -1.708540, -13.760660, -0.568650, 1.575980,
                             -1.143810, 2.232160, 1.077230, 0.157130, -2.537520, -0.022530,
                             0.459510, -2.074870, -0.851790, -1.600360, 0.527730, 0.066810,
                             -3.757770, 1.011850, -0.042270, -1.960260, 2.299020, 7.068130,
                             -1.950690, -3.009230, -9.800740, -3.752540, -0.901030, -1.425210])

    for member in range(0, M):
        act[member] = 0.0

    # input layer
    for member in range(0, INPNODES):
        act[member] = in_err[member]

    # hidden layer
    for member in range(0, HIDNODES):
        unit = member + INPNODES
        sum_err = 0.0
        for source in range(0, INPNODES):
            sum_err = sum_err + (act[source] * weights[(member * INPNODES) + source])
        if ((sum_err + biases[unit]) < 10000.0):
            act[unit] = 1 / (1 +  np.exp(-sum_err - biases[unit]))
        else:
            act[unit] = 0.0

    # output layer
    for member in range(0, OUTNODES):
        unit = member + INPNODES + HIDNODES
        sum_err = 0.0
        for source in range(0, HIDNODES):
            sum_err = sum_err + (act[source + INPNODES]) * weights[(INPNODES * HIDNODES) + source]
        if ((sum_err + biases[unit]) < 10000.0):
            act[unit] = 1 / (1 +  np.exp(-sum_err - biases[unit]))
        else:
            act[unit] = 0.0

    # the result
    for member in range(0, OUTNODES):
        unit = member + INPNODES + HIDNODES
        out[member] = act[unit]
    return out


# end of IMAZ_prediction
def imaz_nolv_network(IMAZ_IN):
    # Объявление констант
    INPNODES = 6
    HIDNODES1 = 70
    HIDNODES2 = 70
    OUTNODES = 1

    N = (INPNODES * HIDNODES1) + (HIDNODES1 * HIDNODES2) + (OUTNODES * HIDNODES2)
    M = (INPNODES + HIDNODES1 + HIDNODES2 + OUTNODES)
    # массивы типа real. массив(0:3) это (11 22 445 11), одномерный со случ.значениями

    IMAZ_OUT = np.zeros(OUTNODES)
    act = np.zeros (M)

    # Чтение из txt-файлов, формирование массивов np.array
    data_biases = _pyimaz._get_imaz_data_biases()
    data_weights = _pyimaz._get_imaz_data_weights()
    # input layer

    for member in range(0, INPNODES):
        act[member] = IMAZ_IN[member]
    #print('act = ', act)
        # hidden layer
    for member in range(0, HIDNODES1):
        unit = member + INPNODES
        IMAZ_sum = 0.0
        for source in range(0, INPNODES):
            IMAZ_sum = IMAZ_sum + act[source] * data_weights[(member * INPNODES) + source]
        if (IMAZ_sum + data_biases[unit]) < 10000.0:
            act[unit] = 1 / (1 + np.exp((-IMAZ_sum) - (data_biases[unit])))
        else:
            act[unit] = 0.0

    # hidden layer 2
    for member in range(0, HIDNODES2):
        unit = member + INPNODES + HIDNODES1
        IMAZ_sum = 0.0
        for source in range(0, HIDNODES1):
            IMAZ_sum = IMAZ_sum + (
                    act[source + INPNODES] * data_weights[(member * HIDNODES1) + (HIDNODES1 * INPNODES) + source])
        if (IMAZ_sum + data_biases[unit]) < 10000.0:
            act[unit] = 1 / (1 + np.exp(-IMAZ_sum - data_biases[unit]))
        else:
            act[unit] = 0.0

    # output layer

    for member in range(0, OUTNODES):
        unit = member + INPNODES + HIDNODES1 + HIDNODES2
        IMAZ_sum = 0.0
        for source in range(0, HIDNODES2):
            IMAZ_sum = IMAZ_sum + (act[source + INPNODES + HIDNODES1] * data_weights[
                (INPNODES * HIDNODES1) + (HIDNODES1 * HIDNODES2)+(HIDNODES2 * member) + source])
        if (IMAZ_sum + data_biases[unit]) < 10000.0:
            act[unit] = 1 / (1 + np.exp(-IMAZ_sum - data_biases[unit]))
        else:
            act[unit] = 0.0

    # the result
    for member in range(0, OUTNODES):
        unit = member + INPNODES + HIDNODES1 + HIDNODES2
        IMAZ_OUT[member] = act[unit]
        # end of IMAZ_prediction for no Lv case
    #print("out", IMAZ_OUT)
    return IMAZ_OUT


def detlmt(ah, alat):
    #
    # this subroutine is designed to determine the local magnetic time
    # from the hour and geographic latitude given
    #
    # inputs: ah --> time in UT
    #       alat --> geographic latitude
    #
    # output: almt --> local magnetic time in hours
    #


    if (alat > 60.0):
        Y = 21.433
    else:
        Y = 6.717

    almt = Y + (ah - 24.0)
    if (almt < 0.0):
        almt = almt + 24.0
    #print("almt", almt)
    return almt


# end of detlmt

def csza(ld, t, flat, flon):
    # this subroutine is designed to determine the solar zenith angle
    # from the day, hour and geographic coordinates given
    #
    # inputs: ld --> daynumber
    #          t --> time in UT
    #       flat --> geographic latitude
    #       flon --> geographic longitude
    #
    # output: z --> zenith angle in degrees
    p = np.array([0.0, 0.017203534, 0.034407068, 0.051610602, 0.068814136, 0.0, 0.103221204])
    ARGMAX = 88.0
    # pi=atan(1.0)*4.0
    pi = np.float32(np.arctan(1.0) * 4.0)
    UMR = pi / 180.0
    humr = pi / 12.0
    dumr = pi / 182.5
    dec = np.zeros(7)
    # s/r is formulated in terms of WEST longitude.......................
    wlon = 360.0 - flon  #IMAZ-ошибка (указано Elon)

    # time of equinox for 1980...........................................
    td = ld + (t + wlon / 15.0) / 24.0
    te = td + 0.9369

    # declination of the sun..............................................
    dec[0] = 23.256 * np.sin(p[1] * (te - 82.242))
    dec[1] = 0.381 * np.sin(p[2] * (te - 44.855))
    dec[2] = 0.167 * np.sin(p[3] * (te - 23.355))
    dec[3] = 0.013 * np.sin(p[4] * (te + 11.97))
    dec[4] = 0.011 * np.sin(p[6] * (te - 10.41))
    dcl = dec[0] + dec[1] + dec[2] - dec[3] + dec[4] + 0.339137
    declin = dcl
    dc = dcl * UMR

    # the equation of time................................................
    tf = te - 0.5
    eqt = -7.38 * np.sin(p[1] * (tf - 4.0)) - 9.87 * np.sin(p[2] * (tf + 9.0)) + 0.27 * np.sin(p[3] * (tf - 53.0)) - 0.2 * np.cos(
        p[4] * (tf - 17.0))
    et = eqt * UMR / 4.0
    fa = flat * UMR
    phi = humr * (t - 12.0) + et
    a = np.sin(fa) * np.sin(dc)
    b = np.cos(fa) * np.cos(dc)
    np.cosx = a + b * np.cos(phi)
    if (abs(np.cosx) > 1.0):
        if (np.cosx >= 0.0):
            np.cosx = 1.0
        if (np.cosx < 0.0):
            np.cosx = -1.0
    z = np.arccos(np.cosx) / UMR
    return z


# end of csza

def calcchap(z):
    #
    # this subroutine is designed to determine the inverse chapman function
    # from the solar zenith angle
    #
    # inputs:  z --> solar zenith angle in degrees
    #
    # output: ic --> inverse chapman function
    #
    # NB:: the file chapman.prn is required for this subroutine to work
    #


    values = _pyimaz._get_imaz_chapman()

    # unp.sing chi calculate chapman function
    for j in range(1, 362):
        if ((z > values[1, j - 1]) and (z < values[1, j])):
            m = (values[2, j] - values[2, j - 1]) / (values[1, j] - values[1, j - 1])
            c = values[2, j] - (m * values[1, j])
            ch = (m * z) + c

    return ch

    # do j=2,361

# end of calcchap

def calcresabs(bd, bch, bsf):
    #
    # this subroutine is designed to determine the rest absorption
    # from the day number, solar flux value and the chapman function
    # which has already been determined by calcchap
    #
    # inputs:  bd --> day number
    #         bch --> chapman function value
    #         bsf --> solar flux value
    #
    # output: blra --> rest absorption
    #
    # NB:: the file nighttruequiet.txt is required for this subroutine to work
    #

    nttqvalues = np.zeros((2, 365))
    # getting nighttime true quiet values

    nttqvalues =_pyimaz._get_imaz_nighttruequiet()
    blra = 0.0

    # calculating rest absorption
    for j in range(1, 366):
        if ((int(bd)) == j):
            Ln = nttqvalues[1, j]

    Lo1 = 0.1395
    Lo2 = 0.1909
    n1 = 0.5708
    n2 = 0.546
    F1 = 67.0
    F2 = 200.0

    m = (Lo2 - Lo1) / (F2 - F1)
    c = Lo2 - (m * F2)
    Lo = (m * bsf) + c
    m = (n2 - n1) / (F2 - F1)
    c = n2 - (m * F2)
    n = (m * bsf) + c
    blra = Ln + (Lo * (bch ** -n))

    return blra
    # end of calcresab

def dntodm(dyr, dd):
    #
    # this subroutine is designed to determine the month and day
    # from the daynumber
    #
    # inputs: dyr --> year
    #          dd --> day number
    #
    # output: md --> md[1] = month, md[2] = day
    #

    md = np.array([0, 0])
    if ((dyr % 4) != 0):
        if (dd <= 31.0):
            md[0] = 1.0
            md[1] = dd
        elif (dd <= 59.0):
            md[0] = 2.0
            md[1] = dd - 31.0
        elif (dd <= 90.0):
            md[0] = 3.0
            md[1] = dd - 59.0
        elif (dd <= 120.0):
            md[0] = 4.0
            md[1] = dd - 90.0
        elif (dd <= 151.0):
            md[0] = 5.0
            md[1] = dd - 120.0
        elif (dd <= 181.0):
            md[0] = 6.0
            md[1] = dd - 151.0
        elif (dd <= 212.0):
            md[0] = 7.0
            md[1] = dd - 181.0
        elif (dd <= 243.0):
            md[0] = 8.0
            md[1] = dd - 212.0
        elif (dd <= 273.0):
            md[0] = 9.0
            md[1] = dd - 243.0
        elif (dd <= 304.0):
            md[0] = 10.0
            md[1] = dd - 273.0
        elif (dd <= 334.0):
            md[0] = 11.0
            md[1] = dd - 304.0
        elif (dd <= 365.0):
            md[0] = 12.0
            md[1] = dd - 334.0

    else:
        if (dd <= 31.0):
            md[0] = 1.0
            md[1] = dd
        elif (dd <= 60.0):
            md[0] = 2.0
            md[1] = dd - 31.0
        elif (dd <= 91.0):
            md[0] = 3.0
            md[1] = dd - 60.0
        elif (dd <= 121.0):
            md[0] = 4.0
            md[1] = dd - 91.0
        elif (dd <= 152.0):
            md[0] = 5.0
            md[1] = dd - 121.0
        elif (dd <= 182.0):
            md[0] = 6.0
            md[1] = dd - 152.0
        elif (dd <= 213.0):
            md[0] = 7.0
            md[1] = dd - 182.0
        elif (dd <= 244.0):
            md[0] = 8.0
            md[1] = dd - 213.0
        elif (dd <= 274.0):
            md[0] = 9.0
            md[1] = dd - 244.0
        elif (dd <= 305.0):
            md[0] = 10.0
            md[1] = dd - 274.0
        elif (dd <= 335.0):
            md[0] = 11.0
            md[1] = dd - 305.0
        elif (dd <= 366.0):
            md[0] = 12.0
            md[1] = dd - 335.0
        else:
            return md

    return md

    # end of dntodm

def ptoa(cyr, cd, cgl, cpr):
    #
    # this subroutine is designed to determine the altitude
    # at a certain pressure level
    #
    # inputs: cyr --> year
    #          cd --> day number
    #         cgl --> geographic latitude
    #         cpr --> pressure level
    #
    # output: calt --> altitude
    #
    # NB:: this subroutines calls the subroutine dntodm
    #

    pres70 = np.zeros(111, 49)
    pres60 = np.zeros(111, 13)
    mndd = np.zeros(2)
    # real mndd(2), m, c, WN, t, d
    # integer mm, i, W
    mndd[0] = 0.0
    mndd[1] = 0.0
    # call
    mndd = dntodm(cyr, cd)

    if (cgl < 67.0):

        pres60 = _pyimaz._get_imaz_press_60deg()

        mm = int(mndd[0]) + 1
        if ((cpr > pres60[1, mm]) or (cpr < pres60[111, mm])):
            calt = 160.0

            return calt

        for i in range(2, 112):
            if ((cpr <= pres60[i - 1, mm]) and (cpr > pres60[i, mm])):
                break

        m = (pres60[i, 1] - pres60[i - 1, 1]) / ( np.log10(pres60[i, mm]) -  np.log10(pres60[i - 1, mm]))
        c = pres60[i - 1, 1] - (m *  np.log10(pres60[i - 1, mm]))
        calt = (m *  np.log10(cpr)) + c
    else:
        pres70 = _pyimaz._get_imaz_press_70deg()

        d = 7.75
        if (mndd[0] == 2.0):
            d = 7.0
        if ((mndd[0] == 4.0) or (mndd[0] == 6.0) or (mndd[0] == 9.0) or (mndd[0] == 11)):
            d = 7.5
            t = mndd[1] / d
            WN = ((mndd[0] - 1.0) * 4.0) + (int(t) + 1)
        if (WN > 48.0):
            WN = 48.0
            W = int(WN) + 1
        if ((cpr > pres70[0, W-1]) or (cpr < pres70[110, W-1])):
            calt = 160.0

            return calt

        for i in range(2, 111):
            if ((cpr <= pres70[i - 1, W]) and (cpr > pres70[i, W])):  # уточнить!!!!
                m = (pres70[i, 1] - pres70[i - 1, 1]) / ( np.log10(pres70[i, W]) -  np.log10(pres70[i - 1, W]))
                c = pres70[i - 1, 1] - (m *  np.log10(pres70[i - 1, W]))
                calt = (m *  np.log10(cpr)) + c
    return calt

    # end of ptoa

def atop(eyr, ed, egl, ealt):
    #
    # this subroutine is designed to determine the pressure
    # at a certain altitude
    #
    # inputs: cyr --> year
    #          cd --> day number
    #         cgl --> geographic latitude
    #         calt --> altitude
    #
    # output: cpr --> pressure
    #
    # NB:: this subroutines calls the subroutine dntodm
    #

    mndd = np.zeros(2)
    mndd[0] = 0.0
    mndd[1] = 0.0
    # call
    mndd = dntodm(eyr, ed)
    #print('mndd', mndd)
    a = int(ealt) - 50
    if (egl < 67.0):
        pres60 = _pyimaz._get_imaz_press_60deg()
        mm = int(mndd[0]) 
        epr = pres60[a-1, mm]

    else:
        pres70 = _pyimaz._get_imaz_press_70deg()
        d = 7.75
        if (mndd[0] == 2.0):
            d = 7.0
        if ((mndd[0] == 4.0) or (mndd[0] == 6.0) or (mndd[0] == 9.0) or (mndd[0] == 11)):
            d = 7.5
        t = mndd[1] / d
        WN = ((mndd[0] - 1.0) * 4.0) + (int(t) + 1)
        if (WN > 48.0):
            WN = 48.0
        W = int(WN)
        epr = pres70[a-1, W]
    return epr
# end of atop
