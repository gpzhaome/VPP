__author__ = 'guopingzhao'

from PyDSTool import *
from copy import copy

dt_global = 1e-4
abseps_global = 1e-11

abseps = abseps_global
dt = dt_global
max_step = dt * 10
# algparams = {'init_step': dt_global, 'max_step': max_step, 'max_pts': 100000}

allgen_names = ['stance', 'flight']

def makeVPP2D_Radau(pars, dt=dt_global, abseps=abseps_global):
    stance_args, flight_args = makeDS_parts(pars, dt, abseps, 'c')

    stanceDS = Generator.Radau_ODEsystem(stance_args)
    flightDS = Generator.Radau_ODEsystem(flight_args)

    stanceMI = makeInterface(stanceDS, True)
    flightMI = makeInterface(flightDS, False)

    return makeVPPModel(stanceMI, flightMI)


def makeVPP2D_Dopri(pars, dt=dt_global, abseps=abseps_global):
    stance_args, flight_args = makeDS_parts(pars, dt, abseps, 'c')

    stanceDS = Generator.Dopri_ODEsystem(stance_args)
    flightDS = Generator.Dopri_ODEsystem(flight_args)

    stanceMI = makeInterface(stanceDS, True)
    flightMI = makeInterface(flightDS, False)

    return makeVPPModel(stanceMI, flightMI)

def makeVPP2D_Vode(pars, dt=dt_global, abseps=abseps_global):
    stance_args, flight_args = makeDS_parts(pars, dt, abseps, 'c')

    stanceDS = Generator.Vode_ODEsystem(stance_args)
    flightDS = Generator.Vode_ODEsystem(flight_args)

    stanceMI = makeInterface(stanceDS, True)
    flightMI = makeInterface(flightDS, False)

    return makeVPPModel(stanceMI, flightMI)


def makeDS_parts(pars, dt, abseps, targetlang='python'):
    assert dt < 1, "dt should be less than 1.0"
    assert abseps < 0.2, "abseps should be less than 0.2"

    if targetlang == 'python':
        max_step = dt
    else:
        max_step = dt * 10

    algparams = {'init_step': dt,
                 'max_step': max_step,
                 'rtol': 1.0e-11,
                 'atol': 1.0e-10,
                 'max_pts': 100000}

    # define events
    liftoff_args = {'eventtol': abseps / 10,
                    'eventdelay': abseps * 10,
                    'eventinterval': abseps * 10,
                    'active': True,
                    'term': True,
                    'precise': True,
                    'name': 'liftoff'}
    liftoff_ev = Events.makeZeroCrossEvent(
        'callenSt(ycom,initcond(ycom),zcom,thetaH,initcond(thetaH)) - l0', 1,
        liftoff_args, ['ycom', 'zcom', 'thetaH'], ['l0','d', 'gam'],
        fnspecs={'callenSt': (['ycom','ycomic','zcom','thH','thHic'],
                              'sqrt(calyrel(calyhip(ycom,thH),calyhip(ycomic,thHic))**2 + calzhip(zcom,thH)**2)'),
                 'calyrel': (['y', 'yic'], 'y-yic+l0*cos(gam)'),
                 'calyhip': (['y', 'thH'], 'y-d*cos(thH)'),
                 'calzhip': (['z', 'thH'], 'z-d*sin(thH)')},
        targetlang=targetlang)

    touchdown_args = {'eventtol': abseps / 10,
                      'eventdelay': abseps * 10,
                      'eventinterval': abseps * 10,
                      'active': True,
                      'term': True,
                      'precise': True,
                      'name': 'touchdown'}
    touchdown_ev = Events.makeZeroCrossEvent('calzhip(zcom,thetaH) - l0*sin(gam)', -1,
                                             touchdown_args, ['zcom', 'thetaH'], ['l0', 'd', 'gam'],
                                             fnspecs={'calzhip': (['z', 'thH'], 'z-d*sin(thH)')},
                                             targetlang=targetlang)

    peak_args = {'eventtol': abseps / 10,
                 'eventdelay': abseps * 10,
                 'eventinterval': abseps * 10,
                 'active': True,
                 'term': False,
                 'precise': True,
                 'name': 'peak'}
    peak_ev = Events.makeZeroCrossEvent('zcomdot', -1, peak_args, ['zcomdot'], [], targetlang=targetlang)

    nadir_args = {'eventtol': abseps / 10,
                 'eventdelay': abseps * 10,
                 'eventinterval': abseps * 10,
                 'active': True,
                 'term': False,
                 'precise': True,
                 'name': 'nadir'}
    nadir_ev =Events.makeZeroCrossEvent('zcomdot', 1, nadir_args, ['zcomdot'], [], targetlang=targetlang)

    # phase arguments
    stance_args = getStanceArgs(algparams, [liftoff_ev, nadir_ev], pars, abseps)
    flight_args = getFlightArgs(algparams, [touchdown_ev, peak_ev], pars, abseps)


    return (stance_args, flight_args)

