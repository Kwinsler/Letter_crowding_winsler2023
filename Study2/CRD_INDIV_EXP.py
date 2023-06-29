## Experiment code for study 2 of " "
# -kpw

from psychopy import core, visual, gui, data, event, monitors
import numpy as np
import pandas as pd
from numpy.random import shuffle
import random

# Experiment info
expInfo = {'Subject':'###',
                    'Practice?':True}

expInfo['dateStr'] = data.getDateStr()  # add the current time

# Present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='CRD - Individual differences', fixed=['dateStr'])
if dlg.OK:
    
    monitor = monitors.Monitor(name='104_Dell')  
    monitor.setSizePix((1920,1200))
    monitor.setWidth(52)
    monitor.setDistance(100)
    monitor.saveMon()
    ## Create a visual window:
    win = visual.Window(
        monitor = '104_Dell', 
        units='deg',
        screen=0, 
        fullscr=True 
        )
    win.mouseVisible = False
    
    frameRate = win.getMsPerFrame(nFrames=60, showVisual=False, msg='', msDelay=0.0)

    if expInfo['Practice?'] == False:
        fileName = expInfo['Subject'] + '_INDIV' + expInfo['dateStr']
        dataFile = open(fileName+'.csv', 'w')
        dataFile.write('Hemifield,Eccentricity,Spacing,Correct,Response,TargetLetter,RightLetter,LeftLetter,TargetOnset,TargetOffset,ResponseTime,RT,FrameDropped\n')

else:
    core.quit()  # the user hit cancel so exit

## Experiment parameters

if expInfo['Practice?'] == True:
    stairTrials = 3 #number of trials for each stair to run
else:
    stairTrials = 70

stimSize = 1
stimDur = .1 #time (s) target/flanks are on screen
preStimDur = 1 #ITI (s) after last response before next trial apears
tarPresentaionFlips = int(round(stimDur/frameRate[0]*1000))

hemifields = [-1, 1] # left or right
eccentricities = [2, 4, 6] # in visual degrees

totalTrials = stairTrials*6 #not including probes, 420

letters = ['S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']

target = visual.TextStim(win, pos=[0,0.2],text= letters[1], height=stimSize, font="Arial")
rightFlank = visual.TextStim(win, pos=[0,0.2],text= letters[2], height=stimSize, font="Arial")
leftFlank = visual.TextStim(win, pos=[0,0.2],text= letters[3], height=stimSize, font="Arial")

# number of trials before each break
if expInfo['Practice?'] == True:
    breakTrialArray = [100,100,100] # placeholder (not used for practice)
else:
    breakTrialInterval = 60 #must be divisible by 6
    breakTrialArray = np.linspace(breakTrialInterval,(stairTrials*6)-breakTrialInterval,int((stairTrials*6)/breakTrialInterval)-1)
    breakTrialArray = [ int(x) for x in breakTrialArray ]

## Make probes

numProbes = 42 # one of each letter per location
probeLetters = np.repeat(letters, 48/len(letters))
shuffle(probeLetters)
probeLetters = probeLetters[0:numProbes]

probeHemi = np.repeat(hemifields, numProbes/len(hemifields))
shuffle(probeHemi)

probeEccent = np.repeat(eccentricities, numProbes/len(eccentricities))
shuffle(probeEccent)

# matrix to read from/write to
probeMatrix = pd.DataFrame({'probeNum':np.arange(0, numProbes, 1),
                            'probeLetter':probeLetters,
                            'probeHemi':probeHemi,
                            'probeEccent':probeEccent,
                            'resp':np.empty(numProbes, dtype=str),
                            'correct':np.zeros(numProbes)})

# psuedorandom probe spacing
probeIntervals = np.repeat([9,10,11], numProbes/3)
shuffle(probeIntervals)

probeVector = np.zeros(numProbes)
i = 0
xSum = 0
# fill list with trial numbers to add a probe trial
for x in probeIntervals:
    xSum = xSum + x
    probeVector[i] = xSum
    i = i + 1

