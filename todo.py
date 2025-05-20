import json
import os

# Fonction pour sauvegarder les tâches dans un fichier JSON

def save_tasks():
    with open("tasks.json", "w", encoding="utf-8") as fichier:
        json.dump(tasks, fichier, ensure_ascii=False, indent=4)

# Fonction pour charger les tâches

def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r", encoding="utf-8") as fichier:
            tasks = json.load(fichier)
    except FileNotFoundError:
        tasks = []



# Liste des tâches
tasks = []

# Fonction pour ajouter une tâche
def add_task():
    titre = input("Titre : ")
    description = input("Description : ")
    date_limite = input("Date limite(YYYY-MM-JJ) : ")
    priorite = input("Priorité : ")

    task = {
        "titre": titre,
        "description": description,
        "date_limite": date_limite,
        "priorite": priorite,
        "terminee": False  # Tâche non terminée par défaut
    }
    tasks.append(task)

    save_tasks()

    print("Tâche ajoutée avec succès.")

# Fonction pour afficher toutes les tâches
def show_tasks():
    if not tasks:
        print("Aucune tâche enregistrée.")
        return

    for index, task in enumerate(tasks, start=1):
        statut = "Terminée" if task["terminee"] else "À faire"
        print(f"\nTâche {index}:")
        print(f"Titre       : {task['titre']}")
        print(f"Description : {task['description']}")
        print(f"Date limite : {task['date_limite']}")
        print(f"Priorité    : {task['priorite']}")
        print(f"Statut      : {statut}")

#  Fonction pour marquer une tâche comme terminée
def mark_task_done():
    if not tasks:
        print("Aucune tâche à marquer.")
        return

    show_tasks()
    try:
        num = int(input("\nNuméro de la tâche à marquer comme terminée : "))
        if 1 <= num <= len(tasks):
            tasks[num - 1]["terminee"] = True

            save_tasks()

            print("Tâche marquée comme terminée.")
        else:
            print("Numéro invalide.")
    except ValueError:
        print("Veuillez entrer un nombre valide.")

#   Fonction pour supprimer une tâche
def delete_task():
    if not tasks:
        print("Aucune tâche à supprimer.")
        return

    show_tasks()
    try: 
        num = int(input("Numéro de la tâche à supprimer : "))
        if 1 <= num <= len(tasks): 
            del tasks[num - 1]
            save_tasks()
            print("Tâche supprimée avec succès.")
        else: 
            print("Numéro invalide.")
    except ValueError: 
        print("Veuillez entrer un nombre valide.")

#   Fonction pour modifier une tâche
def modify_task():
    if not tasks:
        print("Aucune tâche à modifier.")
        return

    show_tasks()
    try:
        num = int(input("\nNuméro de la tâche à modifier : "))
        if 1 <= num <= len(tasks):
            tache = tasks[num - 1]
            print("\nLaisse vide si tu ne veux pas modifier un champ.")

            nouveau_titre = input(f"Nouveau titre [{tache['titre']}] : ")
            nouvelle_description = input(f"Nouvelle description [{tache['description']}] : ")
            nouvelle_date = input(f"Nouvelle date limite [{tache['date_limite']}] : ")
            nouvelle_priorite = input(f"Nouvelle priorité [{tache['priorite']}] : ")

            if nouveau_titre:
                tache['titre'] = nouveau_titre
            if nouvelle_description:
                tache['description'] = nouvelle_description
            if nouvelle_date:
                tache['date_limite'] = nouvelle_date
            if nouvelle_priorite:
                tache['priorite'] = nouvelle_priorite

            save_tasks()

            print("Tâche modifiée avec succès.")
        else:
            print("Numéro invalide.")
    except ValueError:
        print("Veuillez entrer un nombre valide.")

# trie des tâche
def sort_tasks():
    if not tasks:
        print("Aucune tâche à trier.")
        return

    PRIORITE_MAP = {"haute": 1, "moyenne": 2, "basse": 3}

    show_sort_menu()
    choix = input("Choisis une option de tri : ")

    if choix == "1":
        tasks.sort(key=lambda x: x["date_limite"])
        print("Tâches triées par date limite.")
    elif choix == "2":
        tasks.sort(key=lambda x: PRIORITE_MAP.get(x["priorite"].lower(), 4))
        print("Tâches triées par priorité.")
    elif choix == "3":
        tasks.sort(key=lambda x: x["terminee"])
        print("Tâches triées par statut.")
    elif choix == "4":
        tasks.sort(key=lambda x: x["titre"].lower())
        print("Tâches triées par titre.")
    elif choix == "5":
        print("Tri annulé.")
    else:
        print("Option invalide.")

    save_tasks()

# Fonction pour rechercher une tâche
def search_task():
    if not tasks:
        print("Aucune tâche à rechercher.")
        return

    recherche = input("Entrez le mot-clé de recherche : ").lower()
    resultats = [task for task in tasks if recherche in task["titre"].lower()]

    if resultats:
        for index, task in enumerate(resultats, start=1):
            statut = "Terminée" if task["terminee"] else "À faire"
            print(f"\nTâche {index}:")
            print(f"Titre       : {task['titre']}")
            print(f"Description : {task['description']}")
            print(f"Date limite : {task['date_limite']}")
            print(f"Priorité    : {task['priorite']}")
            print(f"Statut      : {statut}")
    else:
        print("Aucune tâche trouvée avec ce mot-clé.")

# menu de tâches        

def show_sort_menu():
    print("\n--- TRIER LES TÂCHES ---")
    print("1. Par date limite")
    print("2. Par priorité")
    print("3. Par statut (Terminée / À faire)")
    print("4. Par titre")
    print("5. Annuler")

# Affichage du menu
def show_menu():
    print("\n--- MENU ---")
    print("1. Ajouter une tâche")
    print("2. Afficher les tâches")
    print("3. Marquer une tâche comme terminée") 
    print("4. Supprimer une tâche")
    print("5. Modifier une tâche")
    print("6. Trier les tâches")
    print("7. Rechercher une tâche")
    print("8. Quitter")

#  Boucle principale du programme

load_tasks()

while True:
    
    os.system("cls" if os.name == "nt" else "clear")

    show_menu()

    choix = input("Choisis une option : ")

    if choix == "1":
        add_task()
        input("\nAppuie sur Entrée pour continuer...")
    elif choix == "2":
        show_tasks()
        input("\nAppuie sur Entrée pour continuer...")
    elif choix == "3":
        mark_task_done() 
        input("\nAppuie sur Entrée pour continuer...")
    elif choix == "4":
        delete_task()
        input("\nAppuie sur Entrée pour continuer...")
    elif choix == "5":
        modify_task()
        input("\nAppuie sur Entrée pour continuer...")
    elif choix == "6":
        sort_tasks()
        input("\nAppuie sur Entrée pour continuer...")
    elif choix == "7":
        search_task()
        input("\nAppuie sur Entrée pour continuer...")
    elif choix == "8":
        print("Fermeture du programme.")
        break
    else:
        print("Option invalide. Veuillez réessayer.")
        input("\nAppuie sur Entrée pour continuer...")
