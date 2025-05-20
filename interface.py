import json
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

fenetre = tk.Tk()
fenetre.title("Smart ToDo")
fenetre.geometry("600x650")
fenetre.configure(bg="#f4f7fa")

tasks = []

COULEUR_FOND = "#f4f7fa"
COULEUR_TEXTE = "#333"
COULEUR_BOUTON = "#4CAF50"
COULEUR_TEXTE_BOUTON = "white"
POLICE = ("Segoe UI", 10)
POLICE_TITRE = ("Segoe UI", 16, "bold")

def style_bouton(btn):
    btn.configure(bg=COULEUR_BOUTON, fg=COULEUR_TEXTE_BOUTON, font=POLICE, relief="flat", padx=10, pady=5)

container = tk.Frame(fenetre, bg=COULEUR_FOND)
container.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

titre = tk.Label(container, text="Smart ToDo", font=POLICE_TITRE, bg=COULEUR_FOND, fg=COULEUR_TEXTE)
titre.pack(pady=(10, 5))

frame_recherche = tk.Frame(container, bg=COULEUR_FOND)
frame_recherche.pack(pady=5, fill=tk.X)

recherche_entry = tk.Entry(frame_recherche, font=POLICE)
recherche_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

btn_recherche = tk.Button(frame_recherche, text="Rechercher", command=lambda: search_task())
style_bouton(btn_recherche)
btn_recherche.pack(side=tk.RIGHT)

def champ_et_label(parent, texte):
    label = tk.Label(parent, text=texte, bg=COULEUR_FOND, fg=COULEUR_TEXTE, font=POLICE)
    label.pack(anchor="w")
    champ = tk.Entry(parent, font=POLICE)
    champ.pack(fill=tk.X, pady=2)
    return champ

entry_titre = champ_et_label(container, "Titre")
entry_description = champ_et_label(container, "Description")
entry_date_limite = champ_et_label(container, "Date limite")
entry_priorite = champ_et_label(container, "Priorité")

frame_actions = tk.Frame(container, bg=COULEUR_FOND)
frame_actions.pack(pady=8)

task_listbox = tk.Listbox(container, width=70, height=8, font=("Segoe UI", 9))
task_listbox.pack(pady=10, fill=tk.BOTH, expand=False)

frame_tri = tk.Frame(container, bg=COULEUR_FOND)
frame_tri.pack(pady=5)

label_tri = tk.Label(frame_tri, text="Trier par :", bg=COULEUR_FOND, font=POLICE)
label_tri.pack(side=tk.LEFT, padx=5)

combo_tri = ttk.Combobox(frame_tri, values=["titre", "priorite", "date_limite"], font=POLICE)
combo_tri.pack(side=tk.LEFT, padx=5)

btn_trier = tk.Button(frame_tri, text="Trier", command=lambda: sort_tasks())
style_bouton(btn_trier)
btn_trier.pack(side=tk.LEFT, padx=5)

def search_task():
    mot_cle = recherche_entry.get().lower()
    if not mot_cle:
        messagebox.showwarning("Attention", "Veuillez entrer un mot-clé.")
        return
    task_listbox.delete(0, tk.END)
    for task in tasks:
        if mot_cle in task["titre"].lower() or mot_cle in task["description"].lower():
            prefixe = "✅" if task.get("terminee") else ""
            task_listbox.insert(tk.END, f"{prefixe}{task['titre']} - {task['priorite']} - {task['date_limite']}")

def add_task():
    titre = entry_titre.get()
    description = entry_description.get()
    date_limite = entry_date_limite.get()
    priorite = entry_priorite.get()
    if not titre or not description or not date_limite or not priorite:
        messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
        return
    task = {"titre": titre, "description": description, "date_limite": date_limite, "priorite": priorite, "terminee": False}
    tasks.append(task)
    save_tasks()
    task_listbox.insert(tk.END, f"{titre} - {priorite} - {date_limite}")
    entry_titre.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_date_limite.delete(0, tk.END)
    entry_priorite.delete(0, tk.END)
    messagebox.showinfo("Succès", "Tâche ajoutée.")

def modify_task():
    try:
        index = task_listbox.curselection()[0]
        task = tasks[index]
        titre = entry_titre.get()
        description = entry_description.get()
        date_limite = entry_date_limite.get()
        priorite = entry_priorite.get()
        if not titre or not description or not date_limite or not priorite:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
            return
        task.update({"titre": titre, "description": description, "date_limite": date_limite, "priorite": priorite})
        task_listbox.delete(index)
        prefixe = "✅" if task.get("terminee") else ""
        task_listbox.insert(index, f"{prefixe}{titre} - {priorite} - {date_limite}")
        save_tasks()
        messagebox.showinfo("Succès", "Tâche modifiée.")
    except IndexError:
        messagebox.showwarning("Attention", "Sélectionnez une tâche.")

def delete_task():
    try:
        index = task_listbox.curselection()[0]
        del tasks[index]
        task_listbox.delete(index)
        save_tasks()
        messagebox.showinfo("Succès", "Tâche supprimée.")
    except IndexError:
        messagebox.showwarning("Attention", "Sélectionnez une tâche.")

def mark_task_done():
    try:
        index = task_listbox.curselection()[0]
        tasks[index]["terminee"] = True
        task = tasks[index]
        task_listbox.delete(index)
        task_listbox.insert(index, f"✅ {task['titre']} - {task['priorite']} - {task['date_limite']}")
        save_tasks()
        messagebox.showinfo("Succès", "Tâche terminée.")
    except IndexError:
        messagebox.showwarning("Attention", "Sélectionnez une tâche.")

def reset_tasks():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        marque = "✅" if task.get("terminee") else ""
        task_listbox.insert(tk.END, f"{marque}{task['titre']} - {task['priorite']} - {task['date_limite']}")

def sort_tasks():
    critere = combo_tri.get()
    if not critere:
        messagebox.showwarning("Attention", "Choisissez un critère.")
        return
    try:
        tasks.sort(key=lambda x: x[critere])
        reset_tasks()
    except KeyError:
        messagebox.showerror("Erreur", "Critère invalide.")

def save_tasks():
    with open(FICHIER_TACHES, "w") as f:
        json.dump(tasks, f, indent=4)

def load_tasks():
    if os.path.exists(FICHIER_TACHES):
        with open(FICHIER_TACHES, "r") as f:
            try:
                data = json.load(f)
                tasks.extend(data)
                reset_tasks()
            except json.JSONDecodeError:
                pass

FICHIER_TACHES = "taches.json"
load_tasks()

for texte, commande in [
    ("Ajouter", add_task),
    ("Modifier", modify_task),
    ("Supprimer", delete_task),
    ("Terminer", mark_task_done),
    ("Réinitialiser", reset_tasks)
]:
    btn = tk.Button(frame_actions, text=texte, command=commande)
    style_bouton(btn)
    btn.pack(side=tk.LEFT, padx=5, pady=2)

fenetre.mainloop()
