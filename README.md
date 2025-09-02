# 📄 PaperMind

![Python](https://img.shields.io/badge/python-3.10+-blue) ![LangChain](https://img.shields.io/badge/langchain-v1.0+-green) ![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-orange) ![GPT](https://img.shields.io/badge/GPT-4o-purple)

Un outil en **ligne de commande (CLI)** qui permet de :

* 📂 Importer un PDF.
* 🤖 Résumer automatiquement son contenu via **IA**.
* 💬 Utiliser le contenu résumé comme **contexte de chat**.
* ⚡ Configurable avec **deux modèles** : `Gemini 2.5 Flash` ou `GPT-4o`.

---

## 🚀 Fonctionnalités

1. **Import PDF**

   * Sélection de fichier via terminal.
   * Prise en charge des chemins absolus ou relatifs.

2. **Résumé automatique**

   * Chaque page du PDF est résumée automatiquement.
   * Résumé concaténé pour servir de contexte à la conversation.
   * Barre de progression en temps réel avec `rich` pendant le résumé.

3. **Chat interactif**

   * Pose des questions en se basant sur le contexte du PDF.
   * Les réponses sont générées via le modèle IA sélectionné.
   * Le contexte est mis à jour automatiquement après chaque réponse.

4. **Multi-modèle**

   * Choix entre **Gemini 2.5 Flash** (Google) et **GPT-4o** (OpenAI).
   * Gestion des quotas et retrys automatique en cas de dépassement.

---

## ⚙️ Installation

1. **Cloner le projet**

```bash
git clone https://github.com/Haja-NRN/PaperMind.git
cd PaperMind
```

2. **Créer un environnement Python**

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Ajouter vos clés API**

* Pour **Gemini 2.5 Flash** :

```bash
export GOOGLE_API_KEY="VOTRE_API_KEY"
```

* Pour **GPT-4o (OpenAI)** :

```bash
export OPENAI_API_KEY="VOTRE_API_KEY"
```

---

## 🖥️ Utilisation

### 1. Lancer le programme

```bash
python main.py
```

### 2. Sélection du modèle

* Le programme demande de choisir **Gemini 2.5 Flash** ou **GPT-4o**.

### 3. Importer un PDF

* Entrez le chemin du PDF dans le terminal.
* Une barre de progression s’affiche pendant le résumé.

### 4. Chat interactif

* Posez vos questions en se basant sur le contenu du PDF.
* Tapez `exit` pour quitter le chat.

---

## 💡 Exemple d’usage

```bash
📂 Entrez le chemin du fichier : ./documents/rapport.pdf
Résumé en cours... █████████████████████ 100%
🎉 Résumé terminé avec succès !

Me: Quelle est la conclusion du rapport ?
Gemini : La conclusion du rapport indique que...
```

---

## 🛠️ Technologies utilisées

* **Python 3.10+**
* **LangChain** → gestion des modèles et des prompts.
* **pypdf** → lecture des PDF.
* **Rich** → affichage stylisé, barre de progression et titres.
* **PyFiglet** → titres ASCII stylisés.
* **Gemini 2.5 Flash** (Google) et **GPT-4o** (OpenAI).

---

## 🔧 Personnalisation

* Changer le modèle par défaut :

  * `model_provider="google_genai"` pour Gemini
  * `model_provider="openai"` pour GPT-4o
* Modifier la stratégie de résumé ou le prompt système selon vos besoins.

---

## 📂 Structure du projet

```
pdf-chat-cli/
│
├── main.py           # Script principal
├── requirements.txt  # Dépendances Python
├── README.md
└── utils.py          # Fonctions utilitaires (PDF, prompt, etc.)
```

---

## ⚠️ Limitations

* Quotas API Gemini et GPT → risque d’erreur `429` si trop de requêtes.
* La qualité du résumé dépend de la taille et de la complexité du PDF.
* Les PDFs très lourds (>200 pages) peuvent ralentir le processus et requierent beaucoup plus de requete.

---

## 📜 Licence

MIT License – voir `LICENSE` pour plus de détails.
