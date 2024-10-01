###################################
# CS B551 Fall 2022, Assignment #3
# Your names and user ids: Megha Nagabhushana Reddy (menaga), Chetan Sahrudhai Kimidi (ckimidi)
# (Based on skeleton code by D. Crandall)
#References listed below and code explained in the project report
import math, numpy as np
from copy import deepcopy

class Solver:
    def __init__(self):
        self.wordgroup = {}   # The dictionary of all words with keys and values consisting the tagwords and respective counts
        self.countag = {}     # The dictinary with counts of all tags
        self.occurs = {}      # Dictionary with respective tag occurring probabilities
        self.emissps = {}     # Dictionary containing values of emission probabilities for  words (Emis Prob = Wordcount/Tagcount)
        self.prEmiscMC = {}   # Dictionary containing emission counts for the MCMC
        self.precurC = {}     # Contains counts of current and prev tag combination
        self.beginner = {}    # Sentence beginning tag counts
        self.beginps = {}     # Respective beginner tag occurring probabilities
        self.move = {}        # Chance of moving between two states
        self.triDepMove = {}  # Conditional probability where third state depends (or not) on previous two states
        self.wprEmiscMC = self.consectagsc = {}      
   
    def tracker(self, data): #usage - keeping track of the counts of all tags, words 
        for bit in range(len(data)):
            wL, tL  = data[bit]
            for seg in range(len(wL)):                
                presw = wL[seg]
                prest = tL[seg]

                if seg<len(tL)-1:
                    succt = tL[seg+1]
                if seg>1:
                    grptag = tL[seg-1] + "<>" + tL[seg-2]
                    self.trimoveC(prest, grptag)
                if seg != 0:
                    beft = tL[seg-1]
                    self.preWTCounter(presw, prest, beft)
                if seg == 0:
                    self.startC(prest)
                self.numWCounter(presw, prest)
                self.numTCounter(prest)
                self.moveC(prest, succt)
                
    def startC(self, T):
        if T in self.beginner:
            self.beginner[T] += 1
        else:
            self.beginner[T] = 1

    def numWCounter(self, W, T):
        if W in self.wordgroup:
            if T in self.wordgroup[W]:
                self.wordgroup[W][T] += 1
                self.emissps[W][T] += 1
            else:
                self.wordgroup[W][T] = 1
                self.emissps[W][T] = 1 
        else:
            self.wordgroup[W] = {T:1}
            self.emissps[W] = {T:1}

    def numTCounter(self, T):                
        if T in self.countag:
            self.countag[T] += 1
        else:
            self.countag[T] = 1
            
    def moveC(self, tpres, tsucc):
        if tpres in self.move:
            if tsucc in self.move[tpres]:
                self.move[tpres][tsucc] += 1
            else:
                self.move[tpres][tsucc] = 1
        else:
            self.move[tpres] = {tsucc:1}
    
    def trimoveC(self, presenT, grpretag):
        if grpretag in self.consectagsc:
            self.consectagsc[grpretag] += 1
        else:
            self.consectagsc[grpretag] = 1
        if presenT in self.triDepMove:
            if grpretag in self.triDepMove[presenT]:
                self.triDepMove[presenT][grpretag] += 1
            else:
                self.triDepMove[presenT][grpretag] = 1
        else:
            self.triDepMove[presenT] = {grpretag:1}
        
    def preWTCounter(self, presenW, presenT, beft):
        wordtagGroup = beft + "<>" + presenT
        if wordtagGroup in self.precurC:
            self.precurC[wordtagGroup] += 1
        else:
            self.precurC[wordtagGroup] = 1
            
        if presenW in self.prEmiscMC:
            if wordtagGroup in self.prEmiscMC[presenW]:
                self.prEmiscMC[presenW][wordtagGroup] += 1
            else:
                self.prEmiscMC[presenW][wordtagGroup] = 1
        else:
            self.prEmiscMC[presenW]={wordtagGroup:1}
 
    def occurrences(self,data):        
        length = len(data)
        TCount = sum(self.countag.values())
        Tag12Group = ['noun','adj','verb','.', 'prt','pron', 'det','x','adp','conj','num','adv']
        BASE = 10**-10
        for W in self.emissps:
            for givenT in Tag12Group:
                if givenT in self.emissps[W]:
                    self.emissps[W][givenT]/=self.countag[givenT]
                else:
                    self.emissps[W][givenT]=BASE
        for i in self.countag:
            self.occurs[i]=self.countag[i]/TCount
        for j in self.beginner:
            self.beginps[j]=self.beginner[j]/length
        for k in self.prEmiscMC:
            self.wprEmiscMC[k]={}
            for grp in self.prEmiscMC[k]:
                res = self.precurC[grp]
                self.wprEmiscMC[k][grp] = self.prEmiscMC[k][grp]/res
        for W in self.triDepMove:
            for grp in self.triDepMove[W]:
                self.triDepMove[W][grp] /= self.consectagsc[grp]
        for state in self.move:
            TSum = sum(self.move[state].values())
            for nexT in Tag12Group:
                if nexT in self.move[state]:
                    self.move[state][nexT] /= TSum
                else:
                    self.move[state][nexT] = BASE
     
