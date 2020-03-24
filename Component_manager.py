from Stack_manager import stack

class Component_manager:
    def __init__(self):
        self.Comercial_Resistors = [1, 1.2, 1.5, 1.8, 2.2,
                                    2.7, 3.3, 3.9, 4.7, 5.1,
                                    5.6, 6.8, 8.2, 10]
        self.Comercial_Capacitors = [1, 1.2, 2.2, 3.3,
                                     4.7, 5.6, 6.8, 8.2]

    def __str__(self):
            return 'Esta clase recibe capacitores y resistencias'

    def string_to_float(self, C):
        self.index = 0
        self.Component_stack = stack()
        self.Current_Component = C
        self.dot_amount = 0
        self.multiplier_amount = 0
        self.multiplier = 0
        self.Error_Component_vector = False
        while self.index < len(self.Current_Component) and self.dot_amount < 2 and self.multiplier_amount < 2:
            self.Component = self.Current_Component[self.index]
            if self.Component in "1234567890.":
                if self.Component == '.':
                    self.dot_amount += 1
                self.Component_stack.push(self.Component)
            elif self.Component.lower() in "kmun":
                self.multiplier = self.Component.lower()
                self.multiplier_amount += 1
            else:
                self.Error_Component_vector = True
            self.index += 1
        if (self.dot_amount > 1 or self.multiplier_amount > 1 or self.Error_Component_vector == True):
            self.Component_stack.Empty()
            self.Error_Component_vector = True
            return self.Error_Component_vector
        else:
            if self.multiplier == 'k':
                return float(self.Component_stack.listToString())*1000
            elif self.multiplier == 'm':
                return float(self.Component_stack.listToString())*1000000
            elif self.multiplier == 'u':
                return float(self.Component_stack.listToString())*0.000001
            elif self.multiplier == 'n':
                return float(self.Component_stack.listToString())*0.000000001
            else:
                return float(self.Component_stack.listToString())

    def Aprox(self, C, type):
        if isinstance(C,str):
            C = self.string_to_float(C)
            if C == True:
                return 'Error en ingreso'
        if type.lower() == 'c' or type.lower() == 'r':
            if type.lower() == 'c':
                self.normalization_value = self.normalization(C)
                C = C * pow(10, self.normalization_value)
        else:
            return 'Error en ingreso'
        self.tmp = C
        self.Component_container = stack()
        while self.tmp >= 1:
            self.Component_values = self.heavier_values_Component(self.tmp)
            self.Component_container.push(self.Comercial_comparation(self.Component_values, type)*pow(10,self.get_exp(self.tmp)))
            self.tmp = self.tmp - self.Comercial_comparation(self.Component_values, type)*pow(10,self.get_exp(self.tmp))
        if type.lower() == 'c':
            self.Component_container.normalize(self.normalization_value)
        return self.Component_container.get_stack()

    def normalization(self,C):
        self.exp_normalization = 0
        while(C <= 100):
            C*=10
            self.exp_normalization+=1
        return self.exp_normalization

    def heavier_values_Component(self,C):
        self.Component_tmp = C
        while 10 <= self.Component_tmp:
            self.Component_tmp/=10
        return self.Component_tmp

    def Comercial_comparation(self,C, type):
        if type.lower() == 'r':
            self.vector_component = self.Comercial_Resistors
        elif type.lower() == 'c':
            self.vector_component = self.Comercial_Capacitors
        self.index = 0
        while(C >= self.vector_component[self.index]):
            self.index+=1
        return self.vector_component[self.index - 1]

    def get_exp(self, number):
        self.number = number
        self.times = 0
        while (number>=1):
            number /= 10
            if number >= 1:
             self.times += 1
        return self.times




