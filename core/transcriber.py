import whisper
import os

WHISPER_MODEL=os.getenv("WHISPER_MODEL","small")


_modle=None

def load_model():

    global _model

    if _model is None:
        print("model loading")
        _model=whisper.load_model(WHISPER_MODEL)
        print("whisper loaded succsesfully")

    return _model

def transcribe_chunk(chunk_path):
        

