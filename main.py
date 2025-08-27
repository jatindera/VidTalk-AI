from dotenv import load_dotenv
import openai

load_dotenv()

audio_file = open("aliens.mp3", "rb")
transcript = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
# Save transcript to a text file
with open("aliens_transcript.txt", "w", encoding="utf-8") as f:
    f.write(transcript.text)

print("Transcript saved to aliens_transcript.txt")
