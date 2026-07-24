# Personal Productivity Agent ⚡

An AI-powered daily task manager, time-blocking planner, study schedule generator, and productivity coach built with **Python**, **Streamlit**, and the **Google Gemini API**.

---

## 🌟 Key Features

- **📋 Interactive Task Manager & AI Prioritizer**:
  - Add, filter, categorize, and prioritize daily tasks.
  - Generates Eisenhower Matrix analysis (Do First, Schedule, Quick Wins, Reconsider) and optimal execution sequences using Gemini.
- **📅 Daily AI Time-Blocking Planner**:
  - Automatically transforms pending tasks into an hour-by-hour structured daily schedule tailored to user-specified working hours and break preferences.
- **🎓 AI Study Schedule Generator**:
  - Creates custom academic study roadmaps, phase-by-phase prep schedules, Pomodoro routines, and active recall strategies based on subjects, exam dates, and daily study hours.
- **🎯 Goal Summarizer & AI Productivity Coach**:
  - Evaluates daily completed vs. pending tasks, processes reflections, and computes a productivity score (1-100) with actionable recommendations for tomorrow.
- **💾 Local Persistence**:
  - Automatically saves tasks to a local `tasks_data.json` file so progress is preserved across sessions.
- **🎨 Sleek Modern UI**:
  - Dark mode aesthetic, metric badges, responsive layout, glassmorphic UI elements, and instant markdown downloads for plans and summaries.

---

## 📁 Project Structure

```
Personal-Productivity-Agent/
├── app.py              # Streamlit dashboard & user interface
├── planner.py          # Gemini API wrapper, core business logic & data persistence
├── prompts.py          # Structured prompt templates for AI features
├── requirements.txt    # Python dependencies
├── README.md           # Documentation
└── .gitignore          # Git exclusion rules
```

---

## 🚀 Quick Start & Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/0ANSHKUMARSINGH4/Personal-Productivity-Agent.git
cd Personal-Productivity-Agent
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get a Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Create an API key.
3. Either create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   Or input your API key directly in the app's sidebar UI!

### 5. Launch the Application
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 💡 How to Use

1. **Configure API Key**: Enter your Gemini API Key in the left sidebar.
2. **Add Tasks**: Go to `📋 Task Manager & AI Prioritizer` to input tasks with deadlines, estimated hours, and categories.
3. **Analyze Priorities**: Click **⚡ Run AI Priority Analysis** to see the Eisenhower matrix and task sequence.
4. **Time-Block Your Day**: Open `📅 Daily AI Planner` to generate an hour-by-hour daily schedule.
5. **Generate Study Plan**: Open `🎓 Study Schedule Generator`, enter your subjects and target exam date for a multi-phase study plan.
6. **Daily Wrap-Up**: Open `🎯 Goal Summarizer & AI Coach` to get your daily score, accomplishments summary, and coaching advice.

---

## 🛠️ Built With

- **[Python 3.9+](https://www.python.org/)**
- **[Streamlit](https://streamlit.io/)**
- **[Google Gemini API (`google-genai`)](https://github.com/googleapis/python-genai)**
- **[python-dotenv](https://github.com/theskumar/python-dotenv)**

---

## 📄 License

This project is licensed under the MIT License - feel free to use and customize for your productivity needs!
