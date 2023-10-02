__author__ = 'guopingzhao'

from PyDSTool import *


def VPP_plot(VPP, trajnameAll, plottype=['plane']):
    if not isinstance(plottype, list):
        plottpye = [plottype]

    for trajname in trajnameAll:

        # tmp = VPP.sample('test')
        # tSta = tmp['t'][0]
        # tEnd = tmp['t'][-1]
        # tt = np.arange(tSta, tEnd, 0.01)
        # plotData = VPP(trajname, tt)

        # plotData = VPP.sample(trajname, dt=0.01, doEvents=False, precise=True)
        plotData = VPP.sample(trajname, dt=0.01, doEvents=False, precise=True)

        gam = VPP.query('pars')['gam']

        d = VPP.query('pars')['d']
        l0 = VPP.query('pars')['l0']
        # rvh = VPP.query('pars')['rvh']
        # phi = VPP.query('pars')['phi']

        if 'plane' in plottype:
            tim = plotData['t']
            plt.figure(1)
            plt.plot(tim)

            # tor = plotData['torhip2tru']
            ycom = plotData['ycom']
            zcom = plotData['zcom']
            yhip = plotData['yhip']
            zhip = plotData['zhip']
            yvpp = plotData['yvpp']
            zvpp = plotData['zvpp']
            # grfy = plotData['grfy']
            # grfz = plotData['grfz']

            dd = sqrt((ycom-yhip)**2+(zcom-zhip)**2)
            ll = sqrt((ycom-yvpp)**2+(zcom-zvpp)**2)
            plt.figure(11)
            plt.plot(tim, dd)
            plt.plot(tim, ll)

            # thetaH = plotData['thetaH']
            # thetaHdot = plotData['thetaHdot']
            # plt.figure(2)
            # plot(tim, thetaHdot/pi*180.0)
            # plt.title('thetaHdot')
            #
            # plt.figure(3)
            # plot(tim, thetaH/pi*180.0)
            # plt.title('thetaH')
            # evs = VPP.getTrajEventTimes(trajname)
            # # evName = ['touchdown', 'liftoff', 'peak']
            # ievName = 'touchdown'
            # tEv = evs[ievName]
            # ptIEv = VPP(trajname, tEv)
            # for itEv in tEv:
            #     plt.figure(3)
            #     plt.plot([itEv, itEv], [80,100], 'r-')
            #
            # ievName = 'liftoff'
            # tEv = evs[ievName]
            # ptIEv = VPP(trajname, tEv)
            # for itEv in tEv:
            #     plt.figure(3)
            #     plt.plot([itEv, itEv], [80,100], 'g-')

            # frcaxi = plotData['frcaxi']
            # frcPer = plotData['frcper']
            # tt1 = plotData['tt1']
            # tt2 = plotData['tt2']
            # tt3 = plotData['tt3']
            #
            # plt.figure(22)
            # plot(tim, grfy)
            # plot(tim, grfz)
            # yhip = ycom - d*cos(thetaH)
            # zhip = zcom - d*sin(thetaH)
            #
            # plt.figure(1)
            # plot(tim, tt3)
            # plt.title('tt3')
            #

            #
            # plt.figure(3)
            # plot(tim[-500:], frcaxi[-500:])
            # plt.title('frcaxi')

            # plt.figure(2)
            # plot(tim, tor)
            # plt.title('tor')

            # plt.figure(3)
            # plt.ylabel('z')
            # plt.xlabel('y')
            #
            # plineCom = plot(ycom, zcom, 'c')
            # plineHip = plot(yhip, zhip, 'y')
            #

            # evs = VPP.getTrajEventTimes(trajname)
            # numTDs = len(evs['touchdown'])
            # numLOs = len(evs['liftoff'])
            # numPEs = len(evs['peak'])
            # # evName = ['touchdown', 'liftoff', 'peak']
            # evName = ['peak']
            # for iEv in range(len(evName)):
            #     ievName = evName[iEv]
            #     tEv = evs[ievName]
            #     ptIEv = VPP(trajname, tEv)
            #
                # plt.figure(iEv+10)
                # plt.title(ievName)
                # plt.subplot(2,2,1)
                # plot(tEv, ptIEv['zcom'], 'o-', label='zcom')
                # plt.ylabel('zcom')
                # plt.subplot(2,2,2)
                # plot(tEv, ptIEv['ycomdot'], 'o-', label='ycomdot')
                # plt.ylabel('ycomdot')
                # plt.subplot(2,2,3)
                # plot(tEv, ptIEv['thetaH']*180/pi, 'o-', label='thetaH')
                # plt.ylabel('thetaH')
                # plt.subplot(2,2,4)
                # plot(tEv, ptIEv['thetaHdot']*180/pi, 'o-', label='thetaHdot')
                # plt.ylabel('thetaHdot')

            # pekEvs = evs['peak']
            # ptPek = VPP(trajname, pekEvs)
            # ycomdotPek = ptPek['ycomdot']
            # zcomPek = ptPek['zcom']
            # thetaHPek = ptPek['thetaH']
            # thetaHdotPek = ptPek['thetaHdot']
            # plt.figure(4)
            # plt.subplot(2,2,1)
            # plot(pekEvs, zcomPek, 'o-', label='zcom')
            # plt.ylabel('zcom')
            # plt.subplot(2,2,2)
            # plot(pekEvs, ycomdotPek, 'o-', label='ycomdot')
            # plt.ylabel('zcomdot')
            # plt.subplot(2,2,3)
            # plot(pekEvs, thetaHPek*180/pi, 'o-', label='thetaHPek')
            # plt.ylabel('thetaHPek')
            # plt.subplot(2,2,4)
            # plot(pekEvs, thetaHdotPek*180/pi, 'o-', label='thetaHdotPek')
            # plt.ylabel('thetaHdotPek')
            #
            # for ixEvs in range(numTDs):
            #     tdEv = evs['touchdown'][ixEvs]
            #     pt1 = VPP(trajname, tdEv)
            #
            #     ycomEv = pt1('ycom')
            #     zcomEv = pt1('zcom')
            #     thetaHEv = pt1('thetaH')
            #     yhipEv = ycomEv - d*cos(thetaHEv)
            #     zhipEv = zcomEv - d*sin(thetaHEv)
            #     yfooEv = yhipEv - l0*cos(gam)
            #     zfooEv = 0
            #
            #     plot([ycomEv,yhipEv,yfooEv], [zcomEv,zhipEv,zfooEv], 'r-', linewidth=3)
            #
            #     if ixEvs<numLOs:
            #         loEv = evs['liftoff'][ixEvs]
            #         pt2 = VPP(trajname, loEv)
            #
            #         ycomEv = pt2('ycom')
            #         zcomEv = pt2('zcom')
            #         thetaHEv = pt2('thetaH')
            #         yhipEv = ycomEv - d * cos(thetaHEv)
            #         zhipEv = zcomEv - d * sin(thetaHEv)
            #
            #         plot([ycomEv,yhipEv,yfooEv], [zcomEv,zhipEv,zfooEv], 'g-', linewidth=3)