# Calculate the log of the posterior probability of a given sentence with a given part-of-speech labeling.
    def posterior(self, model, sentence, label):
        BASE = 10**-10
        result = 0
        if model == "Simple":
            for bit in range(len(sentence)):
                W = sentence[bit]
                bitT = label[bit]
                if W in self.wordgroup:
                    if bitT in self.wordgroup[W]:
                        result += math.log(self.emissps[W][bitT]*self.occurs[bitT])
                else:
                    greatesT = max(self.countag, key=self.countag.get)
                    result += math.log(self.occurs[greatesT])
            return result
        elif model == "HMM":
            for bit in range(len(sentence)):
                W = sentence[bit]
                bitT = label[bit]
                occur = self.occurs[bitT]
                if bit < len(sentence)-1:
                        succt = label[bit+1]
                        result += math.log(occur* self.move[bitT][succt])
                if bit == 0:
                    if W in self.emissps:
                        result += math.log(self.beginner[bitT] * self.emissps[W][bitT])
                    else:
                        result += math.log(BASE)
                else:
                    if W in self.emissps:
                        result += math.log(self.emissps[W][bitT])
                    else:
                        result += math.log(BASE)
            return result
        elif model == "Complex":
            length = len(sentence)
            for bit in range(len(sentence)):
                W=sentence[bit]
                bitT=label[bit]
                if W in self.emissps[W]:
                    E = math.log(self.emissps[W][bitT])
                else:
                    E = math.log(BASE)
                if bit<length-1:
                    succw=sentence[bit+1]
                    succt=label[bit+1]
                    if succw in self.wprEmiscMC:
                        if bitT+"<>"+succt in self.wprEmiscMC[succw]:
                            emissprob = math.log(self.wprEmiscMC[succw][bitT+"<>"+succt])
                        else:
                            emissprob = math.log(BASE)
                    else:
                        emissprob = math.log(BASE)
                if (bit!=0) and (bit < length-2):
                    followT=label[bit+2]
                    succt=label[bit+1]
                    if followT in self.triDepMove:
                        if succt+"<>"+bitT in self.triDepMove[followT]:
                            moveOccur = math.log(self.triDepMove[followT][succt+"<>"+bitT])
                        else:
                            moveOccur = math.log(BASE)
                    else:
                        moveOccur = math.log(BASE)
                else:
                    moveOccur = math.log(BASE)
                if bit!=0 and(bit<length-1):
                    succt=label[bit+1]
                    moveP = math.log(self.move[succt][bitT])
                else:
                    moveP = math.log(BASE)
                if bit!=0:
                    beft=label[bit-1]
                    if W in self.wprEmiscMC:
                        if beft+"<>"+bitT in self.wprEmiscMC[W]:
                            premissprob = math.log(self.wprEmiscMC[W][beft+"<>"+bitT])
                        else:
                            premissprob = math.log(BASE)
                    else:
                        premissprob = math.log(BASE)
                if bit>1:
                    beft=label[bit-1]
                    behindT=label[bit-2]
                    if bitT in self.triDepMove:
                        if beft+"<>"+behindT in self.triDepMove[bitT]:
                            premoveP = math.log(self.triDepMove[bitT][beft+"<>"+behindT])
                        else:
                            premoveP = math.log(BASE)
                    else:
                        premoveP = math.log(BASE)
                if bit == 0:
                    result+=math.log(self.beginps[bitT])+E
                elif bit == 1:
                    result+=E+emissprob+moveOccur+moveP
                elif bit==length-2:
                    result+= premoveP + moveP + E + math.log(self.move[label[bit-1]][bitT]) + premissprob
                elif bit==length-1:
                    result+=premoveP+moveP+E+math.log(self.move[label[bit-1]][bitT])
                else:
                    result+=moveOccur+premissprob+E+moveP+math.log(self.move[label[bit-1]][bitT]) +emissprob +  premissprob
            return result
        else:
            print("Unknown algo!")

