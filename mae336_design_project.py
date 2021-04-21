import iapws
from iapws import IAPWS97
import matplotlib.pyplot as plt

col_width = 10

class State():

    def __init__(self,**kwargs):

        self.T = kwargs.get('T')
        self.P = kwargs.get('P')
        self.h = kwargs.get('h')
        self.x = kwargs.get('x')
        self.s = kwargs.get('s')
        self.v = kwargs.get('v')

        self.iapws = self.get_iapws()

        if self.iapws != None:
            self.calculable = True
            if self.T == None:
                self.T = self.iapws.T
            if self.P == None:
                self.P = self.iapws.P
            if self.h == None:
                self.h = self.iapws.h
            if self.x == None:
                self.x = self.iapws.x
            if self.s == None:
                self.s = self.iapws.s
            if self.v == None:
                self.v = self.iapws.v
        else:
            self.calculable = False
        
    def get_iapws(self):

        if self.T != None and self.P !=None:
            return IAPWS97(T=self.T, P=self.P)
        elif self.P != None and self.x !=None:
            return IAPWS97(x=self.x, P=self.P)
        elif self.P != None and self.s !=None:
            return IAPWS97(s=self.s, P=self.P)
        elif self.T != None and self.s !=None:
            return IAPWS97(s=self.s, T=self.T)
        elif self.P != None and self.h !=None:
            return IAPWS97(P=self.P, h=self.h)
        else:
            return None

    def get_csv_line(self, state_id):

        columns = [
            '',
            str(round(self.T,3)),
            str(round(self.P,4)),
            str(round(self.h,3)),
            str(round(self.s,3)),
            str(round(self.x,3)),
            str(round(self.v,5))
        ]
        if state_id != None:
            columns[0] = state_id
        line = ';'.join(columns)

        return line + "\n"
    
    def get_csv_header():
        columns = [
            ' ',
            'T (K)',
            'P (MPa)',
            'h (kJ/kg)',
            's (kJK/kg)',
            'x (-)',
            'v (m3/kg)'
        ]
        line = ';'.join(columns)

        return line + "\n"

    def print_state(self, state_id = None):

        columns = [
            '',
            round(self.T,3),
            round(self.P,4),
            round(self.h,3),
            round(self.s,3),
            round(self.x,3),
            round(self.v,5)
        ]
        if state_id != None:
            columns[0] = state_id

        line = ''
        for col in columns:
            col = str(col)
            if len(col) < col_width:
                col = ''.join([' ' for x in range(col_width - len(col))]) + col
            line = line + col + ' | '
        
        print(line)
        print(''.join(['-' for x in line]))

    def print_headers():
        columns = [
            '',
            'T (K)',
            'P (MPa)',
            'h (kJ/kg)',
            's (kJK/kg)',
            'x (-)',
            'v (m3/kg)'
        ]

        line = ''
        for col in columns:
            if len(col) < col_width:
                col = ''.join([' ' for x in range(col_width - len(col))]) + col
            line = line + col + ' | '

        print()
        print(''.join(['-' for x in line]))
        print(line)
        print(''.join(['-' for x in line]))
       
'''

Pressure:       P (MPa)
Temperature:    T (K)
Enthalpy:       h (kJ/kg)
Entropy:        s (kJ K/kg) 

'''


# Pressure Closed Heater
p_ch = 2

# Pressure Open Heater
p_oh = 0.3

# Pressure Condenser
p_cond = 0.006

p_ch_list = []
th_list = []
y2_list = []
y3_list = []
y4_list = []
qin_list = []
qout_list = []
wnet_list = []

