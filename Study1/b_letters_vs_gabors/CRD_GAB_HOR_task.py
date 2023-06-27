## Experiment code for study 1b of " " 
# Crowding for letters vs Gabor patches

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
dlg = gui.DlgFromDict(expInfo, title='CRD_GAB_HOR', fixed=['dateStr'])
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
    
    # if not practice, start data file
    if expInfo['Practice?'] == False:
        fileName = expInfo['Subject'] + '_GAB_HOR' + expInfo['dateStr']
        dataFile = open(fileName+'.csv', 'w')  
        dataFile.write('Condition,Hemifield,Eccentricity,Spacing,Correct,Response,TargetStim,RightStim,LeftStim,TargetOnset,TargetOffset,ResponseTime,RT,FrameDropped\n')
    
else:
    core.quit()  # the user hit cancel so exit

if expInfo['Practice?'] == True:
    stairTrials = 2 # for practice, will equal 24 trials total
else:
    stairTrials = 50 # number of trials per staircase
    
# letter stims
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

# gabor stims (labels)
gabors = [
    'H0'
    ,
    'H1'
    ,
    'H2'
    ,
    'H3'
    ,
    'L0'
    ,
    'L1'
    ,
    'L2'
    ,
    'L3'
    ]

stimSize = 1 # height in visual degrees

# info for gabors
orientations = [0,45,90,135]
orientationsKey = ['0','1','2','3']
orientationMap = dict(zip(orientationsKey, orientations))

sfs = [2.5,5.5]
sfsKey = ['L','H']
sfMap = dict(zip(sfsKey, sfs))

# more stim parameters
stimDur = .1 #time (s) target/flanks are on screen
preStimDur = 1 #ITI (s) after last response before next trial apears
tarPresentaionFlips = int(round(stimDur/frameRate[0]*1000))

hemifields = [-1, 1] # left or right
eccentricities = [2, 4, 6] # in visual degrees
conditions = ['Letter','Gabor'] #

# stims
letter_target = visual.TextStim(win, pos=[0,0.2],text= letters[1], height=stimSize, font="Arial", flipVert = False)
letter_rightFlank = visual.TextStim(win, pos=[0,0.2],text= letters[2], height=stimSize, font="Arial", flipVert = False)
letter_leftFlank = visual.TextStim(win, pos=[0,0.2],text= letters[3], height=stimSize, font="Arial", flipVert = False)

gabor_target = visual.GratingStim(win, tex='sin', mask='gauss', size=stimSize, sf=5, ori=0)
gabor_rightFlank = visual.GratingStim(win, tex='sin', mask='gauss', size=stimSize, sf=5, ori=0)
gabor_leftFlank = visual.GratingStim(win, tex='sin', mask='gauss', size=stimSize, sf=5, ori=0)

def SetupTrial(thisHemi, thisEccent, thisSpacing, condition):  # info supplied per trial
    
    # get positions
    tarPos = [thisHemi*thisEccent,0]
    rightPos = [thisHemi*thisEccent + thisSpacing*thisEccent, 0]
    leftPos = [thisHemi*thisEccent - thisSpacing*thisEccent, 0]
    
    # by condition
    if condition == 'Letter':
        # pick letters
        tarLet = random.choice(letters)
        rightLet = random.choice(np.setdiff1d(letters,tarLet))
        leftLet = random.choice(np.setdiff1d(letters,[tarLet, rightLet]))
        
        # set letters
        letter_target.setText(tarLet)
        letter_rightFlank.setText(rightLet)
        letter_leftFlank.setText(leftLet)
        
        # set positions
        letter_target.pos = tarPos
        letter_rightFlank.pos = rightPos
        letter_leftFlank.pos = leftPos
     
    if condition == 'Gabor':
        # pick gabors
        tarGab = random.choice(gabors)
        rightGab = random.choice(np.setdiff1d(gabors,tarGab))
        leftGab = random.choice(np.setdiff1d(gabors,[tarGab, rightGab]))
        
        # get orientation
        tarOri = orientationMap.get(tarGab[1])
        rightOri = orientationMap.get(rightGab[1])
        leftOri = orientationMap.get(leftGab[1])
        
        # set orientations
        gabor_target.ori = tarOri
        gabor_rightFlank.ori = rightOri
        gabor_leftFlank.ori = leftOri
        
        # get SFs
        tarSF = sfMap.get(tarGab[0])
        rightSF = sfMap.get(rightGab[0])
        leftSF = sfMap.get(leftGab[0])
        
        # set SFs
        gabor_target.sf = tarSF
        gabor_rightFlank.sf = rightSF
        gabor_leftFlank.sf = leftSF
        
        # set positions
        gabor_target.pos = tarPos
        gabor_rightFlank.pos = rightPos
        gabor_leftFlank.pos = leftPos
        
        # for access in response...
        SetupTrial.gabor_target = tarGab
        SetupTrial.gabor_rightFlank = rightGab
        SetupTrial.gabor_leftFlank = leftGab
    

