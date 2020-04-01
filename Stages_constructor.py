from Stage_constructor import Stage
import Component_manager
from Stack_manager import stack


class Amplifier:
    def __init__(self, RL, RS, AV, fc):
        self.RL = RL
        self.RS = RS
        self.AV = AV
        self.fc = fc
        self.VCC = 0
        self.Components = 0
        self.RL_tmp = 0
        self.stage = 0
        self.Parameters_container = {}
        self.name = ''
        self.models_EC = stack()
        self.models_CC = stack()
        self.tmp = ''

    def Power_amplifier(self, model, PowerUp):
        for self.index in range(len(model)):
            if model[self.index][0] == 'e' and model[self.index][1] == 'c':
                for self.index2 in range(3, len(model[self.index])):
                    self.tmp += model[self.index][self.index2]
                self.models_EC.push(self.tmp)
                self.tmp = ''
            elif model[self.index][0] == 'c' and model[self.index][1] == 'c' and len(self.models_CC.get_stack()) < 2:
                for self.index2 in range(3, len(model[self.index])):
                    self.tmp += model[self.index][self.index2]
                self.models_CC.push(self.tmp)
                self.tmp = ''
            else:
                raise AssertionError('No se puede usar mas de 2 transistores para etapa de corriente')
        self.AV_divided = pow(self.AV, 1 / (len(self.models_EC.get_stack())))
        for self.index in range(len(self.models_EC.get_stack())):
            if self.index == 0:
                self.stage = Stage(self.models_EC.get_stack()[self.index])
                self.stage.build_stage_EC(self.RL, self.AV_divided, self.fc, 0)
                self.name = f'{self.models_EC.get_stack()[self.index]}:{self.index}'
                self.Parameters_container[self.name] = self.stage.get_parameters()
                self.VCC = self.stage.get_parameters()['VCC']
                self.RL_tmp = self.stage.get_parameters()['Ren']
            elif self.index == len(self.models_EC.get_stack()) - 1:
                self.stage = Stage(self.models_EC.get_stack()[self.index])
                self.stage.build_stage_RS_EC(self.RL_tmp, self.RS, self.AV_divided, self.fc, self.VCC)
                self.name = f'{self.models_EC.get_stack()[self.index]}:{self.index}'
                self.Parameters_container[self.name] = self.stage.get_parameters()
            else:
                self.stage = Stage(self.models_EC.get_stack()[self.index])
                self.stage.build_stage_EC(self.RL_tmp, self.AV_divided, self.fc, self.VCC)
                self.name = f'{self.models_EC.get_stack()[self.index]}:{self.index}'
                self.Parameters_container[self.name] = self.stage.get_parameters()
                self.RL_tmp = self.stage.get_parameters()['Ren']

        def cc_power_up(RL):
            if len(self.models_CC.get_stack()) > 1:
                darlington = True
                stage1 = Stage(self.models_CC.get_stack()[0])
                stage2 = Stage(self.models_CC.get_stack()[1])
                hfe = stage1.Values_model_transistor['hfe.MAX']*stage2.Values_model_transistor['hfe.MAX']*0.8
                if stage1.Values_model_transistor['IC.Stable'] > stage2.Values_model_transistor['IC.Stable']:
                    ic_stable = stage1.Values_model_transistor['IC.Stable']
                    self.stage = stage1
                else:
                    ic_stable = stage2.Values_model_transistor['IC.Stable']
                    self.stage = stage2
            else:
                darlington = False
                self.stage = Stage(self.models_CC.get_stack()[0])
                hfe = self.stage.Values_model_transistor['hfe.MAX']*self.stage.Values_model_transistor['hfe.MAX']*0.8
                ic_stable = self.stage.Values_model_transistor['IC.Stable']
            if self.RL < (0.026 / ic_stable)*hfe*0.7 + hfe*0.7*0.5*RL:
                if darlington:
                    self.stage.buld_stage_CC(RL, self.RL, self.VCC, self.fc, hfe, darlington)
                    name = f'{self.models_CC.get_stack()[0]}:{self.models_CC.get_stack()[1]}:Darlington_Current_stage'
                    self.Parameters_container[name] = self.stage.get_parameters()
                else:
                    self.stage.buld_stage_CC(RL, self.RL, self.VCC, self.fc, hfe, darlington)
                    name = f'{self.models_CC.get_stack()[0]}:Current_stage'
                    self.Parameters_container[name] = self.stage.get_parameters()
                return self.Parameters_container
            else:
                raise AssertionError(
                    f'el {self.models_CC.get_stack()} no tiene hfe suficiente para la RL = {self.RL} con un diseño estable, se sugiere usar darlington')
        if PowerUp:
            return cc_power_up
        else:
            return self.Parameters_container