probeVector = [ int(x) for x in probeVector ] # make integers
probeNum = 0 # set probe counter

## Functions
def SetupTrial(thisHemi, thisEccent, thisSpacing):
    
    # pick letters
    tarLet = random.choice(letters)
    rightLet = random.choice(np.setdiff1d(letters,tarLet))
    leftLet = random.choice(np.setdiff1d(letters,[tarLet, rightLet]))
    
    # get positions
    tarPos = [thisHemi*thisEccent,0]
    rightPos = [thisHemi*thisEccent + thisSpacing*thisEccent, 0]
    leftPos = [thisHemi*thisEccent - thisSpacing*thisEccent, 0]
    
    # set letters
    target.setText(tarLet)
    rightFlank.setText(rightLet)
    leftFlank.setText(leftLet)
    
    # set positions
    target.pos = tarPos
    rightFlank.pos = rightPos
    leftFlank.pos = leftPos
    
    return(tarLet)

def DrawTrial():
    target.draw()
    rightFlank.draw()
    leftFlank.draw()
    
    fixation.draw()
    fixation_dot.draw()

    win.flip()

# function to give a isolated probe trial
def GiveIsolate():
    
    global probeNum
    
    trialTimer = core.CountdownTimer(preStimDur)
    
    #get parameters
    thisHemi = probeMatrix['probeHemi'][probeNum]
    thisEccent = probeMatrix['probeEccent'][probeNum]
    targetLet = probeMatrix['probeLetter'][probeNum]
    
    target.pos = [thisHemi*thisEccent,0]
    
    # set probe text
    target.setText(targetLet)
    
    fixation.draw()
    fixation_dot.draw()

    win.flip()
    
    # pre trial timer loop
    while trialTimer.getTime() > 0:
        fixation.draw()
        fixation_dot.draw()

        win.flip()
        
    # PRESENT TARGETS
    
    for flip in range(0,tarPresentaionFlips):
        fixation.draw()
        fixation_dot.draw()

        target.draw()
        win.flip()
    
    fixation.draw()
    fixation_dot.draw()
    win.flip()
    
    # get response
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey=='s':
                if targetLet == 'S': thisResp = 1  # correct
                else: thisResp = 0                # incorrect
            
            elif thisKey=='d':
                if targetLet == 'D': thisResp = 1
                else: thisResp = 0
            
            elif thisKey=='f':
                if targetLet == 'F': thisResp = 1
                else: thisResp = 0
            
            elif thisKey=='g':
                if targetLet == 'G': thisResp = 1
                else: thisResp = 0
            
            elif thisKey=='h':
                if targetLet == 'H': thisResp = 1
                else: thisResp = 0
            
            elif thisKey=='j':
                if targetLet == 'J': thisResp = 1
                else: thisResp = 0
            
            elif thisKey=='k':
                if targetLet == 'K': thisResp = 1
                else: thisResp = 0
            
            elif thisKey=='l':
                if targetLet == 'L': thisResp = 1
                else: thisResp = 0
            
            elif thisKey in ['escape']:
                core.quit()  # abort experiment
                
    
    # record data
    probeMatrix.loc[probeNum, 'resp'] = thisKey
    probeMatrix.loc[probeNum, 'correct'] = thisResp
    
def GiveBreak():
    breakTxt1 = visual.TextStim(win, pos=[0,+2], height=1.5, text='Take a break!')
    breakTxt2 = visual.TextStim(win, pos=[0,-2], height=.5, text='Look at the circle and press any key to continue')
    
    breakTxt1.draw()
    breakTxt2.draw()
    fixation.draw()
    win.flip()
    
    event.waitKeys()
    
    fixation0.draw()
    win.flip()
    core.wait(1)
    
    fixation.draw()
    win.flip()
    core.wait(1)
    
## QUEST PARAMETERS
nTrials = stairTrials
priorMean = .5
priorSD = .2
pThreshold = .82 
beta = 3.5
delta = .02
gamma = .125

# make stairs
stairs = []

LPstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Hemifield': -1, 'Eccentricity' : 6})
stairs.append(LPstair)

RPstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Hemifield':1, 'Eccentricity' : 6})
stairs.append(RPstair)

LFstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Hemifield': -1, 'Eccentricity' : 4})
stairs.append(LFstair)

RFstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Hemifield':1, 'Eccentricity' : 4})
stairs.append(RFstair)

RNstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Hemifield': 1, 'Eccentricity' : 2})
stairs.append(RNstair)

LNstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Hemifield': -1, 'Eccentricity' : 2})
stairs.append(LNstair)

# make fixations
fixation = visual.Circle(win, fillColor=[-1,-1,-1], lineColor=[-1,-1,-1], pos=(0, 0), colorSpace='rgb', radius=0.10)
fixation_dot = visual.Circle(win,fillColor=[-0.1,-0.1,-0.1], lineColor=[-1,-1,-1], pos=(0, 0), colorSpace='rgb', radius=0.05)

fixation0 = visual.Circle(win, fillColor=[-0.2,-0.2,-0.2], lineColor=[-0.5,-0.5,-0.5], pos=(0, 0) , colorSpace='rgb', radius=0.15)


# give intructions
instructionsText = visual.TextStim(
    win=win,
    font='Arial',
    pos=(0.0, 0.0),
    height=1,
    wrapWidth = 20
    )
instructionsText.setText(
    'In this task sets of three letters, and occationally single letters, will briefly appear on the screen.\n\n'
    'After each trial, you are to report the center or single letter by pressing that key on the keyboard.\n\n'
    'The possible letter choices are:\n'
    '[S, D, F, G, H, J, K, L]\n\n'
    'Press any key to continue.'
    )

instructionsText.draw()
win.flip()

# intructions 2

event.waitKeys()#pause until there's a keypress

if expInfo['Practice?'] == True:
    instructionsText.setText(
    'While viewing these letters, you must keep your gaze fixated on the dot in the center of the screen.\n\n'
    'It is important to respond as accurately as possible, not as fast as possible.\n\n'
    'If you need to look at the keyboard, look back to the fixation point before responding.\n\n'
    'Press any key to begin the practice run.'
    )
else:
    instructionsText.setText(
    'While viewing these letters, you must keep your gaze fixated on the dot in the center of the screen.\n\n'
    'It is important to respond as accurately as possible, not as fast as possible.\n\n'
    'If you need to look at the keyboard, look back to the fixation point before responding.\n\n'
    'Press any key to begin the experiment.'
    )

instructionsText.draw()
win.flip()#to show drawn stims

event.waitKeys()#pause until there's a keypress

fixation0.draw()
win.flip()
core.wait(1)

fixation.draw()
win.flip()
core.wait(1)

## START ACTUAL RUN ##

globalClock = core.Clock()
critFrameDrops = 0 #set frame drop counter (for targets)
trialNum = 0 # set trial number counter

