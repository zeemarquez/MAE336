# %%

import numpy as np
import numpy.linalg as lg
import matplotlib.pyplot as plt
from print_functions import *

k = 0.85
alpha = 5.5 * (10**(-7))
Ti = 25 + 273
Tair = 25 + 273
Tgas = 350 + 273
hgas = 100
hair = 5
l = 50/1000

dt = 10

hours = 5

t = 0
t_final = hours * 3600 # Seconds
t_steady = t_final
steady = True


tau = (alpha*dt)/(l**2)

# INITIAL TEMPERATURE (KELVIN)

T_0 = np.zeros((22,1))
T_0 = T_0 + (25+273)


c1 = 1-(4*tau)-((hgas*l*2*tau)/k)
c2 = 1-(4*tau)
c3 = 1-(4*tau)-((hair*l*2*tau)/k)
c4 = 1-((8/3)*tau)-((4*tau*hgas*l)/(3*k))
c5 = 1-((4)*tau)-((4*tau*hair*l)/(k))
c6 = (hgas*2*tau*l*Tgas)/(k)
c7 = (hair*2*tau*l*Tair)/(k)

def T(i):
    return T_0[i-1][0]

while t < t_final:

    T_1 = np.array([[
        T(1)*c1 + T(5)*2*tau + T(2)*2*tau + c6,
        tau*(T(3)+T(1)+T(6)+T(6)) + T(2)*c2,
        tau*(T(4)+T(2)+T(7)+T(7)) + T(3)*c2,
        T(4)*c3 + T(8)*2*tau + T(3)*2*tau + c7,
        T(5)*c1 + T(1)*tau + T(9)*tau + T(6)*2*tau + c6,
        tau*(T(7)+T(5)+T(10)+T(2)) + T(6)*c2,
        tau*(T(8)+T(6)+T(11)+T(3)) + T(7)*c2,
        T(8)*c3 + T(4)*tau + T(12)*tau + T(7)*2*tau + c7,
        T(9)*c1 + T(5)*tau + T(13)*tau + T(10)*2*tau + c6,
        tau*(T(11)+T(9)+T(14)+T(6)) + T(10)*c2,
        tau*(T(12)+T(10)+T(15)+T(7)) + T(11)*c2,
        T(12)*c3 + T(8)*tau + T(16)*tau + T(11)*2*tau + c7,
        T(13)*c4 + T(9)*(4*tau/3) + T(14)*(4*tau/3)  + (4*tau/3)*(c6/2),
        tau*(T(15)+T(13)+T(17)+T(10)) + T(14)*c2,
        tau*(T(16)+T(14)+T(18)+T(11)) + T(15)*c2,
        T(16)*c3 + T(12)*tau + T(19)*tau + T(15)*2*tau + c7,
        tau*(T(18)+T(14)+T(18)+T(14)) + T(17)*c2,
        tau*(T(19)+T(17)+T(20)+T(15)) + T(18)*c2,
        T(19)*c3 + T(16)*tau + T(21)*tau + T(18)*2*tau + c7,
        tau*(T(21)+T(18)+T(21)+T(18)) + T(20)*c2,
        T(21)*c3 + T(19)*tau + T(22)*tau + T(20)*2*tau + c7,
        T(22)*c5 + T(21)*4*tau + 4*tau*c7,
    ]]).T

    T_0 = T_1

    '''
    if steady and np.max(np.abs(T_1-T_0)) < 0.01:
        t_steady = t
        print()
        print('t steady:',t_steady)
        break
    '''



    t += dt

# %%

printTemperatures(T_1, 'explicit_' + str(hours) + ' hours')
exportTemperatures(T_1, 'explicit_' + str(hours) + 'h')

Pos = np.array([
    [0,0],  #1
    [0,1],  #2
    [0,2],  #3
    [0,3],  #4 
    [1,0],  #5
    [1,1],
    [1,2],
    [1,3],
    [2,0],  #9
    [2,1],
    [2,2],
    [2,3],
    [3,0],  #13
    [3,1],
    [3,2],
    [3,3],
    [4,1],  #17
    [4,2],
    [4,3],
    [5,2],  #20
    [5,3],
    [6,3]   #22
])

def findIndex(x,y):
    indx = None
    for i,row in enumerate(Pos):
        if row[0] == x and row[1] == y:
            indx = i
    return indx

def findT(x,y):
    if findIndex(x,y) != None:
        return T_1[findIndex(x,y)][0]
    else:
        return None

ylist = np.array([i for i in range(4)])
X, Y = np.meshgrid(Pos[:,0], ylist)
Z = np.zeros(np.shape(X))

for i_row,row in enumerate(Z):
    for i_col,col in enumerate(row):
        Z[i_row][i_col] = findT(X[0][i_col],Y[i_row][0])


fig, ax = plt.subplots()
CS = ax.contourf(X, Y, Z,levels=range(240,640,40))
ax.clabel(CS, inline=False, fontsize=10)
ax.set_title('Isothermal lines',pad=30)
ax.grid(True, color='black')
ax.yaxis.set_ticks(np.arange(0, 4, 1))
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.set_aspect('equal')

i = 1
for x,y in Pos:
    ax.text(x-0.15, y-0.15, str(i), style='italic', bbox={'facecolor': 'white', 'alpha': 1, 'pad': 5}, fontsize=6)
    i += 1

fig.colorbar(CS)
plt.show()


# %%
