class B3Companies:
    
    _B3_COMPANIES = {
        'RADL3.SA': 60,
        'BBDC4.SA': 60,
        'CMIG4.SA': 60,
        'BBDC3.SA': 60,
        'JBSS3.SA': 60,
        'EQTL3.SA': 60,
        'BBSE3.SA': 60,
        'CCRO3.SA': 60,
        'BRKM5.SA': 60,
        'USIM5.SA': 60,
        'MULT3.SA': 60,
        'ITSA4.SA': 60,
        'BBAS3.SA': 60,
        'ENBR3.SA': 60,
        'OIBR4.SA': 60,
        'ECOR3.SA': 60,
        'UGPA3.SA': 60,
        'KLBN11.SA': 60,
        'PETR3.SA': 60,
        'SBSP3.SA': 60,
        'LREN3.SA': 60,
        'PETR4.SA': 60
    }
    
    def __init__(self, symbols = _B3_COMPANIES):
        self._symbols = list(symbols.keys())
        self._configs = symbols
    
    @property
    def symbols(self):
        return self._symbols
    
    @symbols.setter
    def symbols(self, new_symbol):
        raise ValueError("It is not possible to change the symbols list, only add to it.")
        return self._symbols
    
    def add_new_company(self, company, update_frequency):

            if isinstance(company, str) and isinstance(update_frequency, int):
                new_dict = {}
                new_dict[company] = update_frequency
                self._symbols.update(new_dict)
            else:
                 raise ValueError("Company must be string and update_frequency int.")

        
        

class UpdateFrequency:
    
    def __init__(self, freq = "60m"):
        self.freq = freq