# Psychopy version of a change localization VWM task
# Used for CRD_INDIV
# Currently just supports 6 locations (SS 6)
# kpw Feb 2022

# Load packages
from psychopy import core, visual, gui, data, event, monitors
import numpy as np
import pandas as pd
import math
from numpy.random import shuffle, choice

# Experiment info
expInfo = {'Subject':'###',
                    'Practice?':True}
expInfo['dateStr'] = data.getDateStr()  # add the current time

# Present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='VWM_change_location', fixed=['dateStr'])

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
    
    # If not practice, start a data file
    if expInfo['Practice?'] == False:
        fileName = expInfo['Subject'] + '_VWM' + expInfo['dateStr']
        ntrials = 96

    else:
        ntrials = 12
else:
    core.quit()  # the user hit cancel so exit

# Parameters
# Current colors (in percentage values)
colors1 = [[0.9236, 0.57265, 0.5443], [0.74389, 0.6642, 0.38753], [0.43881, 0.73438, 0.5203], [0.17659, 0.74133, 0.8008], [0.52024, 0.68075, 0.94849], [0.85156, 0.58299, 0.81817], [0.31186, 0.71945, 0.90645], [0.71083, 0.63052, 0.91575], [0.92412, 0.55933, 0.68284], [0.85801, 0.61436, 0.43585], [0.59956, 0.70653, 0.41896], [0.27276, 0.74608, 0.65991]]
colors2 = [[0.31186, 0.71945, 0.90645], [0.71083, 0.63052, 0.91575], [0.92412, 0.55933, 0.68284], [0.85801, 0.61436, 0.43585], [0.59956, 0.70653, 0.41896], [0.27276, 0.74608, 0.65991], [0.9236, 0.57265, 0.5443], [0.74389, 0.6642, 0.38753], [0.43881, 0.73438, 0.5203], [0.17659, 0.74133, 0.8008], [0.52024, 0.68075, 0.94849], [0.85156, 0.58299, 0.81817]]
colors = colors1 + colors2 # actual list of 24 colors

#timing  
ITIDuration = 1 #seconds
rememberDuration = .2
retentionDuration = .9

# in flips
frameDur = frameRate[0]
ITIFlips = int(round(ITIDuration/frameDur*1000))
stimFlips = int(round(rememberDuration/frameDur*1000))
retentionFlips = int(round(retentionDuration/frameDur*1000))

#trial types (n = trpercond x targ x dist) 
chLocs = [1,2,3,4,5,6]
colorPicks = [0,1,2,3,4,5] #6,7,8,9,10,11]
colorLists = [1,2]

## Make trial list
trialList = []
for t in list(range(0,ntrials)):

    # choose change location
    chLoc = choice(chLocs, size = 1)

    # choose colors
    theseColorPicks = choice(colorPicks, size = 6, replace = False) # the set of 12
    theseColorSets = choice(colorLists, size = 6, replace = True) # for deciding which set

    theseActualColors = [] # the actual colors used
    for c in list(range(0,len(theseColorPicks))):

        # get first color
        if theseColorSets[c] == 2: 
            theseActualColors.append(colors1[theseColorPicks[c]+6])
        else:
            theseActualColors.append(colors1[theseColorPicks[c]])

        # get 1 change color for the change location
        if chLoc == c+1:
            if theseColorSets[c] == 2: 
                chColor = colors2[theseColorPicks[c] + 6]
            else:
                chColor = colors2[theseColorPicks[c]]
        
    # add info to trial list
    trialList.append({
        'Subject'       : expInfo['Subject'],
        'TrialNumber'   : t,
        'ChangeLocation': chLoc,
        'Loc1Color'     : theseActualColors[0],
        'Loc2Color'     : theseActualColors[1],
        'Loc3Color'     : theseActualColors[2],
        'Loc4Color'     : theseActualColors[3],
        'Loc5Color'     : theseActualColors[4],
        'Loc6Color'     : theseActualColors[5],
        'ChLocColor'    : chColor,
        'Response'      : 0,
        'Accuracy'      : 0,
        'OnsetTime'     : 0,
        'OffsetTime'    : 0,
        'ResponseTime'  : 0,
        'FrameDrop'     : 0
        })

# end trial list loop

## Make stimuli 

fixation = visual.TextStim(
    win=win,
    font='Arial',
    pos=(0.0, 0.0),
    height=.5,
    text = '+'
    )

# mouse?
cursor = visual.Circle(win,radius=0.1,lineColor=[-.5,-.5,-.5],fillColor=[-.4,-.4,-.4],pos=(0, 0))

#circle stimuli
stimRect = .7 # Size of circle stimuli
sizeCircle = 3 # radius of the circle that 

# calculate locations
circleRads = (360/6)*math.pi/180

circlePosisions = []
for cir in list(range(1,len(chLocs)+1)):
    circleDist = circleRads*(cir-6)
    circleX = sizeCircle*math.sin(circleDist)
    circleY = sizeCircle*math.cos(circleDist)
    
    circlePosisions.append([circleX,circleY])

# Locations are like this...
#       6
#   5       1
#   4       2
#       3
circle1 = visual.Circle(
    win=win,
    radius=.5,
    pos=circlePosisions[0],
    fillColor = 1
    )

circle2 = visual.Circle(
    win=win,
    radius=.5,
    pos=circlePosisions[1],
    fillColor = 1
    )

circle3 = visual.Circle(
    win=win,
    radius=.5,
    pos=circlePosisions[2],
    fillColor = 1
    )

