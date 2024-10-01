#!/usr/bin/python
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# Authors: Chetan Sahrudhai Kimidi (ckimidi), Megha Nagabhushana Reddy (menaga)
# (based on skeleton code by D. Crandall, Oct 2020)
#References and explanation listed in the report
from PIL import Image, ImageDraw, ImageFont
import sys
import numpy as np
CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25
def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    global TRAIN_LETTERS
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

def MarkovEmiss(train_letters : list, test_letters : list) -> np.array:
    N = 0.1
    imagepxls = CHARACTER_HEIGHT * CHARACTER_WIDTH
    HMMprob = np.zeros((len(train_letters), len(test_letters)))
    imps = {'MS' : 0.9, 'MB' : 0.32, 'MSB' : 1.3, 'MBS' : -0.5 }
    for letter1 in range(len(test_letters)):
        for letter2 in range(len(train_letters)):  
            MS = MB = MSB = MBS = 0  
            learn = list(train_letters.values())[letter2]
            pred = test_letters[letter1]
            for pxl1 in range(CHARACTER_HEIGHT):
                for pxl2 in range(CHARACTER_WIDTH):
                    if learn[pxl1][pxl2] == pred[pxl1][pxl2]:
                        if learn[pxl1][pxl2] == '*':
                            MS += 1
                        else:
                            MB += 1
                    else:
                        if learn[pxl1][pxl2] == '*' and pred[pxl1][pxl2] == ' ':    
                            MSB += 1
                        else:
                            MBS += 1
            HMMprob[letter2][letter1] = (1-N) * (MS * imps['MS'] +  MB * imps['MB'] ) +  N * (MSB * imps['MSB'] +  MBS * imps['MBS']) 
    HMMprob = (HMMprob + 1) / (imagepxls + len(TRAIN_LETTERS)) 
    return HMMprob

def initialise(dataTrainF : str) -> list:
    identities = []
    if (('bc.train' in dataTrainF.lower()) or ('bc.test' in dataTrainF.lower())): 
        with open(dataTrainF, 'r') as F : 
            for sentence in F:
                D =[id for id in sentence.split()]
                identities += D[0::2]
                identities = identities + ' '
        F.close()
    else:
        with open(dataTrainF, 'r') as F:
            sentences = F.readlines()
            for sentence in sentences:
                identities += [id + ' ' for id in sentence.split()]
        F.close()
    return identities           
    
def trialProbability(identities : list):
    startPs = [0] * len(TRAIN_LETTERS)
    for id in identities:
        if id[0] in TRAIN_LETTERS:
            startPs[TRAIN_LETTERS.index(id[0])] += 1
    trialPs = np.array([((startPs[T] + 1) / (len(identities) + len(TRAIN_LETTERS))) for T in range(len(startPs))])
    return trialPs

def changeProbability(identities):
    letters = [letter for word in identities for letter in word]
    changePs = np.zeros((len(TRAIN_LETTERS), len(TRAIN_LETTERS)))
    for bit in range(len(letters)-1):
        if letters[bit] in TRAIN_LETTERS and letters[bit+1] in TRAIN_LETTERS:
            changePs[TRAIN_LETTERS.index(letters[bit]), TRAIN_LETTERS.index(letters[bit+1])] += 1
    divisor = np.sum(changePs, axis=1)
    change =  np.array([[(changePs[bit,bit2] + 1) / (divisor[bit] + len(TRAIN_LETTERS)) for bit2 in range(len(TRAIN_LETTERS))] for bit in range(len(TRAIN_LETTERS))])
    return change    

def Bayesian(test_letters : list, MarkovProb : np.array) -> list:
    exps = np.argmax(MarkovProb, axis=0)
    outp = [TRAIN_LETTERS[entity] for entity in exps]
    return outp

def ViterbiHMM(train_letters, test_letters, trial, change, MarkovProb):
    imp = 0.0018
    matrix = np.zeros((len(train_letters), len(test_letters)))
    optimum = np.zeros_like(matrix, dtype=np.int16)
    for L in range(len(train_letters)):
        matrix[L,0] =  imp * np.log(trial[L]) + np.log(MarkovProb[L,0])
    for bit1 in range(1,len(test_letters)):
        for bit2 in range(len(train_letters)):
            buffer = [ (matrix[L,bit1-1] + (imp * np.log(change[L, bit2])) + ( np.log(MarkovProb[bit2,bit1]))) for L in range(len(train_letters)) ]
            maxval = max(buffer)
            matrix[bit2,bit1] = maxval
            optimum[bit2,bit1] = buffer.index(maxval)
    optim = np.zeros(len(test_letters), dtype=np.int16)
    optim[-1] = np.argmax(matrix[:,-1])
    for let in np.arange(len(test_letters)-1, 0, -1): 
        optim[let-1] = optimum[optim[let],let]
    finalsol = [TRAIN_LETTERS[i] for i in optim]
    return finalsol 
###### main program
if len(sys.argv) != 4: 
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")
(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)
W = initialise(train_txt_fname)
MarkovProbs = MarkovEmiss(train_letters, test_letters)
BayesianSolution = Bayesian(test_letters, MarkovProbs)
trialPs = trialProbability(W)
change = changeProbability(W)
HiddenMarkovSolution = ViterbiHMM(train_letters, test_letters, trialPs, change, MarkovProbs) 
print("Simple: " + "".join(BayesianSolution))
print("   HMM: " + "".join(HiddenMarkovSolution))