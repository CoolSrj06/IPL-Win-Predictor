import os
import pickle

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)


TEAMS = [
    "Sunrisers Hyderabad",
    "Mumbai Indians",
    "Royal Challengers Bangalore",
    "Kolkata Knight Riders",
    "Kings XI Punjab",
    "Chennai Super Kings",
    "Rajasthan Royals",
    "Delhi Capitals",
]

CITIES = [
    "Hyderabad",
    "Mumbai",
    "Bangalore",
    "Kolkata",
    "Chandigarh",
    "Chennai",
    "Jaipur",
    "Delhi",
    "Pune",
    "Indore",
    "Visakhapatnam",
    "Ahmedabad",
    "Abu Dhabi",
    "Dubai",
    "Sharjah",
]

THEMES = {
    "light": {
        "primary": "#0f6cbd",
        "accent": "#0b3d91",
        "bg_main": "#ffffff",
        "bg_soft": "#f4f7fb",
        "card": "#ffffff",
        "input_bg": "#eef4ff",
        "nav_bg": "#d4dff0",
        "text": "#0f172a",
        "muted": "#475569",
        "border": "#d8e1ee",
        "ok": "#198754",
        "warn": "#b54708",
    },
    "dark": {
        "primary": "#5cc8ff",
        "accent": "#8ad7ff",
        "bg_main": "#0b1220",
        "bg_soft": "#111a2d",
        "card": "#131f36",
        "input_bg": "#1b2a47",
        "nav_bg": "#1b2a47",
        "text": "#e6edf7",
        "muted": "#9fb1cf",
        "border": "#2b3d63",
        "ok": "#3fbf7f",
        "warn": "#ffb454",
    },
}


if "theme" not in st.session_state:
    st.session_state.theme = "light"


def apply_theme(theme_name: str) -> dict:
    c = THEMES[theme_name]
    st.markdown(
        f"""
<style>
:root {{
    --primary: {c['primary']};
    --accent: {c['accent']};
    --bg-main: {c['bg_main']};
    --bg-soft: {c['bg_soft']};
    --card: {c['card']};
    --input-bg: {c['input_bg']};
    --nav-bg: {c['nav_bg']};
    --text: {c['text']};
    --muted: {c['muted']};
    --border: {c['border']};
}}

[data-testid="stAppViewContainer"] {{
    background:
        radial-gradient(circle at 10% -20%, color-mix(in srgb, var(--primary) 12%, transparent), transparent 42%),
        radial-gradient(circle at 100% 0%, color-mix(in srgb, var(--accent) 10%, transparent), transparent 40%),
        var(--bg-main);
    color: var(--text);
}}

[data-testid="stHeader"] {{
    background: color-mix(in srgb, var(--bg-main) 90%, transparent);
    border-bottom: 1px solid var(--border);
}}

[data-testid="stSidebar"] {{
    background: var(--bg-soft);
    border-right: 1px solid var(--border);
}}

[data-testid="stSidebar"] * {{
    color: var(--text) !important;
}}

[data-testid="stMarkdownContainer"],
label,
.stMetric label,
.stSelectbox label,
.stNumberInput label,
.stTextInput label {{
    color: var(--text) !important;
}}

p, li, small, .stCaption {{
    color: var(--muted) !important;
}}

.hero {{
    background: linear-gradient(110deg, color-mix(in srgb, var(--primary) 14%, var(--card)), var(--card));
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 22px 24px;
    margin: 10px 0 14px 0;
}}

.top-nav {{
    background: var(--nav-bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    backdrop-filter: blur(6px);
}}

.brand-wrap {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

.brand-logo {{
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    color: #ffffff;
    font-size: 16px;
}}

.brand-title {{
    color: var(--text);
    font-size: 1.02rem;
    font-weight: 700;
    margin: 0;
}}

.brand-sub {{
    color: var(--muted);
    font-size: 0.82rem;
    margin: 0;
}}

.nav-actions {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: flex-end;
}}

.nav-chip {{
    border: 1px solid var(--border);
    background: var(--bg-soft);
    color: var(--text);
    border-radius: 999px;
    padding: 5px 10px;
    font-size: 0.8rem;
    font-weight: 600;
}}

.hero-title {{
    color: var(--primary);
    margin: 0;
    font-size: clamp(1.8rem, 2.5vw, 2.6rem);
    font-weight: 800;
    letter-spacing: 0.2px;
}}

.hero-sub {{
    margin: 8px 0 0 0;
    color: var(--muted);
    font-size: 1.02rem;
    max-width: 980px;
}}

.block-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 12px 14px 4px 14px;
    margin-bottom: 12px;
}}

.section-title {{
    color: var(--accent);
    font-size: 1.3rem;
    font-weight: 700;
    margin: 2px 0 8px 0;
}}

.status-chip {{
    display: inline-block;
    border: 1px solid var(--border);
    background: var(--bg-soft);
    border-radius: 999px;
    padding: 6px 12px;
    color: var(--text);
    font-size: 0.92rem;
    margin-top: 4px;
}}

.info-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px 16px;
    margin-top: 14px;
}}

.info-card a {{
    color: var(--primary) !important;
    text-decoration: none;
}}

.info-card a:hover {{
    text-decoration: underline;
}}

.disclaimer-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px 16px;
    margin-top: 10px;
    border-left: 4px solid var(--primary);
}}

.stMetric {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px;
}}

.stProgress > div > div > div > div {{
    background: linear-gradient(90deg, var(--primary), var(--accent));
}}

[data-testid="stSelectbox"] > div,
[data-testid="stNumberInput"] > div {{
    border-radius: 10px;
}}

[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] button,
[data-testid="stNumberInput"] div[role="spinbutton"] {{
    background-color: var(--input-bg) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}}

[data-testid="stSelectbox"] [data-baseweb="select"] svg {{
    color: var(--text) !important;
}}

@media (max-width: 900px) {{
    .top-nav {{
        padding: 10px 12px;
    }}

    .brand-sub {{
        display: none;
    }}

    .nav-actions {{
        gap: 6px;
    }}

    .nav-chip {{
        font-size: 0.74rem;
        padding: 4px 8px;
    }}
}}

</style>
        """,
        unsafe_allow_html=True,
    )
    return c


