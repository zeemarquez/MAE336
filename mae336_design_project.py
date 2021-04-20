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

        return line
    
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

        return line

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

efficiency = 0.8
m1 = 1.5 * (10**4) #kg/s

_1 = State(T=(480+273),P=12)

_2s = State(P=2, s= _1.s)
_3s = State(P=0.3, s= _1.s)
_4s = State(P=0.006, s= _1.s)

h2 = _1.h + efficiency*(_2s.h - _1.h)
h3 = _1.h + efficiency*(_3s.h - _1.h)
h4 = _1.h + efficiency*(_4s.h - _1.h)

_2 = State(h=h2, P=2)
_3 = State(h=h3, P=0.3)
_4 = State(h=h4, P=0.006)

_5 = State(P=0.006, x=0)
_6s = State(P=0.3,s=_5.s)

h6 = _5.h + ((_6s.h - _5.h)/efficiency)

_6 = State(h=h6, P=0.3)
_7 = State(x=0,P=0.1)

_8s = State(P=12,s=_7.s)     #P8 = P9 = 12MPa

h8 = _7.h + ((_8s.h - _7.h)/efficiency)

_8 = State(h=h8, P=12)
_9 = State(T=(210+273), P=12)
_10 = State(P=2, x=0)       # h10 = h11
_11 = State(P=0.3, h=_10.h)

m2 = m1 * (abs(_9.h-_8.h)/abs(_2.h-_10.h))
m4 = (m1*(1- (_7.h/_3.h)) - m2*(1-(_11.h/_3.h)))/(1-(_6.h/_3.h))
m3 = m1 - m2 - m4

# Steam Generator Heat
Q_sg = m1*(_1.h - _9.h)

# Turbine power output
W_t = (m1*_1.h) - (m2*_2.h) - (m3*_3.h) - (m4*_4.h)

# Condenser
Q_cond = m4*(_4.h - _5.h)

# Pump 1 power input
W_p1 = m4*(_6.h - _5.h)

# Pump 2 power input
W_p2 = m1*(_8.h - _7.h)


state_list = [_1,_2,_3,_4,_5,_6,_7,_8,_9,_10,_11]

State.print_headers()

for n, st in enumerate(state_list):
    st.print_state('State '+ str(n + 1))











