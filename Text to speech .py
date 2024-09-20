from gtts import gTTS
from playsound import playsound

# Set the text you want to convert to speech
text = "Hello, this is a text-to-speech conversion using gTTS."

# Convert text to speech
tts = gTTS(text=text, lang='en')

# Save the speech to a file
tts.save("output.mp3")

# Play the speech
playsound("output.mp3")
