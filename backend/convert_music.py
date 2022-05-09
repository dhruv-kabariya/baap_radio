from os import path
from pydub import AudioSegment

# files                                                                         
src = "music/bollywood/Brothers Anthem.mp3"
dst = "music/bollywood/Brothers Anthem.wav"


# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")