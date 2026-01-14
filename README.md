# VibeTune-AI-Music-Suggester
An intelligent music recommendation engine built with LangGraph and OpenAI that analyzes user descriptions to detect mood and age, providing personalized song suggestions.
# 🎵 VibeTune: AI-Powered Music Suggester

VibeTune is a specialized recommendation engine that uses Large Language Models (LLMs) and graph-based orchestration to suggest songs based on a user's current "vibe." Unlike traditional algorithms, it analyzes the emotional context and estimated age demographic from a short text description to find the perfect track.

## 🚀 Features
- **Mood Analysis**: Uses structured LLM output to categorize feelings into states like Happy, Sad, Energetic, or Heartbroken.
- **Demographic Guessing**: Estimates the user's age to tailor song eras (e.g., 80s, 2000s, Recent).
- **Stateful Graph Orchestration**: Built using **LangGraph** to manage the flow from initial insight gathering to specific category-based song selection.
- **Structured Data**: Implements **Pydantic** schemas for consistent, error-free song metadata (Artist, Album, Genre, Era).

## 🛠️ Technical Stack
- **Orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph)
- **LLM**: OpenAI GPT models (configured for structured output)
- **UI Framework**: Streamlit
- **Schema Validation**: Pydantic
- **Environment Management**: Python-dotenv

## 📋 How It Works
The application follows a directed acyclic graph (DAG):
1. **Input**: User provides a description of their day or feelings.
2. **Insights Node**: The LLM extracts `age` and `mood` from the text.
3. **Router**: A conditional edge (`checkmood`) directs the flow to the appropriate suggester node based on the detected mood.
4. **Suggester Nodes**: Specific nodes for Happy, Sad, Energetic, or Heartbroken vibes generate a tailored song recommendation.
5. **Output**: Returns a structured song object including artist, album, and genre.

## ⚙️ Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/hardslugger/VibeTune-AI-Music-Suggester
