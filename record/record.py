import keyboard
import sounddevice as sd
import numpy as np
import wave
from start.start import micro  # Assurez-vous que micro est bien un module existant contenant la fonction choisir_microphone

wav_file = None  # Déclarer wav_file en dehors de la fonction record_audio()

def record_audio():
    def microphone():
        microphone_index = micro()  # Sélectionnez le microphone une seule fois
        return microphone_index

    def record_parm(microphone_index):
        samplerate = 44100  # Fréquence d'échantillonnage
        recording = sd.InputStream(device=microphone_index, channels=1, samplerate=samplerate, dtype=np.int16)    
        return recording

    def stat_program(e):
        nonlocal record_stat
        record_stat = not record_stat
        
        if record_stat:
            global wav_file
            wav_file = wave.open('enregistrement2.wav', 'wb')
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(44100)
            recording.start()
            print("Enregistrement démarré.")
        else:
            recording.stop()
            print("Enregistrement arrêté.")
            if wav_file is not None:
                wav_file.close()
                print("Audio enregistré dans 'enregistrement2.wav'.")

    record_stat = False

    microphone_index = microphone()  # Appel de la fonction pour récupérer l'index du microphone
    recording = record_parm(microphone_index)  # Initialisation de l'enregistrement avec le microphone sélectionné

    keyboard.on_press_key('*', stat_program)
    while True:
        pass  # Boucle infinie pour maintenir le programme en cours d'exécution

if __name__ == "__main__":
    record_audio()
