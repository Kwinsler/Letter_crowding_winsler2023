## Experiment code for study 1a of " " 
# Crowding for letters vs inverted letters

# imports
from psychopy import core, visual, gui, data, event, monitors
import numpy as np
import pandas as pd
from numpy.random import shuffle
import random

# Experiment info (can be modified when script is run)
expInfo = {'Subject':'###',
                    'Practice?':True}

expInfo['dateStr'] = data.getDateStr()  # add the current time

# Present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='CRD_INV_HOR', fixed=['dateStr'])
if dlg.OK:
    
    monitor = monitors.Monitor(name='104_Dell')   #expInfo['Monitor'])
    monitor.setSizePix((1920,1200))
    monitor.setWidth(52)
    monitor.setDistance(100)
    monitor.saveMon()
    ## Create a visual window:
    win = visual.Window(
        monitor = '104_Dell', #expInfo['Monitor'],
        units='deg',
        screen=0, #screen=0 for primary monitor, screen=1 to display on secondary monitor
        fullscr=True 
        )
    win.mouseVisible = False
    
    frameRate = win.getMsPerFrame(nFrames=60, showVisual=False, msg='', msDelay=0.0)
    
    # if not practice, start data file
    if expInfo['Practice?'] == False:
        fileName = expInfo['Subject'] + '_INV_HOR' + expInfo['dateStr']
        dataFile = open(fileName+'.csv', 'w')  
        dataFile.write('Condition,Hemifield,Eccentricity,Spacing,Correct,Response,TargetLetter,RightLetter,LeftLetter,TargetOnset,TargetOffset,ResponseTime,RT,FrameDropped\n')
        
else:
    core.quit()  # the user hit cancel so exit

if expInfo['Practice?'] == True:
    stairTrials = 2 # for practice, will equal 24 trials total
else:
    stairTrials = 50 # number of trials per staircase
    
letters = [
    'F'
    ,
    'G'
    ,
    'J'
    ,
    'L'
    ,
    'N'
    ,
    'S'
    ,
    'R'
    ,
    'Z'
    ]

stimSize = 1 # height in visual degrees
stimDur = .1 #time (s) target/flanks are on screen
preStimDur = 1 #ITI (s) after last response before next trial apears
tarPresentaionFlips = int(round(stimDur/frameRate[0]*1000))

# stim par
hemifields = [-1, 1] # left or right
eccentricities = [2, 4, 6] # in visual degrees
conditions = ['Vertical','Inverted'] #

# stims
target = visual.TextStim(win, pos=[0,0.2],text= letters[1], height=stimSize, font="Arial")
rightFlank = visual.TextStim(win, pos=[0,0.2],text= letters[2], height=stimSize, font="Arial")
leftFlank = visual.TextStim(win, pos=[0,0.2],text= letters[3], height=stimSize, font="Arial")

def SetupTrial(thisHemi, thisEccent, thisSpacing, condition): # info supplied per trial
    
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
    
    # set condition
    if condition == 'Vertical':
        target.flipVert = False
        rightFlank.flipVert = False
        leftFlank.flipVert = False
     
    if condition == 'Inverted':
        target.flipVert = True
        rightFlank.flipVert = True
        leftFlank.flipVert = True

def DrawTrial(): # one frame
    target.draw()
    rightFlank.draw()
    leftFlank.draw()
    
    fixation.draw()
    fixation_dot.draw()

    win.flip()

# resp array set up
respSeparation = 2
respY = 2
respWidth = 0.8

# response circles (invisible)
respCircle1 = visual.Circle(win, radius=respWidth,lineColor=0,fillColor=0,pos=[0,-2])
respCircle2 = visual.Circle(win, radius=respWidth,lineColor=0,fillColor=0,pos=[0,-2])
respCircle3 = visual.Circle(win, radius=respWidth,lineColor=0,fillColor=0,pos=[0,-2])
respCircle4 = visual.Circle(win, radius=respWidth,lineColor=0,fillColor=0,pos=[0,-2])
respCircle5 = visual.Circle(win, radius=respWidth,lineColor=0,fillColor=0,pos=[0,-2])
respCircle6 = visual.Circle(win, radius=respWidth,lineColor=0,fillColor=0,pos=[0,-2])
respCircle7 = visual.Circle(win, radius=respWidth,lineColor=0,fillColor=0,pos=[0,-2])
respCircle8 = visual.Circle(win, radius=respWidth,lineColor=0,fillColor=0,pos=[0,-2])

