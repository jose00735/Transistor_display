from Stage_constructor import StageEC
from Component_manager import Component_manager


class Amplifier:
    def __init__(self, RL, RS, AV):
        self.RL = RL
        self.RS = RS
        self.AV = AV
        self.VCC = 0
        self.RL_tmp = 0
        self.s = 0
        self.Parameters_container = {}
        self.name = ''
    def ec(self, model):
        self.AV_divided = pow(self.AV, 1/(len(model)))
        for self.index in range(len(model)):
            if self.index == 0:
                self.s = StageEC(model[self.index])
                self.s.build_stage(self.RL, self.AV_divided, 0)
                self.name = f'{model[self.index]}:{self.index}'
                self.Parameters_container[self.name] = self.s.get_parameters()
                self.VCC = self.s.get_parameters()['VCC']
                self.RL_tmp = self.s.get_parameters()['Ren']
            elif self.index == len(model) - 1:
                self.s = StageEC(model[self.index])
                self.s.build_stage_RS(self.RL, self.RS,self.AV_divided, self.VCC)
                self.name = f'{model[self.index]}:{self.index}'
                self.Parameters_container[self.name] = self.s.get_parameters()
            else:
                self.s = StageEC(model[self.index])
                self.s.build_stage(self.RL_tmp, self.AV_divided, self.VCC)
                self.name = f'{model[self.index]}:{self.index}'
                self.Parameters_container[self.name] = self.s.get_parameters()
                self.RL_tmp = self.s.get_parameters()['Ren']
        return self.Parameters_container

A = Amplifier(5000,50,10000)
model=['bc547b','2n3904','bc547b','2n3904','bc547b','2n3904','bc547b','2n3904','bc547b','2n3904']
Amplifier_parameters = A.ec(model)

for index in Amplifier_parameters:
    print(Amplifier_parameters[index])








