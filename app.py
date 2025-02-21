import streamlit as st
from InputProcessing import InputProcessor
from anime_list import AniList
import time
import random
import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()
api_key = st.secrets["GITHUB_TOKEN"]
class OpenAIClient:
    def __init__(self):
        self.token = api_key
        self.endpoint = "https://models.inference.ai.azure.com"
        self.model_name = "gpt-4o"
        try:
            self.client = OpenAI(
                base_url=self.endpoint,
                api_key=self.token,
            )
        except OpenAIError as e:
            print(f"Failed to initialize OpenAI client: {e}")
            self.client = None

    def get_response(self, messages, temperature=1.0, top_p=1.0, max_tokens=1000):
        if not self.client:
            return "OpenAI client is not initialized."
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                model=self.model_name
            )
            html_response = f"<p>{response.choices[0].message.content}</p>"
            
            return html_response
        except OpenAIError as e:
            return f"Failed to get response from OpenAI: {e}"

processor = InputProcessor()
client = OpenAIClient()
ListAnime = AniList()
greeting_responses = {  
    "hello": ["Hello! How can I assist you today?", "Hi there! How can I help you?", "Hello! What can I do for you today?"],
    "hi": ["Hi! How's it going?", "Hey! How can I assist you?", "Hello! What's up?"],
    "hey": ["Hey there! How can I help?", "Hi! What's on your mind?", "Hey! Need help with something?"],
    "good morning": ["Good morning! How can I help you today?", "Morning! What can I do for you?", "Good morning! How’s everything?"],
    "good afternoon": ["Good afternoon! How’s your day going?", "Afternoon! How can I assist?", "Good afternoon! What can I do for you?"],
    "good evening": ["Good evening! How can I help?", "Evening! What’s up?", "Good evening! How can I assist you tonight?"],
    "how are you": ["I'm doing great, thank you for asking! How about you?", "I'm here and ready to assist! How are you?", "I'm good! How can I help you today?"],
    "what's up": ["Not much! How can I assist you?", "Hey! What can I do for you?", "Not much, just here to help! What's up with you?"],
    "how's it going": ["It’s going great! How about you?", "I’m doing well, thanks! How’s everything on your end?", "I’m doing great! How can I help?"],
    "yo": ["Yo! What’s up?", "Hey yo! How can I assist you?", "Yo! Need help with something?"],
    "sup": ["Sup! How can I help you?", "Hey! What's going on?", "Not much, just here to help! What’s up?"],
    "hey there": ["Hey there! How can I assist you today?", "Hi there! What can I do for you?", "Hey there! How's it going?"],
    "greetings": ["Greetings! How can I assist you?", "Hello! How can I help today?", "Hi! What can I do for you?"],
    "salutations": ["Salutations! How can I assist you today?", "Greetings! How can I help?", "Salutations! What’s on your mind?"],
    "hi there": ["Hi there! How’s everything?", "Hello! How can I help you?", "Hi there! Need any assistance?"],
    "howdy": ["Howdy! How can I assist you?", "Howdy! What’s up?", "Howdy! What can I do for you today?"],
    "what's new": ["Not much! How about you?", "Same old, same old! What’s new with you?", "Nothing much, just here to help! What's new with you?"],
    "long time no see": ["It’s been a while! How can I assist?", "Long time no see! How’s everything?", "Hey there! What can I help you with today?"],
    "good day": ["Good day! How can I assist you?", "Hello! What’s on your mind?", "Good day! How can I help today?"],
    "bonjour": ["Bonjour! How can I assist?", "Bonjour! How are you today?", "Bonjour! What can I do for you?"],
    "hola": ["Hola! How can I assist you?", "Hola! ¿Cómo estás?", "Hola! What can I do for you today?"],
    "g'day": ["G'day! How can I help?", "G'day! What can I do for you?", "G'day! How’s everything going?"],
    "how do you do": ["I’m doing great, thanks! How about you?", "I’m doing well, thank you for asking!", "I’m doing well! How are you today?"],
    "nice to meet you": ["Nice to meet you too! How can I assist?", "It's great to meet you! How can I help?", "Nice to meet you! What can I do for you?"]
}

def isRelatedAnime(query):
    keywords = ["like","love","recommend","suggest","good","best","popular","top","watch","series","movie","anime","genre","list","favorites"]
    return any(keyword in query.lower() for keyword in keywords)
def isGreetings(query):
    greetings = [
        "hello", "hi", "hey", "good morning", "good afternoon", "good evening", 
        "how are you", "what's up", "how's it going", "yo", "sup", "hey there", 
        "greetings", "salutations", "hi there", "howdy", "what's new", "long time no see", 
        "good day", "bonjour", "hola", "g'day", "how do you do", "nice to meet you"
    ]
    return any(keyword in query.lower() for keyword in greetings)

def generate_response(prompt):
    processed = processor.process_input(prompt)
    genres = set(processed["genres"])
    tags = set(processed["tags"])
    min_score = processed["min_score"]
            
    recommendations = ListAnime.recommend_anime(tags, genres, min_score)
       
    if not recommendations:
        return 0
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
    if isRelatedAnime(user_input):
        if user_input:
            response = generate_response(user_input)
            if response == 0:
                response = client.get_response([
                    { 
                        "role" : "system", 
                        "content" : "You are a helpful assistant." 
                     },
                    {
                        "role": "system",
                        "content": "You are a helpful assistant to recommend some good anime",
                    },
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ])
        st.session_state.messages.append({"user" : user_input, "assistant" : response})
        st.session_state.input_text = ""
        

    elif isGreetings(user_input):
        # Check for the greeting and return a random response
        greeting = next((greeting for greeting in greeting_responses if greeting in user_input.lower()), None)
        if greeting:
            response = random.choice(greeting_responses[greeting])
        else:
            response = "Hello! How can I assist you today?"
        
        st.session_state.messages.append({"user": user_input, "assistant": response})
        st.session_state.input_text = ""
    else: 
        response = client.get_response([
        {
            "role": "system",
            "content": "You are a helpful assistant",
        },
        {
            "role": "user",
            "content": user_input,
        }
    ])
        st.session_state.messages.append({"user": user_input, "assistant": response})
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