# response letters
resp1 = visual.TextStim(win, pos=[0,-2],text= letters[0], height=stimSize, font="Arial", flipVert = True)
resp2 = visual.TextStim(win, pos=[0,-2],text= letters[1], height=stimSize, font="Arial", flipVert = True)
resp3 = visual.TextStim(win, pos=[0,-2],text= letters[2], height=stimSize, font="Arial", flipVert = True)
resp4 = visual.TextStim(win, pos=[0,-2],text= letters[3], height=stimSize, font="Arial", flipVert = True)
resp5 = visual.TextStim(win, pos=[0,-2],text= letters[4], height=stimSize, font="Arial", flipVert = True)
resp6 = visual.TextStim(win, pos=[0,-2],text= letters[5], height=stimSize, font="Arial", flipVert = True)
resp7 = visual.TextStim(win, pos=[0,-2],text= letters[6], height=stimSize, font="Arial", flipVert = True)
resp8 = visual.TextStim(win, pos=[0,-2],text= letters[7], height=stimSize, font="Arial", flipVert = True)

# response positions
respPositions = [[-3*respSeparation,respY],
                [-1*respSeparation,respY],
                [1*respSeparation,respY],
                [3*respSeparation,respY],
                [3*respSeparation,-respY],
                [1*respSeparation,-respY],
                [-1*respSeparation,-respY],
                [-3*respSeparation,-respY]]

# posision shuffle
shuffledPositions = [0,1,2,3,4,5,6,7] # will be shuffled per trial

# cursor
cursor = visual.Circle(win,radius=0.1,lineColor=[-.5,-.5,-.5],fillColor=[-.4,-.4,-.4],pos=(0, 0))

def GetResponse(condition):
    global critFrameDrops
    
    shuffle(shuffledPositions)
    
    # set positions
    respCircle1.pos = respPositions[shuffledPositions[0]]
    resp1.pos = respPositions[shuffledPositions[0]]
        
    respCircle2.pos = respPositions[shuffledPositions[1]]
    resp2.pos = respPositions[shuffledPositions[1]]
    
    respCircle3.pos = respPositions[shuffledPositions[2]]
    resp3.pos = respPositions[shuffledPositions[2]]
    
    respCircle4.pos = respPositions[shuffledPositions[3]]
    resp4.pos = respPositions[shuffledPositions[3]]
    
    respCircle5.pos = respPositions[shuffledPositions[4]]
    resp5.pos = respPositions[shuffledPositions[4]]
    
    respCircle6.pos = respPositions[shuffledPositions[5]]
    resp6.pos = respPositions[shuffledPositions[5]]
    
    respCircle7.pos = respPositions[shuffledPositions[6]]
    resp7.pos = respPositions[shuffledPositions[6]]
    
    respCircle8.pos = respPositions[shuffledPositions[7]]
    resp8.pos = respPositions[shuffledPositions[7]]
    
    # set conditions
    if condition == 'Vertical':
        resp1.flipVert = False
        resp2.flipVert = False
        resp3.flipVert = False
        resp4.flipVert = False
        resp5.flipVert = False
        resp6.flipVert = False
        resp7.flipVert = False
        resp8.flipVert = False
     
    if condition == 'Inverted':
        resp1.flipVert = True
        resp2.flipVert = True
        resp3.flipVert = True
        resp4.flipVert = True
        resp5.flipVert = True
        resp6.flipVert = True
        resp7.flipVert = True
        resp8.flipVert = True
        
    thisResp=None
    responseLet = None
    RT = 0
    core.wait(0.5)
    
    mouse = event.Mouse(visible = False, win = win)
    mouse.setPos([0,0])
    cursor.pos=mouse.getPos()
    
    while responseLet == None:
        
        respCircle1.draw()
        resp1.draw()
        respCircle2.draw()
        resp2.draw()
        respCircle3.draw()
        resp3.draw()
        respCircle4.draw()
        resp4.draw()
        respCircle5.draw()
        resp5.draw()
        respCircle6.draw()
        resp6.draw()
        respCircle7.draw()
        resp7.draw()
        respCircle8.draw()
        resp8.draw()
        
        fixation0.draw()
        
        cursor.pos=mouse.getPos()
        cursor.draw()
        win.flip()
        
        if event.getKeys(keyList=['escape', 'q']):
            win.close()
            core.quit()
        
        if mouse.isPressedIn(respCircle1):
            responseLet = letters[0]
        
        if mouse.isPressedIn(respCircle2):
            responseLet = letters[1]
        
        if mouse.isPressedIn(respCircle3):
            responseLet = letters[2]
        
        if mouse.isPressedIn(respCircle4):
            responseLet = letters[3]
        
        if mouse.isPressedIn(respCircle5):
            responseLet = letters[4]
        
        if mouse.isPressedIn(respCircle6):
            responseLet = letters[5]
        
        if mouse.isPressedIn(respCircle7):
            responseLet = letters[6]
        
        if mouse.isPressedIn(respCircle8):
            responseLet = letters[7]
    
    # while ends
    
    respTime = globalClock.getTime() # get response time
    RT = respTime - presTime # calculate reaction time
    event.clearEvents()
    
    fixation.draw()
    win.flip()
    
    if responseLet == target.text:
        thisResp = 1
    else:
        thisResp = 0
    
    # because first 3 trials of each stair forced to be 50% spaced
    if trialNum < 36:
        thisStair.addData(thisResp, intensity = priorMean)
    else:
        thisStair.addData(thisResp)

    
    if (presTimeOff-presTime)*1000 > 107:
        frameDrop = 1
        critFrameDrops +=1
    else:
        frameDrop = 0
    
    tarLet = target.text
    rightLet = rightFlank.text
    leftLet = leftFlank.text
    
    # write data
    if expInfo['Practice?'] == False:
        dataFile.write('%s,%s,%f,%f,%f,%s,%s,%s,%s,%f,%f,%f,%f,%f\n' %(condition, thisHemi, thisEccent, thisSpacing, thisResp, responseLet, tarLet , rightLet, leftLet, presTime, presTimeOff, respTime, RT, frameDrop))
    
