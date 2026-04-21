import streamlit as st

# 🎨 Global UI Theme
def inject_global_css():
    st.markdown("""
    <style>
    body {
        background: radial-gradient(circle at top, #020617, #000000);
        color: #e2e8f0;
    }

    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    h1 {
        font-size: 36px;
        font-weight: 700;
    }

    input {
        background-color: #0f172a !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 10px !important;
    }

    button[kind="primary"] {
        background: linear-gradient(90deg, #6366f1, #4f46e5);
        border-radius: 12px;
        border: none;
        color: white;
    }

    .card {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 14px;
        margin: 10px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)


# 💬 Chat Bubble (FINAL FIXED)
def chat_bubble(text, is_user=False):
    text = text.replace("\n", "<br>")

    if is_user:
        st.markdown(f"""
<div style="display:flex; justify-content:flex-end; align-items:center; margin:10px 0;">

<div style="
background: linear-gradient(90deg, #6366f1, #4f46e5);
color:white;
padding:10px 15px;
border-radius:20px;
max-width:60%;
text-align:right;
box-shadow:0 4px 10px rgba(0,0,0,0.3);
">
{text}
</div>

<img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
style="width:35px;height:35px;border-radius:50%;margin-left:8px;">

</div>
""".strip(), unsafe_allow_html=True)

    else:
        st.markdown(f"""
<div style="display:flex; align-items:center; margin:10px 0;">

<img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
style="width:35px;height:35px;border-radius:50%;margin-right:8px;">

<div style="
background: rgba(255,255,255,0.05);
color:#e2e8f0;
padding:10px 15px;
border-radius:20px;
max-width:60%;
box-shadow:0 4px 10px rgba(0,0,0,0.3);
">
{text}
</div>

</div>
""".strip(), unsafe_allow_html=True)


# 📊 Dashboard Card
def card(title, value):
    st.markdown(f"""
    <div class="card">
        <div style="font-size:14px;color:#94a3b8;">{title}</div>
        <div style="font-size:28px;font-weight:bold;">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# 📢 Announcement Card
def announcement_card(title, date, priority, icon):
    st.markdown(f"""
    <div class="card">
        {icon} <b>{title}</b><br>
        <small>{date} • {priority}</small>
    </div>
    """, unsafe_allow_html=True)