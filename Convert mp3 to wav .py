from pydub import AudioSegment

input_file = "input.mp3"
output_file = "output.wav"

sound = AudioSegment.from_mp3(input_file)

# Export as WAV
sound.export(output_file, format="wav")
