from Stage_constructor import StageEC
from Transistor_manager import transistor


class Amplifier:
    def __init__(self, RL, RS, AV):
        self.RL = RL
        self.RS = RS
        self.AV = AV
        self.s1 = 0
        self.s2 = 0
        self.s3 = 0
        self.total_parameters = []

    def ec(self, model):
        self.s1 = StageEC(model)
        self.s1.build_stage_RS(self.RL, self.RS, self.AV, 0)
        return self.s1.get_parameters()

    def ec2(self, model1, model2):
        self.AV_divided = pow(self.AV,1/2)
        self.s1 = StageEC(model1)
        self.s2 = StageEC(model2)
        self.s1.build_stage(self.RL, self.AV_divided, 0)
        self.s2.build_stage_RS(int(self.s1.get_parameters()['Ren']), self.RS, self.AV_divided, self.s1.get_parameters()['VCC'])
        print(self.s1.get_parameters())
        print(self.s2.get_parameters())

    def ec3(self, model1, model2, model3):
        self.AV_divided = pow(self.AV,1/3)
        self.s1 = StageEC(model1)
        self.s2 = StageEC(model2)
        self.s3 = StageEC(model3)
        self.s1.build_stage(self.RL, self.AV_divided, 0)
        self.s2.build_stage_RS(int(self.s1.get_parameters()['Ren']), self.RS, self.AV_divided, self.s1.get_parameters()['VCC'])
        self.s3.build_stage_RS(int(self.s2.get_parameters()['Ren']), self.RS, self.AV_divided, self.s1.get_parameters()['VCC'])
        print(self.s1.get_parameters())
        print(self.s2.get_parameters())
        print(self.s3.get_parameters())

A = Amplifier(10000, 50, 2000)
print(A.ec3('2n3904', '2n3904', '2n3904'))








