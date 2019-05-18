import json
import os
import numpy as np
#Pulled from https://www.datacamp.com/community/tutorials/fuzzy-string-python
def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return "The strings are {} edits away".format(distance[row][col])
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
class Agent:
    def __init__(self,name,friendsList,emotionScore):
        self.name = name
        self.friendsList = friendsList
        self.emotionScore = emotionScore
def getInput(data):
    ts = []
    data = {}
    data['stories'] = []     
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
         ,what="Bob and Carol have dinner and discuss the Doctor's Mother's Death. Bob was sad" ))
    
    for t in ts:
        data['stories'].append({
            'who':t.who.lower(),
            'what':t.what.lower(),
            'time':t.time,
            'date':t.date
        })

    with open(workingDir+'stories.json', 'w') as outfile:  
        json.dump(data, outfile)

#This file reads json emotions file and loads it into a list of story objects
def loadEmotionWordList():
     with open(workingDir+'emotions.json') as json_file:
        data = json.load(json_file)
        emos = []
        for i in range(0,len(data['emotions'])):
            emos.append(Emotion(name = data['emotions'][i]['name'],
                                score = data['emotions'][i]['score'],
                                words = [x.lower() for x in data['emotions'][i]['words']]))
        return emos

#This file reads json stories file and loads it into a list of story objects
def loadStories():
    #Define a new list
    stories = []
    with open(workingDir+'stories.json') as json_file:  
        #If JSON has data
        if os.stat(workingDir+'stories.json').st_size > 0:
            data = json.load(json_file)
            for s in data['stories']:
                stories.append(Story(who=s['who'],date=s['date'],time=s['time'],what=s['what']))
    return stories