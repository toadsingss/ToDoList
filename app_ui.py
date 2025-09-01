import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

FICHIER = "taches.json"

# Charger les tâches existantes
if os.path.exists(FICHIER):
    with open(FICHIER, "r") as f:
        tasks = json.load(f)
else:
    tasks = []

# Fonction pour sauvegarder
def sauvegarder():
    with open(FICHIER, "w") as f:
        json.dump(tasks, f)

# Rafraîchir Treeview
def rafraichir_liste():
    for row in tree.get_children():
        tree.delete(row)
    for i, t in enumerate(tasks, 1):
        statut = "✅" if t["fait"] else "❌"
        tag = "fait" if t["fait"] else "nonfait"
        tree.insert("", tk.END, iid=i-1, values=(t["titre"], t["categorie"], statut), tags=(tag,))

# Ajouter une tâche
def ajouter_tache():
    titre = entry_tache.get().strip()
    categorie = entry_categorie.get().strip() or "Autre"
    if not titre:
        messagebox.showwarning("Erreur", "La tâche ne peut pas être vide")
        return
    tasks.append({"titre": titre, "fait": False, "categorie": categorie})
    entry_tache.delete(0, tk.END)
    entry_categorie.delete(0, tk.END)
    rafraichir_liste()
    sauvegarder()

# Marquer comme faite
def marquer_faite():
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Erreur", "Sélectionne une tâche")
        return
    index = int(selection[0])
    tasks[index]["fait"] = True
    rafraichir_liste()
    sauvegarder()

# Supprimer une tâche
def supprimer_tache():
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Erreur", "Sélectionne une tâche")
        return
    index = int(selection[0])
    tasks.pop(index)
    rafraichir_liste()
    sauvegarder()

# Filtrer par catégorie
def filtrer_par_categorie():
    cat = simpledialog.askstring("Filtrer", "Nom de la catégorie :")
    if not cat:
        return
    for row in tree.get_children():
        tree.delete(row)
    trouve = False
    for i, t in enumerate(tasks, 1):
        if t["categorie"].lower() == cat.lower():
            statut = "✅" if t["fait"] else "❌"
            tag = "fait" if t["fait"] else "nonfait"
            tree.insert("", tk.END, iid=i-1, values=(t["titre"], t["categorie"], statut), tags=(tag,))
            trouve = True
    if not trouve:
        messagebox.showinfo("Info", "Aucune tâche dans cette catégorie.")

# Fenêtre principale
root = tk.Tk()
root.title("To-Do List 📝")

style = ttk.Style()
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
style.configure("Treeview", font=("Helvetica", 10))
style.configure("TButton", font=("Helvetica", 10, "bold"))

# Frame Entrée
frame_input = ttk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Tâche:").grid(row=0, column=0, padx=5, pady=2)
entry_tache = ttk.Entry(frame_input, width=30)
entry_tache.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_input, text="Catégorie:").grid(row=1, column=0, padx=5, pady=2)
entry_categorie = ttk.Entry(frame_input, width=30)
entry_categorie.grid(row=1, column=1, padx=5, pady=2)

btn_add = ttk.Button(frame_input, text="Ajouter", command=ajouter_tache)
btn_add.grid(row=2, column=0, columnspan=2, pady=5)

# Treeview
columns = ("Tâche", "Catégorie", "Statut")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(pady=10)

# Couleurs pour statut
tree.tag_configure("fait", foreground="green")
tree.tag_configure("nonfait", foreground="red")

# Frame Boutons
frame_btns = ttk.Frame(root)
frame_btns.pack(pady=5)

btn_done = ttk.Button(frame_btns, text="Marquer comme faite", command=marquer_faite)
btn_done.grid(row=0, column=0, padx=5)

btn_delete = ttk.Button(frame_btns, text="Supprimer", command=supprimer_tache)
btn_delete.grid(row=0, column=1, padx=5)

btn_filter = ttk.Button(frame_btns, text="Filtrer par catégorie", command=filtrer_par_categorie)
btn_filter.grid(row=0, column=2, padx=5)

rafraichir_liste()
root.mainloop()
