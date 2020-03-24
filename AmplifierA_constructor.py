from Component_manager import Component_manager
from Transistor_manager import transistor
from Values_constructor import Values_constructor

class Amplifier:
    def __init__(self):
        self.Resistors = {}
        self.VT = 0.026
        self.tmp = 0
    def stage_EC_build(self, Parameters):
        self.Transistor = transistor()
        self.Values_constructor = Values_constructor()
        self.HFE = self.Transistor.get_values(Parameters['Model'],"HFE.MAX")
        self.hfe = self.Transistor.get_values(Parameters['Model'],"hfe.MAX")
        self.Re = 0.1*Parameters['RL']
        self.RB = self.Re*0.1*self.hfe
        self.ICQ = Values_constructor.ICQ(Parameters)
        self.hib = self.VT/self.ICQ
        self.Ren = Values_constructor.Ren_EC(self.RB,self.hib*self.hfe,self.hfe,self.Re)
        self.tmp = Values_constructor.AV_EC(Parameters, self.hib)
        self.AV = self.tmp['AV']
        if Parameters['Mode'] == 'R/E':
            self.Re1= self.tmp['Re1']
            self.Re1 = self.tmp['Re2']
        if Parameters['Rs'] != 0:
            self.Ren = Parameters['Rs'] + self.Ren
        return self.ICQ
    def stage_BC_build(self):
        return 'jejej hola'

    def stage_CC_build(self):
        return 'jejej hola'

A1 = Amplifier()
Parameters = {
    'RL': 1000,
    'VCC': 12,
    'Model': '2n3904',
    'Rs': 0,
    'Mode': 'nd'
}
print(A1.stage_EC_build(Parameters))







