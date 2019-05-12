from pyknow import *
import Data

class Emotion(Fact):
    pass

class Story(Fact):
    pass
#Test
class EvaluateStories(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        #print(engine.facts)
        yield Fact(action='evaluate')

    #@Rule(Fact(action='evaluate'),
    #      NOT(Fact(Emotion=W())))
    #def loadWords(self):      
        
    
    @Rule(Fact(action='evaluate'),
          NOT(Fact(Stories=W())))
    def loadStories(self):      
        rawFacts = Data.loadFacts()
        for p in rawFacts['stories']:
            #engine.declare(Story(who=p['who'],what=p['what'],where=p['where'],why=p['why'],when=p['when']))
            emoList = Data.loadEmotionWordList()        
            for e in emoList.keys():
                for w in emoList[e]:
                    if w in p['what'].split(' '):
                        print('Emotion='+e)
                    #engine.declare(Emotion(name=e,words=w))            
                    
engine = EvaluateStories()
engine.reset()
engine.run()