def DrawTrial(condition): # one frame
    
    if condition == 'Letter':
        letter_target.draw()
        letter_rightFlank.draw()
        letter_leftFlank.draw()
        
    if condition == 'Gabor':
        gabor_target.draw()
        gabor_rightFlank.draw()
        gabor_leftFlank.draw()
        
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
letter_resp1 = visual.TextStim(win, pos=[0,-2],text= letters[0], height=stimSize, font="Arial", flipVert = False)
letter_resp2 = visual.TextStim(win, pos=[0,-2],text= letters[1], height=stimSize, font="Arial", flipVert = False)
letter_resp3 = visual.TextStim(win, pos=[0,-2],text= letters[2], height=stimSize, font="Arial", flipVert = False)
letter_resp4 = visual.TextStim(win, pos=[0,-2],text= letters[3], height=stimSize, font="Arial", flipVert = False)
letter_resp5 = visual.TextStim(win, pos=[0,-2],text= letters[4], height=stimSize, font="Arial", flipVert = False)
letter_resp6 = visual.TextStim(win, pos=[0,-2],text= letters[5], height=stimSize, font="Arial", flipVert = False)
letter_resp7 = visual.TextStim(win, pos=[0,-2],text= letters[6], height=stimSize, font="Arial", flipVert = False)
letter_resp8 = visual.TextStim(win, pos=[0,-2],text= letters[7], height=stimSize, font="Arial", flipVert = False)

# response gabors 
gabor_resp1 = visual.GratingStim(win, tex='sin', mask='gauss', size=stimSize, pos = [-7,1], sf= sfMap.get(gabors[0][0]), ori= orientationMap.get(gabors[0][1])) #H0
gabor_resp2 = visual.GratingStim(win, tex='sin', mask='gauss', size=stimSize, pos = [-5,1], sf= sfMap.get(gabors[1][0]), ori= orientationMap.get(gabors[1][1])) #H1
gabor_resp3 = visual.GratingStim(win, tex='sin', mask='gauss', size=stimSize, pos = [-3,1],  sf= sfMap.get(gabors[2][0]), ori= orientationMap.get(gabors[2][1])) #H2
gabor_resp4 = visual.GratingStim(win, tex='sin', mask='gauss', size=stimSize, pos = [-1,1],  sf= sfMap.get(gabors[3][0]), ori= orientationMap.get(gabors[3][1])) #H3
gabor_resp5 = visual.GratingStim(win, tex='sin', mask='gauss', size=stimSize, pos = [1,1],  sf= sfMap.get(gabors[4][0]), ori= orientationMap.get(gabors[4][1])) #L0
gabor_resp6 = visual.GratingStim(win, tex='sin', mask='gauss', size=stimSize, pos = [3,1],  sf= sfMap.get(gabors[5][0]), ori= orientationMap.get(gabors[5][1])) #L1
gabor_resp7 = visual.GratingStim(win, tex='sin', mask='gauss', size=stimSize, pos = [5,1],  sf= sfMap.get(gabors[6][0]), ori= orientationMap.get(gabors[6][1])) #L2
gabor_resp8 = visual.GratingStim(win, tex='sin', mask='gauss', size=stimSize, pos = [7,1],  sf= sfMap.get(gabors[7][0]), ori= orientationMap.get(gabors[7][1])) #L3

