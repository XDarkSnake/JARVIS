import sounddevice as sd
import numpy as np
from time import sleep
from micro.micro import choisir_microphone  # Assurez-vous que micro est bien un module existant contenant la fonction choisir_microphone
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

def record_audio():
    
    def set_volume(vol):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session._ctl.QueryInterface(ISimpleAudioVolume)
            # set the volume (0.0 to 1.0)
            interface.SetMasterVolume(vol, None)
        
    def change_volume(delta):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session._ctl.QueryInterface(ISimpleAudioVolume)
            # Get the actual volume
            current_volume = interface.GetMasterVolume()
            # Calculate the new volume
            new_volume = max(0.0, min(1.0, current_volume + delta))
            # Set the volume
            interface.SetMasterVolume(new_volume, None)
    
    def microphone():
        microphone_index = choisir_microphone()  # Sélectionnez le microphone une seule fois
        return microphone_index

    def record_parm(microphone_index):
        samplerate = 44100  # Fréquence d'échantillonnage
        recording = sd.InputStream(device=microphone_index, channels=1, samplerate=samplerate, dtype=np.int16)    
        return recording

    def start_recording():
        global recording
        recording = record_parm(microphone())
        recording.start()
        print("Enregistrement démarré.")

    def stop_recording():
        global recording
        if recording:
            recording.stop()
            print("Enregistrement arrêté.")

    def detect_volume_change():
        # Insérez ici le code pour détecter le changement de volume
        print("Detection de changement de volume...")
        return False  # À remplacer par votre logique de détection
    
    def detect_silence():
        # Insérez ici le code pour détecter le silence pendant 2 secondes
        print("Detection de silence...")
        return False  # À remplacer par votre logique de détection

    # Démarrage de l'enregistrement si le volume change
    set_volume(0.5)  # Définir le volume initial
    while True:
        change_volume(0.1)  # Augmenter progressivement le volume
        if detect_volume_change():
            start_recording()
            break
    
    # Attente de la fin de l'enregistrement
    sleep(10)  # Vous pouvez ajuster la durée d'enregistrement ici
    
    # Arrêt de l'enregistrement si le silence est détecté
    set_volume(0.1)  # Baisser le volume pour simuler le silence
    while True:
        change_volume(-0.1)  # Diminuer progressivement le volume
        if detect_silence():
            stop_recording()
            break

record_audio()