for trialn in range(nTrials):
    
    trialTimer = core.CountdownTimer(preStimDur)
    
    shuffle(stairs)
    
    for thisStair in stairs:
        
        # check if it's time for an isolate
        if trialNum in probeVector:
            GiveIsolate()
            probeNum = probeNum + 1
            trialTimer = core.CountdownTimer(preStimDur)
        else:
            pass
        
        # check if it's time for a break
        if trialNum in breakTrialArray:
            GiveBreak()
            trialTimer = core.CountdownTimer(preStimDur)
        else:
            pass
        
        # force first 3 trials of each stair to be 50% spaced
        if trialNum < 36:
            thisSpacing = priorMean
        else:
            thisSpacing = next(thisStair)
        
        thisHemi = thisStair.extraInfo['Hemifield']
        thisEccent = thisStair.extraInfo['Eccentricity']
        
        targetLet = SetupTrial(thisHemi = thisHemi, thisEccent = thisEccent, thisSpacing = thisSpacing)
        
        # pre trial timer loop
        while trialTimer.getTime() > 0:
            fixation.draw()
            fixation_dot.draw()
            win.flip()
        
        presTime = globalClock.getTime()
        
        # PRESENT TARGETS        
        for flip in range(0,tarPresentaionFlips):
            
            DrawTrial()
        
        presTimeOff = globalClock.getTime()
        
        fixation.draw()
        fixation_dot.draw()
        win.flip()
        
        # get response
        thisResp=None
        while thisResp==None:
            allKeys=event.waitKeys()
            for thisKey in allKeys:
                if thisKey=='s':
                    if targetLet == 'S': thisResp = 1  # correct
                    else: thisResp = 0                # incorrect
                
                elif thisKey=='d':
                    if targetLet == 'D': thisResp = 1
                    else: thisResp = 0
                
                elif thisKey=='f':
                    if targetLet == 'F': thisResp = 1
                    else: thisResp = 0
                
                elif thisKey=='g':
                    if targetLet == 'G': thisResp = 1
                    else: thisResp = 0
                
                elif thisKey=='h':
                    if targetLet == 'H': thisResp = 1
                    else: thisResp = 0
                
                elif thisKey=='j':
                    if targetLet == 'J': thisResp = 1
                    else: thisResp = 0
                
                elif thisKey=='k':
                    if targetLet == 'K': thisResp = 1
                    else: thisResp = 0
                
                elif thisKey=='l':
                    if targetLet == 'L': thisResp = 1
                    else: thisResp = 0
                
                elif thisKey in ['escape']:
                    core.quit()  # abort experiment
                
            respTime = globalClock.getTime() # get response time
            RT = respTime - presTime # calculate reaction time
            event.clearEvents()  # clear other (eg mouse) events - they clog the buffer
        # response while ends
        
        fixation.draw()
        win.flip()
        
        if trialNum < 36:
            thisStair.addData(thisResp, intensity = priorMean)
        else:
            thisStair.addData(thisResp)
        
        
        if (presTimeOff-presTime)*1000 > 107:
            frameDrop = 1
            critFrameDrops +=1
        else:
            frameDrop = 0
        
        if expInfo['Practice?'] == False:
            dataFile.write('%s,%f,%f,%f,%s,%s,%s,%s,%f,%f,%f,%f,%f\n' %(thisHemi, thisEccent, thisSpacing, thisResp, thisKey, targetLet, rightFlank.text, leftFlank.text, presTime, presTimeOff, respTime, RT, frameDrop))
        
        trialNum +=1
        
        trialTimer = core.CountdownTimer(preStimDur)

# check if it's time for an isolate
if trialNum in probeVector:
    GiveIsolate()

# if practice, end here
if expInfo['Practice?'] == True:
    end1 = visual.TextStim(win, pos=[0,+2], height=1.5, text='End of practice')
    end2 = visual.TextStim(win, pos=[0,-2], height=1.5, text='Do you have any questions?')
    end1.draw()
    end2.draw()
    win.flip()
    core.wait(5)
    win.close()
    core.quit()

# Record summary data
stairSum = pd.DataFrame({'Stair':['LNstair', 'LFstair', 'LPstair', 'RNstair', 'RFstair', 'RPstair'],
                         'Mean':np.zeros(6),
                         'SD':np.zeros(6),
                         'CIwidth':np.zeros(6)})

stairSum=stairSum.reindex(['Stair','Mean','SD','CIwidth'], axis=1)

idx = 0

# re sort stairs
stairs.sort(key = lambda staircase: staircase.extraInfo['Eccentricity'], reverse = False)
stairs.sort(key = lambda staircase: staircase.extraInfo['Hemifield'], reverse = False)

# fill summary
for stair in stairs:
    
    stairSum.iloc[idx,1] = stair.mean()
    stairSum.iloc[idx,2] = stair.sd()
    stairSum.iloc[idx,3] = stair.confInterval(getDifference=True)
    
    idx = idx + 1

# save summaries
stairSum.to_csv(path_or_buf = fileName+'_SUMMARY.csv', index = False)

# save probes
probeMatrix.to_csv(path_or_buf = fileName+'_Probes.csv', index = False)

print( "Dropped ", critFrameDrops, " critical frames...")
core.wait(5)

win.close()
core.quit()
