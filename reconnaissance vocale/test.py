import audioop
import io
import pyaudio
import wave

class Recognizer:
    def __init__(self, room_threshold_db):
        self.CHUNK = 1024
        self.SAMPLE_RATE = 44100
        self.SAMPLE_WIDTH = 2
        self.room_threshold_db = room_threshold_db
        self.stream = self._initialize_microphone_stream()
        self.energy_threshold = 300
        self.dynamic_energy_threshold = True
        self.dynamic_energy_adjustment_damping = 0.15
        self.dynamic_energy_ratio = 1.5
        self.pause_threshold = 0.8
        self.operation_timeout = None
        self.phrase_threshold = 0.3
        self.non_speaking_duration = 0.5

    def _initialize_microphone_stream(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        return stream

    def adjust_for_ambient_noise(self, duration=1):
        """
        Adjusts the energy threshold dynamically using audio from the recognizer's microphone stream to account for ambient noise.

        Intended to calibrate the energy threshold with the ambient energy level. Should be used on periods of audio without speech - will stop early if any speech is detected.

        The ``duration`` parameter is the maximum number of seconds that it will dynamically adjust the threshold for before returning. This value should be at least 0.5 in order to get a representative sample of the ambient noise.
        """
        assert self.stream is not None, "Audio source must be entered before adjusting"
        assert self.pause_threshold >= self.non_speaking_duration >= 0

        seconds_per_buffer = (self.CHUNK + 0.0) / self.SAMPLE_RATE
        elapsed_time = 0

        # adjust energy threshold until a phrase starts
        while True:
            elapsed_time += seconds_per_buffer
            if elapsed_time > duration: break
            buffer = self.stream.read(self.CHUNK)
            energy = audioop.rms(buffer, self.SAMPLE_WIDTH)  # energy of the audio signal

            # dynamically adjust the energy threshold using asymmetric weighted average
            damping = self.dynamic_energy_adjustment_damping ** seconds_per_buffer  # account for different chunk sizes and rates
            target_energy = energy * self.dynamic_energy_ratio
            self.energy_threshold = self.energy_threshold * damping + target_energy * (1 - damping)

    def start_recording_on_sound(self):
        print("Enregistrement en cours...")
        frames = io.BytesIO()
        while True:
            buffer = self.stream.read(self.CHUNK)
            frames.write(buffer)

            if self.is_sound_above_threshold(buffer):
                break

        return frames.getvalue()

    def stop_recording_on_silence(self):
        print("Fin de l'enregistrement.")
        frames = io.BytesIO()
        while True:
            buffer = self.stream.read(self.CHUNK)
            frames.write(buffer)

            if not self.is_sound_above_threshold(buffer):
                break

        return frames.getvalue()

    def is_sound_above_threshold(self, buffer):
        rms = audioop.rms(buffer, self.SAMPLE_WIDTH)
        db = 20 * (1 / self.SAMPLE_WIDTH) * rms
        return db > self.room_threshold_db

    def record_with_sound_detection(self):
        self.adjust_for_ambient_noise()  # Adjust for ambient noise before recording
        start_frames = self.start_recording_on_sound()
        stop_frames = self.stop_recording_on_silence()
        return start_frames + stop_frames

if __name__ == "__main__":
    room_threshold_db = 60
    recognizer = Recognizer(room_threshold_db)

    while True:
        # Record audio
        recorded_audio = recognizer.record_with_sound_detection()

        # Save the recorded audio to a WAV file
        with wave.open("recorded_audio.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(recognizer.SAMPLE_WIDTH)
            wf.setframerate(recognizer.SAMPLE_RATE)
            wf.writeframes(recorded_audio)
