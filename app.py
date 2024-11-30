import streamlit as st
from streamlit_chat import message
from Ollama_client import OllamaClient
from InputProcessing import InputProcessor
from anime_list import AniList

processor = InputProcessor()
Ollama = OllamaClient("llama3")
ListAnime = AniList()

def isAnimeRelated(query):
    keywords = ["recommend", "anime", "watch", "genres", "score", "hobby", "series"]
    return any(word in query.lower() for word in keywords)

def handle_input():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{
            "role" : "bot",
            "content" : "Hello! How can I help you?"
        }]
        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                message(msg["content"], is_user=True)
            else:
                message(msg["content"])
        
        user_input = st.text_input("Your messages: ", "")
        
        if st.button("Send"):
            if not user_input.strip():
                st.error("Please enter a valid message !!!!!")
            else:
                st.session_state["messages"].append({"role" : "user", "content" : user_input})

                if isAnimeRelated(user_input):
                    try:
                        processed = processor.process_input(user_input)
                        genres = set(processed["genres"])
                        minScore = processed["min_score"]

                        recommendations = ListAnime.recommend_anime(genres, minScore)

                        if recommendations:
                            bot_response = "Here are some anime recommendations:\n" + "\n".join(f"- {anime}" for anime in recommendations)
                        else:
                            bot_response = "I couldn't find any anime with your discrpitions. Try being more specific!"
                    except Exception as e:
                        bot_response = f"An error occurred while processing your request: {str(e)}"
                
                else:
                    try:
                        bot_response = Ollama.generate_text(user_input)
                    except Exception as e:
                        bot_response = f"An error occurred while generating a response: {str(e)}"
                    
                st.session_state["messages"].append({"role" : "bot", "content" : bot_response})
                st.session_state.input_text = ""

        
