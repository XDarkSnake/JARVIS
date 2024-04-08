import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
import logging

from micro.micro import obtenir_microphones_disponibles

def micro():
    """
    Permet à l'utilisateur de choisir un microphone parmi ceux disponibles.

    Returns:
        str: L'index du microphone choisi.
    """
    chemin_parent = Path(__file__).resolve().parent
    chemin_parent.mkdir(parents=True, exist_ok=True)
    chemin_logs = chemin_parent / "logs_micro.log"
    chemin_ico = chemin_parent.parent / "ressources" / "logo_micro.ico"
    print(chemin_ico)
    
    logging.basicConfig(filename=chemin_logs, level=logging.INFO, format="%(levelname)s - %(message)s")
    with open(chemin_logs, "w"):
        pass
    
    microphone_choisi = None  
    
    while microphone_choisi is None or microphone_choisi == "":
        micros_disponibles = obtenir_microphones_disponibles()

        if not micros_disponibles:
            logging.error("Aucun microphone disponible.")
            return None

        app = ctk.CTk()
        app.title("Choix du microphone")
        app.iconbitmap(chemin_ico)

        etiquette_micro = ctk.CTkLabel(app, text="Choisissez un microphone:", font=("Arial", 14))
        etiquette_micro.pack()

        def callback_optionmenu_micro(choix):
            nonlocal microphone_choisi
            nonlocal micros_disponibles
            index_microphone = [micro[1] for micro in micros_disponibles].index(choix)
            microphone_choisi = micros_disponibles[index_microphone][0]
            app.destroy()

        optionmenu_var_micro = ctk.StringVar(value=micros_disponibles[0][1])
        optionmenu_micro = ctk.CTkOptionMenu(app, values=[micro[1] for micro in micros_disponibles], command=callback_optionmenu_micro, variable=optionmenu_var_micro, font=("Arial", 14))
        optionmenu_micro.pack()

        def sur_fermeture_fenetre():
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un microphone pour continuer !")

        app.protocol("WM_DELETE_WINDOW", sur_fermeture_fenetre)

        larg_ecran = app.winfo_screenwidth()
        haut_ecran = app.winfo_screenheight()
        larg_fenetre = 550
        haut_fenetre = 100
        x_position = (larg_ecran - larg_fenetre) // 2
        y_position = (haut_ecran - haut_fenetre) // 2
        app.geometry(f"{larg_fenetre}x{haut_fenetre}+{x_position}+{y_position}")
        app.resizable(False, False)
        app.mainloop()

    return microphone_choisi

def model():
    chemin_parent = Path(__file__).resolve().parent
    chemin_parent.mkdir(parents=True, exist_ok=True)
    chemin_logs = chemin_parent / "logs_model.log"
    chemin_ico = chemin_parent.parent / "ressources" / "logo_model.ico"

    logging.basicConfig(filename=chemin_logs, level=logging.INFO, format="%(levelname)s - %(message)s")
    with open(chemin_logs, "w"):
        pass
    
    models = {"Minuscule": "tiny", "Basique": "base", "Petit": "small", "Moyen": "medium", "Grand": "large"}
    model_choisi = None
    
    while model_choisi is None or model_choisi == "":
        if not models:
            logging.error("Aucun modèle disponible.")
            return None

        app = ctk.CTk()
        app.title("Choix du modèle")
        app.iconbitmap(chemin_ico)

        etiquette_micro = ctk.CTkLabel(app, text="Choisissez un modèle:", font=("Arial", 16))
        etiquette_micro.pack()

        def callback_optionmenu_model(choix: str):
            nonlocal model_choisi
            model_choisi = models.get(choix)
            app.destroy()

        optionmenu_var_model = ctk.StringVar(value=list(models.keys())[0])
        optionmenu_model = ctk.CTkOptionMenu(app, values=list(models.keys()), command=callback_optionmenu_model, variable=optionmenu_var_model, font=("Arial", 16))
        optionmenu_model.pack()

        def sur_fermeture_fenetre():
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un modèle pour continuer !")

        app.protocol("WM_DELETE_WINDOW", sur_fermeture_fenetre)

        larg_ecran = app.winfo_screenwidth()
        haut_ecran = app.winfo_screenheight()
        larg_fenetre = 550
        haut_fenetre = 100
        x_position = (larg_ecran - larg_fenetre) // 2
        y_position = (haut_ecran - haut_fenetre) // 2
        app.geometry(f"{larg_fenetre}x{haut_fenetre}+{x_position}+{y_position}")
        app.resizable(False, False)

        app.mainloop()

    return model_choisi


if __name__ == "__main__":
    micro()
    model()
    print(model)