def getStanceArgs(algparams, eventAll, pars, abseps):
    return {'pars': pars, # l0, m, iner, k, phi, r, d, rvh
            'fnspecs': {'calgrfy': (['y','yic','z','zic','thH','thHic'],
                                    'calfrcaxi(y,yic,z,thH,thHic)*cos(calthetaSt(y,yic,z,thH,thHic)) + calfrcper(y,yic,z,thH,thHic)*sin(pi-calthetaSt(y,yic,z,thH,thHic))'),
                        'calgrfz': (['y','yic','z','zic','thH','thHic'],
                                    'calfrcaxi(y,yic,z,thH,thHic)*sin(calthetaSt(y,yic,z,thH,thHic)) + calfrcper(y,yic,z,thH,thHic)*cos(pi-calthetaSt(y,yic,z,thH,thHic))'),
                        'calfrcaxi': (['y','yic','z','thH','thHic'],
                                      'k * (l0-callenSt(y,yic,z,thH,thHic))'),
                        'calfrcper': (['y','yic','z','thH','thHic'],
                                      'calfrcaxi(y,yic,z,thH,thHic) * caltanalpha(y,yic,z,thH,thHic)'),
                        'callenSt': (['ycom','ycomic','zcom','thH','thHic'],
                                     'sqrt(calyrel(calyhip(ycom,thH),calyhip(ycomic,thHic))**2 + calzhip(zcom,thH)**2)'),
                        'calyrel': (['y','yic'], 'y-yic+l0*cos(gam)'),
                        'calyfooinit': (['ycomic','thHic'], 'ycomic-d*cos(thHic)-l0*cos(gam)'),
                        'calthetaSt': (['y','yic','z','thH','thHic'],
                                       'acos( calyrel(calyhip(y,thH),calyhip(yic,thHic)) / callenSt(y,yic,z,thH,thHic) )'),
                        'caltanalpha': (['y','yic','z','thH','thHic'],
                                        'sin(thH+psi+pi-calthetaSt(y,yic,z,thH,thHic)) * rvh / (callenSt(y,yic,z,thH,thHic) - rvh*cos(thH+psi+pi-calthetaSt(y,yic,z,thH,thHic)))'),
                        'caltorhip2tru': (['y','yic','z','thH','thHic'],
                                          'calfrcper(y,yic,z,thH,thHic) * callenSt(y,yic,z,thH,thHic)'),
                                          # 'calfrcper(y,yic,z,thH,thHic) * callenSt(y,yic,z,thH,thHic) * sign(calyvpp(y,thH)-calyhip(y,thH))'),
                        'calthetaVF': (['y','yic','z','thH','thHic'],
                                       'acos( calyrel(calyvpp(y,thH),calyhip(yic,thHic))/sqrt(calyrel(calyvpp(y,thH),calyhip(yic,thHic))**2+calzvpp(z,thH)**2) )'),
                        'calyvpp': (['ycom', 'thetaH'], 'r*cos(phi+thetaH) + ycom'),
                        'calzvpp': (['zcom', 'thetaH'], 'r*sin(phi+thetaH) + zcom'),
                        'calyhip': (['ycom', 'thetaH'], 'ycom-d*cos(thetaH)'),
                        'calzhip': (['zcom', 'thetaH'], 'zcom-d*sin(thetaH)'),
                        'caltt1': (['y','yic','z','thH','thHic'], 'sign(calthetaSt(y,yic,z,thH,thHic) - calthetaVF(y,yic,z,thH,thHic))'),
                        'caltt2': (['y','yic','z','thH','thHic'], 'caltanalpha(y,yic,z,thH,thHic)')},
            'varspecs': {'ycom': "ycomdot",
                         'ycomdot': "calgrfy(ycom,initcond(ycom),zcom,initcond(zcom),thetaH,initcond(thetaH)) / m",
                         'zcom': "zcomdot",
                         'zcomdot': "calgrfz(ycom,initcond(ycom),zcom,initcond(zcom),thetaH,initcond(thetaH)) / m - g",
                         'thetaH': "thetaHdot",
                         # 'thetaHdot': "( calgrfy(ycom,initcond(ycom),zcom,initcond(zcom),thetaH,initcond(thetaH))*zcom + calgrfz(ycom,initcond(ycom),zcom,initcond(zcom),thetaH,initcond(thetaH))*(-ycom+calyfooinit(initcond(ycom),initcond(thetaH))) )/ iner",
                         'thetaHdot': "( caltorhip2tru(ycom,initcond(ycom),zcom,thetaH,initcond(thetaH)) - m*g*d*cos(thetaH) )/ iner",
                         # 'lenSt': "callenSt(ycom,initcond(ycom),zcom,thetaH,initcond(thetaH))",
                         'frcaxi': "calfrcaxi(ycom,initcond(ycom),zcom,thetaH,initcond(thetaH))",
                         'frcper': "calfrcper(ycom,initcond(ycom),zcom,thetaH,initcond(thetaH))",
                         'torhip2tru': "caltorhip2tru(ycom,initcond(ycom),zcom,thetaH,initcond(thetaH))",
                         'grfy': "calgrfy(ycom,initcond(ycom),zcom,initcond(zcom),thetaH,initcond(thetaH))",
                         'grfz': "calgrfz(ycom,initcond(ycom),zcom,initcond(zcom),thetaH,initcond(thetaH))",
                         'yvpp': "calyvpp(ycom,thetaH)",
                         'zvpp': "calzvpp(zcom,thetaH)",
                         'yhip': "calyhip(ycom,thetaH)",
                         'zhip': "calzhip(zcom,thetaH)",
                         'yfoo': "initcond(ycom)-d*cos(initcond(thetaH))-l0*cos(gam)",
                         'zfoo': "initcond(zcom)-d*sin(initcond(thetaH))-l0*sin(gam)",
                         # 'tt3': "caltanalpha(ycom,initcond(ycom),zcom,thetaH,initcond(thetaH))",
                         # 'tt3': "calthetaSt(ycom,initcond(ycom),zcom,thetaH,initcond(thetaH)) - atan(caltanalpha(ycom,initcond(ycom),zcom,thetaH,initcond(thetaH)))",
                         'incontact': "0"},
            'auxvars': ['frcaxi', 'frcper', 'torhip2tru', 'grfy', 'grfz', 'yvpp', 'zvpp', 'yhip', 'zhip', 'yfoo', 'zfoo'],
            # 'auxvars': ['lenSt', 'frcaxi', 'frcper', 'torhip2tru', 'grfy', 'grfz', 'yvpp', 'zvpp', 'yhip', 'zhip', 'yfoo', 'zfoo', 'tt3'],
            # 'auxvars': ['yfoo', 'zfoo'],
            'xdomain': {'ycom': [0,Inf], 'zcom': [0,Inf], 'thetaH': [-pi,pi], 'incontact': 1},
            'pdomain': {'gam': [pi/2,pi]},
            # 'ics': {'lenSt': 1.0, 'frcaxi': 0.0, 'frcper': 0.0, 'torhip2tru': 0.0, 'incontact': 1},
            'ics': {'incontact': 1},
            'xtype': {'incontact': int},
            'algparams': algparams,
            'events': eventAll,
            'abseps': abseps,
            'name': 'stance'}

