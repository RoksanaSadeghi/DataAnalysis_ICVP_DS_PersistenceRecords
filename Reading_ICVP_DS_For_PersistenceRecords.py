# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 10:56:14 2022

@author: roksana
"""
import os
#import numpy as np

#reading the directories and files
def FileDir( directory, nametag ):
    sessiondir = []
    dir = os.listdir(directory)
    for item in dir:
        if nametag in item:
            sessiondir.append(item)
    return sessiondir   

#reading ICVP_DS user input output files
def ReadUserInputFile(userInputDir):
    textFile = []
    trials = []
    with open(userInputDir) as ui: textFile = ui.readlines()
    #Find the main table
    isTable = False
    for line in textFile:
        if (not isTable) and (line.startswith("UserID")): isTable = True
        elif isTable:
            trials.append(line)
    return trials
    
# combine all trials 
def CombineAllTrials( mainDir ):
    trials = []
    for session in FileDir(mainDir, "Session"):
        userInputFiles = FileDir(mainDir + "\\" + session, "user_input")
        for userInput in userInputFiles:
            userInputDir = mainDir + "\\" + session + "\\" + userInput
            trials.extend( ReadUserInputFile(userInputDir) )
    return trials

# extract the comments and select trials that has specific keywords in the comment
def FilterTrials(allTrials, included_keywords):
    ifIncludedKey = False 
    trials_filtered = []
    comments = []
    for trial in allTrials:
        comment = trial.split(" ; ")[-1].strip("\n")
        for k in included_keywords:
            if k.lower() in comment.lower(): ifIncludedKey = True    
        if ifIncludedKey: 
            trials_filtered.append(trial)
            comments.append(comment)
            ifIncludedKey = False
    return trials_filtered, comments
            
# convert the hex electrodeID to decimal
def ConvertElecID_Hex2Dec(trialsList): 
    trialsList_elecDec = []
    for trial in trialsList:
        gDec = ""
        t = trial.split(" ; ")
        group = t[2].split(" , ")
        for g in group:
            eDec = ""
            electrodes = g.strip(" ").split("-")
            for e in electrodes:
                eDec = eDec + "-" + str(int(e[0:2],16)) + "," + str( int(e[2:4],16)+1 )
            gDec = gDec + " , " + eDec.strip("-")
        t[2] = gDec.strip(" , ")
        trialsList_elecDec.append(" ; ".join(t))
        
    return trialsList_elecDec



mainDir = os.getcwd() + "\ICVP_DS_Data"
allTrials = CombineAllTrials(mainDir)
trials_filtered, comments = FilterTrials(allTrials, ['pers','seconds','slow','later','offset','delay','fade','continue'])
trials_filtered = ConvertElecID_Hex2Dec(trials_filtered)
with open(mainDir+"\\filteredTrials.txt",'w') as f:
    f.writelines("Looking for Persistance Records in ICVP_DS data\nExctract trials that the comments included: 'pers','seconds','slow','later','offset','delay','fade','continue'\n")
    f.writelines("UserID ; Time ; Electrodes ; Frequency (Hz) ; Cathodic Phase Duration (us) ; Train Length (ms) ; Duty On (ms); Duty Off (ms) ; Inter-train Length (ms) ; Amplitude (uA) ; Sent to Gateway ; Response ; Response Latency (ms) ; Response Duration (ms) ; Comments\n")
    f.writelines(trials_filtered)
#trials_filtered, comments = FilterTrials(allTrials, ['anything','nothing',])


























