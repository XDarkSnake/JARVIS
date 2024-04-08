import logging
import pyaudio

def obtenir_microphones_disponibles():
    """
    Récupère la liste des microphones disponibles sur l'ordinateur.

    Returns:
        list: Liste des microphones disponibles, sous forme de tuples (index, nom).
    """
    try:
        pyaudio_instance = pyaudio.PyAudio()
        liste_microphones = []
        for i in range(pyaudio_instance.get_device_count()):
            infos_micro = pyaudio_instance.get_device_info_by_index(i)
            if infos_micro.get('maxInputChannels') and int(infos_micro['maxInputChannels']) > 0:
                if infos_micro['hostApi'] == pyaudio_instance.get_default_host_api_info()['index']:
                    liste_microphones.append((i, infos_micro['name']))
        pyaudio_instance.terminate()

        logging.info("Microphones disponibles et utilisables:")
        for index, microphone in liste_microphones:
            logging.info(f"{index}: {microphone}")
            print(f"{index}: {microphone}")
            print("-" * 50)
        return liste_microphones

    except Exception as erreur:
        logging.error(f"Une erreur s'est produite : {erreur}")
        return []

if __name__ == "__main__":
    microphones_disponibles = obtenir_microphones_disponibles()
    print(microphones_disponibles)
