import whisper
import os

WHISPER_MODEL=os.getenv("WHISPER_MODEL","small")


_model=None

def load_model():

    global _model

    if _model is None:
        print("model loading")
        _model=whisper.load_model(WHISPER_MODEL)
        print("whisper loaded succsesfully")

    return _model

def transcribe_chunk(chunk_path:str,translate :bool=False)->str:
    model=load_model()
    task="translate" if translate else "transcribe"
    result=model.transcribe(chunk_path,task=task)

    return result['text']

def transcribe_all(chunks:list,translate : bool=False)->str:
    full_transcript=""

    for i,chunk in enumerate(chunks):
        print(f"transcribing {i+1}th chunk")
        text=transcribe_chunk(chunk,translate=translate)

        full_transcript=text + " "
    
    return full_transcript
    
    print("Transcription done")

