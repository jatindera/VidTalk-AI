import subprocess
import shutil
import platform

def get_ffmpeg_command():
    if platform.system() == "Windows":
        print("Windows detected")
        return r"C:\\jatinder\\ffmpeg\bin\\ffmpeg.exe"  # Change this to your actual Windows path
    else:
        return "ffmpeg"  # On Linux, it's assumed to be installed and in PATH

def convert_webm_to_mp3(input_file, output_file, bitrate="128k"):
    ffmpeg = get_ffmpeg_command()
    if shutil.which(ffmpeg) is None:
        print("❌ ffmpeg not found. Please install it or check your PATH.")
        return

    try:
        subprocess.run(
            [ffmpeg, "-y", "-i", input_file, "-vn", "-ab", bitrate, output_file],  # <- Note "-y"
            check=True
        )
        print("✅ Conversion successful!")
    except subprocess.CalledProcessError as e:
        print("❌ Error during conversion:", e)


# Example usage
convert_webm_to_mp3("aliens2.mp4", "aliens2.mp3")
