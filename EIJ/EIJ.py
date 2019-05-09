from pyknow import *
import json
import os
#Parameters
workingDir = 'C:\\Users\\Jacob Penrod\\Google Drive\\DePaul\\CSC594\\EIJ\\'
data = {}
data['facts'] = []
class GatherFacts(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        with open(workingDir+'facts.json') as json_file:  
            if os.stat(workingDir+'facts.json').st_size > 0:
                data = json.load(json_file)
                InitialFact()
                for p in data['facts']:
                    engine.declare(Fact(who=p['who'],what=p['what'],where=p['where'],why=p['why'],when=p['when']))                
                print(engine.facts)
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
        print("The Facts\nWho: %s\nWhat: %s\nWhen: %s\nWhere: %s\nWhy: %s" % (who,what,when,where,why))   
        data['facts'].append({  
        'who': who,
        'what': what,
        'where': where,
        'when': when,
        'why': why
        })
        print(engine.facts)
        with open(workingDir+'facts.json', 'w') as outfile:  
            json.dump(data, outfile)

engine = KnowledgeEngine()
engine = GatherFacts()
engine.reset()
engine.run()
i=''
while i != 'quit':
    i = input('Would you like to enter in another event? (type quit to stop) ')
    if i!= 'quit':
        engine.reset()
        engine.run()
   # print('Here are the current facts',engine.facts)