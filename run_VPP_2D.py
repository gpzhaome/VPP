__author__ = 'guopingzhao'

from PyDSTool import *
from VPP_2D import *
from VPP_plot import VPP_plot
from VPP_animation import VPP_ani
import time

# l0, m, iner, k, g, gam, phi, r, d, rvh
phi = -0.0/180.0*pi
r = 0.1
d = 0.1
rvh = sqrt(d*d+r*r-2*d*r*cos(pi-phi))
psi = asin(r*sin(pi-phi)/rvh)

l0 = 1.0
m = 80.0
iner = 4.58 + m*d*d
k = 20.0e3
g = 9.81
gam = (180.0-67.0)*pi/180.0

pars = {'k':k, 'g':g, 'gam':gam, 'l0':l0, 'm':m, 'iner':iner, 'phi':phi, 'psi':psi, 'r':r, 'd':d, 'rvh':rvh}
info(pars, "Parameter values")

zcomic = 1.05
zcomdotic = 0.0
ycomic = 0.0
ycomdotic = 4.9
thetaHic = 90.0/180.0*pi
thetaHdotic = -10.0/180.0*pi

ics = {'ycom':ycomic, 'ycomdot':ycomdotic, 'zcom':zcomic, 'zcomdot':zcomdotic,
       'thetaH':thetaHic, 'thetaHdot':thetaHdotic, 'incontact': 0}
info(ics, "Initial conditions")

VPP = makeVPP2D_Radau(pars, 1e-3)
# VPP = makeVPP2D_Dopri(pars)
# VPP = makeVPP2D_Vode(pars)
VPP.set(verboselevel=0)

t_start = time.clock()

print phi, rvh
print("Computing trajectory...\n")
VPP.compute(force=True, trajname='test', tdata=[0,5], ics=ics, verboselevel=0)

# phi = 10.0/180.0*pi
# r = 0.1
# d = 0.1
# rvh = sqrt(d*d+r*r-2*d*r*cos(pi-phi))
# psi = asin(r*sin(pi-phi)/rvh)
# print phi, rvh, psi
# VPP.compute(pars={'phi':phi, 'psi':psi, 'rvh':rvh}, force=True, trajname='test2', tdata=[0,50], ics=ics, verboselevel=1)
#
# phi = -10.0/180.0*pi
# r = 0.1
# d = 0.1
# rvh = sqrt(d*d+r*r-2*d*r*cos(pi-phi))
# psi = asin(r*sin(pi-phi)/rvh)
# print phi, rvh, psi
# VPP.compute(pars={'phi':phi, 'psi':psi, 'rvh':rvh}, force=True, trajname='test3', tdata=[0,50], ics=ics, verboselevel=1)

t_elapsed = (time.clock() - t_start)
print t_elapsed

# tmp = VPP.sample('test')
# tSta = tmp['t'][0]
# tEnd = tmp['t'][-1]
# tt = np.arange(tSta, tEnd, 0.01)
# pts = VPP('test', tt)
# tim = pts['t']
# print tim.shape
# evs = VPP.getTrajEventTimes('test')
# numTDs = len(evs['touchdown'])
# numLOs = len(evs['liftoff'])
# numPEs = len(evs['peak'])
#
# tEv = evs['touchdown']
# ptIEv1 = VPP('test', tEv)
#
# tEv = evs['liftoff']
# ptIEv2 = VPP('test', tEv)
#
# tEv = evs['peak']
# ptIEv3 = VPP('test', tEv)
#
# dd = tim[1:] - tim[0:-1]
#
# plt.figure(1)
# plt.plot(dd, '+')
#
# plt.figure(2)
# plt.plot(tim, 'x')
# plot([0, 1000], [ptIEv1['t'][2], ptIEv1['t'][2]], 'r-')
# plot([0, 1000], [ptIEv2['t'][2], ptIEv2['t'][2]], 'g-')
# plot([0, 1000], [ptIEv3['t'][2], ptIEv3['t'][2]], 'b-')
# plt.show()

# VPP_plot(VPP, ['test', 'test2', 'test3'], 'plane')
# VPP_plot(VPP, ['test'], 'plane')
#
VPP_ani(VPP, 'test')
show()

# pts = VPP.sample('test')
# a = pts['yfoo']
# b = pts['zfoo']

# plt.figure(1)
# plt.plot(pts['t'], pts['zcom'], 'b', linewidth=2, label='zcom')
# plt.plot(pts['t'], pts['zcomdot'], 'r', linewidth=2, label='zcomdot')
# plt.legend()
# plt.xlabel('t')
# plt.grid()
# plt.show()
#
# plt.figure(1)
# plt.plot(pts['t'], pts['lenSt'], 'b', linewidth=2, label='lenSt')
# # plt.plot(pts['t'], pts['zcomdot'], 'r', linewidth=2, label='zcomdot')
# plt.legend()
# plt.xlabel('t')
# plt.grid()
# plt.show()

