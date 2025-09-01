import os
import json

file = "tasks.json"

if os.path.exists(file):
    with open(file, "r") as f:
        tasks = json.load(f)
else:
    tasks = []

def show():
    if not tasks:
        print("\nPas de tâche pour l'instant.")
    else:
        for i,t in enumerate(tasks, 1):
            statut = "✅​" if t["done"] else "❌​"
            print(f"\n{i}. [{t['category']}] {t['title']} {statut}")

def showByCategory():
    category = input("\nQuelle catégorie voulez vous afficher ? : ")
    found = False
    for i, t in enumerate(tasks, 1):
        if t["category"].lower() == category.lower():
            statut = "✅​" if t["done"] else "❌​"
            print(f"\n{i}. [{t['category']}] {t['title']} {statut}")
            found = True
    if not found:
        print("\n⚠️ Aucune tâche dans cette catégorie.")

def add():
    title = input("\nQuelle est votre tâche ? : ")
    category = input("Dans quelle catégorie cette tache entre ? (exemple : Maison, Travail, Autre...) : ")
    tasks.append({"title": title, "done": False, "category": category})
    print("✅ Tâche ajoutée !")

def markAsDone():
    show()
    try:
        choice = int(input("\nNuméro de la tâche faite : ")) - 1
        tasks[choice]["done"] = True
        print("✅ Tâche complétée !")
    except (ValueError, IndexError):
        print("❌ Choix invalide.")

def markAsNotDone():
    show()
    try:
        choice = int(input("\nNuméro de la tâche non-faite : ")) - 1
        tasks[choice]["done"] = False
        print("✅ Tâche marquée comme incomplète !")
    except (ValueError, IndexError):
        print("❌ Choix invalide.")

def remove():
    show()
    try:
        choice = int(input("\nNuméro de la tâche à supprimer : ")) - 1
        tasks.pop(choice)
        print("🗑️ Tâche supprimée ! ")
    except (ValueError, IndexError):
        print("❌ Choix invalide.")

def save():
    with open(file, "w") as f:
        json.dump(tasks, f)

while True:
    print("\n<--- To-do List --->")
    print("1. Afficher les tâches")
    print("2. Afficher les tâches par catégorie")
    print("3. Ajouter une tâche")
    print("4. Marquer comme faite")
    print("5. Marquer comme non-faite")
    print("6. Supprimer une tâche")
    print("7. Quitter")

    choice = input("\nChoisissez une action : ")

    if choice == "1":
        show()

    elif choice == "2":
        showByCategory()

    elif choice == "3":
        add()

    elif choice == "4":
        markAsDone()

    elif choice == "5":
        remove()

    elif choice == "6":
        markAsNotDone()

    elif choice == "7":
        save()
        print("\nÀ bientôt !")
        break
    
    else:
        print("❌ Option invalide, veuillez réessayer.")
