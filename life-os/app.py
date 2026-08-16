import streamlit as st
import pandas as pd
import os
import requests
from urllib.parse import quote
from google import genai

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Life-OS | Wellbeing Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS (minimal — only structural tweaks)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .metric-container { padding: 1rem; border-radius: 8px; }
    .stMetric { background: #1A1D2E; border-radius: 8px; padding: 1rem; }
    div[data-testid="metric-container"] { background: #1A1D2E; border-radius: 8px; padding: 1rem; }
    .block-container { padding-top: 2rem; }
    .stDivider { margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), "screentime.csv")
    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


df = load_data()
all_dates = sorted(df["Date"].dt.date.unique(), reverse=True)


# ─────────────────────────────────────────────
# SIDEBAR CONTROLS
# ─────────────────────────────────────────────
st.sidebar.markdown("## 🎛️ Control Panel")
st.sidebar.divider()

selected_date = st.sidebar.selectbox(
    "📅 Select Day",
    options=all_dates,
    format_func=lambda x: x.strftime("%A, %b %d %Y"),
)

daily_goal = st.sidebar.slider(
    "🎯 Daily Goal (minutes)",
    min_value=60,
    max_value=600,
    value=180,
    step=15,
    help="Set your maximum acceptable daily screen time in minutes.",
)

st.sidebar.divider()
st.sidebar.markdown(f"""
**📊 Quick Stats**
- Days tracked: `{len(all_dates)}`
- Goal: `{daily_goal} min ({daily_goal/60:.1f}h)`
""")


# ─────────────────────────────────────────────
# FILTER TODAY'S DATA
# ─────────────────────────────────────────────
today_df = df[df["Date"].dt.date == selected_date]
total_today = int(today_df["Minutes_Used"].sum())

by_app = today_df.groupby("App_Name")["Minutes_Used"].sum()
most_used_app = by_app.idxmax() if not by_app.empty else "N/A"
most_used_minutes = int(by_app.max()) if not by_app.empty else 0

delta = total_today - daily_goal
goal_pct = round((total_today / daily_goal) * 100, 1) if daily_goal > 0 else 0


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("# 🧠 Life-OS Wellbeing Dashboard")
st.caption(
    f"Screen time intelligence · {selected_date.strftime('%A, %B %d, %Y')} · "
    f"Goal: {daily_goal} min"
)
st.divider()


# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
hours = total_today // 60
mins = total_today % 60
delta_label = f"{abs(delta)} min {'over ⚠️' if delta > 0 else 'under ✅'} goal"

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        label="📱 Total Screen Time",
        value=f"{hours}h {mins}m",
        delta=delta_label,
        delta_color="inverse",
    )

with kpi2:
    st.metric(
        label="🏆 Most Used App",
        value=most_used_app,
        delta=f"{most_used_minutes} min today",
        delta_color="off",
    )

with kpi3:
    st.metric(
        label="🎯 Goal Achievement",
        value=f"{goal_pct}%",
        delta=f"{'Over' if delta > 0 else 'Under'} by {abs(delta)} min",
        delta_color="inverse",
    )

st.divider()


# ─────────────────────────────────────────────
# VISUALIZATIONS
# ─────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Today's Breakdown by Category")
    if not today_df.empty:
        cat_data = (
            today_df.groupby("Category")["Minutes_Used"]
            .sum()
            .sort_values(ascending=False)
        )
        st.bar_chart(cat_data, color="#6C63FF")
    else:
        st.info("No data for this day.")

with col_right:
    st.subheader("📈 14-Day Screen Time Trend")
    trend_data = (
        df.groupby("Date")["Minutes_Used"]
        .sum()
        .reset_index()
        .rename(columns={"Minutes_Used": "Minutes"})
        .set_index("Date")
    )
    st.line_chart(trend_data, color="#FF6584")

st.divider()


# ─────────────────────────────────────────────
# AI HELPERS
# ─────────────────────────────────────────────
def aggregate_for_ai(df: pd.DataFrame, date) -> str:
    day_df = df[df["Date"].dt.date == date]
    summary = (
        day_df.groupby("Category")["Minutes_Used"]
        .sum()
        .reset_index()
        .rename(columns={"Minutes_Used": "Total_Minutes"})
        .sort_values("Total_Minutes", ascending=False)
    )
    summary["Hours"] = (summary["Total_Minutes"] / 60).round(2)
    return summary.to_string(index=False)


