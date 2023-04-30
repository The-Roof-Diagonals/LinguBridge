import whisper
import os

def transcribe_audio(filename):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    print(result["text"])
    return result["text"]
