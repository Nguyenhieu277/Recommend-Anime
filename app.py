import streamlit as st
from Ollama_client import OllamaClient
from InputProcessing import InputProcessor
from anime_list import AniList
import time

processor = InputProcessor()
Ollama = OllamaClient("llama3")
ListAnime = AniList()

def isAnimeRelated(query):
    keywords = ["recommend", "anime", "watch", "genres", "score", "hobby", "series"]
    return any(word in query.lower() for word in keywords)

if "messages" not in st.session_state:
    st.session_state.message = []
def generate_response(prompt):
    if isAnimeRelated(prompt):
        processed = processor.process_input(prompt)
        genres = set(processed["genres"])
        min_score = processed["min_score"]
            
        recommendations = ListAnime.recommend_anime(genres, min_score)
        
        if recommendations:
            bot_response = "Here are some anime recommendations:\n" + "\n".join(f"- {anime}" for anime in recommendations)
        else:
            bot_response = "I couldn't find any anime matching your criteria. Try being more specific!"
    else:
        bot_response = Ollama.generate_text(prompt)
    return bot_response

def handle_input():
    user_input = st.session_state.input_text
    if user_input:
        response = generate_response(user_input)

        st.session_state.message.append({"user" : user_input, "content" : response})
        st.session_state.input_text = ""
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    # Display the chat history
for chat in st.session_state.messages[:-1]:
    st.markdown(f"""
    <div style="display: flex; justify-content: flex-start; color: white;">
        <div style="background-color:rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
            <strong>You:</strong> {chat['user']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display: flex; justify-content: flex-end; color: white;">
        <div style="background-color: rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
            <strong>Assistant:</strong> {chat['assistant']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Placeholder for the current assistant's response, displayed in real-time
if st.session_state.messages:
    current_chat = st.session_state.messages[-1]
    st.markdown(f"""
    <div style="display: flex; justify-content: flex-start; color: white;">
        <div style="background-color: rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
            <strong>You:</strong> {current_chat['user']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    assistant_response = st.empty()
    response_words = current_chat['assistant'].split()
    displayed_response = ""

    for word in response_words:
        displayed_response += word + " "
        assistant_response.markdown(f"""
        <div style="display: flex; justify-content: flex-end; color: white;">
            <div style="background-color: rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
                <strong>Assistant:</strong> {displayed_response}
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.1)

    # Input from user at the bottom of the screen
st.text_input("You: ", key="input_text", on_change=handle_input)