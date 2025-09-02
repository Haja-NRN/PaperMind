import os

from google.api_core.exceptions import ResourceExhausted
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from pypdf import PdfReader
from rich.panel import Panel
from rich.progress import Progress
from rich.console import Console
from rich.text import Text
import pyfiglet
from yaspin import yaspin
import inquirer


# === Configuration ===
os.environ["GOOGLE_API_KEY"] = "AIzaSyBJ6vIhn58QllNa8Al4YECrmymbT0zerAY"
os.environ["OPENAI_API_KEY"] = "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"

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

# Fonction de titre
def cli_title(text: str):
    # Gros titre ASCII art
    banner = pyfiglet.figlet_format(text)
    console.print(f"[bold cyan]{banner}[/bold cyan]", justify="center")

    # Présentation brève
    presentation = Text(
        f"Bienvenue dans [bold magenta]Gemini CLI Project[/bold magenta] 🚀\n"
        "Un outil en ligne de commande pour :\n"
        " - 📂 Importer et résumer vos PDF\n"
        " - 🤖 Discuter avec Gemini en mode chat\n"
        " - ⚡ Fournir des réponses rapides et contextuelles\n",
        justify="center",
    )

    panel = Panel(
        presentation,
        border_style="bright_blue",
        title="ℹ️ Présentation",
        padding=(1, 2),
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
    cli_title("MyApp CLI")
    main()
