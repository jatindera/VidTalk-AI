import subprocess
import shutil
import platform
import os
import math
from pydub import AudioSegment
from pydub import utils
import os

# Set ffmpeg and ffprobe paths
AudioSegment.converter = r"C:\\jatinder\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\\jatinder\\ffmpeg\\bin\\ffprobe.exe"

# Monkey-patch the ffprobe finder to use your custom path
utils.get_prober_name = lambda: AudioSegment.ffprobe

MAX_SIZE_MB = 25  # OpenAI Whisper limit


def get_ffmpeg_command():
    if platform.system() == "Windows":
        print("Windows detected")
        return r"C:\\jatinder\\ffmpeg\bin\\ffmpeg.exe"
    else:
        return "ffmpeg"

def convert_mp4_to_mp3(input_file, output_file, bitrate="64k"):
    ffmpeg = get_ffmpeg_command()
    if shutil.which(ffmpeg) is None:
        print("❌ ffmpeg not found. Please install it or check your PATH.")
        return False

    try:
        subprocess.run(
            [ffmpeg, "-y", "-i", input_file, "-vn", "-ab", bitrate, output_file],
            check=True
        )
        print("✅ MP3 conversion successful!")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Error during conversion:", e)
        return False

def split_mp3_if_needed(mp3_path, chunk_dir="chunks", max_size_mb=MAX_SIZE_MB):
    size_mb = os.path.getsize(mp3_path) / (1024 * 1024)

    if size_mb <= max_size_mb:
        print(f"✅ File is {size_mb:.2f} MB — within limit. No splitting needed.")
        return [mp3_path]

    print(f"⚠️ File is {size_mb:.2f} MB — splitting into chunks...")

    # Now try loading a known .mp3 file
    print("Loading MP3...")
    audio = AudioSegment.from_mp3(mp3_path)
    print("✅ MP3 loaded successfully!")

    os.makedirs(chunk_dir, exist_ok=True)

    # Estimate total number of chunks
    total_chunks = math.ceil(size_mb / max_size_mb)

    # Calculate duration per chunk
    duration_per_chunk_ms = len(audio) / total_chunks

    output_files = []
    for i in range(total_chunks):
        start = int(i * duration_per_chunk_ms)
        end = int((i + 1) * duration_per_chunk_ms)
        chunk = audio[start:end]
        chunk_filename = os.path.join(chunk_dir, f"chunk_{i + 1}.mp3")
        chunk.export(chunk_filename, format="mp3", bitrate="64k")
        output_files.append(chunk_filename)
        print(f"✅ Created chunk: {chunk_filename}")

    return output_files

# Example usage
input_video = "alien-podcast-long.mp4"
output_mp3 = "alien-podcast-long.mp3"

if convert_mp4_to_mp3(input_video, output_mp3):
    chunks = split_mp3_if_needed(output_mp3)
    print(f"🎧 Ready for transcription: {chunks}")
