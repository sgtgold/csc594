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
import json
import os
#Parameters
#
workingDir = '.\\'
class Story:
    def __init__(self,who,date,time,what):
        self.who = who
        self.date = date
        self.time = time
        self.what = what
class Emotion:
    def __init__(self,name,score,words):
        self.name = name
        self.score = score
        self.words = words




def getInput(data):
    ts = []
    
    ts.append(Story(who='Bob,Carol'
    ,time='0700'
    ,date='2019/05/12'
    ,what='Bob went out breakfast with Carol'))
    
    ts.append(Story(
         who='Carol,Doctor'
         ,date='5/12/2019'
         ,time='1200'
         ,what="Carol had a Doctor's appointment - use fuzzy lookup to find doctor" ))
    
    ts.append(Story(
         who='Carol,Doctor,[Mother]'
         ,date='5/12/2019'
         ,time='1205'
         ,what="Carol had a Doctor's appointment"))
    
    ts.append(Story(
         who='Carol,Bob,[Doctor],[Mother]'
         ,date='5/12/2019'
         ,time='1900'
         ,what="Bob and Carol have dinner and discuss the Doctor's Mother's Death" ))
    
    for t in ts:
        data['stories'].append({
            'who':t.who.lower(),
            'what':t.what.lower(),
            'time':t.time,
            'date':t.date
        })

    with open(workingDir+'stories.json', 'w') as outfile:  
        json.dump(data, outfile)

def loadEmotionWordList():
     with open(workingDir+'emotions.json') as json_file:
        data = json.load(json_file)
        emos = []
        for i in range(0,len(data['emotions'])):
            emos.append(Emotion(name = data['emotions'][i]['name'],
                                score = data['emotions'][i]['score'],
                                words = [x.lower() for x in data['emotions'][i]['words']]))
        return emos
#Main
def loadFacts():
    data = {}
    data['stories'] = [] 
    with open(workingDir+'stories.json') as json_file:  
        #If JSON has data
        if os.stat(workingDir+'stories.json').st_size > 0:
            data = json.load(json_file)
            data['stories'] = data['stories']
    return data

loadingMode = 0
if(loadingMode == 1):
    data = loadFacts()
    if i!= 'quit':
        getInput(data)
