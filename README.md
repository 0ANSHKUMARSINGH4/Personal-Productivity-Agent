# Personal Productivity Agent ⚡

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google%20Gemini%20API-genai-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An intelligent, modular **Personal Productivity Agent** powered by Python, Streamlit, and Google's Gemini API. Designed to help users streamline task prioritization, build hour-by-hour daily time-blocked schedules, generate multi-phase academic study roadmaps, and receive daily performance summaries with AI coaching.

---

## 🌟 Key Features

- **📋 Task Management & AI Priority Matrix**:
  - Full CRUD operations with priority tags (`High`, `Medium`, `Low`), categories, deadlines, and estimated completion hours.
  - One-click **Eisenhower Matrix** breakdown (*Do First*, *Schedule*, *Delegate*, *Reconsider*) and optimal step-by-step execution sequence.
- **📅 Daily AI Time-Blocking Planner**:
  - Automatically transforms pending task lists into realistic, hour-by-hour time-blocked agendas.
  - Tailored to user-defined working hours, lunch slots, and rest preferences to prevent cognitive burnout.
- **🎓 AI Study Schedule Generator**:
  - Generates multi-phase academic roadmaps (*Concept Mastery*, *Practice & Application*, *Final Revision*).
  - Includes active recall techniques (Feynman technique, spaced repetition) and daily Pomodoro routines.
- **🎯 Goal Summarizer & AI Productivity Coach**:
  - Analyzes completed vs. pending tasks alongside user reflections.
  - Calculates a **Daily Productivity Score (1–100)** with key achievement highlights and 3 actionable goals for tomorrow.
- **💾 Local Data Persistence**:
  - Auto-saves all user tasks locally to `tasks_data.json` for seamless cross-session task tracking.
- **🎨 Glassmorphic Modern Interface**:
  - Customized Streamlit UI with vibrant gradient banners, dark-mode cards, metric chips, and instant `.md` file export buttons.

---

## 🧠 AI Model Architecture, Resilience & Stress Testing

To ensure peak performance and 99.9% uptime, the agent features a **resilient model execution engine** in `planner.py`:

### 🛡️ Multi-Tier Model Fallback Cascade
The agent dynamically negotiates with Google Gemini endpoints across a prioritized model cascade:
1. **`gemini-2.0-flash`**: Primary model optimized for rapid response times and high instruction compliance.
2. **`gemini-2.0-flash-lite`**: Lightweight fallback tier for maximum quota efficiency.
3. **`gemini-1.5-flash`**: Stable fallback for legacy environments.
4. **`gemini-2.5-flash`**: Next-generation flash model integration.

### 🔄 Exponential Backoff & Fault Tolerance
- **Rate-Limit Guard**: Automatically intercepts HTTP `429 RESOURCE_EXHAUSTED` errors and executes exponential backoff retries (sleep & retry).
- **Graceful Error Handling**: Non-blocking failovers ensure the Streamlit UI remains responsive even during API quota window resets.

### 🧪 Stress Testing & Performance Benchmark
The core API engine was subjected to automated multi-capability stress testing under heavy workloads:

| Test Benchmark | Target Capability | Avg. Output Length | Resilience Status |
| :--- | :--- | :---: | :---: |
| **Eisenhower Matrix** | Multi-Task Prioritization | ~1,800 chars | ✅ Verified |
| **Time-Blocking Agenda** | Daily Schedule Allocation | ~2,200 chars | ✅ Verified |
| **Study Roadmap** | Academic Phase Generation | ~2,500 chars | ✅ Verified |
| **Goal Wrap-Up** | Scoring & AI Coaching | ~1,600 chars | ✅ Verified |

---

## 📁 Project Structure

```
Personal-Productivity-Agent/
├── app.py              # Streamlit web app UI & interactive tabs
├── planner.py          # Gemini API wrapper, model cascade & task persistence
├── prompts.py          # Centralized prompt templates & prompt builders
├── requirements.txt    # Project dependencies
├── .env.example        # Environment variable reference template
├── README.md           # Project documentation
└── .gitignore          # Git exclusion entries
```

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/0ANSHKUMARSINGH4/Personal-Productivity-Agent.git
cd Personal-Productivity-Agent
```

### 2. Create & Activate Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your Gemini API Key
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Get a free API key from [Google AI Studio](https://aistudio.google.com/))*

### 5. Launch the Application
```bash
streamlit run app.py
```
The app will automatically open in your browser at `http://localhost:8501`.

---

## 💡 How to Use

1. **Task Manager**: Add your tasks with categories, priorities (`High`/`Medium`/`Low`), deadlines, and estimated hours.
2. **Prioritize Work**: Click **⚡ Run AI Priority Analysis** to view your Eisenhower Matrix and execution plan.
3. **Generate Agenda**: Switch to **📅 Daily AI Planner**, configure your day bounds, and click **🗓️ Generate AI Daily Schedule**.
4. **Build Study Plan**: Open **🎓 Study Schedule Generator**, enter subjects and target exam date for a customized roadmap.
5. **Daily Wrap-Up**: End your day in **🎯 Goal Summarizer & AI Coach** to view your daily score, reflection feedback, and tomorrow's goals.

---

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **Frontend Framework**: Streamlit
- **Generative AI SDK**: `google-genai` (Google Gemini API)
- **Environment Management**: `python-dotenv`
- **Data Persistence**: Local JSON Storage (`tasks_data.json`)

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
