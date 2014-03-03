#!/usr/bin/python
import wx
import Image
import time
import os
from espeak import espeak
espeak.set_parameter(espeak.Parameter.Rate, 130)  # 110 is kinda sloooow, 220 is very fast.

os.environ['DISPLAY'] = ':0'

fname='/tmp/gfi_box.png'

def getImage(cntY=0):  # startX and startY are ints for what line we are on.
        print "Running getImageCompare()"
        t = wx.App() # required, unused
        screen = wx.ScreenDC()
        bmp = wx.EmptyBitmap(160, 25)

        #abStartX=1050  # initial start X coordinate
        abStartY=164   # initial start Y coordinate
        ycoord = abStartY+(25*cntY) # move down per iteration of cntY
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, 160, 25, screen, 1050, ycoord) # get only the area we need
        del mem # Release image

        # save to file - don't like this but other options are Windows only
        bmp.SaveFile(fname, wx.BITMAP_TYPE_PNG)
        return True

def getImageCompare(rows=0):
        getImage(rows)
        im = Image.open(fname)
        sample = im.getcolors()  # -> (count,(R,G,B))

        for i in sample:
                r,g,b = i[1]
                if r==255 and g==0 and b==0: # if all red but not green or blue
                        print "getImageCompare returned True"
                        return True
        print "getImageCompare returned False"
        return False

def playMessage(text="",delay=5):
        print "Playing message"
        espeak.synth(text)
        time.sleep(delay)



def checkForRed(rows):
        # run getImageCompare 'rows' times to find count of servers that are offline
        # breaks and returns count at first non-offline server
        print "start checkForRed(%s)" % rows
        cnt=0
        for i in range(0,(rows-1)):
                print "starting loop at %s position" % i
                t = getImageCompare(i)
                if t == True:
                        cnt+=1
                else:
                        break; # first time we see an online server we break as they are _always_ on the top
        print "finished checkForRed(%s), returned %s" % (rows, cnt)
        return cnt

# Text-to-Speech bank, change text to suit here
tts_warning = "Warning"
tts_offlineserver_single = "offline server has been detected"
tts_offlineserver_multiple = "offline servers have been detected"
tts_stilloffline_single = "server still offline"
tts_stilloffline_multiple = "servers still offline"
tts_nooffline = "All servers are online"
tts_num = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
tts_morethanten = "More than ten"

counter=0
sleeptimer=60
checkRowCount=20
history=0

while True:
        print "While start"
        #if getImageCompare() == True:
        t = checkForRed(checkRowCount)
        if t>0: # at least one server is offline
                counter+=1

                # first, see if we've already mentioned this event
                # check var to see if last mentioned value is same as current value

                if t == history:
                        # var is the same, only mention every second time
                        if counter%2==0:
                                playMessage(tts_num[(t-1)],0)
                                if t>1:
                                        playMessage(tts_stilloffline_multiple,4)
                                else:
                                        playMessage(tts_stilloffline_single,4)
                        # else don't play
                else:
                        # t is different from history, update history to equal t
                        history = t
                        # now play the alert for however many servers are offline
                        if t<=10:
                                playMessage(tts_warning,1)
                                playMessage(tts_num[(t-1)],0)
                                if t>1:
                                        playMessage(tts_offlineserver_multiple,4)
                                else:
                                        playMessage(tts_offlineserver_single,4)
                        else:
                                # more than ten servers are offline
                                playMessage(tts_warning,1)
                                playMessage(tts_morethanten,2)
                                playMessage(tts_offlineserver_multiple,4)
                sleeptimer=300 # five minutes
        else: # t = 0, no servers offline
                if counter>0: # play message first time we have zero
                        #playMessage(tts_nooffline,4) # uncomment out to play this message
                        # above line only plays the first time we go from an offline event to no-offline (when uncommented)
                        sleeptimer = 60
                        counter = 0
        print "Beginning sleep for %s seconds" % sleeptimer
        time.sleep(sleeptimer)