# Do the training!
    def train(self, data):
        self.tracker(data)
        self.occurrences(data)

# Functions for each algorithm.

# the accuracy(words) is 93.92% and accuracy(sentences) is 47.45% for the big test file
# whereas accuracy(words) is 97.62%, accuracy(sentences) is 66.67% for the tiny test file.
    def simplified(self, sentence): # simplified - uses Naive Bayes ; each entity does not depend on its consecutive one.
        estimaT=[]
        for bit in range(len(sentence)):
            W = sentence[bit]
            if W in self.wordgroup:
                wsum=sum(self.wordgroup[W].values())
                chance = {tag : self.wordgroup[W][tag]/wsum for tag in self.wordgroup[W]}               
                maxprob=max(chance,key=chance.get)   
                estimaT.append(maxprob)
            else:
                estimaT.append(max(self.countag,key=self.countag.get))
        return estimaT

# the accuracy(words) is 94.86% and accuracy(sentences) is 51.90% for the big test file
# whereas accuracy(words) is 97.62%, accuracy(sentences) is 66.67% for the tiny test file.
    def hmm_viterbi(self, sentence): # outputs a Viterbi sequence by computing forward probabilities and rebounding to expect the tags.
        Tag12Group =['noun','adj','verb','.', 'prt','pron', 'det','x','adp','conj','num','adv']
        vitdict = tablecopy = {}
        length=len(sentence)
        BASE=10**-10
        for bit in range(length):
            W=sentence[bit]
            if W not in self.emissps:
                self.emissps[W]={}
                for type in Tag12Group:
                    self.emissps[W][type]=BASE        
        vitdict = {type : [0]*length for type in Tag12Group}
        tablecopy = deepcopy(vitdict)

        for type in Tag12Group:
            vitdict[type][0]=self.beginps[type]*self.emissps[sentence[0]][type]         
        for bit in range(1,length):
            for type in Tag12Group:
                bufdict={}
                vitdict[type][bit] = self.emissps[sentence[bit]][type]
                for var in Tag12Group:
                    bufdict[var]=self.move[var][type]*vitdict[var][bit-1]
                T = max(bufdict,key=bufdict.get)                
                tablecopy[type][bit]=T
                vitdict[type][bit]*=vitdict[T][bit-1]*self.move[T][type]        
        V = [""] * length
        bufdictwo = {}
        for type in Tag12Group:
            bufdictwo[type]=vitdict[type][bit]
        bufdictwo={ type : vitdict[type][bit] for type in Tag12Group}       
        expecT = max(bufdictwo,key=bufdictwo.get)
        V[length-1]=expecT
        for bit in range(length-2, -1, -1):
            V[bit] = tablecopy[V[bit+1]][bit+1]
        return V
    
