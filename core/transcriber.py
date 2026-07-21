import os
import requests
from pydub import AudioSegment
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

# Sarvam limits
SARVAM_PIECE_SECONDS = 25
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_STT_TRANSLATE_URL = "https://api.sarvam.ai/speech-to-text-translate"
SARVAM_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v2.5")

# Initialize Groq Client for Whisper API
# We use Groq because it hosts Whisper-large-v3-turbo for free and is incredibly fast.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(GROQ_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY, timeout=120.0) if GROQ_API_KEY else None
GROQ_PIECE_SECONDS = 120  # 2 minutes
def transcribe_chunk_whisper(chunk_path: str) -> str:
    """
    Splits a large audio chunk into smaller MP3 pieces and
    sends each piece to Groq Whisper.
    """

    if not groq_client:
        raise RuntimeError("GROQ_API_KEY is not set in environment / .env")

    audio = AudioSegment.from_file(chunk_path)

    piece_ms = GROQ_PIECE_SECONDS * 1000

    full_text = ""

    total_pieces = (len(audio) + piece_ms - 1) // piece_ms

    for i, start in enumerate(range(0, len(audio), piece_ms)):

        piece = audio[start:start + piece_ms]

        piece_path = f"{chunk_path}_groq_{i}.mp3"

        # Export as compressed MP3
        piece.export(
            piece_path,
            format="mp3",
            bitrate="64k"
        )

        try:

            size_mb = os.path.getsize(piece_path) / (1024 * 1024)

            print(f" → Groq piece {i+1}/{total_pieces} ({size_mb:.2f} MB)")

            with open(piece_path, "rb") as file:

                transcription = groq_client.audio.transcriptions.create(

                    file=(os.path.basename(piece_path), file),

                    model="whisper-large-v3-turbo",

                    response_format="json",
                )

            full_text += transcription.text + " "

        finally:

            if os.path.exists(piece_path):

                os.remove(piece_path)

    return full_text.strip()

def _send_to_sarvam(piece_path: str) -> str:
    """Send one ≤30s WAV file to Sarvam and return the English transcript."""
    headers = {"api-subscription-key": SARVAM_API_KEY}

    with open(piece_path, "rb") as f:
        files = {"file": (os.path.basename(piece_path), f, "audio/wav")}
        data = {"model": SARVAM_MODEL, "with_diarization": "false"}
        response = requests.post(
            SARVAM_STT_TRANSLATE_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=120,
        )

    if not response.ok:
        print(f"\n❌ Sarvam returned {response.status_code}")
        print(f"Response body: {response.text}\n")
        response.raise_for_status()

    return response.json().get("transcript", "")

def transcribe_chunk_sarvam(chunk_path: str) -> str:
    """
    Sarvam sync API only accepts ≤30s audio. We split this chunk into
    25-second pieces, send each separately, and join the transcripts.
    """
    if not SARVAM_API_KEY:
        raise RuntimeError("SARVAM_API_KEY is not set in environment / .env")

    audio = AudioSegment.from_wav(chunk_path)
    piece_ms = SARVAM_PIECE_SECONDS * 1000

    full_text = ""
    total_pieces = (len(audio) + piece_ms - 1) // piece_ms

    for i, start in enumerate(range(0, len(audio), piece_ms)):
        piece = audio[start: start + piece_ms]
        piece_path = f"{chunk_path}_sv_{i}.wav"
        piece.export(piece_path, format="wav")

        try:
            print(f"  → Sarvam piece {i + 1}/{total_pieces} ...")
            full_text += _send_to_sarvam(piece_path) + " "
        finally:
            if os.path.exists(piece_path):
                os.remove(piece_path)

    return full_text.strip()

def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    """
    Route one chunk to Whisper (via Groq API) or Sarvam depending on language choice.
    - english  → Groq Whisper API
    - hinglish → Sarvam (translates to English while transcribing)
    """
    if language.lower() == "hinglish":
        return transcribe_chunk_sarvam(chunk_path)
    return transcribe_chunk_whisper(chunk_path)

def transcribe_all(chunks: list, language: str = "english") -> str:
    full_transcript = "" 
    engine = "Sarvam AI" if language.lower() == "hinglish" else "Groq Whisper API"
    print(f"Using {engine} for transcription.")

    for i, chunk in enumerate(chunks):  
        print(f"Transcribing chunk {i + 1}/{len(chunks)}...")
        text = transcribe_chunk(chunk, language=language)  
        full_transcript += text + " "  

    print("Transcription complete.")
    return full_transcript.strip()