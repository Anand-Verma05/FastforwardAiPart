from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

path = "downloads\how to stay happy in every situation ｜ English story to learn ｜ English story with subtitles.wav_chunk_0.wav"  # use the actual chunk file that failed
print(os.path.getsize(path)/1024/1024, "MB")

with open(path, "rb") as f:
    r = client.audio.transcriptions.create(
        file=(os.path.basename(path), f.read()),
        model="whisper-large-v3-turbo",
        response_format="json"
    )
print(r.text)