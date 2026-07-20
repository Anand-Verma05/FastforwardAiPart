from dotenv import load_dotenv
load_dotenv()
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
source="https://youtu.be/HisYsqqszq0?si=t5zd6ZLV1szztlZ9"
language="hinglish"

chunks=process_input(source)
transcript=transcribe_all(chunks,language=language)
# print(transcribe_all(chunks))
print(transcript)