# end response function

## Set up trial arrays
totalTrials = stairTrials*12 #not including probes

numProbes = 48 # two per letter*stair
# Set up isolated letter probes to gauge lapses..
# make randomized but evenly represented list of 24 letters
probeLetters = np.repeat(letters, 6)
shuffle(probeLetters)
# make randomized but evenly represented list of 24 locations
probeHemi = np.repeat(hemifields, 6*4)
shuffle(probeHemi)

probeEccent = np.repeat(eccentricities, 8*2)
shuffle(probeEccent)

probeCond = np.repeat(conditions, 24)
shuffle(probeCond)

# matrix to read from/write to
probeMatrix = pd.DataFrame({'probeNum':np.arange(0, numProbes, 1),
                            'probeCondition' : probeCond,
                            'probeLetter':probeLetters,
                            'probeHemi':probeHemi,
                            'probeEccent':probeEccent,
                            'resp':np.empty(numProbes, dtype=str),
                            'correct':np.zeros(numProbes)})

probeVector = np.zeros(numProbes)

# clunky way to make list of trial numbers to have isolated probe trials
m = 2 # odd/even counter
i = 8 # starting value, will be incremented
# fill list with trial numbers to add a probe trial
for x in range(0,numProbes):
    probeVector[x] = i
    if (m % 2) == 0:
        i = i + 12
    else:
        i = i + 13
    
    m = m + 1
    
probeVector = [ int(x) for x in probeVector ] # make integers
probeNum = 0 # set probe counter

