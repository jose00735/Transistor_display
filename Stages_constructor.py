from Stage_constructor import StageEC
from Component_manager import Component_manager

class Amplifier:
    def __init__(self, RL, RS, AV):
        self.RL = RL
        self.RS = RS
        self.AV = AV
        self.s1 = 0
        self.s2 = 0
        self.s3 = 0
        self.total_parameters = []

    def ec1(self, model):
        self.s1 = StageEC(model)
        self.s1.build_stage_RS(self.RL, self.RS, self.AV, 0)
        return self.s1.get_parameters()

    def ec2(self, model):
        self.AV_divided = pow(self.AV,1/2)
        self.s1 = StageEC(model[0])
        self.s2 = StageEC(model[1])
        self.s1.build_stage(self.RL, self.AV_divided, 0)
        self.s2.build_stage_RS(int(self.s1.get_parameters()['Ren']), self.RS, self.AV_divided, self.s1.get_parameters()['VCC'])
        print(self.s1.get_parameters())
        print(self.s2.get_parameters())


A = Amplifier(5000,50,50)
model=['2n3904','2n3904']
print(A.ec2(model))