def getFlightArgs(algparams, eventAll, pars, abseps):
    return {'pars': pars,
            'fnspecs': {'calzhip': (['z', 'thH'], 'z-d*sin(thH)')},
            'varspecs': {'ycom': "ycomdot",
                         'ycomdot': "0",
                         'zcom': "zcomdot",
                         'zcomdot': "-g",
                         'thetaH': "thetaHdot",
                         'thetaHdot': "0",
                         # 'lenSt': "l0",
                         'frcaxi': "0",
                         'frcper': "0",
                         'torhip2tru': "0",
                         'grfy': "0",
                         'grfz': "0",
                         'yvpp': "r*cos(phi+thetaH) + ycom",
                         'zvpp': "r*sin(phi+thetaH) + zcom",
                         'yhip': "ycom-d*cos(thetaH)",
                         'zhip': "zcom-d*sin(thetaH)",
                         'yfoo': "ycom-d*cos(thetaH)-l0*cos(gam)",
                         'zfoo': "zcom-d*sin(thetaH)-l0*sin(gam)",
                         # 'tt3': "0",
                         'incontact': "0"},
            'auxvars': ['frcaxi', 'frcper', 'torhip2tru', 'grfy', 'grfz', 'yvpp', 'zvpp', 'yhip', 'zhip', 'yfoo', 'zfoo'],
            # 'auxvars': ['lenSt', 'frcaxi', 'frcper', 'torhip2tru', 'grfy', 'grfz', 'yvpp', 'zvpp', 'yhip', 'zhip', 'yfoo', 'zfoo', 'tt3'],
            # 'auxvars': ['yfoo', 'zfoo'],
            'xdomain': {'ycom': [0,Inf], 'zcom': [0,Inf], 'thetaH': [-pi,pi], 'incontact': 0},
            'pdomain': {'gam': [pi/2,pi]},
            # 'ics': {'lenSt': 1.0, 'frcaxi': 0.0, 'frcper': 0.0, 'torhip2tru': 0.0, 'incontact': 0},
            'ics': {'incontact': 0},
            'xtype': {'incontact': int},
            'algparams': algparams,
            'events': eventAll,
            'abseps': abseps,
            'name': 'flight'}

