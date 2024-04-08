import sounddevice as sd
import numpy as np

def detect_audio_changes(duration=2, decibel_threshold=2, silence_threshold=-40):
    samplerate = 44100
    channels = 1
    duration_frames = int(duration * samplerate)
    
    def callback(indata, frames, time, status):
        dbfs = 20 * np.log10(np.max(np.abs(indata)))
        
        if dbfs > decibel_threshold:
            callback.decibel_increase_frames += frames
            callback.silence_frames = 0
        else:
            callback.decibel_increase_frames = 0
        
        if dbfs < silence_threshold:
            callback.silence_frames += frames
        else:
            callback.silence_frames = 0
        
        if callback.decibel_increase_frames >= duration_frames:
            print("Hausse de décibels détectée pendant au moins 2 secondes.")
            callback.decibel_increase_frames = 0
        
        if callback.silence_frames >= duration_frames:
            print("Silence détecté pendant au moins 2 secondes.")
            callback.silence_frames = 0
    
    callback.decibel_increase_frames = 0
    callback.silence_frames = 0
    
    with sd.InputStream(callback=callback, channels=channels, samplerate=samplerate):
        print("Début de la surveillance des changements audio...")
        while True:
            pass

if __name__ == "__main__":
    detect_audio_changes()
