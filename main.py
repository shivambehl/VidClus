import sys
import os
import re
import time
import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def video_to_audio(fileName):
   try:
       file, extension = os.path.splitext(fileName)
       # file = pipes.quote(file)
       video_wav = 'ffmpeg -i ' + file + extension + ' ' + file + '.wav'
       audio = 'lame ' + file + '.wav ' + file + '.mp3'
       os.system(video_wav)
       os.system(audio)
       print("Sucessfully converted ", fileName, " into audio!")
   except OSError as err:
       print(err.reason)
       exit(1)


def audio_to_text(fileName):
   r = sr.Recognizer()
   file = sr.AudioFile(fileName)
   with file as source:
       audio = r.record(source,  duration=100)
   text = r.recognize_google(audio)
   print("Sucessfully converted ", fileName, " into text!")
   return text


def get_sentiment(text):
   analyzer = SentimentIntensityAnalyzer()
   vs = analyzer.polarity_scores(text)
   if vs['compound'] > 0.55:
       return 1
   elif vs['compound'] < 0.55:
       return -1
   else:
       return 0


def main():
   if len(sys.argv) < 1 or len(sys.argv) > 2:
       print('Wrong number of args')
   else:
       filePath = sys.argv[1]
       try:
           if os.path.exists(filePath):
               print('File Found!')
       except OSError as err:
           print(err.reason)
           exit(1)

       video_to_audio(filePath)
       file, extension = os.path.splitext(filePath)
       audio_file = file + '.wav'
       text = audio_to_text(audio_file)
       print(text)
       print("Sentiment Score of text is ", get_sentiment(text))
       time.sleep(1)


if __name__ == '__main__':
   main()
