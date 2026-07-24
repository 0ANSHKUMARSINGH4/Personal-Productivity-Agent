"""
Planner module for Personal Productivity Agent.
Handles task storage, local JSON persistence, and interaction with the Google Gemini API.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

import prompts

# Attempt importing google.genai or fallback to google.generativeai
GENAI_AVAILABLE = False
GENAI_SDK_TYPE = None

try:
    from google import genai
    GENAI_AVAILABLE = True
    GENAI_SDK_TYPE = "genai"
except ImportError:
    try:
        import google.generativeai as genai_legacy
        GENAI_AVAILABLE = True
        GENAI_SDK_TYPE = "legacy"
    except ImportError:
        GENAI_AVAILABLE = False

DATA_FILE = "tasks_data.json"


class TaskManager:
    """Handles local storage and CRUD operations for tasks."""

    def __init__(self, storage_path: str = DATA_FILE):
        self.storage_path = storage_path
        self.tasks: List[Dict[str, Any]] = self.load_tasks()

    def load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from JSON file if exists."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading tasks file: {e}")
                return []
        return []

    def save_tasks(self) -> bool:
        """Save current tasks to JSON file."""
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving tasks file: {e}")
            return False

    def add_task(
        self,
        title: str,
        description: str = "",
        category: str = "General",
        priority: str = "Medium",
        deadline: str = "",
        estimated_hours: float = 1.0
    ) -> Dict[str, Any]:
        """Add a new task."""
        new_id = int(datetime.now().timestamp() * 1000)
        task = {
            "id": new_id,
            "title": title.strip(),
            "description": description.strip(),
            "category": category,
            "priority": priority,
            "deadline": deadline,
            "estimated_hours": estimated_hours,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def update_task(self, task_id: int, updated_fields: Dict[str, Any]) -> bool:
        """Update existing task fields."""
        for t in self.tasks:
            if t["id"] == task_id:
                t.update(updated_fields)
                self.save_tasks()
                return True
        return False

    def toggle_completed(self, task_id: int) -> bool:
        """Toggle task completion status."""
        for t in self.tasks:
            if t["id"] == task_id:
                t["completed"] = not t.get("completed", False)
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID."""
        initial_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        if len(self.tasks) < initial_len:
            self.save_tasks()
            return True
        return False

    def clear_all(self):
        """Clear all tasks."""
        self.tasks = []
        self.save_tasks()


class GeminiPlanner:
    """Handles interactions with Google Gemini API for productivity analysis."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initialize the appropriate GenAI client."""
        if not self.api_key or not GENAI_AVAILABLE:
            return

        try:
            if GENAI_SDK_TYPE == "genai":
                self.client = genai.Client(api_key=self.api_key)
            elif GENAI_SDK_TYPE == "legacy":
                genai_legacy.configure(api_key=self.api_key)
                self.client = genai_legacy
        except Exception as e:
            print(f"Error initializing Gemini client: {e}")
            self.client = None

    def is_configured(self) -> bool:
        """Check if Gemini API is properly configured."""
        return self.client is not None and len(self.api_key.strip()) > 0

    def _generate_content(self, system_prompt: str, user_prompt: str) -> str:
        """Internal helper to call Gemini API and return generated text."""
        if not self.is_configured():
            return "⚠️ **Gemini API key is not configured.** Please provide a valid Gemini API Key in the sidebar or `.env` file to enable AI features."

        full_prompt = f"{system_prompt}\n\nUser Input:\n{user_prompt}"

        try:
            if GENAI_SDK_TYPE == "genai":
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_prompt
                )
                return response.text
            elif GENAI_SDK_TYPE == "legacy":
                model = genai_legacy.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(full_prompt)
                return response.text
            else:
                return "⚠️ No supported Google GenAI SDK installed."
        except Exception as e:
            # Fallback attempt with model names if primary fails
            try:
                if GENAI_SDK_TYPE == "genai":
                    response = self.client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=full_prompt
                    )
                    return response.text
            except Exception as inner_e:
                pass
            return f"❌ **Error generating response from Gemini API:** {str(e)}"

    def analyze_priorities(self, tasks: List[Dict[str, Any]]) -> str:
        """Generate priority matrix and execution sequence for tasks."""
        if not tasks:
            return "💡 Please add some tasks first before requesting AI Priority Analysis."

        user_prompt = prompts.build_priority_prompt(tasks)
        return self._generate_content(prompts.SYSTEM_PROMPT_PRIORITY_ANALYSIS, user_prompt)

    def generate_daily_schedule(
        self,
        tasks: List[Dict[str, Any]],
        start_time: str = "09:00 AM",
        end_time: str = "05:00 PM",
        break_pref: str = "15-min break every 90 mins, 45-min lunch"
    ) -> str:
        """Generate hour-by-hour daily schedule."""
        user_prompt = prompts.build_daily_plan_prompt(tasks, start_time, end_time, break_pref)
        return self._generate_content(prompts.SYSTEM_PROMPT_DAILY_PLANNER, user_prompt)

    def generate_study_schedule(
        self,
        subjects: str,
        target_date: str,
        daily_hours: float,
        focus_areas: str
    ) -> str:
        """Generate study roadmap and routine."""
        if not subjects.strip():
            return "💡 Please enter at least one subject to generate a study plan."

        user_prompt = prompts.build_study_plan_prompt(subjects, target_date, daily_hours, focus_areas)
        return self._generate_content(prompts.SYSTEM_PROMPT_STUDY_SCHEDULER, user_prompt)

    def summarize_goals(
        self,
        completed_tasks: List[Dict[str, Any]],
        pending_tasks: List[Dict[str, Any]],
        reflection_text: str
    ) -> str:
        """Generate daily summary, productivity score, and recommendations."""
        user_prompt = prompts.build_goal_summary_prompt(completed_tasks, pending_tasks, reflection_text)
        return self._generate_content(prompts.SYSTEM_PROMPT_GOAL_SUMMARIZER, user_prompt)