# the accuracy(words) is 93.92% and accuracy(sentences) is 47.45% for the big test file
# whereas accuracy(words) is 97.62%, accuracy(sentences) is 66.67% for the tiny test file. 
    def MCMCalgo(self,sentence,epochs,defaulttext,Tag12Group):
        testcases=[self.defaulttext]
        BASE = 10**-10
        for ep in range(epochs):
            case=[]
            sample=testcases[-1]
            for seg in range(len(sentence)):
                presw=sentence[seg]
                if seg<len(sentence)-1:
                    succw=sentence[seg+1]                
                possibles={}
                for T in Tag12Group:
                    beginningP = self.beginps[T]
                    if presw in self.emissps:
                        cemissprob = self.emissps[presw][T]
                    else:
                        cemissprob = BASE
                    
                    if seg<len(sentence)-1:
                        if succw in self.wprEmiscMC:
                            if T+"<>"+sample[seg+1] in self.wprEmiscMC[succw]:
                                emissprob = self.wprEmiscMC[succw][T+"<>"+sample[seg+1]]
                            else:
                                emissprob = BASE
                        else:
                            emissprob = BASE                    
                    if (seg!=0) and (seg < len(sentence)-2):
                        if sample[seg+2] in self.triDepMove:                            
                            if sample[seg+1]+"<>"+T in self.triDepMove[sample[seg+2]]:
                                moveOccur = self.triDepMove[sample[seg+2]][sample[seg+1]+"<>"+T]
                            else:
                                moveOccur = BASE
                        else:
                            moveOccur = BASE
                    else:
                        moveOccur = BASE
                    if seg!=0 and(seg<len(sentence)-1):
                        moveP = self.move[sample[seg+1]][T]
                    else:
                        moveP = BASE                     
                    if seg!=0:
                        if presw in self.wprEmiscMC:
                            if case[seg-1]+"<>"+T in self.wprEmiscMC[presw]:
                                premissprob = self.wprEmiscMC[presw][case[seg-1]+"<>"+T]
                            else:
                                premissprob = BASE
                        else:
                            premissprob = BASE                            
                    if seg>1: 
                        if T in self.triDepMove:
                            if case[seg-1]+"<>"+case[seg-2] in self.triDepMove[T]:
                                premoveP = self.triDepMove[T][case[seg-1]+"<>"+case[seg-2]]
                            else:
                                premoveP = BASE
                        else:
                            premoveP = BASE
                    if seg == 0:
                        P = math.log(beginningP) + math.log(cemissprob) 
                    elif seg == 1:
                         
                        P = math.log(emissprob) +math.log(moveOccur) +math.log(premissprob) +math.log(self.move[case[seg-1]][T])+ math.log(cemissprob)+ math.log(moveP)
                    
                    elif seg == len(sentence)-2:
                        
                        P = math.log(premoveP) + math.log(moveP) +  math.log(cemissprob)  + math.log(self.move[case[seg-1]][T]) + math.log(premissprob) 
                    
                    elif seg == len(sentence)-1:
                        
                        P = math.log(premoveP)+  math.log(cemissprob) +math.log(self.move[case[seg-1]][T])
                    else:
                        P = math.log(moveOccur) +math.log(premoveP)+math.log(cemissprob) +math.log(moveP) +math.log(self.move[case[seg-1]][T]) +math.log(emissprob) +  math.log(premissprob) 
                    final_prob=math.exp(P)
                    possibles[T]=final_prob
                cumulative=sum(possibles.values())
                for key in possibles:
                    possibles[key] /= cumulative                    
                pList=list(possibles.items())
                pro=[pList[i][1] for i in range(len(pList))]
                index = [pList[i][0] for i in range(len(pList))]   
                bitT= np.random.choice(index,1,p=pro)
                case.append(bitT[0])                
            testcases.append(case)
        return testcases
    
    def complex_mcmc(self, sentence):
        D = {}
        epochs=150
        self.defaulttext=['noun'] * len(sentence) 
        Tag12Group =['noun','adj','verb','.', 'prt','pron', 'det','x','adp','conj','num','adv']
        testcases=self.MCMCalgo(sentence, epochs, self.defaulttext, Tag12Group)
        for bit in range(len(testcases)):
            cases=testcases[bit]
            for seg in range(len(cases)):
                bitT=cases[seg]
                if seg in D:
                    if bitT in D[seg]:
                        D[seg][bitT]+=1
                    else:
                        D[seg][bitT]=1
                else:
                    D[seg]={}
        solution=[]
        for bit in D:
            wc=D[bit]
            Mode = max(wc,key=wc.get)
            solution.append(Mode)
        return solution

# This solve() method is called by label.py, so you should keep the interface the same, but you can change the code itself. 
# It should return a list of part-of-speech labelings of the sentence, one part of speech per word.
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")

# REFERENCE LINKS
#https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
#https://medium.com/data-science-in-your-pocket/pos-tagging-using-hidden-markov-models-hmm-viterbi-algorithm-in-nlp-mathematics-explained-d43ca89347c4
#https://newbedev.com/np-random-choice-probabilities-do-not-sum-to-1 For normalizing probabilities.
#https://towardsdatascience.com/gibbs-sampling-8e4844560ae5
#Prof Crandall lecture and video codes