# instruction gabors 
gabor_inst1 = visual.GratingStim(win, tex='sin', mask='gauss',  size=stimSize, pos = [2.6,1], sf= sfMap.get(gabors[0][0]), ori= orientationMap.get(gabors[0][1])) #H0
gabor_inst2 = visual.GratingStim(win, tex='sin', mask='gauss',  size=stimSize, pos = [3.6,1], sf= sfMap.get(gabors[1][0]), ori= orientationMap.get(gabors[1][1])) #H1
gabor_inst3 = visual.GratingStim(win, tex='sin', mask='gauss',  size=stimSize, pos = [4.6,1],  sf= sfMap.get(gabors[2][0]), ori= orientationMap.get(gabors[2][1])) #H2
gabor_inst4 = visual.GratingStim(win, tex='sin', mask='gauss',  size=stimSize, pos = [5.6,1],  sf= sfMap.get(gabors[3][0]), ori= orientationMap.get(gabors[3][1])) #H3
gabor_inst5 = visual.GratingStim(win, tex='sin', mask='gauss', size=stimSize, pos = [6.6,1],  sf= sfMap.get(gabors[4][0]), ori= orientationMap.get(gabors[4][1])) #L0
gabor_inst6 = visual.GratingStim(win, tex='sin', mask='gauss',  size=stimSize, pos = [7.6,1],  sf= sfMap.get(gabors[5][0]), ori= orientationMap.get(gabors[5][1])) #L1
gabor_inst7 = visual.GratingStim(win, tex='sin', mask='gauss',  size=stimSize, pos = [8.6,1],  sf= sfMap.get(gabors[6][0]), ori= orientationMap.get(gabors[6][1])) #L2
gabor_inst8 = visual.GratingStim(win, tex='sin', mask='gauss',  size=stimSize, pos = [9.6,1],  sf= sfMap.get(gabors[7][0]), ori= orientationMap.get(gabors[7][1])) #L3

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
    respCircle2.pos = respPositions[shuffledPositions[1]]
    respCircle3.pos = respPositions[shuffledPositions[2]]
    respCircle4.pos = respPositions[shuffledPositions[3]]
    respCircle5.pos = respPositions[shuffledPositions[4]]
    respCircle6.pos = respPositions[shuffledPositions[5]]
    respCircle7.pos = respPositions[shuffledPositions[6]]
    respCircle8.pos = respPositions[shuffledPositions[7]]

    if condition == 'Letter':
        letter_resp1.pos = respPositions[shuffledPositions[0]]
        letter_resp2.pos = respPositions[shuffledPositions[1]]
        letter_resp3.pos = respPositions[shuffledPositions[2]]
        letter_resp4.pos = respPositions[shuffledPositions[3]]
        letter_resp5.pos = respPositions[shuffledPositions[4]]
        letter_resp6.pos = respPositions[shuffledPositions[5]]
        letter_resp7.pos = respPositions[shuffledPositions[6]]
        letter_resp8.pos = respPositions[shuffledPositions[7]]
    
    if condition == 'Gabor':
        gabor_resp1.pos = respPositions[shuffledPositions[0]]
        gabor_resp2.pos = respPositions[shuffledPositions[1]]
        gabor_resp3.pos = respPositions[shuffledPositions[2]]
        gabor_resp4.pos = respPositions[shuffledPositions[3]]
        gabor_resp5.pos = respPositions[shuffledPositions[4]]
        gabor_resp6.pos = respPositions[shuffledPositions[5]]
        gabor_resp7.pos = respPositions[shuffledPositions[6]]
        gabor_resp8.pos = respPositions[shuffledPositions[7]]
        
    thisResp=None
    responseStim = None
    RT = 0
    core.wait(0.5)
    
    mouse = event.Mouse(visible = False, win = win)
    mouse.setPos([0,0])
    cursor.pos=mouse.getPos()
    
    while responseStim == None:
        
        respCircle1.draw()
        respCircle2.draw()
        respCircle3.draw()
        respCircle4.draw()
        respCircle5.draw()
        respCircle6.draw()
        respCircle7.draw()
        respCircle8.draw()
        
        if condition == 'Letter':
            letter_resp1.draw()
            letter_resp2.draw()
            letter_resp3.draw()
            letter_resp4.draw()
            letter_resp5.draw()
            letter_resp6.draw()
            letter_resp7.draw()
            letter_resp8.draw()
        
        if condition == 'Gabor':
            gabor_resp1.draw()
            gabor_resp2.draw()
            gabor_resp3.draw()
            gabor_resp4.draw()
            gabor_resp5.draw()
            gabor_resp6.draw()
            gabor_resp7.draw()
            gabor_resp8.draw()
        
        fixation0.draw()
        
        cursor.pos=mouse.getPos()
        cursor.draw()
        win.flip()
        
        if event.getKeys(keyList=['escape', 'q']):
            win.close()
            core.quit()
        
        # if letter condition
        if condition == 'Letter':
            if mouse.isPressedIn(respCircle1):
                responseStim = letters[0]
            
            if mouse.isPressedIn(respCircle2):
                responseStim = letters[1]
            
            if mouse.isPressedIn(respCircle3):
                responseStim = letters[2]
            
            if mouse.isPressedIn(respCircle4):
                responseStim = letters[3]
            
            if mouse.isPressedIn(respCircle5):
                responseStim = letters[4]
            
            if mouse.isPressedIn(respCircle6):
                responseStim = letters[5]
            
            if mouse.isPressedIn(respCircle7):
                responseStim = letters[6]
            
            if mouse.isPressedIn(respCircle8):
                responseStim = letters[7]
        
        # if gabor
        if condition == 'Gabor':
            if mouse.isPressedIn(respCircle1):
                responseStim = gabors[0]
            
            if mouse.isPressedIn(respCircle2):
                responseStim = gabors[1]
            
            if mouse.isPressedIn(respCircle3):
                responseStim = gabors[2]
            
            if mouse.isPressedIn(respCircle4):
                responseStim = gabors[3]
            
            if mouse.isPressedIn(respCircle5):
                responseStim = gabors[4]
            
            if mouse.isPressedIn(respCircle6):
                responseStim = gabors[5]
            
            if mouse.isPressedIn(respCircle7):
                responseStim = gabors[6]
            
            if mouse.isPressedIn(respCircle8):
                responseStim = gabors[7]
        
    # while ends
    
    respTime = globalClock.getTime() # get response time
    RT = respTime - presTime # calculate reaction time
    event.clearEvents()
    
    fixation.draw()
    fixation_dot.draw()
    win.flip()
    
    if condition == 'Letter':
        
        tarStim = letter_target.text
        rightStim = letter_rightFlank.text
        leftStim = letter_leftFlank.text
    
        if responseStim == tarStim:
            thisResp = 1
        else:
            thisResp = 0
            
    if condition == 'Gabor':
        
        tarStim = SetupTrial.gabor_target
        rightStim = SetupTrial.gabor_rightFlank
        leftStim = SetupTrial.gabor_leftFlank
    
        if responseStim == tarStim:
            thisResp = 1
        else:
            thisResp = 0
    
    # because first 3 trials of each stair forced to be 50% spaced
    if trialNum < 36:
        thisStair.addData(thisResp, intensity = priorMean)
    else:
        thisStair.addData(thisResp)

    # check if frame drop
    if (presTimeOff-presTime)*1000 > 107:
        frameDrop = 1
        critFrameDrops +=1
    else:
        frameDrop = 0
    
    # write data
    if expInfo['Practice?'] == False:
        dataFile.write('%s,%s,%f,%f,%f,%s,%s,%s,%s,%f,%f,%f,%f,%f\n' %(condition, thisHemi, thisEccent, thisSpacing, thisResp, responseStim, tarStim , rightStim, leftStim, presTime, presTimeOff, respTime, RT, frameDrop))
    
