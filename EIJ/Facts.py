from pyknow import *



class EvaluateFacts(KnowledgeEngine):
    
    def _initial_action(self):
        yield Fact(action='evaluate')
    #def gather(self,who,what,where,when,why):
    #    print("The Facts\nWho: %s\nWhat: %s\nWhen: %s\nWhere: %s\nWhy: %s" % (who,what,when,where,why))   
    #    print(engine.facts)
       


engine = KnowledgeEngine()
engine = EvaluateFacts()
engine.reset()
engine.run()

# print('Here are the current facts',engine.facts)