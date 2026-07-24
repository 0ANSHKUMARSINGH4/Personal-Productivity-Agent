"""
Personal Productivity Agent - Streamlit Application
A modern, AI-powered app to manage tasks, generate study plans, prioritize work, and summarize daily goals using Gemini.
"""

import os
from datetime import datetime, date
import streamlit as st
from dotenv import load_dotenv

from planner import TaskManager, GeminiPlanner

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Personal Productivity Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design Aesthetics
st.markdown("""
    <style>
    /* Main layout & background styling */
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Gradient Banner */
    .main-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
        padding: 24px 32px;
        border-radius: 16px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 10px 25px -5px rgba(7f, 38, 237, 0.3);
    }
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        font-size: 1.05rem;
        margin-top: 6px;
        opacity: 0.9;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Priority Badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-high { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .badge-medium { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .badge-low { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
    .badge-category { background: rgba(99, 102, 241, 0.2); color: #a5b4fc; border: 1px solid rgba(99, 102, 241, 0.4); }

    /* Task Box Container */
    .task-box {
        background: #1e293b;
        border-left: 4px solid #6366f1;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
        transition: all 0.2s ease;
    }
    .task-box-completed {
        background: #111827;
        border-left: 4px solid #10b981;
        opacity: 0.7;
    }

    /* Output Container */
    .ai-output-box {
        background: #171e2e;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin-top: 16px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize Session State & Core Objects
if "task_mgr" not in st.session_state:
    st.session_state.task_mgr = TaskManager()

task_mgr: TaskManager = st.session_state.task_mgr

# Sidebar Setup
with st.sidebar:
    st.title("⚡ AI Agent Settings")
    st.caption("Personal Productivity Assistant powered by Gemini API")
    
    st.markdown("---")
    
    # Initialize Gemini Planner from .env / Environment
    planner = GeminiPlanner()
    
    st.markdown("---")
    
    # Statistics Widget
    st.subheader("📊 Task Statistics")
    all_tasks = task_mgr.tasks
    total_count = len(all_tasks)
    completed_count = len([t for t in all_tasks if t.get("completed")])
    pending_count = total_count - completed_count
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{pending_count}</div><div class="metric-label">Pending</div></div>', unsafe_allow_html=True)
    with col_s2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{completed_count}</div><div class="metric-label">Completed</div></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Reset & Utility buttons
    if st.button("🗑️ Clear All Tasks", use_container_width=True, help="Delete all stored tasks permanently"):
        task_mgr.clear_all()
        st.rerun()
        
    st.markdown("---")
    st.caption("Developed with Python & Streamlit • 2026")


# Main Dashboard Header
st.markdown("""
    <div class="main-header">
        <h1>Personal Productivity Agent 🚀</h1>
        <p>AI-driven task management, daily time-blocking, study plan generation, and goal summarization.</p>
    </div>
""", unsafe_allow_html=True)


# Main Application Navigation Tabs
tab_tasks, tab_planner, tab_study, tab_goals = st.tabs([
    "📋 Task Manager & AI Prioritizer",
    "📅 Daily AI Planner",
    "🎓 Study Schedule Generator",
    "🎯 Goal Summarizer & AI Coach"
])


# ==========================================
# TAB 1: TASK MANAGEMENT & AI PRIORITIZER
# ==========================================
with tab_tasks:
    st.subheader("📋 Task Manager")
    
    # Form to add a new task
    with st.expander("➕ Add New Task", expanded=False):
        with st.form("add_task_form", clear_on_submit=True):
            col_f1, col_f2 = st.columns([2, 1])
            with col_f1:
                title = st.text_input("Task Title *", placeholder="e.g. Complete Machine Learning Assignment")
                description = st.text_area("Description / Notes", placeholder="Key details, links, or specific requirements...", height=80)
            with col_f2:
                category = st.selectbox("Category", ["Work", "Study", "Personal", "Health", "Finance", "Other"])
                priority = st.selectbox("Priority Level", ["High", "Medium", "Low"], index=1)
                deadline = st.date_input("Deadline", min_value=date.today()).strftime("%Y-%m-%d")
                est_hours = st.number_input("Estimated Hours", min_value=0.25, max_value=24.0, value=1.0, step=0.25)
                
            submitted = st.form_submit_button("Save Task", use_container_width=True)
            if submitted:
                if title.strip():
                    task_mgr.add_task(title, description, category, priority, deadline, est_hours)
                    st.success(f"Task '{title}' added successfully!")
                    st.rerun()
                else:
                    st.error("Task title cannot be empty!")

    st.markdown("---")

    # Task Filtering Options
    col_filter1, col_filter2, col_filter3 = st.columns([2, 2, 3])
    with col_filter1:
        filter_status = st.selectbox("Filter Status", ["All", "Pending Only", "Completed Only"])
    with col_filter2:
        filter_cat = st.selectbox("Filter Category", ["All Categories"] + list(set([t.get("category", "General") for t in all_tasks])))
    with col_filter3:
        st.write("") # Spacing
        run_priority_ai = st.button("⚡ Run AI Priority Analysis", type="primary", use_container_width=True)

    # Filter tasks list
    filtered_tasks = all_tasks
    if filter_status == "Pending Only":
        filtered_tasks = [t for t in filtered_tasks if not t.get("completed")]
    elif filter_status == "Completed Only":
        filtered_tasks = [t for t in filtered_tasks if t.get("completed")]
        
    if filter_cat != "All Categories":
        filtered_tasks = [t for t in filtered_tasks if t.get("category") == filter_cat]

    # Task List View
    st.write(f"### Current Tasks ({len(filtered_tasks)})")
    if not filtered_tasks:
        st.info("No tasks found matching your filters. Add some tasks above to get started!")
    else:
        for t in filtered_tasks:
            t_id = t["id"]
            is_completed = t.get("completed", False)
            p_class = f"badge-{t.get('priority', 'Medium').lower()}"
            
            col_chk, col_content, col_act = st.columns([0.5, 8, 1.5])
            
            with col_chk:
                if st.checkbox("", value=is_completed, key=f"chk_{t_id}"):
                    if not is_completed:
                        task_mgr.toggle_completed(t_id)
                        st.rerun()
                else:
                    if is_completed:
                        task_mgr.toggle_completed(t_id)
                        st.rerun()
                        
            with col_content:
                completed_style = "text-decoration: line-through; opacity: 0.6;" if is_completed else ""
                st.markdown(f"""
                    <div style="{completed_style}">
                        <strong>{t['title']}</strong> &nbsp;
                        <span class="badge {p_class}">{t.get('priority')}</span>
                        <span class="badge badge-category">{t.get('category')}</span>
                        <small style="color: #94a3b8; margin-left: 10px;">📅 Deadline: {t.get('deadline')} | ⏱️ {t.get('estimated_hours')}h</small>
                        {f'<div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">{t["description"]}</div>' if t.get("description") else ''}
                    </div>
                """, unsafe_allow_html=True)
                
            with col_act:
                if st.button("🗑️ Delete", key=f"del_{t_id}", use_container_width=True):
                    task_mgr.delete_task(t_id)
                    st.rerun()

    # AI Priority Matrix Output
    if run_priority_ai:
        if not planner.is_configured():
            st.error("⚠️ Please set your `GEMINI_API_KEY` in the `.env` file first!")
        elif not all_tasks:
            st.warning("Please add some tasks before generating priority recommendations.")
        else:
            with st.spinner("🤖 Gemini is analyzing your tasks and generating the priority matrix..."):
                analysis = planner.analyze_priorities(all_tasks)
                st.markdown("### 🎯 AI Priority Matrix & Execution Plan")
                st.markdown(f'<div class="ai-output-box">{analysis}</div>', unsafe_allow_html=True)


# ==========================================
# TAB 2: DAILY AI PLANNER & TIME-BLOCKING
# ==========================================
with tab_planner:
    st.subheader("📅 Daily Time-Blocking Generator")
    st.write("Let Gemini build a structured hour-by-hour agenda for your day based on your pending tasks.")
    
    col_p1, col_p2, col_p3 = st.columns([1, 1, 2])
    with col_p1:
        start_time = st.time_input("Day Start Time", value=datetime.strptime("09:00", "%H:%M").time()).strftime("%I:%M %p")
    with col_p2:
        end_time = st.time_input("Day End Time", value=datetime.strptime("17:00", "%H:%M").time()).strftime("%I:%M %p")
    with col_p3:
        break_pref = st.text_input("Break Preferences", value="15-min break every 90 mins, 45-min lunch at 1:00 PM")
        
    generate_plan = st.button("🗓️ Generate AI Daily Schedule", type="primary", use_container_width=True)
    
    if generate_plan:
        if not planner.is_configured():
            st.error("⚠️ Please set your `GEMINI_API_KEY` in the `.env` file first!")
        else:
            with st.spinner("⏳ Building your optimal daily time-blocked schedule..."):
                schedule_res = planner.generate_daily_schedule(all_tasks, start_time, end_time, break_pref)
                st.markdown("### ⏰ Today's AI Time-Blocked Schedule")
                st.markdown(f'<div class="ai-output-box">{schedule_res}</div>', unsafe_allow_html=True)
                st.download_button("📥 Download Schedule (.md)", data=schedule_res, file_name="daily_schedule.md", mime="text/markdown")


# ==========================================
# TAB 3: STUDY SCHEDULE GENERATOR
# ==========================================
with tab_study:
    st.subheader("🎓 AI Study Schedule & Roadmap Generator")
    st.write("Generate a structured academic prep plan with active recall tactics and micro-routines.")
    
    col_st1, col_st2 = st.columns([2, 1])
    with col_st1:
        subjects = st.text_input("Subjects / Topics to Cover *", placeholder="e.g. Data Structures, Linear Algebra, Machine Learning")
        focus_areas = st.text_area("Weak Areas / Specific Focus Topics", placeholder="e.g. Dynamic Programming graph algorithms, Eigenvalues & Eigenvectors", height=90)
    with col_st2:
        target_date = st.date_input("Exam / Target Goal Date", min_value=date.today()).strftime("%Y-%m-%d")
        daily_hours = st.slider("Available Daily Study Hours", min_value=1.0, max_value=12.0, value=4.0, step=0.5)
        
    generate_study = st.button("📚 Generate AI Study Plan", type="primary", use_container_width=True)
    
    if generate_study:
        if not planner.is_configured():
            st.error("⚠️ Please set your `GEMINI_API_KEY` in the `.env` file first!")
        elif not subjects.strip():
            st.error("Please provide at least one subject to study!")
        else:
            with st.spinner("🧠 Gemini is creating your customized study roadmap..."):
                study_plan = planner.generate_study_schedule(subjects, target_date, daily_hours, focus_areas)
                st.markdown("### 📖 Customized AI Study Plan")
                st.markdown(f'<div class="ai-output-box">{study_plan}</div>', unsafe_allow_html=True)
                st.download_button("📥 Download Study Plan (.md)", data=study_plan, file_name="study_plan.md", mime="text/markdown")


# ==========================================
# TAB 4: GOAL SUMMARIZER & AI COACH
# ==========================================
with tab_goals:
    st.subheader("🎯 Daily Goal Summarizer & AI Coach")
    st.write("Wrap up your day, reflect on your wins, and get personalized coaching feedback.")
    
    completed_t = [t for t in all_tasks if t.get("completed")]
    pending_t = [t for t in all_tasks if not t.get("completed")]
    
    st.write(f"**Completed Today:** {len(completed_t)} tasks | **Pending:** {len(pending_t)} tasks")
    
    reflection_text = st.text_area(
        "Daily Reflection & Notes",
        placeholder="What went well today? Did you hit any roadblocks or distractions? Anything specific you learned?",
        height=100
    )
    
    summarize_btn = st.button("✨ Summarize Daily Goals & Insights", type="primary", use_container_width=True)
    
    if summarize_btn:
        if not planner.is_configured():
            st.error("⚠️ Please set your `GEMINI_API_KEY` in the `.env` file first!")
        else:
            with st.spinner("🌟 Gemini is reviewing your daily accomplishments and generating insights..."):
                goal_summary = planner.summarize_goals(completed_t, pending_t, reflection_text)
                st.markdown("### 🏆 Daily Wrap-Up & AI Coaching")
                st.markdown(f'<div class="ai-output-box">{goal_summary}</div>', unsafe_allow_html=True)
                st.download_button("📥 Download Summary (.md)", data=goal_summary, file_name="daily_productivity_summary.md", mime="text/markdown")
