import json
import logging
import keyboard
import sounddevice as sd
import numpy as np
import wave

from pathlib import Path

wav_file = None

def record_audio():
    chemin_travail = Path().cwd()
    chemin_travail.mkdir(parents=True, exist_ok=True)
    
    chemin_logs = chemin_travail / "logs" /"logs_record.log"
    chemin_settings = chemin_travail / "settings.json"
    
    logging.basicConfig(filename=chemin_logs, level=logging.INFO, format="%(levelname)s - %(message)s")
    with open(chemin_logs, "w"):
        pass

    def microphone():
        with open(chemin_settings, "r") as f:
            settings = json.load(f)
        return settings.get('micro', None)

    def record_parm(microphone_index):
        samplerate = 44100  
        recording = sd.InputStream(device=microphone_index, channels=1, samplerate=samplerate, dtype=np.int16)    
        return recording

    def stat_program():
        nonlocal record_stat
        record_stat = not record_stat
        
        if record_stat:
            global wav_file
            wav_file = wave.open('enregistrement.wav', 'wb')
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(44100)
            recording.start()
            logging.info("Enregistrement demarre.")
        else:
            recording.stop()
            logging.info("Enregistrement arrete.")
            if wav_file is not None:
                wav_file.close()
                logging.info("Audio enregistré dans 'enregistrement.wav'.")

    record_stat = False

    microphone_index = microphone()  
    if microphone_index is None:
        logging.error("Impossible de récupérer l'index du microphone.")
        return

    recording = record_parm(microphone_index)  

    keyboard.on_press_key('*', stat_program)
    while True:
        pass  

if __name__ == "__main__":
    record_audio()
