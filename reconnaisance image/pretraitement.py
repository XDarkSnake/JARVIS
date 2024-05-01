import cv2
from pathlib import Path
import logging

def preprocess_images():
    def preprocess_image(image):
        try:
            image_resized = cv2.resize(image, (28, 28))
            image_normalized = image_resized / 255.0
            image_contrast = cv2.equalizeHist((image_normalized * 255).astype('uint8'))
            image_smoothed = cv2.GaussianBlur(image_contrast, (5, 5), 0)
            return image_smoothed
        except Exception as e:
            logging.error(f"Erreur lors du prétraitement de l'image : {e}")
            return None

    chemin_travail = Path.cwd()
    chemin_travail.mkdir(parents=True, exist_ok=True)
    chemin_logs = chemin_travail / "logs" / "logs_traitement.log"
    logging.basicConfig(filename=chemin_logs, level=logging.INFO, format="%(levelname)s - %(asctime)s %(message)s")
    with open(chemin_logs, "w"):
        pass

    parent = Path(__file__).parent
    repertoire_images = parent / "images"
    repertoire_images.mkdir(parents=True, exist_ok=True)
    repertoire_pretraitees = parent / "images_traitees"
    repertoire_pretraitees.mkdir(parents=True, exist_ok=True)

    for image_path in repertoire_images.glob("*.jpg"):
        try:
            image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

            if image is not None:
                image_pretraitee = preprocess_image(image)

                if image_pretraitee is not None:
                    nom_image_pretraitee = f"{image_path.stem}_pretraitee.jpg"
                    chemin_image_pretraitee = repertoire_pretraitees / nom_image_pretraitee
                    cv2.imwrite(str(chemin_image_pretraitee), image_pretraitee)
                    logging.info(f"Image {image_path.name} prétraitée et sauvegardée avec succès.")
                else:
                    logging.warning(f"Impossible de prétraiter l'image {image_path.name}.")
            else:
                logging.warning(f"Impossible de charger l'image {image_path.name}.")
        except Exception as e:
            logging.error(f"Erreur lors du traitement de l'image {image_path.name} : {e}")

    logging.info("Toutes les images ont été prétraitées et sauvegardées.")

if __name__ == "__main__":
    preprocess_images()