# function to give a isolated probe trial
def GiveIsolate():
    
    global probeNum
    
    trialTimer = core.CountdownTimer(preStimDur)
    
    #get parameters
    thisCond = probeMatrix['probeCondition'][probeNum]
    thisHemi = probeMatrix['probeHemi'][probeNum]
    thisEccent = probeMatrix['probeEccent'][probeNum]
    targetLet = probeMatrix['probeLetter'][probeNum]
    
    target.pos = [thisHemi*thisEccent,0]
    
    # set probe text
    target.setText(targetLet)
    
        
    if thisCond == 'Vertical':
        target.flipVert = False
    if thisCond == 'Inverted':
        target.flipVert = True
        
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
    
    ## Response 
    
    shuffle(shuffledPositions)
    
    # set positions
    respCircle1.pos = respPositions[shuffledPositions[0]]
    resp1.pos = respPositions[shuffledPositions[0]]
        
    respCircle2.pos = respPositions[shuffledPositions[1]]
    resp2.pos = respPositions[shuffledPositions[1]]
    
    respCircle3.pos = respPositions[shuffledPositions[2]]
    resp3.pos = respPositions[shuffledPositions[2]]
    
    respCircle4.pos = respPositions[shuffledPositions[3]]
    resp4.pos = respPositions[shuffledPositions[3]]
    
    respCircle5.pos = respPositions[shuffledPositions[4]]
    resp5.pos = respPositions[shuffledPositions[4]]
    
    respCircle6.pos = respPositions[shuffledPositions[5]]
    resp6.pos = respPositions[shuffledPositions[5]]
    
    respCircle7.pos = respPositions[shuffledPositions[6]]
    resp7.pos = respPositions[shuffledPositions[6]]
    
    respCircle8.pos = respPositions[shuffledPositions[7]]
    resp8.pos = respPositions[shuffledPositions[7]]
    
        # set conditions
    if thisCond == 'Vertical':
        resp1.flipVert = False
        resp2.flipVert = False
        resp3.flipVert = False
        resp4.flipVert = False
        resp5.flipVert = False
        resp6.flipVert = False
        resp7.flipVert = False
        resp8.flipVert = False
     
    if thisCond == 'Inverted':
        resp1.flipVert = True
        resp2.flipVert = True
        resp3.flipVert = True
        resp4.flipVert = True
        resp5.flipVert = True
        resp6.flipVert = True
        resp7.flipVert = True
        resp8.flipVert = True
    
    thisResp=None
    responseLet = None
    core.wait(0.5)
    
    mouse = event.Mouse(visible = False, win = win)
    mouse.setPos([0,0])
    cursor.pos=mouse.getPos()
    
    while responseLet == None:
        
        respCircle1.draw()
        resp1.draw()
        respCircle2.draw()
        resp2.draw()
        respCircle3.draw()
        resp3.draw()
        respCircle4.draw()
        resp4.draw()
        respCircle5.draw()
        resp5.draw()
        respCircle6.draw()
        resp6.draw()
        respCircle7.draw()
        resp7.draw()
        respCircle8.draw()
        resp8.draw()
        
        fixation0.draw()
        
        cursor.pos=mouse.getPos()
        cursor.draw()
        win.flip()
        
        if event.getKeys(keyList=['escape', 'q']):
            win.close()
            core.quit()
        
        if mouse.isPressedIn(respCircle1):
            responseLet = letters[0]
        
        if mouse.isPressedIn(respCircle2):
            responseLet = letters[1]
        
        if mouse.isPressedIn(respCircle3):
            responseLet = letters[2]
        
        if mouse.isPressedIn(respCircle4):
            responseLet = letters[3]
        
        if mouse.isPressedIn(respCircle5):
            responseLet = letters[4]
        
        if mouse.isPressedIn(respCircle6):
            responseLet = letters[5]
        
        if mouse.isPressedIn(respCircle7):
            responseLet = letters[6]
        
        if mouse.isPressedIn(respCircle8):
            responseLet = letters[7]
    
    # while ends
    event.clearEvents()
    
    fixation.draw()
    win.flip()
    
    if responseLet == targetLet:
        thisResp = 1
    else:
        thisResp = 0
    
    probeMatrix.loc[probeNum, 'resp'] = responseLet
    probeMatrix.loc[probeNum, 'correct'] = thisResp
    
    probeNum += 1

## Breaks set up - currently 9 breaks

# number of trials before each break
breakTrialInterval = 60 #must divide into the total trials

if expInfo['Practice?'] == True:
    breakTrialArray = [100,100,100] # placeholder (unused for practice)
else:
    breakTrialArray = np.linspace(breakTrialInterval,totalTrials-breakTrialInterval,int(totalTrials/breakTrialInterval)-1)
    breakTrialArray = [ int(x) for x in breakTrialArray ] 

