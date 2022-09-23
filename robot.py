import gtts
from playsound import playsound

tts = gtts.gTTS("Hallo, hoe gaan dit", lang="af")
tts.save("hola.mp3")
playsound("hola.mp3")


