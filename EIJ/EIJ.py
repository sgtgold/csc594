import queue 
import Data
import json
import numpy as np
from numpy.linalg import inv
def interpretMagnitude(magnitude):
    modifier = ''
    if abs(magnitude) < .49:
        modifier = 'mildly'
    if abs(magnitude) >= .5 and abs(magnitude) < 1.0 :
        modifier = ''
    if abs(magnitude) >= 1:
        modifier = 'very'
    return modifier
def outputPrimeEmotion(agent,score,emotionCategory,rawStory,startIndex,endIndex,isPresent,magnitude):
    if(isPresent == 1):
        modifier = interpretMagnitude(float(magnitude))
    else:
        modifier = ''
    rv = ''
    rv += '\nThe Story is ' + rawStory
    pText = ''
    if(isPresent == 0):
        pText = ' and it was being discussed, even though they were not present'
    if score <= 0:
        rv += ("\n{} had a {} negative emotion, they were {}"+pText).format(agent,modifier,emotionCategory)
    else:    
        rv += ("\n{} had a {} positive emotion, they were {}"+pText).format(agent,modifier,emotionCategory)
    storyArray = rawStory.split(' ')
    sep = ' '
    rv += "\nI believe this because of this story '{}' in this Journal".format(sep.join(storyArray[startIndex:endIndex]))
    return rv
def outputEmpathy(primeAgent,friend,score,emotionCategory,magnitude):
    modifier = interpretMagnitude(float(magnitude))
    if score <= 0.0:
        return "\n{} heard that {} was {}, they were {} sad because they were friends ".format(friend,primeAgent,emotionCategory,modifier)
    else:
        return "\n{} heard that {} was {}, they were {} glad because they were friends ".format(friend,primeAgent,emotionCategory,modifier)
   