for j in range(5,115,10):

    p_ch = j/10

    efficiency = 0.8
    m1 = 1.5 * (10**4) #kg/s

    _1 = State(T=(480+273),P=12)

    _2s = State(P=p_ch, s= _1.s)
    _3s = State(P=p_oh, s= _1.s)
    _4s = State(P=p_cond, s= _1.s)

    h2 = _1.h + efficiency*(_2s.h - _1.h)
    h3 = _1.h + efficiency*(_3s.h - _1.h)
    h4 = _1.h + efficiency*(_4s.h - _1.h)

    _2 = State(h=h2, P=p_ch)
    _3 = State(h=h3, P=p_oh)
    _4 = State(h=h4, P=p_cond)

    _5 = State(P=p_cond, x=0)
    _6s = State(P=p_oh,s=_5.s)

    h6 = _5.h + ((_6s.h - _5.h)/efficiency)

    _6 = State(h=h6, P=p_oh)
    _7 = State(x=0, P=p_oh)

    _8s = State(P=12,s=_7.s)     #P8 = P9 = 12MPa

    h8 = _7.h + ((_8s.h - _7.h)/efficiency)

    _8 = State(h=h8, P=12)
    _9 = State(T=(210+273), P=12)
    _10 = State(P=p_ch, x=0)       # h10 = h11
    _11 = State(P=p_oh, h=_10.h)

    m2 = m1 * (abs(_9.h-_8.h)/abs(_2.h-_10.h))
    m4 = (m1*(1- (_7.h/_3.h)) - m2*(1-(_11.h/_3.h)))/(1-(_6.h/_3.h))
    m3 = m1 - m2 - m4

    # Steam Generator Heat
    Q_in = m1*(_1.h - _9.h)

    # Turbine power output
    W_t = (m1*_1.h) - (m2*_2.h) - (m3*_3.h) - (m4*_4.h)

    # Condenser
    Q_out = m4*(_4.h - _5.h)

    # Pump 1 power input
    W_p1 = m4*(_6.h - _5.h)

    # Pump 2 power input
    W_p2 = m1*(_8.h - _7.h)

    # Net Power
    W_net = (W_t-W_p1-W_p2)
    # Thermal efficiency
    th = W_net/Q_in

    p_ch_list.append(p_ch*10)
    th_list.append(th*100)
    y2_list.append(m2/m1)
    y3_list.append(m3/m1)
    y4_list.append(m4/m1)
    qin_list.append(Q_in/m1)
    qout_list.append(Q_out/m1)
    wnet_list.append(W_net/m1)

plt.plot(p_ch_list,th_list)
plt.xlabel('Higher pressure extracted (bar)')
plt.ylabel('Thermal efficiency (%)')
plt.grid(color='gray', ls = '-.', lw = 0.25)
plt.show()

plt.plot(p_ch_list,y2_list, label=r'$\frac{\dot{m}_2}{\dot{m}_1}$')
plt.plot(p_ch_list,y3_list, label=r'$\frac{\dot{m}_3}{\dot{m}_1}$')
plt.legend(loc="center right")
plt.xlabel('Higher pressure extracted (bar)')
plt.ylabel('Fraction extracted (-)')
plt.grid(color='gray', ls = '-.', lw = 0.25)
plt.show()

fig, axs = plt.subplots(3, 1)
axs[0].plot(p_ch_list, qout_list, label=r'$\dot{q}_{out}$')
axs[0].legend(loc="upper right")
axs[0].grid(color='gray', ls = '-.', lw = 0.25)
axs[1].plot(p_ch_list, wnet_list, 'tab:orange', label=r'$\dot{w}_{net}$')
axs[1].legend(loc="upper right")
axs[1].grid(color='gray', ls = '-.', lw = 0.25)
axs[2].plot(p_ch_list, qin_list, 'tab:green', label=r'$\dot{q}_{in}$')
axs[2].legend(loc="upper right")
axs[2].grid(color='gray', ls = '-.', lw = 0.25)

for ax in axs.flat:
    ax.set(xlabel='Higher pressure extracted (bar)', ylabel='(kJ/kg)')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

plt.show()


# View States Table

def printCycleTable():
    print('\n\n-------------------------------------')
    print("Thermal efficiency:",round(th*100,3),"%")
    print('-------------------------------------')
    print("Net Power:",round(W_net/m1,3),"kW/kg")
    print('-------------------------------------')
    print("Heat added:",round(Q_in/m1,3),"kW/kg")
    print('-------------------------------------')
    print("Heat released:",round(Q_out/m1,3),"kW/kg")
    print('-------------------------------------')
    print("Mass fraction 2:",round(m2/m1,3))
    print('-------------------------------------')
    print("Mass fraction 3:",round(m3/m1,3))
    print('-------------------------------------')
    print("Mass fraction 4:",round(m4/m1,3))
    print('-------------------------------------\n\n')

def export_results(filename='results.csv'):
    state_list = [_1,_2,_3,_4,_5,_6,_7,_8,_9,_10,_11]
    csv_file = open(filename,"w")
    State.print_headers()
    csv_file.write(State.get_csv_header())

    for n, st in enumerate(state_list):
        csv_file.write(st.get_csv_line('State '+ str(n + 1)))

    csv_file.close()






