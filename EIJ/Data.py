import json
import os
#Parameters
workingDir = '.\\'

def getInput(data):
    who='me'#input('Who?')
    what=input('What?')
    where='here'#input('Where?')
    when='now'#input('When?')
    why='because'#input('Why?')
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
        emos = {}
        for i in range(0,len(data['emotions'])):
            emos[data['emotions'][i]['name']] = data['emotions'][i]['words']
        return emos
#Main
def loadFacts():
     data = {}
     data['facts'] = []
     with open(workingDir+'facts.json') as json_file:  
        #If JSON has data
        if os.stat(workingDir+'facts.json').st_size > 0:
            data = json.load(json_file)
            data['facts'] = data['facts']
     return data['facts']
loadingMode = 1
if(loadingMode == 0):
    i='' 
    while i != 'quit':
        data = loadFacts()
        i = input('Would you like to enter in another event? (type quit to stop) ')
        if i!= 'quit':
            getInput(data)
