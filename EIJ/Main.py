import json
import os
#Parameters
workingDir = '.\\'

def getInput(data):
    who=input('Who?')
    what=input('What?')
    where=input('Where?')
    when=input('When?')
    why=input('Why?')
    data['facts'].append({  
        'who': who,
        'what': what,
        'where': where,
        'when': when,
        'why': why
        })
    with open(workingDir+'facts.json', 'w') as outfile:  
        json.dump(data, outfile)

def loadEmotionWordList():
     with open(workingDir+'emotions.json') as json_file:
        data = json.load(json_file)
        emotions = {}
        for i in range(0,len(data['emotions'])):
            emotions[data['emotions'][i]['name']] = data['emotions'][i]['words']
        #print(emotions)
#Main
with open(workingDir+'facts.json') as json_file:  
        #If JSON has data
        if os.stat(workingDir+'facts.json').st_size > 0:
            data = json.load(json_file)
            #InitialFact()
            #for p in data['facts']:
            #    engine.declare(Fact(who=p['who'],what=p['what'],where=p['where'],why=p['why'],when=p['when']))
        else:
            data = {}
            data['facts'] = []
loadEmotionWordList()
i='' 
while i != 'quit':
    i = input('Would you like to enter in another event? (type quit to stop) ')
    if i!= 'quit':
        getInput(data)
