from gtts import gTTS
import speech_recognition as sr
import sounddevice as sd
import os
import base64


def listen_voice(language="en-IN"):
    recognizer = sr.Recognizer()

    try:
        duration = 5
        samplerate = 16000

        print("🎤 Listening...")
        audio_data = sd.rec(int(duration * samplerate),
                            samplerate=samplerate,
                            channels=1,
                            dtype='int16')
        sd.wait()

        audio_bytes = audio_data.tobytes()
        audio = sr.AudioData(audio_bytes, samplerate, 2)

        text = recognizer.recognize_google(audio, language=language)
        return text

    except Exception:
        return "Sorry, could not understand"


def speak_text(text, language="en"):
    try:
        filename = "voice_output.mp3"

        tts = gTTS(text=text, lang=language)
        tts.save(filename)

        # Read file and encode
        with open(filename, "rb") as f:
            audio_bytes = f.read()

        return audio_bytes

    except Exception as e:
        print("Voice error:", e)
        return None