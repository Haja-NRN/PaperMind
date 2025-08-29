import getpass
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = input("Enter API key for Google Gemini: ")



model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
messages = [
    SystemMessage(content="Retourner la reponse en format json seulement"),
    HumanMessage(content="Donnez 5 nom d'aliment et son type que ce soit fruit ou legume"),
]

print(model.invoke(messages))