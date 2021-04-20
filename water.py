import iapws
from iapws import IAPWS97


def printTable(water, title = ''):
    print()
    print('---------------------------------------')
    print(' '+title)
    print('---------------------------------------')
    print('T (K)  ', '\t', water.T)
    print('---------------------------------------')
    print('P (MPa)', '\t', water.P)
    print('---------------------------------------')
    print('h (kJ) ', '\t', water.h)
    print('---------------------------------------')
    print('s (kJ) ', '\t', water.s)
    print('---------------------------------------')
    print('v (m3) ', '\t', water.v)
    print('---------------------------------------')
    print('x (-)  ', '\t', water.x)
    print('---------------------------------------')
    print()


water1 = IAPWS97(   P=0.01, x = 0.0     )       # Pressure (P) and quality (x) known
water2 = IAPWS97(   P=15,   s = 0.6492  )       # Pressure (P) and entropy (s) known
water3 = IAPWS97(   P=15,   T = 873     )       # Pressure (P) and temperature (T) known
water4 = IAPWS97(   T=873,   s = 0.6492 )       # Temperature (T) and entropy (s) known
water5 = IAPWS97(   T=485,   h = 2789 ) 


printTable(water5)