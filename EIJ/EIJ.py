from pyknow import *

import queue 
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

    #Comma separated list to parse the input for agents who are present
    #Emotion Words are assigned to the closest agents, even if not present 
    #(Not Present = not listed in who variable)
    #Degrees of separation are implied by position in sentance and assigned thusly
    #For instance, take the following stories
    #t0{
    #who:Bob,Carol
    #date:5/12/2019
    #time: 0700
    #What:Bob went out breakfast with Carol
    #Score: 0 - No emotion words found} 
    #t1{
    #who:Carol,Doctor
    #date:5/12/2019
    #time:1200
    #What:Carol had a Doctor's appointment - use fuzzy lookup to find doctor 
    #Score: 0 - No emotion words found}
    #t2{
    #who:Carol,Doctor,[Mother]
    #date:5/12/2019
    #time:1205
    #What:Carol's Doctor was upset because his mother passes away 
    #Score: [-1 - for doctor (closest)], [-.5 Carol 1 degree of separation and loss for empathy]}
    #t3{
    #who:Carol,Bob,[Doctor],[Mother]
    #date:5/12/2019
    #time:1900
    #What:Bob and Carol have dinner and discuss the Doctor's Mom's Death}
    #Score: [-.25 for Bob],[-.5 for Carol] (only 2 present)
    #Note about the score, We only assign emotions to those involved directly in the story block, 
    #Doctor and Mom will be mentioned but no present notated by brackets to get the degree of separation correct
    #Simplifying assumption: Emotion words will be assigned to the closet agent 
    #and relationships will be determined by sentence order
    @Rule(Fact(action='evaluate'),
          NOT(Fact(Stories=W())))
    def loadStories(self):      
        stories = Data.loadStories()
        for s in sorted(stories,key=lambda x: x.date):
            #engine.declare(Story(who=p['who'],what=p['what'],where=p['where'],why=p['why'],when=p['when']))
            #Each unique date is a set of t
            #order by date, not sure if time is really important
            emoList = Data.loadEmotionWordList()
            notP = []
            pres = []
            for p in s.who.split(','):    
                if p[0] == '[':
                    notP.append(p.replace('[','').replace(']',''))
                else:
                    pres.append(p)
            all = pres + notP
            preScore = []
            #indices = [i for i, x in enumerate(my_list) if x == "whatever"]
            for e in emoList:
                for w in e.words:
                    indices = [i for i, x in enumerate(s.what.split(' ')) if x == w]
                    if len(indices) > 0:
                        print(e.name,indices,s.what)
            for u in all:
                indices = [i for i, x in enumerate(s.what.split(' ')) if x.replace("'s",'') == u]
                if len(indices) > 0:
                    print(u,indices,s.what)
        #ToDo: Add Fuzzy lookup to find the agents in the sentence
        #Bind the emotion score to the agents
        #Do the math
                    
engine = EvaluateStories()
engine.reset()
engine.run()
