# import os
# from groq import Groq
# from dotenv import load_dotenv
# import traceback
# import requests

# print(requests.get("https://api.groq.com").status_code)

# # Load variables from your .env file
# load_dotenv()

# # Retrieve the API key
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# if not GROQ_API_KEY:
#     print("❌ ERROR: GROQ_API_KEY not found in environment or .env file.")
#     exit(1)

# # Initialize the Groq client
# client = Groq(api_key=GROQ_API_KEY)

# # --- CONFIGURATION ---
# # Change this to the path of an actual short audio file on your computer (.mp3, .wav, .m4a)
# AUDIO_FILE_PATH = r"C:\Users\PUKA\Documents\fastforwardai\downloads\test.wav" 
# # ---------------------
# def test_groq_whisper(file_path):
#     print(os.path.getsize(file_path))
#     print(file_path)
#     if not os.path.exists(file_path):
#         print(f"❌ ERROR: Could not find audio file at '{file_path}'.")
#         print("Please create a short test audio file or change the AUDIO_FILE_PATH variable.")
#         return

#     print(f"🎙️ Sending '{file_path}' to Groq Whisper API...")
    
#     try:
#         # Open the audio file and send it to Groq
#         with open(file_path, "rb") as audio_file:
#             transcription = client.audio.transcriptions.create(
#             file=audio_file,
#             model="whisper-large-v3-turbo",
#             response_format="json"
#     )
        
#         print("\n✅ Transcription Successful!\n")
#         print("--- Transcript Output ---")
#         print(transcription.text)
#         print("-------------------------")
        
#     except Exception:
#         traceback.print_exc()

# if __name__ == "__main__":
#     test_groq_whisper(AUDIO_FILE_PATH)