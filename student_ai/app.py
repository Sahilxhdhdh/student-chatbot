import streamlit as st
import os
import sys
import json
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt


# ── Path setup ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from modules.chatbot import ChatbotEngine
from modules.ui_components import (
    inject_global_css, chat_bubble, announcement_card, card
)


  # every 5 sec

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="EduAI — Student Portal",
    page_icon="🎓",
    layout="wide"
)

inject_global_css()
st_autorefresh(interval=5000, key="refresh")

# ── Load data ──────────────────────────────────────────────
DATA_PATH = os.path.join(BASE_DIR, "data", "student_data.json")

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()


def calculate_cgpa(results):
    grade_map = {
        "A+": 10, "A": 9, "B+": 8,
        "B": 7, "C+": 6, "C": 5,
        "D": 4, "F": 0
    }

    points = []
    for sub in results.values():
        grade = sub["grade"]
        points.append(grade_map.get(grade, 0))

    return round(sum(points) / len(points), 2) if points else 0




def plot_cgpa_graph(results):
    import plotly.graph_objects as go

    grade_map = {
        "A+": 10, "A": 9, "B+": 8,
        "B": 7, "C+": 6, "C": 5,
        "D": 4, "F": 0
    }

    subjects = list(results.keys())
    points = [grade_map.get(v["grade"], 0) for v in results.values()]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=subjects,
        y=points
    ))

    fig.update_layout(
        title="CGPA Analysis",
        template="plotly_dark",
        xaxis_title="Subjects",
        yaxis_title="Grade Points"
    )

    return fig




# 📈 Line Chart (Performance Trend)
def plot_line_chart(results):
    import plotly.graph_objects as go

    subjects = list(results.keys())
    marks = [v["marks"] for v in results.values()]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=subjects,
        y=marks,
        mode='lines+markers'
    ))

    fig.update_layout(
        title="Performance Trend",
        template="plotly_dark",
        xaxis_title="Subjects",
        yaxis_title="Marks"
    )

    return fig


# 🥧 Pie Chart (Grade Distribution)
def plot_pie_chart(results):
    import plotly.express as px

    grades = [v["grade"] for v in results.values()]

    grade_count = {}
    for g in grades:
        grade_count[g] = grade_count.get(g, 0) + 1

    fig = px.pie(
        names=list(grade_count.keys()),
        values=list(grade_count.values()),
        title="Grade Distribution"
    )

    fig.update_layout(template="plotly_dark")

    return fig


# 🎯 AI Insight
def generate_insights(results):
    marks = [v["marks"] for v in results.values()]
    avg = sum(marks) / len(marks)

    if avg >= 85:
        return "🔥 Excellent performance! Keep it up."
    elif avg >= 70:
        return "👍 Good performance. Aim for higher grades."
    else:
        return "⚠️ Needs improvement. Focus on weak subjects."