@st.cache_resource
def load_model():
    model_path = "model.pkl"
    if not os.path.exists(model_path):
        st.error("Model file model.pkl is missing in the project folder.")
        st.stop()
    with open(model_path, "rb") as f:
        return pickle.load(f)


with st.sidebar:
    st.markdown("### Controls")
    theme_option = st.radio(
        "Theme",
        options=["Light", "Dark"],
        index=0 if st.session_state.theme == "light" else 1,
    )
    st.session_state.theme = "light" if theme_option == "Light" else "dark"

    st.markdown("---")
    st.caption("Tip: Use overs + balls instead of decimal overs for realistic inputs.")


colors = apply_theme(st.session_state.theme)

st.markdown(
        f"""
<div class="top-nav">
    <div class="brand-wrap">
        <div class="brand-logo">🏏</div>
        <div>
            <p class="brand-title">IPL Win Predictor</p>
            <p class="brand-sub">Live chase intelligence powered by machine learning</p>
        </div>
    </div>
    <div class="nav-actions">
        <span class="nav-chip">Theme: {st.session_state.theme.title()}</span>
        <span class="nav-chip">Model: Logistic Regression</span>
        <span class="nav-chip">T20 • Inning 2</span>
    </div>
</div>
        """,
        unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
  <h1 class="hero-title">IPL Win Predictor</h1>
  <p class="hero-sub">
    Predict win probability in real time using a model trained on historical IPL data.
    Enter current chase conditions and compare pressure with run-rate dynamics.
  </p>
</div>
    """,
    unsafe_allow_html=True,
)

try:
    pipe = load_model()
except Exception as e:
    st.error(f"Could not load model: {e}")
    st.stop()


st.markdown('<div class="block-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Match Setup</div>', unsafe_allow_html=True)

top1, top2 = st.columns(2)
with top1:
    batting_team = st.selectbox("Batting Team", TEAMS, index=0)
with top2:
    bowling_team = st.selectbox("Bowling Team", [t for t in TEAMS if t != batting_team], index=0)

selected_city = st.selectbox("Venue", CITIES, index=0)
st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="block-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Match Statistics</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    target = st.number_input("Target Score", min_value=1, max_value=300, value=180, step=1)
with c2:
    score = st.number_input("Current Score", min_value=0, max_value=300, value=75, step=1)
with c3:
    wickets_out = st.number_input("Wickets Lost", min_value=0, max_value=10, value=3, step=1)

o1, o2, o3 = st.columns([1, 1, 2])
with o1:
    overs_completed = st.number_input("Completed Overs", min_value=0, max_value=19, value=10, step=1)
with o2:
    balls_in_current_over = st.number_input("Balls in Over", min_value=0, max_value=5, value=2, step=1)
with o3:
    st.write("")
    st.write("")
    predict_btn = st.button("Predict Probability", use_container_width=True, type="primary")

st.markdown("</div>", unsafe_allow_html=True)


if predict_btn:
    balls_bowled = (overs_completed * 6) + balls_in_current_over
    overs_decimal = balls_bowled / 6 if balls_bowled > 0 else 0
    balls_left = 120 - balls_bowled
    runs_left = target - score
    wickets = 10 - wickets_out

    if batting_team == bowling_team:
        st.error("Batting and bowling teams cannot be the same.")
    elif balls_bowled > 120:
        st.error("Invalid overs/balls combination.")
    elif score > target:
        st.error("Current score cannot be greater than target.")
    elif runs_left <= 0:
        st.success("Target already achieved. Batting team wins.")
    elif wickets <= 0:
        st.warning("All out. Batting team cannot continue the chase.")
    elif balls_left <= 0:
        st.warning("No balls remaining.")
    else:
        crr = round(score / overs_decimal, 2) if overs_decimal > 0 else 0.0
        rrr = round((runs_left * 6) / balls_left, 2)

        input_df = pd.DataFrame(
            {
                "batting_team": [batting_team],
                "bowling_team": [bowling_team],
                "city": [selected_city],
                "runs_left": [runs_left],
                "balls_left": [balls_left],
                "wickets": [wickets],
                "total_runs_x": [target],
                "crr": [crr],
                "rrr": [rrr],
            }
        )

        try:
            result = pipe.predict_proba(input_df)
            loss_prob = float(result[0][0])
            win_prob = float(result[0][1])

            left, right = st.columns(2)
            with left:
                st.metric(
                    label=f"{batting_team} Win Probability",
                    value=f"{round(win_prob * 100)}%",
                )
                st.progress(win_prob)

            with right:
                st.metric(
                    label=f"{bowling_team} Win Probability",
                    value=f"{round(loss_prob * 100)}%",
                )
                st.progress(loss_prob)

            s1, s2, s3, s4 = st.columns(4)
            s1.metric("Runs Needed", runs_left)
            s2.metric("Balls Remaining", balls_left)
            s3.metric("Current RR", crr)
            s4.metric("Required RR", rrr)

            if crr >= rrr:
                status = "Batting side is ahead of the required pace."
                status_color = colors["ok"]
            else:
                status = "Batting side needs acceleration to stay in the chase."
                status_color = colors["warn"]

            st.markdown(
                f'<div class="status-chip" style="border-color:{status_color}; color:{status_color};">{status}</div>',
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.error(f"Prediction failed: {e}")


st.markdown(
    """
<div class="info-card">
    <div class="section-title">Project Information</div>
    <p><strong>Training dataset:</strong>
        <a href="https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbGcyc0I0OHpESDV2aDAxN3o0SF96Um5FVjAxQXxBQ3Jtc0ttbWlvSXktNlExazlnWVFKVFhjQ0R6MzVpY1FIWV9ia0UtNHNrRUNzcElZUnVtT3dKdUNxMWhrLXpycjd4VWVoOXVlaWIwWlV0QTR2WWdxanF3N3NwUkVmVDM4dHJsZHFHT3RYcW1ad3BUZ3kzaWtHcw&q=https%3A%2F%2Fwww.kaggle.com%2Framjidoolla%2Fipl-data-set&v=Ok_zkfWC0gI" target="_blank">Open Dataset Link</a>
    </p>
    <p><strong>Model training note:</strong> Only <code>matches.csv</code> and <code>deliveries.csv</code> files were used to train this model.</p>
    <p><strong>Developed by:</strong> Srijan Maurya</p>
    <p><strong>Email:</strong> <a href="mailto:srijanmaurya6602@gmail.com">srijanmaurya6602@gmail.com</a></p>
    <p><strong>GitHub:</strong> <a href="https://github.com/CoolSrj06" target="_blank">https://github.com/CoolSrj06</a></p>
</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="disclaimer-card">
    <div class="section-title">⚠️ Disclaimer</div>
    <p>This is a learning project developed to showcase my skills as a Data Science Engineer. The model predictions are based on historical IPL data and should be used for educational and entertainment purposes only. Actual match outcomes depend on numerous real-world factors not captured in this model. Always verify predictions with official sources before making any decisions.</p>
</div>
    """,
    unsafe_allow_html=True,
)
