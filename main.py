import os
import platform

from google.api_core.exceptions import ResourceExhausted
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from pypdf import PdfReader
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
import pyfiglet
from yaspin import yaspin
import inquirer
from dotenv import load_dotenv

# === Configuration ===
# Charge les variables d'environnement depuis .env
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

console = Console()

# Contexte global (conversation + résumé PDF)
my_context = """Tu es un chatbot humain qui répond naturellement 
et continue la conversation sans jamais mentionner que tu es une IA. 
Réponds comme si nous discutions en temps réel. 
Ta mémoire est la conversation ci-dessous :"""

# === Fonctions utilitaires ===
def load_model(modele):
    if modele=="GPT-4O MINI":
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
    elif modele=="GEMINI 2.5 flash":
        model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    else:
        return None
    return  model

# Effacer le terminal
def clear_terminal():
    # Windows → 'cls', Linux/Mac → 'clear'
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
# Fonction de titre
def cli_title(project_name: str, author: str):
    # Gros titre ASCII
    banner = pyfiglet.figlet_format(project_name,font="3-d")
    console.print(f"[bold cyan]{banner}[/bold cyan]", justify="center")

    # Présentation brève adaptée
    # Présentation directement en markup Rich
    panel_content = (
        f"Bienvenue dans [bold magenta]{project_name}[/bold magenta] 🚀\n\n"
        "Un outil en ligne de commande qui vous permet :\n"
        " - 📂 D'importer et résumer automatiquement vos fichiers PDF\n"
        " - 🤖 De discuter avec des modèles IA : Gemini 2.5 Flash ou GPT-4o\n"
        " - ⚡ D'obtenir des réponses contextuelles basées sur le contenu du PDF\n\n"
        f"Créé par [bold green]{author}[/bold green]"
    )

    # Affichage dans un panel stylé
    panel = Panel(
        panel_content,
        border_style="bright_blue",
        title="ℹ️ Présentation du projet",
        padding=(1, 2),
        highlight=True,
    )
    console.print(panel, justify="center")

def ask_file():
    """Demande à l'utilisateur un fichier existant et renvoie son chemin absolu."""
    file_path = input("📂 Entrez le chemin du fichier : ").strip()

    if os.path.isfile(file_path):
        abs_path = os.path.abspath(file_path)
        console.print(f"✅ Fichier trouvé : {abs_path}", style="green")
        return abs_path
    elif not file_path:
        return None
    else:
        console.print("❌ Fichier introuvable.", style="red")
        return None


def resume_pdf(path: str,model) -> str:
    """Lit et résume chaque page du PDF, retourne un texte consolidé."""
    pdf_content = ""
    reader = PdfReader(path)
    nb_pages = len(reader.pages)
    i=0
    console.print(f"📄 Le PDF contient {nb_pages} pages.", style="bold cyan")
    with yaspin(text=f"Loading {i + 1}/{nb_pages}", color="red") as spinner:
        for i, page in enumerate(reader.pages):
            try:
                # Ajout du spinner dans le terminal
                text = page.extract_text() or ""

                messages = [
                            SystemMessage(content="Résumez le texte suivant de façon concise :"),
                            HumanMessage(content=text),
                        ]
                try:
                    resume = model.invoke(messages).content
                except Exception as e:
                    print(e)
                    break
                pdf_content += resume + "\n"
                i+=1
                spinner.text=f"Loading {i }/{nb_pages}"
            except Exception as e:
                console.print(f"❌ Erreur à la page {i+1}: {e}", style="red")
    spinner.ok("✅ ")
    return pdf_content.strip()


def prompt(user_input: str,model) -> str:
    """Construit le contexte et génère la réponse du chatbot."""
    global my_context

    my_context += f"\nHuman: {user_input}\nBot:"

    messages = [
        SystemMessage(content=my_context),
        HumanMessage(content=user_input),
    ]

    response = model.invoke(messages).content
    my_context += response  # on enrichit la mémoire
    return response


# === Programme principal ===
def main():
    global my_context
    # Choix du modele
    questions = [
        inquirer.List(
            "choix",
            message="Sélectionne un modèle :",
            choices=["GPT-4O MINI","GEMINI 2.5 flash"],
        ),
    ]

    answers = inquirer.prompt(questions)

    model=load_model(answers["choix"])
    # Charger un document si nécessaire
    file_path = ask_file()
    if file_path:
        pdf_content = resume_pdf(file_path,model)
        my_context += (
            f"\n⚡ Voici le sujet de référence, limite-toi à ce contenu :\n{pdf_content}"
        )

    # Boucle de chat
    while True:
        console.print(f"[bold gray]Human:[/bold gray]",end=" ")
        user_input = input()
        if user_input.lower() == "exit":
            break
        bot_reply = prompt(user_input,model)
        console.print(f"[bold magenta]Gemini:[/bold magenta] {bot_reply}")


if __name__ == "__main__":
    clear_terminal()
    cli_title("PaperMind", "Haja Nirina")
    main()
