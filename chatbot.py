import streamlit as st
import base64
from difflib import get_close_matches
import pandas as pd
import datetime

# ✅ Background image + overlay
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(0, 128, 0, 0.3), rgba(0, 128, 0, 0.3)), url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                font-family: 'Segoe UI', sans-serif;
                padding-top: 2rem;
            }}

            h1 {{
                color: #00cc88;
                text-align: center;
                font-size: 42px;
                font-weight: bold;
                margin-bottom: 0.2rem;
                text-shadow: 1px 1px 2px white;
            }}

            .subheading {{
                text-align: center;
                font-size: 22px;
                color: #111;
                font-weight: bold;
                margin-top: -10px;
                margin-bottom: 30px;
                background-color: rgba(255,255,255,0.6);
                padding: 10px;
                border-radius: 10px;
            }}

            .stTextInput > label {{
                font-weight: bold;
                color: #111;
                font-size: 18px;
            }}

            .stTextInput > div > input {{
                background-color: #fff !important;
                color: #111 !important;
                border-radius: 10px !important;
                padding: 10px !important;
                border: 2px solid #00cc88 !important;
                font-size: 16px;
            }}

            button[kind="primary"] {{
                background-color: #00cc88 !important;
                color: white !important;
                border-radius: 10px;
                font-weight: bold;
            }}

            .bold-text {{
                font-weight: bold;
                font-size: 22px;
                color: #222;
                margin-bottom: 10px;
            }}

            .select-label {{
                font-weight: bold;
                font-size: 20px;
                color: #000;
                margin-bottom: 8px;
            }}

            .pink-button button {{
                background-color: #ff66b2 !important;
                color: white !important;
                border-radius: 10px;
                font-weight: bold;
                margin-right: 10px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# 🖼️ Set background
set_bg("healthy_bg.jpg")
st.set_page_config(page_title="Healthy Diet Chatbot", page_icon="🥗")

# ✅ Title section
st.markdown("<h1>🥗 Healthy Diet Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<div class='subheading'><b>Let’s create your personalized healthy journey!</b></div>", unsafe_allow_html=True)

# User data storage (in memory)
if "user" not in st.session_state:
    st.session_state.user = {}
if "track_page" not in st.session_state:
    st.session_state.track_page = "main"

# CSV logging (optional for counting)
def log_user(name, age):
    try:
        df = pd.read_csv("user_log.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "Age", "Date"])
    new_row = pd.DataFrame([{"Name": name, "Age": age, "Date": datetime.datetime.now().strftime("%Y-%m-%d")}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("user_log.csv", index=False)

# Progress tracking
def show_progress(name):
    try:
        df = pd.read_csv("user_log.csv")
        user_entries = df[df.Name == name]
        streak_count = len(user_entries)
        st.info(f"🔥 You've used the chatbot **{streak_count}** time(s). Keep going!")
    except:
        st.warning("No usage data found yet.")

# Step 1: Name input
if "name" not in st.session_state.user:
    name = st.text_input("Enter your name:")
    if name:
        st.session_state.user["name"] = name
        st.rerun()
else:
    st.markdown(f"<div class='bold-text'>Welcome, {st.session_state.user['name']}</div>", unsafe_allow_html=True)
    show_progress(st.session_state.user["name"])

    # Step 2: Age input
    if "age" not in st.session_state.user:
        age = st.text_input("Enter your age:")
        if age:
            st.session_state.user["age"] = age
            log_user(st.session_state.user["name"], age)
            st.rerun()

# Step 3: Proceed
if "name" in st.session_state.user and "age" in st.session_state.user:

    if st.session_state.track_page == "main":
        st.markdown("<div class='bold-text'>🔍 Choose a Topic:</div>", unsafe_allow_html=True)
        st.markdown("<div class='select-label'>What do you want to explore?</div>", unsafe_allow_html=True)
        topic = st.selectbox("", ["Loose Weight", "Gain Weight", "Healthy Tips", "Diet Plan"])

        if topic:
            if topic in ["Loose Weight", "Gain Weight"]:
                focus = st.radio("Choose your focus:", ["Exercise", "Diet"])
                if st.button("Show Plan"):
                    if topic == "Loose Weight" and focus == "Diet":
                        st.markdown("""🍽 **Weight Loss Diet Plan:**
- Morning: Warm lemon water + almonds
- Breakfast: Oats or boiled eggs
- Lunch: Brown rice + dal + salad
- Dinner: Grilled paneer/chicken + veggies""")
                    elif topic == "Loose Weight" and focus == "Exercise":
                        st.markdown("""🏃 **Exercise Plan:**
- 30 mins walk daily
- 3x/week bodyweight workouts
- 1x/week yoga""")
                    elif topic == "Gain Weight" and focus == "Diet":
                        st.markdown("""🍽 **Weight Gain Diet Plan:**
- Morning: Banana + peanut butter toast + milk
- Lunch: Rice + paneer + salad
- Dinner: Roti + sabzi + curd""")
                    elif topic == "Gain Weight" and focus == "Exercise":
                        st.markdown("""🏋️ **Weight Gain Exercises:**
- Strength training 4x/week
- Light cardio 1–2x/week""")

            elif topic == "Healthy Tips":
                st.markdown("<div class='bold-text'>💡 Daily Health Tips:</div>", unsafe_allow_html=True)
                st.markdown("""
- Drink 8 glasses of water  
- Avoid processed food  
- Get 7–8 hours sleep  
- Meditate 10 mins a day
""")

            elif topic == "Diet Plan":
                st.markdown("<div class='bold-text'>🍴 Balanced Diet Chart:</div>", unsafe_allow_html=True)
                st.markdown("""
- 40% Carbs | 30% Protein | 30% Fats  
- Add seasonal fruits & green veggies  
- Avoid sugar-loaded items
""")

            # Ask if user wants to track
            st.markdown("<div class='bold-text'>📆 Do you want to track your days?</div>", unsafe_allow_html=True)
            col1, col2 = st.columns([1,1])
            with col1:
                if st.button("Yes", key="track_yes"):
                    st.session_state.track_page = "streak"
                    st.rerun()
            with col2:
                if st.button("No", key="track_no"):
                    st.session_state.track_page = "thankyou"
                    st.rerun()

    elif st.session_state.track_page == "streak":
        st.markdown("<div class='bold-text'>🗓️ Enter number of days you want to follow:</div>", unsafe_allow_html=True)
        streak = st.number_input("", min_value=1, max_value=365, value=7)
        if st.button("Next"):
            st.session_state.track_page = "thankyou"
            st.rerun()

    elif st.session_state.track_page == "thankyou":
        st.balloons()
        st.markdown("""
        ## 🎉 Thank You for Using the Healthy Diet Chatbot!
        We hope this helps you stay motivated and achieve your wellness goals.  
        Come back tomorrow to continue your streak! 🥗💪
        """)
        if st.button("➕ Add Another Entry"):
            for key in list(st.session_state.user.keys()):
                del st.session_state.user[key]
            st.session_state.track_page = "main"
            st.rerun()




























