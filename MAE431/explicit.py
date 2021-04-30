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

dt = 1

hours = 5

t = 0
t_final = hours * 3600 # Seconds
t_steady = t_final
steady = True


tau = (alpha*dt)/(l**2)
nu = -1-(4*tau)
g = -((hgas*l)/k) - 2 - (1/(2*tau))
a = -((hair*l)/k) - 2 - (1/(2*tau))

# INITIAL TEMPERATURE (KELVIN)

T_1 = 25 + 273
T_2 = 25 + 273
T_3 = 25 + 273
T_4 = 25 + 273
T_5 = 25 + 273
T_6 = 25 + 273
T_7 = 25 + 273
T_8 = 25 + 273
T_9 = 25 + 273
T_10 = 25 + 273
T_11 = 25 + 273
T_12 = 25 + 273
T_13 = 25 + 273
T_14 = 25 + 273
T_15 = 25 + 273
T_16 = 25 + 273
T_17 = 25 + 273
T_18 = 25 + 273
T_19 = 25 + 273
T_20 = 25 + 273
T_21 = 25 + 273
T_22 = 25 + 273

T = np.array([[T_1, T_2, T_3, T_4, T_5, T_6, T_7, T_8, T_9, T_10, T_11, T_12, T_13, T_14, T_15, T_16, T_17, T_18, T_19, T_20, T_21, T_22]]).T

A = np.zeros((22,22))

A[0][0] = g
A[0][1] = 1
A[0][4] = 1

A[1][0] = tau
A[1][1] = nu
A[1][2] = tau
A[1][5] = tau*2

A[2][1] = tau
A[2][2] = nu
A[2][3] = tau
A[2][6] = tau*2

A[3][3] = a
A[3][2] = 1
A[3][8] = 1

A[4][0] = 0.5
A[4][4] = g
A[4][5] = 1
A[4][8] = 0.5

A[5][1] = tau
A[5][4] = tau
A[5][5] = nu
A[5][6] = tau
A[5][9] = tau

A[6][2] = tau
A[6][5] = tau
A[6][6] = nu
A[6][7] = tau
A[6][10] = tau

A[7][3] = 0.5
A[7][7] = a
A[7][6] = 1
A[7][11] = 0.5

A[8][4] = 0.5
A[8][8] = g
A[8][9] = 1
A[8][12] = 0.5

A[9][5] = tau
A[9][8] = tau
A[9][9] = nu
A[9][10] = tau
A[9][13] = tau

A[10][6] = tau
A[10][9] = tau
A[10][10] = nu
A[10][11] = tau
A[10][14] = tau

A[11][7] = 0.5
A[11][11] = a
A[11][10] = 1
A[11][15] = 0.5

A[12][8] = 1
A[12][12] = -((hgas*l)/k)-3-(3/(4*tau))
A[12][13] = 2

A[13][9] = tau
A[13][12] = tau
A[13][13] = nu
A[13][14] = tau
A[13][16] = tau

A[14][10] = tau
A[14][13] = tau
A[14][14] = nu
A[14][15] = tau
A[14][17] = tau

A[15][11] = 0.5
A[15][15] = a
A[15][14] = 1
A[15][18] = 0.5

A[16][13] = 2*tau
A[16][16] = nu
A[16][17] = 2*tau

A[17][14] = tau
A[17][16] = tau
A[17][17] = nu
A[17][18] = tau
A[17][19] = tau

A[18][15] = 0.5
A[18][18] = a
A[18][17] = 1
A[18][20] = 0.5

A[19][17] = 2*tau
A[19][19] = nu
A[19][20] = 2*tau

A[20][18] = 0.5
A[20][20] = a
A[20][19] = 1
A[20][21] = 0.5

A[21][20] = 1
A[21][21] = (a/2) - (hair*l)/(2*k)

A_inv = lg.inv(A)

def f_gas(T_i):
    return (-T_i/(2*tau))-((l*hgas*Tgas)/k)
def f_air(T_i):
    return (-T_i/(2*tau))-((l*hair*Tair)/k)


while t < t_final:

    C = np.zeros((22,1))

    C[0] = f_gas(T[0][0])
    C[1] = -T[1][0]
    C[2] = -T[2][0]
    C[3] = f_air(T[3][0])
    C[4] = f_gas(T[4][0])
    C[5] = -T[5][0]
    C[6] = -T[6][0]
    C[7] = f_air(T[7][0])
    C[8] = f_gas(T[8][0])
    C[9] = -T[9][0]
    C[10] = -T[10][0]
    C[11] = f_air(T[11][0])
    C[12] = (-(3/(4*tau))*T[12][0])-((hgas*l*Tgas)/k)
    C[13] = -T[13][0]
    C[14] = -T[14][0]
    C[15] = f_air(T[15][0])
    C[16] = -T[16][0]
    C[17] = -T[17][0]
    C[18] = f_air(T[18][0])
    C[19] = -T[19][0]
    C[20] = f_air(T[20][0])
    C[21] = (-T[21][0]/(4*tau)) - ((l*hair*Tair)/k)

    T_0 = T
    T =  np.dot(A_inv,C) 

    if steady and np.max(np.abs(T-T_0)) < 0.01:
        t_steady = t
        print()
        print('t steady:',t_steady)
        break



    t += dt

printTemperatures(T, str(hours) + ' hours')
exportTemperatures(T, str(hours) + 'h')

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
        return T[findIndex(x,y)][0]
    else:
        return None

ylist = np.array([i for i in range(4)])
X, Y = np.meshgrid(Pos[:,0], ylist)
Z = np.zeros(np.shape(X))

for i_row,row in enumerate(Z):
    for i_col,col in enumerate(row):
        Z[i_row][i_col] = findT(X[0][i_col],Y[i_row][0])


fig, ax = plt.subplots()
CS = ax.contourf(X, Y, Z,levels=range(300,640,40))
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