def GiveBreak():
    
    breakTxt1.draw()
    breakTxt2.draw()
    fixation.draw()
    win.flip()
    
    mouse = event.Mouse(visible = False, win = win)
    buttons = mouse.getPressed()

    while buttons[0] == 0:
        if event.getKeys(keyList=['escape', 'q']):
            win.close()
            core.quit()
        buttons = mouse.getPressed()
        if buttons [0] > 0:
            break
    
    fixation0.draw()
    win.flip()
    core.wait(1)
    
    fixation.draw()
    win.flip()
    core.wait(.5)


## QUEST PARAMETERS
nTrials = stairTrials
priorMean = .5
priorSD = .3
pThreshold = .82 
beta = 3.5
delta = .02
gamma = .125

#make staircases
stairs = []

# vertical letter stairs
V_LPstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Vertical', 'Hemifield': -1, 'Eccentricity' : 6})
stairs.append(V_LPstair)

V_RPstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Vertical', 'Hemifield':1, 'Eccentricity' : 6})
stairs.append(V_RPstair)

V_LFstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Vertical', 'Hemifield': -1, 'Eccentricity' : 4})
stairs.append(V_LFstair)

V_RFstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Vertical', 'Hemifield':1, 'Eccentricity' : 4})
stairs.append(V_RFstair)

V_RNstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Vertical', 'Hemifield': 1, 'Eccentricity' : 2})
stairs.append(V_RNstair)

V_LNstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Vertical', 'Hemifield': -1, 'Eccentricity' : 2})
stairs.append(V_LNstair)

# inverted letter stairs
I_LPstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Inverted', 'Hemifield': -1, 'Eccentricity' : 6})
stairs.append(I_LPstair)

I_RPstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Inverted', 'Hemifield':1, 'Eccentricity' : 6})
stairs.append(I_RPstair)

I_LFstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Inverted', 'Hemifield': -1, 'Eccentricity' : 4})
stairs.append(I_LFstair)

I_RFstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Inverted', 'Hemifield':1, 'Eccentricity' : 4})
stairs.append(I_RFstair)

I_RNstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Inverted', 'Hemifield': 1, 'Eccentricity' : 2})
stairs.append(I_RNstair)

I_LNstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Inverted', 'Hemifield': -1, 'Eccentricity' : 2})
stairs.append(I_LNstair)

# make fixations
fixation = visual.Circle(win, fillColor=[-1,-1,-1], lineColor=[-1,-1,-1], pos=(0, 0), colorSpace='rgb', radius=0.10)
fixation_dot = visual.Circle(win,fillColor=[-0.1,-0.1,-0.1], lineColor=[-1,-1,-1], pos=(0, 0), colorSpace='rgb', radius=0.05)

fixation0 = visual.Circle(win, fillColor=[-0.2,-0.2,-0.2], lineColor=[-0.5,-0.5,-0.5], pos=(0, 0) , colorSpace='rgb', radius=0.15)

# break text
breakTxt1 = visual.TextStim(win, pos=[0,+2], height=1.5, text='Take a break!')
breakTxt2 = visual.TextStim(win, pos=[0,-2], height=.5, text='Look at the circle and press any key to continue')

# give intructions

instructionsText = visual.TextStim(
    win=win,
    font='Arial',
    pos=(0.0, 0.0),
    height=0.8,
    wrapWidth = 24
    )
instructionsText.setText(
    'In this task, sets of three letters, and occationally a single letter, will briefly appear on the screen.\n\n'
    'After each trial, you are to report the center or single letter by selecting it with the mouse.\n\n'
    'The possible letter choices are:\n'
    '\n\n'
    'While viewing these letters, you must keep your gaze fixated on the dot in the center of the screen.\n\n'
    'It is important to respond as accurately as possible, not as fast as possible.\n\n'
    'Remember to look back to the fixation point as you respond.\n\n'
    'Click the mouse to begin the experiment.'
    )
# stimuli examples
modInstructionsText = visual.TextStim(
    win=win,
    font='Arial',
    pos=(-7.2, 1.0),
    height=1,
    wrapWidth = 24,
    flipVert = True
    )
modInstructionsText.setText(
    "  ".join(letters)
    )
modInstructionsText2 = visual.TextStim(
    win=win,
    font='Arial',
    pos=(2.6, 1.05),
    height=1,
    wrapWidth = 24,
    flipVert = False
    )
