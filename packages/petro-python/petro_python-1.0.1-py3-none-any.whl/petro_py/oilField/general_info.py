class Oilfield_general_info:
    
# Oil Field insights
    def get_wells(self, df):
        
        wells = df['NPD_WELL_BORE_NAME'].unique()
        
        return(wells) 


    def get_number_of_wells (self, df) :
        print(type(df))
        wells = self.get_wells(df)
        number_of_wells = len(wells)

        return(number_of_wells)


    def get_production_wells(self, df):
        
        producers = df[df["FLOW_KIND"] == "production"]
        prod_wells = producers['NPD_WELL_BORE_NAME'].unique()

        number_of_producers = len(prod_wells)
        
        return(
            {
                "names" : prod_wells,
                "number" : number_of_producers
            }
        )


    def get_injection_wells(self, df):
        
        injectors = df[df["FLOW_KIND"] == "injection"]
        inj_wells = injectors['NPD_WELL_BORE_NAME'].unique()
        
        number_of_injectors = len(inj_wells)
        
        return(
            {
                "names" : inj_wells,
                "number" :  number_of_injectors
            }
        )


    def get_converted_wells(self, df):

        injectors = self.get_injection_wells(df)["names"]
        producers = self.get_production_wells(df)["names"]
        
        list_of_wells = []
        
        for injector in injectors:
            for producer in producers:
                if injector == producer:
                    list_of_wells.append(injector)
                    
        return(list_of_wells)