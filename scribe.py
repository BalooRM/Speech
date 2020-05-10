import speech_recognition as sr
import numpy as np
from os import path
from pydub import AudioSegment
import sys

lensegment = 30 * 1000
srcstart = 0
srcend = 0
segstart = 0
segend = 0

# convert mp3 file to wav                                                       
sound = AudioSegment.from_mp3("transcript.mp3")
#sound = AudioSegment.from_mp3("Recording3.mp3")
srcend = len(sound)
print("length =", str(srcend))

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
    print(audiofile)
    segment.export(audiofile[i], format="wav") 
    
print("converted mp3 to wav")

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
