import getpass
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from pypdf import PdfReader
import json


os.environ["GOOGLE_API_KEY"] = "AIzaSyBJ6vIhn58QllNa8Al4YECrmymbT0zerAY"

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

my_context = """Repond comme un vrai chatbot et continuez la conversation suivante en retournant seulement la meilleur reponse au Human en prennant compte de la dialogue en bas comme ta memoire si c'est disponible mais ne dis jamais que tu es un IA et fais comme si on s'envoie des message et on parle seulement que de la :"""

# Fonction pour demander le chemin du fichier
def ask_file():
    while True:
        file_path = input("📂 Entrez le chemin du fichier : ").strip()

        # Vérifie si le chemin existe
        if os.path.isfile(file_path):
            # Convertit en chemin absolu pour éviter les ambiguïtés
            abs_path = os.path.abspath(file_path)
            print(f"✅ Fichier trouvé : {abs_path}")
            return abs_path
        else:
            print("❌ Fichier introuvable, réessayez...")
            return False

def resume_pdf(path):
    pdf_content=""
    i=0
    # Lecture du pdf
    reader = PdfReader(path)

    # Nombre total de pages
    nb_pages = len(reader.pages)

    print(f"📄 Le PDF contient {nb_pages} pages.")
    while i<nb_pages:
        try:
            page = reader.pages[i]
            text = page.extract_text()

            # Demande de resumez la page donnee
            messages = [
                SystemMessage(content="Resumez le texte que je vous donne la"),
                HumanMessage(content=text),
            ]

            # Resumez de la page
            text = model.invoke(messages).content
            # Sauvegarde du texte de la page resumé
            pdf_content+=text
            print("✅ Page {}/{} resumé avec succés".format(i+1, nb_pages))
            i += 1

        except IndexError:
            break

    return pdf_content

def prompt(my_prompt):
    global my_context

    # On ajoute le prompt de l'utilisateur au context comme suit Human:prompt_user
    my_context = f"""{my_context} \nHuman : {my_prompt}\nBot:"""

    messages = [
        SystemMessage(content=my_context),
        HumanMessage(content=my_prompt),
    ]
    # Reponse du bot
    response = model.invoke(messages).content

    # Resumons la reponse du bot
    # resume = [
    #     SystemMessage(content="Resumez ce texte pour être plus concise mais si c'est deja concis alors retournez la tout simplement par ce que c'est pour"),
    #     HumanMessage(content=response),
    # ]

    # Concatenation de la reponse du bot au contexte
    my_context = f"""{my_context}{response}"""


    return response

def main():
    global my_context

    # Document utiliser pour recuperer des données
    file_path = ask_file()
    if file_path:
        pdf_content=resume_pdf(file_path)
        my_context = f"""{my_context}\nVous devez repondre en ce referant seulement au texte suivante mais faite comme si ce n'est que le sujet que tu connais  :{pdf_content}"""

    while True:
        human=input("Me:")
        if human.lower()=="exit":
            break
        bot=prompt(human)
        print(f"Gemini : {bot}")

if __name__=="__main__":
    main()