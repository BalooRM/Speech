import speech_recognition as sr
import numpy as np
from os import path
from pydub import AudioSegment
import re
import sys

lensegment = 30 * 1000
srcstart = 0
srcend = 0
segstart = 0
segend = 0

lstext = ['mp3', 'm4a', 'wav']
myargs = sys.argv    # read command line args
if len(myargs) < 2:  # if there are not enough args, print usage and exit
    print("ERROR: not enough parameters.\n")
    sys.exit()

src = myargs[1] # arg = filename
ext = src[-3:]
#print(ext)

if not ext.lower() in lstext:
    print("ERROR: Unrecognized audio file")
    sys.exit()

# read audio from file with extension as format
sound = AudioSegment.from_file(src, format=ext.lower())

srcend = len(sound)
print("length =", str(srcend))

#srcend = 6.25 * 60 * 1000

numsegments = int(np.ceil((srcend - srcstart) / lensegment))
print("#segments =", str(numsegments))

audiofile = []
time = []
for i in range(0, numsegments):
    segstart = i * lensegment
    segend = min((i + 1) * lensegment, srcend)
    time.append(str(segstart) + "-" + str(segend))
    print("segment", str(i), ":", time[i])
    segment = sound[segstart:segend]
    audiofile.append("segment_" + str(i).zfill(4) + ".wav")
    #print(audiofile)
    segment.export(audiofile[i], format="wav") 
    
print("converted audio input to wav segments")

# use the audio file as the audio source                                        
r = sr.Recognizer()
for i in range(0, numsegments):
    print(audiofile[i], "\n[", time[i], "]", sep="")
    try:
        with sr.AudioFile(audiofile[i]) as source:
            audio = r.record(source)  # read the entire audio file
            print(r.recognize_google(audio))
    except:
        print("Error processing segment")
        
        #print(e)