circle4 = visual.Circle(
    win=win,
    radius=.5,
    pos=circlePosisions[3],
    fillColor = 1
    )

circle5 = visual.Circle(
    win=win,
    radius=.5,
    pos=circlePosisions[4],
    fillColor = 1
    )

circle6 = visual.Circle(
    win=win,
    radius=.5,
    pos=circlePosisions[5],
    fillColor = 1
    )

## Give instructions

instructionsText = visual.TextStim(
    win=win,
    font='Arial',
    pos=(0.0, 0.0),
    height=0.8,
    wrapWidth = 24)
    
instructionsText.setText(
    'In this task, on each trial you will be briefly shown 6 colored circles. \n\n'
    'Try and remember the color of each circle. \n\n' 
    'The circles will then reappear with one circle having changed color. \n\n' 
    'Click on the circle that changed. \n\n' 
    'Click to continue \n\n'
    )

instructionsText.draw()
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

if expInfo['Practice?'] == True:
    instructionsText.setText('Any questions? \n\n'
        'Click to start the practice')
else:
    instructionsText.setText('Any questions? \n\n'
        'Click to start the experiment')

instructionsText.draw()
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

win.flip()

# start writing file if needed
if expInfo['Practice?'] == False:
    headerTrial = trialList[0]
    header = list(headerTrial.keys())
    header.append('\n')
    header = ','.join(header)
    
    dataFile = open(fileName+'.csv', 'w')
    dataFile.write(header)

globalClock = core.Clock()

## Start task
for thisTrial in trialList:

    for flip in range(0,ITIFlips-1):
        fixation.draw()
        win.flip()

    # Set colors
    circle1.fillColor = thisTrial['Loc1Color']
    circle2.fillColor = thisTrial['Loc2Color']
    circle3.fillColor = thisTrial['Loc3Color']
    circle4.fillColor = thisTrial['Loc4Color']
    circle5.fillColor = thisTrial['Loc5Color']
    circle6.fillColor = thisTrial['Loc6Color']

    circle1.draw()
    circle2.draw()
    circle3.draw()
    circle4.draw()
    circle5.draw()
    circle6.draw()
    fixation.draw()
    win.flip()

    thisTrial['OnsetTime'] = globalClock.getTime()

    # present memory array
    for flip in range(0,stimFlips-1):
        circle1.draw()
        circle2.draw()
        circle3.draw()
        circle4.draw()
        circle5.draw()
        circle6.draw()
        fixation.draw()
        win.flip()

    # retention interval
    fixation.draw()
    win.flip()

    thisTrial['OffsetTime'] = globalClock.getTime()

    # check frame drop
    if thisTrial['OffsetTime'] - thisTrial['OnsetTime'] > rememberDuration + frameDur/2:
        thisTrial['FrameDrop'] = 1

    for flip in range(0,retentionFlips):
        fixation.draw()
        win.flip()

    ## Response

    # change location color
    thisChLoc = thisTrial['ChangeLocation']

    if thisChLoc == 1: circle1.fillColor = thisTrial['ChLocColor']
    if thisChLoc == 2: circle2.fillColor = thisTrial['ChLocColor']
    if thisChLoc == 3: circle3.fillColor = thisTrial['ChLocColor']
    if thisChLoc == 4: circle4.fillColor = thisTrial['ChLocColor']
    if thisChLoc == 5: circle5.fillColor = thisTrial['ChLocColor']
    if thisChLoc == 6: circle6.fillColor = thisTrial['ChLocColor']

    # start
    mouse = event.Mouse(visible = False, win = win)
    mouse.setPos([0,0])
    cursor.pos=mouse.getPos()

    while thisTrial['Response'] == 0:

        # draw
        circle1.draw()
        circle2.draw()
        circle3.draw()
        circle4.draw()
        circle5.draw()
        circle6.draw()
        fixation.draw()

        cursor.pos=mouse.getPos()
        cursor.draw()

        win.flip()

        # check responses
        if event.getKeys(keyList=['escape', 'q']):
            win.close()
            core.quit()
        
        if mouse.isPressedIn(circle1):
            thisTrial['Response'] = 1
        
        if mouse.isPressedIn(circle2):
            thisTrial['Response'] = 2
        
        if mouse.isPressedIn(circle3):
            thisTrial['Response'] = 3
        
        if mouse.isPressedIn(circle4):
            thisTrial['Response'] = 4
        
        if mouse.isPressedIn(circle5):
            thisTrial['Response'] = 5
        
        if mouse.isPressedIn(circle6):
            thisTrial['Response'] = 6

    # while ends
    
    thisTrial['ResponseTime']  = globalClock.getTime() # get response time
    event.clearEvents()
    
    fixation.draw()
    win.flip()
    
    if thisTrial['Response'] == thisChLoc:
        thisTrial['Accuracy'] = 1
    else:
        thisTrial['Accuracy'] = 0

    ## Write data ##
    if expInfo['Practice?'] == False:
        row = [str(val) for val in list(thisTrial.values())]
        row.append('\n')
        row = ','.join(row)
        dataFile.write(row)


# END
if expInfo['Practice?'] == True:
    instructionsText.setText(
    'End of practice\n\n'
    'Any questions?'
    )
    
    instructionsText.draw()
    win.flip()
    core.wait(5)
    core.quit()
    win.close()

else:
    instructionsText.setText(
    'All done\n\n'
    'Thank you!'
    )
        

    instructionsText.draw()
    win.flip()
    dataFile.close()

    core.wait(5)
    core.quit()
    win.close()