# end response function

## Set up trial arrays

totalTrials = stairTrials*12 #not including probes

numProbes = 48 # two per letter*stair
# Set up isolated letter probes to gauge lapses..
# make randomized but evenly represented list of 24 letters

probeStims = letters + gabors
probeStims = np.repeat(probeStims, 3)
shuffle(probeStims)

# make randomized but evenly represented list of 24 locations
probeHemi = np.repeat(hemifields, 24)
shuffle(probeHemi)

probeEccent = np.repeat(eccentricities, 16)
shuffle(probeEccent)

probeConds = []
for stim in probeStims:
        
    if stim in letters:
        probeConds.append('Letter')
    else:
        probeConds.append('Gabor')

# df to read from/write to
probeMatrix = pd.DataFrame({'probeNum':np.arange(0, numProbes, 1),
                            'probeCondition' : probeConds,
                            'probeStim':probeStims,
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
    targetStim = probeMatrix['probeStim'][probeNum]
    
    # set
    if thisCond == 'Letter':
        letter_target.pos = [thisHemi*thisEccent,0]
        letter_target.setText(targetStim)
    if thisCond == 'Gabor':
        gabor_target.pos = [thisHemi*thisEccent,0]
        
        tarOri = orientationMap.get(targetStim[1])
        gabor_target.ori = tarOri
        
        tarSF = sfMap.get(targetStim[0])
        gabor_target.sf = tarSF
        
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

        if thisCond == 'Letter':
            letter_target.draw()
        if thisCond == 'Gabor':
            gabor_target.draw()
            
        win.flip()
    
    fixation.draw()
    fixation_dot.draw()
    win.flip()
    
    ## Response 
    shuffle(shuffledPositions)
    
    # set positions
    respCircle1.pos = respPositions[shuffledPositions[0]]
    respCircle2.pos = respPositions[shuffledPositions[1]]
    respCircle3.pos = respPositions[shuffledPositions[2]]
    respCircle4.pos = respPositions[shuffledPositions[3]]
    respCircle5.pos = respPositions[shuffledPositions[4]]
    respCircle6.pos = respPositions[shuffledPositions[5]]
    respCircle7.pos = respPositions[shuffledPositions[6]]
    respCircle8.pos = respPositions[shuffledPositions[7]]

    if thisCond == 'Letter':
        letter_resp1.pos = respPositions[shuffledPositions[0]]
        letter_resp2.pos = respPositions[shuffledPositions[1]]
        letter_resp3.pos = respPositions[shuffledPositions[2]]
        letter_resp4.pos = respPositions[shuffledPositions[3]]
        letter_resp5.pos = respPositions[shuffledPositions[4]]
        letter_resp6.pos = respPositions[shuffledPositions[5]]
        letter_resp7.pos = respPositions[shuffledPositions[6]]
        letter_resp8.pos = respPositions[shuffledPositions[7]]
    
    if thisCond == 'Gabor':
        gabor_resp1.pos = respPositions[shuffledPositions[0]]
        gabor_resp2.pos = respPositions[shuffledPositions[1]]
        gabor_resp3.pos = respPositions[shuffledPositions[2]]
        gabor_resp4.pos = respPositions[shuffledPositions[3]]
        gabor_resp5.pos = respPositions[shuffledPositions[4]]
        gabor_resp6.pos = respPositions[shuffledPositions[5]]
        gabor_resp7.pos = respPositions[shuffledPositions[6]]
        gabor_resp8.pos = respPositions[shuffledPositions[7]]
        
    thisResp=None
    responseStim = None
    core.wait(0.5)
    
    mouse = event.Mouse(visible = False, win = win)
    mouse.setPos([0,0])
    cursor.pos=mouse.getPos()
    
    while responseStim == None:
        
        respCircle1.draw()
        respCircle2.draw()
        respCircle3.draw()
        respCircle4.draw()
        respCircle5.draw()
        respCircle6.draw()
        respCircle7.draw()
        respCircle8.draw()
        
        if thisCond == 'Letter':
            letter_resp1.draw()
            letter_resp2.draw()
            letter_resp3.draw()
            letter_resp4.draw()
            letter_resp5.draw()
            letter_resp6.draw()
            letter_resp7.draw()
            letter_resp8.draw()
        
        if thisCond == 'Gabor':
            gabor_resp1.draw()
            gabor_resp2.draw()
            gabor_resp3.draw()
            gabor_resp4.draw()
            gabor_resp5.draw()
            gabor_resp6.draw()
            gabor_resp7.draw()
            gabor_resp8.draw()
        
        fixation0.draw()
        
        cursor.pos=mouse.getPos()
        cursor.draw()
        win.flip()
        
        if event.getKeys(keyList=['escape', 'q']):
            win.close()
            core.quit()
        
        # if letter condition
        if thisCond == 'Letter':
            if mouse.isPressedIn(respCircle1):
                responseStim = letters[0]
            
            if mouse.isPressedIn(respCircle2):
                responseStim = letters[1]
            
            if mouse.isPressedIn(respCircle3):
                responseStim = letters[2]
            
            if mouse.isPressedIn(respCircle4):
                responseStim = letters[3]
            
            if mouse.isPressedIn(respCircle5):
                responseStim = letters[4]
            
            if mouse.isPressedIn(respCircle6):
                responseStim = letters[5]
            
            if mouse.isPressedIn(respCircle7):
                responseStim = letters[6]
            
            if mouse.isPressedIn(respCircle8):
                responseStim = letters[7]
        
        # if gabor
        if thisCond == 'Gabor':
            if mouse.isPressedIn(respCircle1):
                responseStim = gabors[0]
            
            if mouse.isPressedIn(respCircle2):
                responseStim = gabors[1]
            
            if mouse.isPressedIn(respCircle3):
                responseStim = gabors[2]
            
            if mouse.isPressedIn(respCircle4):
                responseStim = gabors[3]
            
            if mouse.isPressedIn(respCircle5):
                responseStim = gabors[4]
            
            if mouse.isPressedIn(respCircle6):
                responseStim = gabors[5]
            
            if mouse.isPressedIn(respCircle7):
                responseStim = gabors[6]
            
            if mouse.isPressedIn(respCircle8):
                responseStim = gabors[7]
        
    # while ends
    
    event.clearEvents()
    
    fixation.draw()
    win.flip()
    
    if responseStim == targetStim:
        thisResp = 1
    else:
        thisResp = 0
    
    
    probeMatrix.loc[probeNum, 'resp'] = responseStim
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
L_LPstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Letter', 'Hemifield': -1, 'Eccentricity' : 6})
stairs.append(L_LPstair)

L_RPstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Letter', 'Hemifield':1, 'Eccentricity' : 6})
stairs.append(L_RPstair)

L_LFstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Letter', 'Hemifield': -1, 'Eccentricity' : 4})
stairs.append(L_LFstair)

L_RFstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Letter', 'Hemifield':1, 'Eccentricity' : 4})
stairs.append(L_RFstair)

L_RNstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Letter', 'Hemifield': 1, 'Eccentricity' : 2})
stairs.append(L_RNstair)

L_LNstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Letter', 'Hemifield': -1, 'Eccentricity' : 2})
stairs.append(L_LNstair)

# gabor stairs
G_LPstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Gabor', 'Hemifield': -1, 'Eccentricity' : 6})
stairs.append(G_LPstair)

G_RPstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Gabor', 'Hemifield':1, 'Eccentricity' : 6})
stairs.append(G_RPstair)

G_LFstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Gabor', 'Hemifield': -1, 'Eccentricity' : 4})
stairs.append(G_LFstair)

G_RFstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Gabor', 'Hemifield':1, 'Eccentricity' : 4})
stairs.append(G_RFstair)

G_RNstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Gabor', 'Hemifield': 1, 'Eccentricity' : 2})
stairs.append(G_RNstair)

G_LNstair = data.QuestHandler(priorMean, priorSD, pThreshold= pThreshold, nTrials= nTrials,
                           stopInterval = None, beta= beta, delta= delta, gamma=gamma, 
                           range = 1, grain = .01, minVal = 0, maxVal = 1, extraInfo={'Condition': 'Gabor', 'Hemifield': -1, 'Eccentricity' : 2})
stairs.append(G_LNstair)

# make fixations
fixation = visual.Circle(win, fillColor=[-1,-1,-1], lineColor=[-1,-1,-1], pos=(0, 0), colorSpace='rgb', radius=0.10)
fixation_dot = visual.Circle(win,fillColor=[-0.1,-0.1,-0.1], lineColor=[-1,-1,-1], pos=(0, 0), colorSpace='rgb', radius=0.05)

fixation0 = visual.Circle(win, fillColor=[-0.2,-0.2,-0.2], lineColor=[-0.5,-0.5,-0.5], pos=(0, 0) , colorSpace='rgb', radius=0.15)

# break text
breakTxt1 = visual.TextStim(win, pos=[0,+2], height=1.5, text='Take a break!')
breakTxt2 = visual.TextStim(win, pos=[0,-2], height=.5, text='Look at the circle and click the mouse to continue')

# give intructions

instructionsText = visual.TextStim(
    win=win,
    font='Arial',
    pos=(0.0, 0.0),
    height=0.8,
    wrapWidth = 24
    )
instructionsText.setText(
    'In this task, sets of three stimuli, and occationally a single stimuli, will briefly appear on the screen.\n\n'
    'After each trial, you are to report the center or single stimuli by selecting it with the mouse.\n\n'
    'The possible stimuli are these letters or gratings:\n'
    '\n\n'
    'While viewing these stimuli, you must keep your gaze fixated on the dot in the center of the screen.\n\n'
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
    flipVert = False
    )
modInstructionsText.setText(
    "  ".join(letters)
    )

# instruction gabors
gabor_inst1.draw()
gabor_inst2.draw()
gabor_inst3.draw()
gabor_inst4.draw()
gabor_inst5.draw()
gabor_inst6.draw()
gabor_inst7.draw()
gabor_inst8.draw()

instructionsText.draw()
modInstructionsText.draw() # instruction letters
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
            
            DrawTrial(condition = thisCond)
        
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

# Save summary data
stairSum = pd.DataFrame({'Stair':['L_LNstair', 'L_LFstair', 'L_LPstair', 'L_RNstair', 'L_RFstair', 'L_RPstair', 'G_LNstair', 'G_LFstair', 'G_LPstair', 'G_RNstair', 'G_RFstair', 'G_RPstair'],
                         'Mean':np.zeros(len(stairs)),
                         'SD':np.zeros(len(stairs)),
                         'CIwidth':np.zeros(len(stairs))})

stairSum=stairSum.reindex(['Stair','Mean','SD','CIwidth'], axis=1)

idx = 0

# re sort stairs
stairs.sort(key = lambda staircase: staircase.extraInfo['Eccentricity'], reverse = False)
stairs.sort(key = lambda staircase: staircase.extraInfo['Hemifield'], reverse = False)
stairs.sort(key = lambda staircase: staircase.extraInfo['Condition'], reverse = True) # reversed

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