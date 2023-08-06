from .general_info import Oilfield_general_info
import pandas as pd

class OilField(Oilfield_general_info):
    
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.wells = super().get_wells(self.df)
        self.number_of_wells = super().get_number_of_wells(self.df)
        
        self.production_wells = super().get_production_wells(self.df)["names"]
        self.n_production_wells = super().get_production_wells(self.df)["number"]
        
        self.injection_wells = super().get_injection_wells(self.df)["names"]
        self.n_injection_wells = super().get_injection_wells(self.df)["number"]
        
        self.converted_wells = super().get_converted_wells(self.df)
    

#     // Methods
    def quick_view(self):
        shape = self.df.shape

        print(
            "number_of_wells : {}".format(super().get_number_of_wells(self.df)),
            "number_of_columns : {}".format(shape[1]), 
            "number_of_records: {}".format(shape[0]), 
        )


    def well_history():
        pass
    
#     +249 99 676 3332