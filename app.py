# -------------------------------------------------------------
# app.py  –  Blog + Fitness multi‑feature Streamlit app
# with banner image, custom CSS, download buttons and footer
# -------------------------------------------------------------
import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PIL import Image
from utils import get_joke  # helper that returns a random joke

# ───────────────────────  1. INITIALISE GEMINI  ────────────────────────
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY not found! Put it in a .env file.")
    st.stop()

genai.configure(api_key=api_key)
MODEL_NAME = "gemini-1.5-flash"

# ───────────────────────  2. LLM HELPER FUNCTIONS  ─────────────────────
def call_gemini(prompt: str) -> str:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_blog(topic: str, words: int, voice: str, keywords: str) -> str:
    prompt = (
        f"Write an engaging blog post (~{words} words) on the topic: {topic}.\n"
        f"Brand voice/style: {voice or 'default friendly tone'}.\n"
        f"Include the following keywords naturally: {keywords}.\n"
        "Structure with an introduction, 2–3 sub‑headings, and a conclusion.\n"
        "Return in Markdown format."
    )
    return call_gemini(prompt)

def generate_fitness_plan(goal: str, workout: str, diet: str, weeks: int) -> str:
    prompt = f"""
You are a certified fitness coach. Create a {weeks}-week personalised fitness guide:
Goal: {goal}
Preferred workout type: {workout}
Diet preference: {diet}

For each week, include:
- Weekly focus
- Daily workout schedule (sets / duration)
- Daily meal suggestions (breakfast, lunch, dinner, snacks)
Also add hydration tips, rest advice, and motivation.
Return in Markdown format with headings.
"""
    return call_gemini(prompt)

# ─────────────────────────  3. STREAMLIT UI / STYLING  ──────────────────
st.set_page_config(page_title="BlogMaster AI", page_icon="🤖", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f9f9f9;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, h4 {
        color: #4B8BBE;
    }
    .stButton>button {
        background-color: #4B8BBE;
        color: white;
        border-radius: 10px;
        padding: 0.5em 1.5em;
        font-size: 1em;
    }
    .stTextInput input, .stSelectbox div div, .stSlider {
        border-radius: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown("<h1 style='text-align: center;'>🧠 BlogMaster Multi‑Feature AI Assistant</h1>", unsafe_allow_html=True)

# Banner image (ensure the file exists)
try:
    banner = Image.open("blogmaster_banner.png")
    st.image(banner, use_container_width=700)
except FileNotFoundError:
    st.info("Upload 'blogmaster_banner.png' to show a banner here.")

# ✅ Stylish friendly intro text below banner
st.markdown(
    """
    <h3 style='color:#4B8BBE; text-align:center;'>
    🤖 Hello! I’m BlogMaster, your friendly robot.<br>
    Let’s create a fantastic blog together!
    </h3>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("Navigation")
mode = st.sidebar.radio("Choose a feature:", ["Blog Generator ✍", "Fitness Plan 💪"])

st.sidebar.markdown("---")
st.sidebar.markdown("Powered by *Gemini Flash*   |   Built with *Streamlit*", unsafe_allow_html=True)
st.sidebar.markdown("Made by Jaswanth 💡")

# ───────────────────────  4. FEATURE: BLOG GENERATOR  ──────────────────
if mode.startswith("Blog"):
    st.markdown("---")
    st.subheader("✍ Blog Generator")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Blog Topic")
        words = st.slider("Approximate Word Count", 100, 3000, 800, 100)
    with col2:
        brand_voice = st.text_area("Brand Voice / Style (optional)")
        keywords = st.text_input("SEO Keywords (comma‑separated, optional)")

    st.markdown("### 👇 Enter your details above and click Generate")

    if st.button("Generate Blog"):
        if topic:
            with st.spinner("Writing your blog..."):
                st.write(f"🃏 {get_joke()}")
                blog_md = generate_blog(topic, words, brand_voice, keywords)
            st.success("Done!")
            st.subheader("📝 Your Blog Post")
            st.markdown(blog_md, unsafe_allow_html=True)
            st.download_button("💾 Download Blog", blog_md, file_name="blogmaster_post.md", mime="text/markdown")
        else:
            st.error("Please enter a topic.")

# ───────────────────────  5. FEATURE: FITNESS PLAN  ────────────────────
else:
    st.markdown("---")
    st.subheader("💪 Fitness Plan Generator")

    col1, col2 = st.columns(2)
    with col1:
        goal = st.text_input("Primary fitness goal (e.g. lose fat, build muscle)")
        weeks = st.selectbox("Duration (weeks)", [4, 6, 8, 12])
    with col2:
        workout = st.selectbox(
            "Preferred workout type",
            ["Gym", "Home body‑weight", "Yoga", "Cardio", "Mixed"],
        )
        diet = st.text_input("Diet preference (e.g. vegetarian, high‑protein, keto)")

    if st.button("Generate Fitness Plan"):
        if goal and diet:
            with st.spinner("Creating your personalised plan..."):
                st.write(f"🃏 {get_joke()}")
                plan_md = generate_fitness_plan(goal, workout, diet, weeks)
            st.success("Plan ready!")
            st.subheader("📋 Your Fitness Guide")
            st.markdown(plan_md, unsafe_allow_html=True)
            st.download_button("📥 Download Plan", plan_md, file_name="fitness_plan.md", mime="text/markdown")
        else:
            st.error("Please fill in goal and diet preference.")

# ─────────────────────────────  FOOTER  ────────────────────────────────
st.markdown("---")
st.markdown("© 2025 BlogMaster | Built with ❤ using [Gemini](https://ai.google.dev) + [Streamlit](https://streamlit.io)")