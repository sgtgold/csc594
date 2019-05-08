from pyknow import *
 
class GatherFacts(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action='gather')
    
    @Rule(Fact(action='gather'),
         NOT(Fact(who=W())))
    def ask_who(self):
        self.declare(Fact(who=input("Who?")))
    
    @Rule(Fact(action='gather'),
         NOT(Fact(where=W())))
    def ask_where(self):
        self.declare(Fact(where=input("Where?")))
    
    @Rule(Fact(action='gather'),
         NOT(Fact(when=W())))
    def ask_when(self):
        self.declare(Fact(when=input("When?")))
    
    @Rule(Fact(action='gather'),
         NOT(Fact(what=W())))
    def ask_what(self):
        self.declare(Fact(what=input("What?")))
    
    @Rule(Fact(action='gather'),
         NOT(Fact(why=W())))
    def ask_why(self):
        self.declare(Fact(why=input("Why?")))

    @Rule(Fact(action='gather'),
        Fact(who=MATCH.who),
        Fact(what=MATCH.what),
        Fact(where=MATCH.where),
        Fact(when=MATCH.when),
        Fact(why=MATCH.why))
    def gather(self,who,what,where,when,why):
        print("Hi %s! How is the weather in %s?" % (who, where))
engine = GatherFacts()
engine.reset()  # Prepare the engine for the execution.
engine.run()