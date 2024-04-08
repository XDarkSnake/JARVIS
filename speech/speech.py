import whisper
import logging
from pathlib import Path

from start.start import model

def speech_to_text():
    """
    Fonction qui exécute le processus de transcription de la vidéo en texte.
    """
    # Définition du niveau de logging
    logging.basicConfig(level=logging.INFO)

    # Définition des chemins des fichiers
    CURR_DIR = Path.cwd()
    FILE_TXT = CURR_DIR / "text.txt"

    try:
        model_choisi = str(model())
        logging.info("Génération du fichier txt en cours...")

        logging.info("Chargement du modèle en cours...")
        model_w = whisper.load_model(model_choisi)
        logging.info("Chargement du modèle terminé")

        logging.info("Transcription de la vidéo en cours...")
        result = model_w.transcribe("video.mp4", fp16=False)

        # Vérification du type du résultat et formatage du texte
        if isinstance(result["text"], list):
            text = '\n\n'.join(map(str, result["text"]))
        else:
            text = result["text"]
        
        logging.info("Texte transcrit : %s", text)

        # Écriture du texte dans le fichier avec des sauts de ligne
        with open(FILE_TXT, "w", encoding="utf-8") as f:
            f.write(text)
        
        
        logging.info("Génération du fichier txt terminée.")
    
    except Exception as e:
        logging.error("Une erreur est survenue : %s", e)

# Exécution de la fonction
if __name__ == "__main__":
    speech_to_text()