def makeInterface(DS, incontact):
    # initial conditions are dummies
    # end time 100 is arbitrary but should be much longer than possibly needed
    ycomd = 0.1
    zcomd = 1.8
    thetaHd = pi/2
    return intModelInterface(embed(DS,
                                   icdict={'ycom': ycomd,
                                           'zcom': zcomd,
                                           'thetaH': thetaHd,
                                           # 'lenSt': 1.0,
                                           'frcaxi': 0.0,
                                           'frcper': 0.0,
                                           'torhip2tru': 0.0,
                                           'yvpp': 0.0,
                                           'zvpp': 0.0,
                                           'grfy': 0.0,
                                           'grfz': 0.0,
                                           'yhip': 0.0,
                                           'zhip': 0.0,
                                           'yfoo': 0.0,
                                           'zfoo': 0.0,
                                           # 'tt3': 0.0,
                                           'incontact': int(incontact)},
                                   tdata=[0,200]))

def makeVPPModel(stanceMI, flightMI):
    flightMI_info = makeModelInfoEntry(flightMI, allgen_names,
                                       [('touchdown', ('stance', EvMapping({"incontact": "1"}, model=flightMI.model)))])
    stanceMI_info = makeModelInfoEntry(stanceMI, allgen_names,
                                       [('liftoff', ('flight', EvMapping({"incontact": "0"}, model=stanceMI.model)))])

    modelInfoDict = makeModelInfo([stanceMI_info, flightMI_info])
    VPPModel = Model.HybridModel({'name': 'VPP', 'modelInfo': modelInfoDict})

    # promote aux vars from Generators to "vars" in the hybrid model
    VPPModel.forceIntVars(['frcaxi', 'frcper', 'grfy', 'grfz', 'torhip2tru'])
    # VPPModel.forceIntVars(['lenSt', 'frcaxi', 'frcper', 'grfy', 'grfz', 'torhip2tru'])
    VPPModel.forceIntVars(['yfoo', 'zfoo'])
    return VPPModel