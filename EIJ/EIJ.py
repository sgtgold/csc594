import queue 
import Data
import json
import numpy as np
from numpy.linalg import inv
def interpretMagnitude(magnitude):
    modifier = ''
    if magnitude < .49:
        modifier = 'mildly'
    if magnitude >= .5 and magnitude < 1.0 :
        modifier = ''
    if magnitude >= 1:
        modifier = 'very'
    return modifier

def outputPrimeEmotion(agent,score,emotionCategory,rawStory,startIndex,endIndex,isPresent,magnitude):
    modifier = interpretMagnitude(float(magnitude))    
    print('\nThe Story is "' + rawStory + '"')
    pText = ''
    if(isPresent == 0):
        pText = ' and it was being discussed, even though they were not present'
    if score <= 0:
        print(("{} had a {} negative emotion, they were {}"+pText).format(agent,modifier,emotionCategory))
    else:    
        print(("{} had a {} positive emotion, they were {}"+pText).format(agent,modifier,emotionCategory))
    storyArray = rawStory.split(' ')
    sep = ' '
    print("I believe this because of this story '{}' in this Journal".format(sep.join(storyArray[startIndex:endIndex+2]))) 

def outputEmpathy(primeAgent,friend,score,emotionCategory,magnitude):
    modifier = interpretMagnitude(float(magnitude))
    if score <= 0.0:
        print("{} heard that {} was {}, they were {} sad because they were friends ".format(friend,primeAgent,emotionCategory,modifier))
    else:
         print("{} heard that {} was {}, they were {} glad because they were friends ".format(friend,primeAgent,emotionCategory,modifier))
   
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
        for p in s.who.split(','):    
            #People in brackets are not present but still need to be there for correct assignment
            if str.strip(p)[0] == '[':
                notP.append(p.replace('[','').replace(']',''))
            else:
                pres.append(p)
        all = pres + notP
        preScore = []
        for u in all:
            #Find instances of all users
            #ToDo: Add Fuzzy Lookups
            indicies = [i for i, x in enumerate(s.what.split(' ')) if x.replace("'s",'') == u]
            if len(indicies) > 0:
                for i in indicies:
                    q.append((i,u))
            #Find instances of all emotional words
            #ToDo: Add Fuzzy Lookups
        for e in emoList:
            for w in e.words:
                indices = [i for i, x in enumerate(s.what.split(' ')) if x == w]
                if len(indices) > 0:
                    q.append((i,e.score,e.name))         
        #Sort the list of words and users by index
        sortedQ = sorted(q,key=lambda x: x[0],reverse=True)
        #dos = degrees of separation
        dos = -1
        emotionScore = 0
        emotionWord = ''
        emotionCat = ''
        primeAgent = ''
        #Loop through the storted list and assign scores
        for sq in sortedQ:
            #Initialize to zero
            #This means it is an agent
            e = 1 / (2**dos)
            if type(sq[1]) == type(1):
                emotionScore = sq[1]
                emotionIndex = sq[0]
                emotionCat = sq[2]
            else:
                dos = dos + 1
                present = 1
                if(sq[1] in notP):
                    present = 0
                    allScores.setdefault(sq[1], []).append(0)
                if abs(e * emotionScore) == abs(1):
                        agentIndex = sq[0]
                        primeAgent = sq[1]
                        primeScores.append((primeAgent,emotionScore,emotionCat,s.what,agentIndex,emotionIndex,present,storyId))
                if(present == 1):
                    allScores.setdefault(sq[1], []).append(emotionScore * e)
                    friend = sq[1]
                    if primeAgent != friend:
                        empathyScores.append((primeAgent,friend,(emotionScore * e),emotionCat,storyId))
    #print(allScores)                
    #Find Max Len
    #print(directScores)
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
    #print(agentDir)
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
    for s in range(0,storyId + 1):
        for p in primeScores:      
            for i in range(0,C_x):  
            #Perform our LHM
                if (p[0] == C[i][0] and p[-1] == s):
                    #(agent,score,emotionCategory,rawStory,startIndex,endIndex,isPresent,magnitude)
                    outputPrimeEmotion(p[0],p[1],p[2],p[3],p[4],p[5],p[6],C[i][2])
        for ep in empathyScores:
            for i in range(0,C_x): 
        #(primeAgent,friend,score,emotionCategory,magnitude):
                if (ep[1] == C[i][0] and ep[1] != p[0] and ep[2] != 0.0 and ep[-1] == s):        
                        outputEmpathy(ep[0],ep[1],ep[2],ep[3],C[i][2])
            
            #rows.append(np.array(C[i][2]))
        #print(rows)






#Extra Code
    #print(C)
    #one_col = np.ones((B_x,1))
    #C = np.hstack((B,one_col,bMag))
    #D = C * C.transpose()
    
    #subM = []
    #(C_x,C_y) = C.shape
    #Element wise Row Subtraction all but the last row
    #for i in range(0,C_x - 1):
     #   row = np.array(C[i,:])[0]
      #  row_1 = np.array(C[i+1,:])[0]
      #  subArray = []
      #  for j in range(0,len(row)):
      #      subArray.append(row[j] - row_1[j])
        # Check that all non-i positions (except for last column are 0
      #  subM.append(subArray)
        
        #subM_1 = np.divide(subM[0],subM[0][0])    
        
        #Handle the top row minus the last row
    #row = np.array(C[0,:])[0]
    #row_1 = np.array(C[(C_x-1),:])[0]
    #subArray = []
    #for j in range(0,len(row)):
     #   subArray.append(row[j] -row_1[j])
    #subM.append(subArray)

    #for i in range(0,len(C)):
    #    d_array.append(np.array(C[i])[0])
    #D = np.asmatrix(d_array)
    return json.dumps(allScores)
j = evalStories()
#print(j)
    #print(u,indices,s.what)
    #ToDo: Add Fuzzy lookup to find the agents in the sentence
    #Bind the emotion score to the agents
    #Do the math using numpy
                    