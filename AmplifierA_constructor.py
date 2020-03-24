from Component_manager import Component_manager
from Transistor_manager import transistor


class AmplifierEC:
    def __init__(self, model):
        self.VCC_nominal = [3, 5, 9, 12, 18, 24]
        self.VT = 0.026
        self.index = 0
        self.T = transistor()
        self.Values_model_transistor = self.T.get_values(model)
        self.parameters = {}
    def stage_first(self, RL, RS, AV):
        self.parameters['RS'] = RS
        return self.stage(RL,AV)
    def stage(self, RL, AV):
        self.parameters['RL'] = RL
        self.parameters['hfe_MID'] = self.Values_model_transistor['hfe.MAX']*0.5
        self.parameters['ICQ'] = self.Values_model_transistor['IC.Stable']
        self.parameters['Hib'] = self.VT/self.parameters['ICQ']
        self.parameters['Re1'] = self.parameters['RL']*0.5/AV - self.parameters['Hib']
        self.parameters['VCC'] = self.vcc_selection()
        self.parameters['Re2'] = self.parameters['VCC']/self.parameters['ICQ'] - self.parameters['RL']*1.5
        self.parameters['Re'] = self.parameters['Re2'] + self.parameters['Re1']
        self.parameters['RB'] = self.parameters['Re']*0.1*self.parameters['hfe_MID']
        self.parameters['IB'] = self.parameters['ICQ']/self.parameters['hfe_MID']
        self.parameters['VBB'] = self.parameters['IB']*(self.parameters['RB'] + (self.parameters['hfe_MID'] + 1)*self.parameters['Re']) + 0.7
        self.parameters['R1'] = self.parameters['VCC']*self.parameters['RB']/self.parameters['VBB']
        self.parameters['R2'] = self.parameters['VCC']*self.parameters['RB']/(self.parameters['VCC']-self.parameters['VBB'])
        self.parameters['Ren'] = self.parallel(self.parameters['RB'],self.parameters['hfe_MID']*(self.parameters['Hib']+self.parameters['Re']))
        self.parameters['Stable_status'] = self.parameters['Re1'] >= self.parameters['Hib']*10
        return self.parameters

    def vcc_selection(self):
        self.VCC_Minimun = self.parameters['ICQ'] * (1.5 * self.parameters['RL'] + self.parameters['Re1'])
        for self.index in range(len(self.VCC_nominal)):
            if self.VCC_Minimun < self.VCC_nominal[self.index]:
                return self.VCC_nominal[self.index]
    def parallel(self, R1, R2):
        return R1*R2/(R1+R2)

A = AmplifierEC('2n3904')
print(A.stage(2000, 10))