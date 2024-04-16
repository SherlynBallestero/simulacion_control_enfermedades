from pyswip import Prolog

class Knowledge:
    def __init__(self, PoB: str = 'bbc.pl', LP: str = 'lp.pl', CK: str = 'ck.pl') -> None:
        self.prolog = Prolog()
        self.patterns_of_beh = PoB
        self.local_plans = LP
        self.cooperation_k = CK
        self.current_file = None # Track the currently consulted file

    # Remove a fact
    def remove_fact(self, fact):
        self.prolog.retract(fact)

    # Add a fact
    def add_fact(self, fact):
        self.prolog.asserta(fact)
        
    def query_behavior(self, query):
        self.prolog.consult(self.patterns_of_beh)
        result = list(self.prolog.query(f'{query}'))
        return result

    def query_local_plans(self, query):
        self.prolog.consult(self.local_plans)
        result = list(self.prolog.query(f'{query}'))
        return result
    
    def query_cooperation_k(self, query):
        self.prolog.consult(self.cooperation_k)
        result = list(self.prolog.query(f'{query}'))
        return result

def main():
    k = Knowledge()
    k.add_fact("healthy(frank)")
    k.add_fact("infected(alice)")
    print(k.query_behavior("behavior(frank, Behavior)"))
    
if __name__ == '__main__':
    main()