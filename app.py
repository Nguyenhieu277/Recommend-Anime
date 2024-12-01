import streamlit as st
from InputProcessing import InputProcessor
from anime_list import AniList
from openAI import OpenAIClient
import time

processor = InputProcessor()
client = OpenAIClient()
ListAnime = AniList()

if "messages" not in st.session_state:
    st.session_state.messages = []
def generate_response(prompt):
    processed = processor.process_input(prompt)
    genres = set(processed["genres"])
    min_score = processed["min_score"]
            
    recommendations = ListAnime.recommend_anime(genres, min_score)
       
    if recommendations == 0:
        messages = [
            {
                "role": "assistant",
                "content": "You are a helpful assistant to recommend anime",
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        bot_response = client.get_response(messages)
    # Safeguard and generate response
    bot_response = "".join(
        f"<div>"
        f"<h2>Title: {anime.get('title_english', anime.get('title_romaji', 'N/A'))}</h2>"
        f"<p><strong>Description:</strong> {anime.get('description', 'No description available')}</p>"
        f"<p><strong>Genres:</strong> {', '.join(anime.get('genres', []))}</p>"
        f"<p><strong>Average Score:</strong> {anime.get('averageScore', 'N/A')}</p>"
        f"<p><strong>Episodes:</strong> {anime.get('episodes', 'N/A')}</p>"
        f"</div><br>"
        if isinstance(anime, dict)
        else "<p>Don't have anime based on your description</p>"
        for anime in recommendations
    )
    return bot_response

def handle_input():
    user_input = st.session_state.input_text
    if user_input:
        response = generate_response(user_input)

        st.session_state.messages.append({"user" : user_input, "assistant" : response})
        st.session_state.input_text = ""

st.title("💬 Anime Recommender")
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    # Display the chat history
for chat in st.session_state.messages[:-1]:
    st.markdown(f"""
    <div style="display: flex; justify-content: flex-start; color: white;">
        <div style="background-color:rgba(0, 63, 142, 1); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
            <strong>You:</strong> {chat['user']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display: flex; justify-content: flex-end; color: white;">
        <div style="background-color: rgba(255, 63, 108, 0.4); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
            <strong>Assistant:</strong> {chat['assistant']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Placeholder for the current assistant's response, displayed in real-time
if st.session_state.messages:
    current_chat = st.session_state.messages[-1]
    st.markdown(f"""
    <div style="display: flex; justify-content: flex-start; color: white;">
        <div style="background-color: rgba(0, 63, 142, 1); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
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
            <div style="background-color: rgba(255, 63, 108, 0.4); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
                <strong>Assistant:</strong> {displayed_response}
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.1)

    # Input from user at the bottom of the screen
st.text_input("You: ", key="input_text", on_change=handle_input)