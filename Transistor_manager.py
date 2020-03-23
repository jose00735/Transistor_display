import pandas as pd

class transistor:
    def __init__(self):
        self.count = 0
        self.tdb = pd.read_csv('Transistor_db.csv', sep=';')
        self.specs_dictionary = {}

    def get_values(self, model, spec):
        for self.count in range(len(self.tdb.columns)):
            if self.count >= 2:
                 self.specs_dictionary[self.tdb.columns[self.count]] = float(self.tdb[self.tdb.columns[self.count]][self.tdb['Modelo'] == model])
            else:
                self.specs_dictionary[self.tdb.columns[self.count]] = self.tdb[self.tdb.columns[self.count]][self.tdb['Modelo'] == model]
        return self.specs_dictionary[spec]

    def show_avaliable_transistors_of(self, Type):
        return self.tdb[['Modelo', 'Darlington']][self.tdb['Type'] == Type]