#Comma separated list to parse the input for agents who are present
#Emotion Words are assigned to the closest agents, even if not present 
#(Not Present = not listed in who variable)
#Degrees of separation are implied by position in sentance relative to the prime emotion haver
def evalStories(passedStory = ''):      
    stories = []
    #Load pre-written stories
    if len(passedStory) == 0:
        stories = Data.loadStories()
    #Load story that is passed in via the Socket
    else:
        data = json.loads(passedStory.decode("utf-8"))
        s = data
        stories.append(Data.Story(who=s['who'],date=s['date'],time=s['time'],what=s['what']))
    allScores = {}
    storyId = -1
    primeScores = []
    empathyScores = []
    for s in sorted(stories,key=lambda x: x.date):
        storyId += 1
        q = []
        #Each unique date is a set of t
        #order by date, not sure if time is really important
        emoList = Data.loadEmotionWordList()
        notP = []
        pres = []
        if ',' in s.who:
            for p in s.who.split(','):    
                #People in brackets are not present but still need to be there for correct assignment
                if str.strip(p)[0] == '[':
                    notP.append(p.replace('[','').replace(']',''))
                else:
                    pres.append(p)
        #Only one agent is present
        else:
            pres.append(s.who)
        all = pres + notP
        preScore = []
        for u in all:
            #Find instances of all users
            #Using Fuzzy Lookups with a high enough threshold to get around puncation and small spelling mistakes
            indicies = [i for i, x in enumerate(s.what.split(' ')) if Data.levenshtein_ratio_and_distance(x.replace("'s",''),u) >= 0.95]
            if len(indicies) > 0:
                for i in indicies:
                    if (i,u) not in q:
                        q.append((i,u))
            #Find instances of all emotional words
        for e in emoList:
            for w in e.words:
                #Using Fuzzy Lookups with a high enough threshold to get around puncation and small spelling mistakes
                indices = [i for i, y in enumerate(s.what.split(' ')) if Data.levenshtein_ratio_and_distance(y,w) >= 0.95]
                if len(indices) > 0:
                    q.append((indices[0],e.score,e.name))         
        #Sort the list of words and users by index
        sortedQ = sorted(q,key=lambda x: x[0],reverse=True)
        #dos = degrees of separation
        dos = -1
        emotionScore = 0
        emotionCat = ''
        primeAgent = ''
        #Loop through the storted list and assign scores
        for sq in sortedQ:
            #Initialize to zero
            #This means it is an agent
            if type(sq[1]) == type(1):
                print(sq)
                emotionScore = sq[1]
                emotionIndex = sq[0]
                emotionCat = sq[2]
            else:
                dos = dos + 1
                present = 1
                e = 1 / (2**dos)
                if(sq[1] in notP):
                    present = 0
                    allScores.setdefault(sq[1], []).append(0)
                #If there are no degrees of separation then they are the agent having the emotion
                if dos == 0 and emotionCat != '':
                        agentIndex = sq[0]
                        primeAgent = sq[1]
                        #print(emotionScore)
                        primeScores.append((primeAgent,(emotionScore * e),emotionCat,s.what,agentIndex,emotionIndex+1,present,storyId))
                #Empathizers are agents preset, and hearing about another agent's emotion
                if(present == 1):
                    allScores.setdefault(sq[1], []).append(emotionScore * e)
                    friend = sq[1]
                    if primeAgent != friend:
                        empathyScores.append((primeAgent,friend,(emotionScore * e),emotionCat,storyId))
    #Find Max Len
    maxKey=max(allScores, key=lambda k: len(allScores[k]))
    maxN = len(allScores[maxKey])
    agents = []
    for key,val in allScores.items():
        #print("{} = {}".format(key, val))
        while len(val) < maxN:
            allScores[key].append(0.0)
        agents.append(key) 
    arrays = []
    for key,val in allScores.items():
        arrays.append(np.array(allScores[key]))
    A = np.asmatrix(arrays)
    agentDir = []  
    for key,val in allScores.items():
        agentDir.append([key,np.sum(val)])
    B = (A * A.transpose())
    
    (B_x,B_y) = B.shape
    #Array of Magnitudes
    aMag = []
    #This loop does the equation below (example with row size of 3)
    #magnitude = np.sqrt(row[0]**2 +  row[1]**2 + row[2]**2)
    #For each Row
    for i in range(0,B_x):
        #Reset the magnitude
        m = 0
        #Set the Row
        row = np.array(B[i,:])[0]
        for j in range(0,B_y):
            #Get the individual scores to be summed and squared rooted
            m += row[j]**2
        aMag.append(np.sqrt(m))
    mags = np.array(aMag).reshape(B_x,1)
    C = np.hstack((agentDir,mags))
    (C_x,C_y) = C.shape
    rows = []
    #Now we need to map the emotion scores with the magnitude
    #StoryId is used as part of the join in case an agent is mentioned
    #more than once
    output = ''
    for s in range(0,storyId + 1):
        totalPerStory = 0
        for p in primeScores:      
            for i in range(0,C_x):  
            #Perform our LHM
                if (p[0] == C[i][0] and p[-1] == s):
                    #(agent,score,emotionCategory,rawStory,startIndex,endIndex,isPresent,magnitude)
                    print(C)
                    output += outputPrimeEmotion(p[0],p[1],p[2],p[3],p[4],p[5],p[6],float(C[i][2]) * 2)
                    totalPerStory += 1
        for ep in empathyScores:
            for i in range(0,C_x): 
                if (ep[1] == C[i][0] and ep[1] != p[0] and ep[2] != 0.0 and ep[-1] == s):        
                        #(primeAgent,friend,score,emotionCategory,magnitude):   
                        output += outputEmpathy(ep[0],ep[1],ep[2],ep[3],C[i][2])
                        totalPerStory += 1
            #rows.append(np.array(C[i][2]))
        #print(rows)
        if(totalPerStory == 0):
            output = '\nNo emotions found in the story'
    #print(output)
    return output
print('Hello and welcome to the EIJ Demo')
print('Pass me a story to get started')
#Debug Code
#def dict_from_class(cls):
#    return dict(
#        (key, value)
#        for (key, value) in cls.__dict__.items()
#        )
#d = {}
#d[0] = Data.Story(
#         who = "jake",
#          what =  "jake was elated because it was his birthday",
#          time =  "2000",
#          date =  "1/1/1999")
#
#
#print(evalStories(bytes(json.dumps(dict_from_class(d[0])), "utf-8")))