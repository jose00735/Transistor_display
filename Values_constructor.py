class Values_constructor:
    def __init__(self):
        self.tmp = {}

    def Ren_EC(self, RB, Hie, Beta, RE):
             return (RB*(Hie + (1+Beta)*RE))/(RB + Hie + (1+Beta)*RE)

    def Ren_BC(self, RB, Hie, Beta, RE):
        return (RE * (Hie + RB)) / (Hie + RB + Beta * RE)

    def Ren_CC(self, RB, Hie, Beta, RE):
        return (RB*(Hie + Beta*RE*0.5))/(RB + Hie + Beta*RE*0.5)

    def ICQ(self, Parameters):
        if Parameters['Mode'] == 'nd':
            return Parameters['VCC']/(Parameters['RL']*(3/2)+0.2*Parameters['RL'])
        elif Parameters['Mode'] == 'd':
             return Parameters['VCC']/(Parameters['RL']*(3/2))
        elif Parameters['Mode'] == 'R/E':
             return Parameters['VCC'] / (Parameters['RL'] * (3 / 2) + 0.11*Parameters['RL'])
        else:
             return "Error"

    def AV(self, Parameters, hib):
        if Parameters['Mode'] == 'nd':
            self.tmp['AV'] = Parameters['RL']*0.5/(Parameters['RL']*0.1+hib)
            return self.tmp
        elif Parameters['Mode'] == 'd':
            self.tmp['AV'] = Parameters['RL']*0.5/hib
            return self.tmp
        elif Parameters['Mode'] == 'R/E':
            self.tmp['Re1'] = hib*10
            self.tmp['Re2'] = Parameters['RL']*0.1 - self.tmp['Re1']
            self.tmp['AV'] = Parameters['VCC'] / (Parameters['RL'] * (3 / 2) + 0.11 * Parameters['RL'])
            return self.tmp
        else:
            return "Error"

