# Jeu-d-amazones-en-Python

Le jeu se joue sur un plateau carré (6×6, 8×8 ou 10×10).  
Chaque joueur possède plusieurs pions :  
- **Rouge** (joueur 1)  
- **Bleu** (joueur 2 ou l’IA)  

### Règles :
1. Le joueur actif sélectionne l’un de ses pions.  
2. Il déplace ce pion en ligne droite (horizontale, verticale ou diagonale), sans sauter d’obstacles.  
3. Ensuite, depuis cette nouvelle position, il tire une flèche (qui bloque une case de manière permanente).  
4. Le tour passe à l’adversaire.  
5. Le premier joueur qui **n’a plus de coups possibles** perd la partie.

***

## ⚙️ Fonctionnalités principales

- 🎮 **Modes de jeu** :  
  - Joueur vs Joueur  
  - Joueur vs IA (aléatoire)

- 💾 **Gestion de partie** :  
  - Sauvegarde et chargement (`jeu_save.json`)  
  - Rejouer ou lancer une nouvelle partie  

- 🔊 **Effets sonores** pour les déplacements et les tirs  
- 🧠 **IA simple** qui joue automatiquement pour le joueur bleu  
- 🧱 **Blocages (flèches)** qui rendent des cases inaccessibles  
- 🎨 **Interface Tkinter complète** (clic souris pour jouer)  

***

## 🖥️ Installation

### Prérequis :
- Python 3.x  
- Bibliothèques standard (`tkinter`, `json`, `os`, `random`, `winsound`)

### Étapes :
1. Clone le dépôt :
   ```bash
   git clone https://github.com/<ton_nom_utilisateur>/jeu-adama-ilyass.git
   cd jeu-adama-ilyass
   ```

2. Lance le jeu :
   ```bash
   python main.py
   ```

(Note : sur macOS/Linux, la bibliothèque `winsound` n’est pas disponible. Tu peux la remplacer ou ignorer les sons.)

***

## 🧭 Commandes et interactions

| Action                       | Description |
|-------------------------------|--------------|
| **Nouvelle partie**           | Démarre un nouveau jeu selon la taille choisie |
| **Rejouer**                   | Redémarre avec les paramètres actuels |
| **Sauvegarder**               | Enregistre la partie en cours |
| **Charger**                   | Charge la dernière sauvegarde |
| **Mode IA**                   | Active/désactive le mode IA pour le joueur bleu |

***

## 🎨 Interface du plateau

- Cases claires / foncées : damier de fond  
- Cercles rouges et bleus : pions des joueurs  
- ✖ : flèches bloquantes  
- Bordures colorées :  
  - **Jaune** : mouvements possibles  
  - **Orange** : tirs possibles  
  - **Rose** : pion sélectionné  

***

## 🧠 IA (logique simplifiée)

L’IA choisit :
1. Aléatoirement un de ses pions ayant des mouvements possibles.  
2. Un mouvement valide au hasard.  
3. Tire une flèche sur une case libre choisie au hasard.  

C’est une version basique, parfaite pour apprendre à coder une IA de stratégie.  

***

## 📁 Structure du projet

```
jeu-adama-ilyass/
│
├── main.py              # Code principal (Tkinter + logique du jeu)
├── jeu_save.json        # Fichier de sauvegarde (créé au besoin)
└── README.md            # Documentation du projet
```

***

## 🚀 Améliorations possibles

- Ajouter des **animations de déplacement**
- Créer une **IA plus stratégique**
- Rendre le jeu compatible macOS/Linux (remplacer `winsound`)
- Ajouter un **compteur de tours et un chronomètre**
- Implémenter un **mode en ligne ou local réseau**

***

## 👩‍💻 Auteurs
Développé par **Adama & Ilyass**  
Projet pédagogique — 2026  

***

Souhaites-tu que je te fasse une version du README en **anglais** formatée pour GitHub aussi ?
