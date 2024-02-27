from gtts import gTTS
import os
from playsound import playsound

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    filename = "/mnt/data/speech.mp3"
    tts.save(filename)
    playsound(filename)
    #return filename

# Example usage

