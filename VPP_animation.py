__author__ = 'guopingzhao'
from PyDSTool import *
from matplotlib.patches import Ellipse
from matplotlib import animation

# def initfunc():
#     aniLeg.set_data([], [])
#     aniTru.set_data([], [])
#     aniVpp.set_data([], [])
#     aniCom.set_data([], [])
#     aniHip.set_data([], [])
#     aniFoo.set_data([], [])
#     aniFrc.set_data([], [])
#
#     aniTimeText.set_text('')
#     ax.set_xlim()
#
#     return aniLeg, aniTru, aniVpp, aniCom, aniHip, aniFoo, aniFrc

def anifunc(iFrame, data, aniHandles):
    ax, aniLeg, aniVF, aniCom, aniFoo, aniHip, aniVpp, aniTru, aniTimeText = aniHandles

    tim = data['t'][iFrame]
    posFoo = [data['yfoo'][iFrame], data['zfoo'][iFrame]]
    posCom = [data['ycom'][iFrame], data['zcom'][iFrame]]
    posHip = [data['yhip'][iFrame], data['zhip'][iFrame]]
    posVpp = [data['yvpp'][iFrame], data['zvpp'][iFrame]]
    thetaH = data['thetaH'][iFrame]
    grf = [data['grfy'][iFrame], data['grfz'][iFrame]]

    posTru = [posCom[0]+0.2*cos(thetaH), posCom[1]+0.2*sin(thetaH)]

    aniCom.set_data(posCom)
    aniFoo.set_data(posFoo)
    aniHip.set_data(posHip)
    aniVpp.set_data(posVpp)
    aniTru.center = posTru
    aniTru.angle = thetaH*180.0/pi
    aniTimeText.set_text('time = %.2f s' % tim)

    isStance = data['incontact'][iFrame]
    if isStance:
        aniLeg.set_data([posHip[0], posFoo[0]],
                        [posHip[1], posFoo[1]])
        aniLeg.set_linewidth(4)
        aniLeg.set_color('r')
        th = pi/2.0 - atan(grf[0]/grf[1])
        pTemp = [posFoo[0]+3.0*cos(th), posFoo[1]+3.0*sin(th)]
        aniVF.set_data([posFoo[0], pTemp[0]],
                       [posFoo[1], pTemp[1]])
    else:
        aniLeg.set_data([posHip[0], posFoo[0]],
                        [posHip[1], posFoo[1]])
        aniLeg.set_linewidth(2)
        aniLeg.set_color('b')
        aniVF.set_data([posFoo[0], posFoo[0]],
                       [posFoo[1], posFoo[1]])

    axXMin = posVpp[0] - 0.5
    axXMax = posVpp[0] + 0.5
    ax.set_xlim(axXMin, axXMax)

    return aniCom, aniVF, aniFoo, aniHip, aniVpp, aniTru, aniTimeText

def VPP_ani(VPP, trajName):
    # tmp = VPP.sample('test')
    # tSta = tmp['t'][0]
    # tEnd = tmp['t'][-1]
    # tt = np.arange(tSta, tEnd, 0.01)
    # plotData = VPP(trajName, tt)

    plotData = VPP.sample(trajName, dt=0.01, doEvents=False)
    tim = plotData['t']

#    figAni = plt.figure(20, figsize=(16, 6))
    figAni = plt.figure(20, figsize=(6, 6))
    ax = figAni.add_subplot(111)
    ax.axis('equal')
    axXMax = 0.5
    axXMin = -0.5
    ax.set_xlim(axXMin, axXMax)
    ax.set_ylim(-0.2, 2.0)
    ax.set_xlabel('Fore-aft/meter')
    ax.set_ylabel('Vertical/meter')
    ax.set_title('VPP 2D Running')

    ax.plot([0, 100], [0, 0], color='0.75') # ground level

    aniLeg, = ax.plot([], [], 'b-', lw=2)
    aniVF, = ax.plot([], [], 'k--', lw=1)
    aniCom, = ax.plot([], [], 'ko', ms=6)
    aniFoo, = ax.plot([], [], 'co', ms=4)
    aniHip, = ax.plot([], [], 'mo', ms=6)
    aniVpp, = ax.plot([], [], 'ro', ms=6)
    posCom = [plotData['ycom'][0], plotData['zcom'][0]]
    thetaH = plotData['thetaH']
    posTru = [posCom[0]+0.2*cos(thetaH), posCom[1]+0.2*sin(thetaH)]
    aniTru = Ellipse(xy=[posTru[0], posTru[0]],
                     width=0.7, height=0.3, angle=plotData['thetaH'][0]*180.0/pi)
    aniTru.set_facecolor([147/255.0, 225/255.0, 249/255.0])
    ax.add_artist(aniTru)
    aniTimeText = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    aniHandles = [ax, aniLeg, aniVF, aniCom, aniFoo, aniHip, aniVpp, aniTru, aniTimeText]
    ani = animation.FuncAnimation(figAni, anifunc, frames=len(tim), fargs=(plotData,aniHandles),
                                  interval=20, blit=False)

    mywriter = animation.writers['ffmpeg']
    writer = mywriter(fps=15, metadata=dict(artist='GuopingZhao'), bitrate=1800)
    ani.save('test.mp4', writer=writer)

    plt.show()
