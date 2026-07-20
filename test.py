from utils.audio_processor import process_input
from core.transcriber import transcribe_all

source="https://youtu.be/9LfJq4xXifg?si=qVmC9683qN8CrNWs"

chunks=process_input(source)

print(transcribe_all(chunks))