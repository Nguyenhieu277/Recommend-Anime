import streamlit as st
import ollama
from InputProcessing import InputProcessor
from anime_list import AniList
import time

processor = InputProcessor()

ListAnime = AniList()

def isAnimeRelated(query):
    keywords = ["recommend", "anime", "watch", "genres", "score", "hobby", "series"]
    return any(word in query.lower() for word in keywords)

if "messages" not in st.session_state:
    st.session_state.messages = []
def generate_response(prompt):
    if isAnimeRelated(prompt):
        processed = processor.process_input(prompt)
        genres = set(processed["genres"])
        min_score = processed["min_score"]
            
        recommendations = ListAnime.recommend_anime(genres, min_score)
        
        if recommendations:
            bot_response = (
                "Here are some anime recommendations:\n\n" + 
                "\n".join(
                    f"- Title: {anime.get('title_english', anime.get('title_romaji', 'N/A'))}\n"
                    f"  Description: {anime.get('description', 'No description available')}\n"
                    f"  Genres: {', '.join(anime.get('genres', []))}\n"
                    f"  Average Score: {anime.get('averageScore', 'N/A')}\n"
                    f"  Episodes: {anime.get('episodes', 'N/A')}\n"
                    for anime in recommendations
                )
            )
        else:
            bot_response = "I couldn't find any anime matching your criteria. Try being more specific!"
    else:
        bot_response = ollama.chat(model = 'llama3', stream=True, messages=st.session_state.messages)
    return bot_response

def handle_input():
    user_input = st.session_state.input_text
    if user_input:
        response = generate_response(user_input)

        st.session_state.messages.append({"user" : user_input, "assistant" : response})
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
    # Check if assistant's response exists
    if current_chat['assistant']:
        response_words = current_chat['assistant'].split()
        displayed_response = ""

        # Display response character by character
        for word in response_words:
            displayed_response += word + " "
            assistant_response.markdown(f"""
            <div style="display: flex; justify-content: flex-end; color: white;">
                <div style="background-color: rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
                    <strong>Assistant:</strong> {displayed_response}
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.1)  # Simulate typing effect
    else:
        assistant_response.markdown("<div style='color: white;'>Assistant has no response yet...</div>", unsafe_allow_html=True)

    # Input from user at the bottom of the screen
st.text_input("You: ", key="input_text", on_change=handle_input)