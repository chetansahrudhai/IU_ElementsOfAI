# SeekTruth.py : Classify text objects into two categories
# Team/Contributor: Chetan Sahrudhai Kimidi (ckimidi)
# Based on skeleton code by D. Crandall, October 2021
import sys
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

def load_file(filename):
    objects = []
    labels = []
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ', 1)
            labels.append(parsed[0] if len(parsed) > 0 else "")
            objects.append(parsed[1] if len(parsed) > 1 else "")
    return {"objects": objects, "labels": labels, "classes": sorted(list(set(labels)))}

def classifier(train_data, test_data):
    postComp = []
    k = 1
    c = chance(train_data, k)
    ant = antecedent(train_data["labels"])
    for newdata in testingSet(test_data):
        if (np.log(np.array([c[train_data["classes"][0]].get(x) if x in c[train_data["classes"][0]]
           else c[train_data["classes"][0]].get("missing_word") for x in newdata])).sum() + np.log(ant[train_data["classes"][0]])) \
           > \
           (np.log(np.array([c[train_data["classes"][1]].get(y) if y in c[train_data["classes"][1]]
           else c[train_data["classes"][1]].get("missing_word") for y in newdata])).sum() + np.log(ant[train_data["classes"][1]])):
            cls = train_data["classes"][0]
        else:
            cls = train_data["classes"][1]
        postComp.append(cls)
    return postComp

def chance(train_data, key):
    num = len(train_data["classes"])
    A = np.array(train_data["objects"])[np.array(train_data["labels"]) == np.array(train_data["classes"][0])]
    B = np.array(train_data["objects"])[np.array(train_data["labels"]) == np.array(train_data["classes"][1])]
    wcA = delS(" ".join(list(A))).title().split()
    wcB = delS(" ".join(list(B))).title().split()
    pA = (pd.value_counts(wcA) + key).append(pd.Series({"missing_word": key})) / (len(wcA) + key*num)
    pB = (pd.value_counts(wcB) + key).append(pd.Series({"missing_word": key})) / (len(wcB) + key*num)
    return {train_data["classes"][0]: pA, train_data["classes"][1]: pB}

def testingSet(data):
    testingSet = []
    for newdata in data["objects"]:
        testingSet.append(delS(newdata).title().split())
    return testingSet

def delS(data):
    S = ["(", ")", ".", ",", "'", "!", "?"]
    for i in S:
        data = data.replace(i, "")
    return data

def antecedent(labels):
    return pd.value_counts(labels)/len(labels)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")
    (_, train_file, test_file) = sys.argv
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if (sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")
    
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}
    results = classifier(train_data, test_data_sanitized)
    correct_ct = (np.array(results) == np.array(test_data["labels"])).sum() / len(results)
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct))