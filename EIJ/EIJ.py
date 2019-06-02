import queue 
import Data
import json
import numpy as np
from numpy.linalg import inv
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
    for s in sorted(stories,key=lambda x: x.date):
        q = []
        #Each unique date is a set of t
        #order by date, not sure if time is really important
        emoList = Data.loadEmotionWordList()
        notP = []
        pres = []
        for p in s.who.split(','):    
            #People in brackets are not present but still need to be there for correct assignment
            if p[0] == '[':
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
                    q.append((i,e.score))         
        #Sort the list of words and users by index
        sortedQ = sorted(q,key=lambda x: x[0],reverse=True)
        #dos = degrees of separation
        dos = 0
        emotionScore = 0
        #Loop through the storted list and assign scores
        for sq in sortedQ:
            #Initialize to zero
            #This means it is an agent
            e = 1 / (2**dos)
            if type(sq[1]) == type(1):
                emotionScore = sq[1]
            else:
                if(sq[1] not in notP):
                    allScores.setdefault(sq[1], []).append(emotionScore * e)
                    dos = dos + 1
    #Find Max Len
    maxKey=max(allScores, key=lambda k: len(allScores[k]))
    maxN = len(allScores[maxKey])
    for key,val in allScores.items():
        print("{} = {}".format(key, val))
        while len(val) < maxN:
            allScores[key].append(0.0)
    arrays = []
    for key,val in allScores.items():
        arrays.append(np.array(allScores[key]))
        
    A = np.asmatrix(arrays)
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
        #print(aMag)
    bMag = np.array(aMag).reshape(B_x,1)
    one_col = np.ones((B_x,1))
    C = np.hstack((B,one_col,bMag))
    D = C * C.transpose()
    
    subM = []
    (C_x,C_y) = C.shape
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
print(j)
    #print(u,indices,s.what)
    #ToDo: Add Fuzzy lookup to find the agents in the sentence
    #Bind the emotion score to the agents
    #Do the math using numpy
                    