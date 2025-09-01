import getpass
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
import json

# if not os.environ.get("GOOGLE_API_KEY"):
#   os.environ["GOOGLE_API_KEY"] = input("Enter API key for Google Gemini: ")


os.environ["GOOGLE_API_KEY"] = "AIzaSyBJ6vIhn58QllNa8Al4YECrmymbT0zerAY"

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
# messages = [
#     SystemMessage(content="Retourner la reponse en list seulement"),
#     HumanMessage(content="Fais un cahier de charge de comment faire un site web chat en temps reel au niveau backend"),
# ]
messages = [
    SystemMessage(content="Retourner la reponse en list seulement"),
    HumanMessage(content="Comment devenir Dieu"),
]
response=model.invoke(messages).model_dump_json()
content=json.loads(response)

dialogue=content.pop("content")

print(
    dialogue
)
