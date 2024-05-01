import json
import logging
import keyboard
import sounddevice as sd
import numpy as np
import wave
import speech_recognition as sr

from pathlib import Path

def record_audio():
    chemin_travail = Path.cwd()
    chemin_travail.mkdir(parents=True, exist_ok=True)
    
    chemin_logs = chemin_travail / "logs" / "logs_record.log"
    chemin_settings = chemin_travail / "settings.json"
    
    logging.basicConfig(filename=chemin_logs, level=logging.INFO, format="%(levelname)s - %(asctime)s %(message)s")
    with open(chemin_logs, "w"):
        pass

    def microphone():
        with open(chemin_settings, "r") as f:
            settings = json.load(f)
        return settings.get('micro', None)

    def record_parm(microphone_index):
        samplerate = 44100  
        return sd.InputStream(device=microphone_index, channels=1, samplerate=samplerate, dtype=np.int16)    

    def start_recording(recording):
        wav_file = wave.open('enregistrement.wav', 'wb')
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        recording.start()
        logging.info("Enregistrement démarré.")
        return wav_file

    def stop_recording(recording, wav_file):
        recording.stop()
        logging.info("Enregistrement arrêté.")
        if wav_file is not None:
            wav_file.close()
            logging.info("Audio enregistré dans 'enregistrement.wav'.")
            exit()

    def detect_voice(recording):
        recognizer = sr.Recognizer()
        microphone_index = microphone()

        with sr.Microphone(device_index=microphone_index) as source:
            recognizer.adjust_for_ambient_noise(source)
            logging.info("Attente de la détection de la voix...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_sphinx(audio, language='fr-FR')
            logging.info(f"Texte détecté: {text}")
            if "démarrer enregistrement" in text:
                stop_recording(recording, None)
                recording = record_parm(microphone_index)
                start_recording(recording)
            elif "arrêter enregistrement" in text:
                stop_recording(recording, None)
        except sr.UnknownValueError:
            logging.info("Impossible de comprendre l'audio.")
        except sr.RequestError as e:
            logging.error(f"Erreur lors de la requête à PocketSphinx: {e}")

    recording = None
    keyboard.on_press_key('*', lambda _: stop_recording(recording, None))
    keyboard.on_press_key('-', lambda _: stop_recording(recording, None))
    while True:
        detect_voice(recording)

if __name__ == "__main__":
    record_audio()