def get_ai_coaching(data_string: str, total_min: int, goal_min: int) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        return "⚠️ `GOOGLE_API_KEY` is not set. Add it to your Replit Secrets and restart."

    try:
        client = genai.Client(api_key=api_key)

        over_under = "over" if total_min > goal_min else "under"
        severity = (
            "CRITICALLY over (you have a problem)"
            if total_min > goal_min * 2
            else "significantly over"
            if total_min > goal_min * 1.4
            else over_under
        )

        prompt = f"""You are a holistic life coach who is brutally honest, data-driven, and genuinely invested in the user's wellbeing.

The user's screen time data for today:
{data_string}

Total screen time: {total_min} minutes ({total_min/60:.1f} hours)
Daily goal: {goal_min} minutes ({goal_min/60:.1f} hours)
Status: {severity} their daily goal

Your instructions:
1. Open with a single punchy sentence summarizing what the data tells you about this person's day — no fluff.
2. Analyze EACH category specifically. Do NOT give vague generic advice.
3. For every problematic category (over 45 min), suggest a specific PHYSICAL, REAL-WORLD replacement:
   - Social Media over 2h → specific fitness routine, outdoor activity, or in-person social plan
   - Entertainment over 2h → cooking a new recipe, reading a physical book, a walk outside
   - Coding over 4h → stretching routine, pomodoro enforcement, desk ergonomics check
4. Highlight any positive category (Education, Health) and encourage it.
5. End with ONE powerful, specific action they can take RIGHT NOW to improve tomorrow.
6. Be direct. Be specific. No filler sentences. No "consider trying to maybe reduce..."

Format with clear markdown sections. Use **bold** for category names. Max 380 words."""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text or "No response received from Gemini."

    except Exception as e:
        return f"⚠️ AI analysis error: `{str(e)}`\n\nCheck your `GOOGLE_API_KEY` secret."


def get_avatar_prompt(total_min: int, goal_min: int) -> tuple[str, str]:
    ratio = total_min / goal_min if goal_min > 0 else 1

    if ratio < 0.7:
        label = "🏆 Digital Warrior"
        prompt = (
            "a powerful focused warrior meditating on a mountain summit at sunrise, "
            "digital art, vibrant golden light, no phone, no screen, motivated energetic hero"
        )
    elif ratio < 1.0:
        label = "⚖️ The Balanced One"
        prompt = (
            "a calm balanced person hiking through a lush green forest, "
            "digital art, warm natural colors, peaceful and grounded, no phone visible"
        )
    elif ratio < 1.5:
        label = "😴 The Tired Scroller"
        prompt = (
            "a tired office worker slumped in a chair surrounded by multiple glowing screens, "
            "digital art, muted blue light, slightly zombified expression, dark room"
        )
    else:
        label = "🧟 The Phone Zombie"
        prompt = (
            "a full zombie completely absorbed by an enormous glowing smartphone, "
            "dark eerie room with blue screen glow, digital addiction metaphor, "
            "dramatic horror art style, phone chains around wrists"
        )

    return label, prompt


def fetch_avatar_image(prompt: str) -> bytes | None:
    url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=512&height=512&nologo=true&seed=99"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.content
        return None
    except Exception:
        return None


# ─────────────────────────────────────────────
# AI COACH SECTION
# ─────────────────────────────────────────────
st.subheader("🤖 AI Life Coach")
st.caption("Powered by Google Gemini — brutally honest, action-focused analysis")

if st.button("🔍 Analyze My Day", type="primary", use_container_width=True):
    col_analysis, col_avatar = st.columns([3, 2])

    with col_analysis:
        with st.spinner("🧠 Gemini is reading your digital soul..."):
            data_summary = aggregate_for_ai(df, selected_date)
            analysis = get_ai_coaching(data_summary, total_today, daily_goal)

        # Severity-aware output
        if total_today > daily_goal * 1.5:
            st.warning("⚠️ **Screen time is critically high. Your AI coach has thoughts.**")
        elif total_today > daily_goal:
            st.info("📊 **You're over your goal today. Here's your coaching report:**")
        else:
            st.success("✅ **Within your goal today — here's how to keep it up:**")

        st.markdown(analysis)

    with col_avatar:
        with st.spinner("🎨 Generating your wellness avatar..."):
            avatar_label, avatar_prompt = get_avatar_prompt(total_today, daily_goal)
            img_bytes = fetch_avatar_image(avatar_prompt)

        st.markdown(f"### {avatar_label}")
        st.caption(f"Based on {total_today} min usage vs {daily_goal} min goal")

        if img_bytes:
            st.image(img_bytes, use_container_width=True)
        else:
            st.warning("Avatar generation failed — check your internet connection.")
            st.code(avatar_prompt, language=None)

st.divider()


# ─────────────────────────────────────────────
# APP BREAKDOWN TABLE
# ─────────────────────────────────────────────
with st.expander("📋 Full App Breakdown for Selected Day"):
    if not today_df.empty:
        display_df = (
            today_df[["App_Name", "Category", "Minutes_Used"]]
            .sort_values("Minutes_Used", ascending=False)
            .reset_index(drop=True)
        )
        display_df.index += 1
        display_df["Hours"] = (display_df["Minutes_Used"] / 60).round(2)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.write("No data available for this day.")


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Life-OS Wellbeing Dashboard · MirAI School of Technology · AI Builder Track 2026 · "
    "Built with Streamlit + Google Gemini"
)
