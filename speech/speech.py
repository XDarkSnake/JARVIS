import whisper
import logging
from pathlib import Path


def speech_to_text():
    """
    Fonction qui exécute le processus de transcription de la vidéo en texte.
    """
    chemin_parent = Path(__file__).resolve().parent
    chemin_parent.mkdir(parents=True, exist_ok=True)
    chemin_logs = chemin_parent / "logs_speech.log"
    
    # Définition du niveau de logging
    logging.basicConfig(filename=chemin_logs, level=logging.INFO, format="%(levelname)s - %(message)s")
    with open(chemin_logs, "w"):
        pass

    # Définition des chemins des fichiers
    CURR_DIR = Path.cwd()
    FILE_TXT = CURR_DIR / "text.txt"
    MODEL = CURR_DIR / "model.txt"
    
    FILE_TXT.mkdir(exist_ok=True, parents=True)
    MODEL.mkdir(exist_ok=True, parents=True)
    
    try:
        with open(MODEL, "r") as model:
            model_choisi = model.read()

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
