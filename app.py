import streamlit as st
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 1. Setup & Configuration
load_dotenv()
# Ensure your OPENAI_API_KEY is set in your .env file or environment variables

# Custom CSS for a beautiful "Spotify" look
st.set_page_config(page_title="VibeTune - Music Suggester", page_icon="🎵")

st.markdown("""
    <style>
    .main {
        background-color: #121212;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #1DB954;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1ed760;
        color: white;
    }
    .song-card {
        background-color: #181818;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1DB954;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Define the Graph Logic (from your notebook)
class Description(TypedDict):
    description: str
    age: int
    mood: str
    song: dict

class Insights(BaseModel):
    age: int
    mood: Literal["Happy", "Sad", "Heartbroken", "Energetic"] = Field(description="The mood of the user.")

class SongSchema(BaseModel):
    song: str
    artist: str
    album: str
    genre: str
    eraofmusic: str

# Initialize Model
model = ChatOpenAI(model='gpt-4o') # Recommended stable model
insights_model = model.with_structured_output(Insights)
song_model = model.with_structured_output(SongSchema)

# Node Functions
def get_insights(state: Description):
    res = insights_model.invoke(f"Analyze this description: {state['description']}")
    return {'age': res.age, 'mood': res.mood}

def suggest_song(state: Description):
    prompt = f"The user is {state['age']} years old and feeling {state['mood']}. Suggest a matching song."
    res = song_model.invoke(prompt)
    return {'song': res.model_dump()}

def check_mood(state: Description):
    return "suggest_song"

# Build Graph
workflow = StateGraph(Description)
workflow.add_node("get_insights", get_insights)
workflow.add_node("suggest_song", suggest_song)

workflow.add_edge(START, "get_insights")
workflow.add_edge("get_insights", "suggest_song")
workflow.add_edge("suggest_song", END)

app = workflow.compile()

# 3. Streamlit UI
st.title("🎵 VibeTune")
st.subheader("What's your story today? Let AI find the perfect track.")

user_input = st.text_area("Describe how you're feeling or what you're doing:", 
                          placeholder="e.g., I just finished a long day at work and want to relax...",
                          height=150)

if st.button("Generate Recommendation"):
    if user_input:
        with st.spinner('Analyzing the vibes...'):
            # Run the LangGraph
            initial_state = {"description": user_input}
            result = app.invoke(initial_state)
            
            # Display Results
            st.success(f"Detected Mood: **{result['mood']}** | Estimated Age: **{result['age']}**")
            
            song = result['song']
            st.markdown(f"""
                <div class="song-card">
                    <h2 style='color: #1DB954; margin:0;'>{song['song']}</h2>
                    <p style='font-size: 1.2em; margin:0;'>by <b>{song['artist']}</b></p>
                    <hr style='border-color: #333;'>
                    <p><b>Album:</b> {song['album']}</p>
                    <p><b>Genre:</b> {song['genre']} | <b>Era:</b> {song['eraofmusic']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
    else:
        st.warning("Please enter a description first!")