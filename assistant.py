import os
import time
import subprocess
import webbrowser
import whisper
import sounddevice as sd
import soundfile as sf
import pvporcupine
import psutil
import platform
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from win10toast import ToastNotifier
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import keyboard

# Load API keys from .env file
load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
toaster = ToastNotifier()

# Wake Word Detection
def detect_wake_word():
    print("Listening for wake word... (Say 'Jarvis')")
    sample_rate = 16000
    duration = 3  # 3-second recording

    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, blocking=True)
    audio = (audio * 32767).astype('int16')  # Proper PCM conversion

    porcupine = pvporcupine.create(
        access_key=os.getenv("PICOVOICE_ACCESS_KEY"),
        keywords=["jarvis"]
    )

    frame_length = porcupine.frame_length
    audio = audio.flatten()
    num_frames = len(audio) // frame_length

    for i in range(num_frames):
        frame = audio[i * frame_length:(i + 1) * frame_length]
        if porcupine.process(frame) >= 0:
            return True
    return False

# Speech-to-Text with Whisper
def listen():
    print("Listening...")
    sample_rate = 16000
    duration = 5
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, blocking=True)
    sf.write('command.wav', audio, sample_rate)

    model = whisper.load_model("base")
    result = model.transcribe('command.wav')
    return result["text"].strip()

# Text-to-Speech with ElevenLabs
def speak(text):
    audio = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_monolingual_v1"
    )
    play(audio)

# Launch Applications
def open_app(command):
    command = command.lower()
    if "chrome" in command:
        subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    elif "notepad" in command:
        os.system("notepad.exe")
    elif "spotify" in command:
        subprocess.Popen(["spotify.exe"])  # Update path if needed
    elif "calculator" in command:
        os.system("calc.exe")
    elif "search" in command:
        query = command.split("search for")[-1].strip()
        webbrowser.open(f"https://google.com/search?q={query}")

# Media Control
def set_volume(level=50):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level/100, None)

def media_control(command):
    command = command.lower()
    if "pause" in command or "play" in command:
        keyboard.send("play/pause")
    elif "volume up" in command:
        keyboard.send("volume up")
    elif "volume down" in command:
        keyboard.send("volume down")

# System Info
def get_system_info():
    battery = psutil.sensors_battery()
    return {
        "battery": f"{battery.percent}%",
        "os": platform.system(),
        "wifi": "Connected" if psutil.net_if_stats()["Wi-Fi"].isup else "Offline"
    }

# Notifications
def notify(message="Reminder!", duration=5):
    toaster.show_toast("Assistant", message, duration=duration)

# Main Loop with Exit Command
if __name__ == "__main__":
    try:
        while True:
            if detect_wake_word():
                speak("Yes? How can I help?")
                command = listen()
                print(f"You said: {command}")
                command = command.lower()
                
                if any(word in command for word in ["goodbye", "exit", "stop"]):
                    speak("Goodbye! Have a wonderful day!")
                    break
                elif "hello" in command:
                    speak("Hello! What can I do for you?")
                elif "time" in command:
                    speak(f"It's currently {time.strftime('%H:%M')}")
                elif "date" in command:
                    speak(f"Today is {time.strftime('%A, %B %d')}")
                elif "open" in command:
                    open_app(command)
                    speak("Done!")
                elif "volume" in command or "play" in command:
                    media_control(command)
                elif "battery" in command or "wifi" in command:
                    info = get_system_info()
                    speak(f"Battery is at {info['battery']}. Wi-Fi is {info['wifi']}.")
                elif "notify" in command:
                    notify("Your reminder!")
                    speak("Notification set!")
                else:
                    speak("Sorry, I didn't understand.")
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nGoodbye!")
