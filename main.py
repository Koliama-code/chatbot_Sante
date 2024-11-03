import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Configuration de la page
st.set_page_config(page_title="Assistant Santé", page_icon="💡", layout="centered")

# Ajouter une signature en haut à gauche
st.markdown("""
    <style>
        /* Style de la signature */
        .signature { 
            font-size: 0.85em; 
            color: #78909c; 
            position: absolute;
            top: 10px;
            left: 10px;
            font-family: Arial, sans-serif;
        }
        /* Style de la boîte de chat */
        .stChatMessage--AI { 
            background-color: #e0f7fa; 
            color: #006064;
            border-radius: 8px;
            padding: 10px; 
            margin-bottom: 5px;
        }
        .stChatMessage--Human { 
            background-color: #c8e6c9; 
            color: #2e7d32; 
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 5px;
            text-align: right;
        }
        /* Style général de la page */
        .main { 
            background-color: #f1f8e9; 
            padding: 20px; 
            font-family: Arial, sans-serif;
        }
    </style>
    <div class='signature'>by KOLIAMA</div>
""", unsafe_allow_html=True)

# Titre de l'application
st.title("💬 Bienvenue chez votre Assistant Santé")
st.write("Que puis-je faire pour vous aujourd'hui pour une santé optimale ?")

# Initialiser l'historique de la conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Fonction pour obtenir une réponse
def get_response(query, chat_history):
    template = """
     Tu es un assistant de santé alors tu es fait pour répondre à toutes les questions concernant la santé.
     
     Chat history: {chat_history}
     
     User question: {user_question}
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        temperature=0
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "chat_history": chat_history,
        "user_question": query
    })

# Affichage des messages
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

# Saisie utilisateur
user_query = st.chat_input("Votre message ici...")

if user_query:
    st.session_state.chat_history.append(HumanMessage(user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
    
    with st.chat_message("AI"):
        ai_response = get_response(user_query, st.session_state.chat_history)
        st.markdown(ai_response)
        
    st.session_state.chat_history.append(AIMessage(ai_response))