# ── Session State ──────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── LOGIN ─────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🎓 EduAI Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Smart Student Assistant</p>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login 🚀"):
        for u in data["students"]:
            if u["username"] == username and u["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user = u
                st.rerun()

        st.error("Invalid credentials")

    st.stop()

# ── User Data ─────────────────────────────────────────────
user = st.session_state.user
data = user["data"]

student = data["student"]
attendance = data["attendance"]
results = data["results"]["current_semester"]
fees = data["fees"]
announcements = data["announcements"]

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 👤 {student['name']}")
    st.write(f"{student['course']}")
    st.write(f"Year {student['year']} | Sem {student['semester']}")

    # 🔔 Notification count badge
    st.markdown(f"### 🔔 Notifications ({len(user.get('notifications', []))})")

    for note in user.get("notifications", []):
        st.info(note)

    st.markdown("---")

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

# ── Navigation ─────────────────────────────────────────────
tab = st.sidebar.radio("Go to", [
    "Dashboard", "Results", "Attendance", "Fees", "Chatbot"
])

# ── Dashboard ─────────────────────────────────────────────
if tab == "Dashboard":
    st.markdown(f"<h1>Welcome {student['name']} 👋</h1>", unsafe_allow_html=True)

    # 📊 Cards
    c1, c2, c3 = st.columns(3)

    with c1:
        card("Attendance", f"{attendance['overall']}%")
    with c2:
        card("Subjects", len(attendance["subjects"]))
    with c3:
        cgpa = calculate_cgpa(results)
        card("CGPA", cgpa)

    # 📊 CGPA BAR GRAPH (FULL WIDTH)
    st.markdown("## 📊 CGPA Analysis")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(plot_cgpa_graph(results), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 📊 ADVANCED CHARTS (SIDE BY SIDE)
    st.markdown("## 📈 Advanced Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(plot_line_chart(results), use_container_width=True)

    with col2:
        st.plotly_chart(plot_pie_chart(results), use_container_width=True)

    # 🤖 AI INSIGHT
    st.markdown("## 🤖 AI Insight")
    st.success(generate_insights(results))

    # 📢 ANNOUNCEMENTS (LAST)
    st.markdown("## 📢 Announcements")
    for a in announcements:
        announcement_card(a["title"], a["date"], a["priority"], a["icon"])
    

# ── Results ───────────────────────────────────────────────
elif tab == "Results":
    st.title("📊 Results")
    for sub, val in results.items():
        st.write(f"{sub}: {val['marks']}/{val['max']} ({val['grade']})")

# ── Attendance ────────────────────────────────────────────
elif tab == "Attendance":
    st.title("📅 Attendance")
    for sub, val in attendance["subjects"].items():
        st.write(f"{sub} — {val}%")
        st.progress(val / 100)

# ── Fees ─────────────────────────────────────────────────
elif tab == "Fees":
    st.title("💰 Fees")

    st.write("### Pending Fees")
    if fees["pending"]:
        for f in fees["pending"]:
            st.warning(f"{f['description']} - ₹{f['amount']}")
    else:
        st.success("No pending fees")

    st.write("### Paid Fees")
    for f in fees["paid"]:
        st.success(f"{f['description']} - ₹{f['amount']}")

# ── Chatbot ──────────────────────────────────────────────
elif tab == "Chatbot":
    st.markdown("<h1>🤖 AI Chatbot</h1>", unsafe_allow_html=True)

    intents_path = os.path.join(BASE_DIR, "data", "intents.json")

    if "bot" not in st.session_state:
        st.session_state.bot = ChatbotEngine(intents_path)

    # 👋 Greeting once
    if not st.session_state.chat_history:
        st.session_state.chat_history.append({
            "role": "bot",
            "text": f"👋 Hey {student['name']}! Great to see you. I can help with results, attendance, fees and more."
        })

    # 💬 Show chat
    st.markdown('<div style="max-width:800px; margin:auto;">', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        chat_bubble(msg["text"], is_user=(msg["role"] == "user"))

    st.markdown('</div>', unsafe_allow_html=True)

    user_input = st.text_input("Ask something")

    if st.button("Send"):
        if user_input:
            # User message
            st.session_state.chat_history.append({
                "role": "user",
                "text": user_input
            })

            response = st.session_state.bot.respond(user_input, data)
            reply = response["message"]
            action = response.get("action")

            # Results
            if action == "show_results":
                cgpa = calculate_cgpa(results)

                reply += "\n\n" + "\n".join([
                    f"{s}: {v['marks']}/{v['max']} ({v['grade']})"
                    for s, v in results.items()
                ])

                reply += f"\n\n🎓 CGPA: {cgpa}"
                fig = plot_cgpa_graph(results)
                st.plotly_chart(fig, use_container_width=True)
                st.plotly_chart(plot_line_chart(results), use_container_width=True)
                st.plotly_chart(plot_pie_chart(results), use_container_width=True)

                st.success(generate_insights(results))

            # Attendance
            elif action == "show_attendance":
                lines = [
                    f"{sub}: {val}%"
                    for sub, val in attendance["subjects"].items()
                ]
                reply += "\n\n" + "\n".join(lines)

            # Fees
            elif action == "show_fees":
                if fees["pending"]:
                    lines = [
                        f"{f['description']} - ₹{f['amount']}"
                        for f in fees["pending"]
                    ]
                    reply += "<br><br>" + "<br>".join(lines)
                else:
                    reply += "<br><br>No pending fees"

            # Notification trigger
            if "fee" in user_input.lower():
                msg = "⚠️ Fee reminder generated"

                user["notifications"].append(msg)

                # 🔔 Toast popup
                st.toast(msg, icon="🔔")
                st.audio("https://www.soundjay.com/buttons/sounds/button-3.mp3")

            # Bot reply
            st.session_state.chat_history.append({
                "role": "bot",
                "text": reply
            })

            st.rerun()