modInstructionsText2.setText(
    "  ".join(letters)
    )

modInstructionsText.draw()
modInstructionsText2.draw()
instructionsText.draw()
modInstructionsText.draw()
win.flip()

mouse = event.Mouse(visible = False, win = win)
buttons = mouse.getPressed()

while buttons[0] == 0:
    if event.getKeys(keyList=['escape', 'q']):
        win.close()
        core.quit()
    buttons = mouse.getPressed()
    
    if buttons [0] > 0:
        break

## START RUN ##
critFrameDrops = 0 #set frame drop counter (for targets)
trialNum = 0 # set trial number counter

fixation0.draw()
win.flip()
core.wait(1)

fixation.draw()
fixation_dot.draw()
win.flip()
core.wait(1)

#clock
globalClock = core.Clock()

for trialn in range(nTrials):
    
    trialTimer = core.CountdownTimer(preStimDur)
    
    shuffle(stairs) 
    
    for thisStair in stairs:
        
        # check if it's time for an isolate
        if trialNum in probeVector:
            GiveIsolate()
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
        
        thisCond = thisStair.extraInfo['Condition']
        thisHemi = thisStair.extraInfo['Hemifield']
        thisEccent = thisStair.extraInfo['Eccentricity']
        
        SetupTrial(thisHemi = thisHemi, thisEccent = thisEccent, thisSpacing = thisSpacing, condition = thisCond)
        
        # pre trial timer loop
        while trialTimer.getTime() > 0:
            fixation.draw()
            fixation_dot.draw()
            win.flip()
        
        presTime = globalClock.getTime()
        
        # PRESENT TARGETS
        #fixation.autoDraw(True)
        
        for flip in range(0,tarPresentaionFlips):
            
            DrawTrial()
        
        presTimeOff = globalClock.getTime()
        
        fixation.draw()
        fixation_dot.draw()
        win.flip()
        
        GetResponse(condition = thisCond)
        
        trialNum +=1
        
        trialTimer = core.CountdownTimer(preStimDur)

# check if it's time for an isolate
if trialNum in probeVector:
    GiveIsolate()
else:
    pass

if expInfo['Practice?'] == True:
    end1 = visual.TextStim(win, pos=[0,+2], height=1, text='End of practice')
    end2 = visual.TextStim(win, pos=[0,-2], height=1, text='Do you have any questions?')
else:
    end1 = visual.TextStim(win, pos=[0,+2], height=1.5, text='All done')
    end2 = visual.TextStim(win, pos=[0,-2], height=1.5, text='Thank you!')

end1.draw()
end2.draw()
win.flip()

# save summary data
stairSum = pd.DataFrame({'Stair':['V_LNstair', 'V_LFstair', 'V_LPstair', 'V_RNstair', 'V_RFstair', 'V_RPstair', 'I_LNstair', 'I_LFstair', 'I_LPstair', 'I_RNstair', 'I_RFstair', 'I_RPstair'],
                         'Mean':np.zeros(len(stairs)),
                         'SD':np.zeros(len(stairs)),
                         'CIwidth':np.zeros(len(stairs))})

stairSum=stairSum.reindex(['Stair','Mean','SD','CIwidth'], axis=1)

idx = 0

# re sort stairs
stairs.sort(key = lambda staircase: staircase.extraInfo['Eccentricity'], reverse = False)
stairs.sort(key = lambda staircase: staircase.extraInfo['Hemifield'], reverse = False)
stairs.sort(key = lambda staircase: staircase.extraInfo['Condition'], reverse = True) # reversed!

# fill summary
for stair in stairs:
    
    stairSum.iloc[idx,1] = stair.mean()
    stairSum.iloc[idx,2] = stair.sd()
    stairSum.iloc[idx,3] = stair.confInterval(getDifference=True)
    
    idx = idx + 1
# save summary
if expInfo['Practice?'] == False:
    stairSum.to_csv(path_or_buf = fileName+'_SUMMARY.csv', index = False)

# save probe dataFile
if expInfo['Practice?'] == False:
    probeMatrix.to_csv(path_or_buf = fileName+'_Probes.csv', index = False)

# output dropped frames to console
print( "Dropped ", critFrameDrops, " critical frames...")

core.wait(2)

win.close()
core.quit()
