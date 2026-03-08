import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.scoring import calculate_risk

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="Individual Risk Profile",
    page_icon="👤",
    layout="wide"
)

# ── TITLE ────────────────────────────────────────────
st.title("👤 Individual Risk Profile")
st.markdown("Answer honestly — this is for your own understanding, not a diagnosis")
st.markdown("---")

with st.form("risk_form"):

    # ── SECTION 1 — BASIC INFO ───────────────────────
    st.subheader("👤 Basic Information")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Your Name",
            placeholder="Enter your name..."
        )
        age = st.number_input(
            "Age",
            min_value=10,
            max_value=80,
            value=25
        )

    with col2:
        category = st.selectbox(
            "Category",
            ["Student", "Worker"]
        )
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

    st.markdown("---")

    # ── SECTION 2 — SLEEP ────────────────────────────
    st.subheader("😴 Sleep")
    st.caption("Remember — quality matters as much as quantity")
    col1, col2 = st.columns(2)

    with col1:
        sleep_hours = st.slider(
            "How many hours do you sleep on average?",
            min_value=2.0,
            max_value=12.0,
            value=7.0,
            step=0.5
        )

    with col2:
        sleep_quality = st.slider(
            "How refreshed do you feel after waking up? (1=terrible, 10=great)",
            min_value=1,
            max_value=10,
            value=6
        )

    st.markdown("---")

    # ── SECTION 3 — STRESS & WORK ────────────────────
    st.subheader("💼 Stress & Work")
    st.caption("Stress is normal — what matters is how long it lasts and how it feels")
    col1, col2 = st.columns(2)

    with col1:
        stress_level = st.slider(
            "How stressed do you feel overall? (1=calm, 10=very stressed)",
            min_value=1,
            max_value=10,
            value=5
        )
        work_study_hours = st.slider(
            "How many hours do you work or study per day?",
            min_value=0.0,
            max_value=16.0,
            value=8.0,
            step=0.5
        )

    with col2:
        stress_temporary = st.radio(
            "Is your stress mostly temporary (exams, deadlines) or ongoing for months?",
            ["Temporary — due to specific reasons",
             "Ongoing — has been lasting for months"],
            index=0
        )

    st.markdown("---")

    # ── SECTION 4 — LIFESTYLE ────────────────────────
    st.subheader("🏃 Lifestyle")
    col1, col2 = st.columns(2)

    with col1:
        physical_activity = st.slider(
            "Physical activity level (0=none, 100=very active)",
            min_value=0,
            max_value=100,
            value=50
        )

    with col2:
        dietary_habits = st.selectbox(
            "How would you describe your diet?",
            ["Healthy", "Moderate", "Unhealthy"]
        )

    st.markdown("---")

    # ── SECTION 5 — HOW YOU FEEL ─────────────────────
    st.subheader("💭 How You Actually Feel")
    st.caption("These questions matter more than sleep hours or stress scores")
    col1, col2 = st.columns(2)

    with col1:
        social_support = st.slider(
            "Do you have people you can talk to when things get hard? (1=no one, 10=strong support)",
            min_value=1,
            max_value=10,
            value=6
        )
        enjoy_activities = st.slider(
            "Do you still enjoy things you used to enjoy? (1=not at all, 10=fully)",
            min_value=1,
            max_value=10,
            value=7
        )

    with col2:
        feel_hopeless = st.radio(
            "Do you feel hopeless about the future?",
            ["No — I feel okay about the future",
             "Sometimes but it passes",
             "Yes — most of the time"],
            index=0
        )

    st.markdown("---")

    # ── SECTION 6 — MENTAL HEALTH HISTORY ───────────
    st.subheader("🏥 Background (optional but helps accuracy)")
    col1, col2 = st.columns(2)

    with col1:
        anxiety = st.checkbox("I experience anxiety")
        depression_hist = st.checkbox("I have a history of depression")

    with col2:
        family_history = st.checkbox("Family history of mental illness")
        suicidal_thoughts = st.checkbox(
            "I have had suicidal thoughts in the past"
        )

    st.markdown("---")
    submitted = st.form_submit_button(
        "🔍 Analyse My Risk",
        use_container_width=True
    )

# ── RESULTS ──────────────────────────────────────────
if submitted:

    # Convert inputs
    stress_is_temporary = "Temporary" in stress_temporary

    hopeless_map = {
        "No — I feel okay about the future": False,
        "Sometimes but it passes": False,
        "Yes — most of the time": True
    }
    feel_hopeless_val = hopeless_map[feel_hopeless]

    score, risk_level, factors = calculate_risk(
        sleep_hours=sleep_hours,
        stress_level=stress_level,
        sleep_quality=sleep_quality,
        work_study_hours=work_study_hours,
        physical_activity=physical_activity,
        social_support=social_support,
        enjoy_activities=enjoy_activities,
        feel_hopeless=feel_hopeless_val,
        stress_temporary=stress_is_temporary,
        anxiety=anxiety,
        depression_hist=depression_hist,
        family_history=family_history,
        dietary_habits=dietary_habits,
        suicidal_thoughts=suicidal_thoughts
    )

    st.markdown("---")
    st.subheader(f"Results for {name if name else 'You'}")

    # ── IMPORTANT DISCLAIMER ─────────────────────────
    st.caption("""
    ⚠️ This is not a medical diagnosis. It is a self-reflection tool
    based on common mental health patterns. If you are concerned
    about your mental health, please speak to a professional.
    """)

    # ── RISK DISPLAY ─────────────────────────────────
    col1, col2, col3 = st.columns(3)

    with col1:
        if risk_level == "High":
            st.error("⚠️ Risk Level: **HIGH**")
        elif risk_level == "Medium":
            st.warning("🟠 Risk Level: **MEDIUM**")
        else:
            st.success("✅ Risk Level: **LOW**")

    with col2:
        st.metric("Score", f"{score} pts")

    with col3:
        st.metric("Sleep Hours", f"{sleep_hours}h")

    st.markdown("---")

    # ── FACTORS ──────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 What's affecting your score")
        for factor in factors:
            st.write(factor)

    with col2:
        st.subheader("💡 What this means for you")

        if risk_level == "High":
            st.error("""
            Several factors are combining to create significant
            risk. This doesn't mean something is wrong with you —
            it means you may benefit from some support right now.

            **Consider:**
            - Talking to a counsellor or therapist
            - Reaching out to someone you trust
            - Taking a break if possible
            - Speaking to a doctor if things feel overwhelming
            """)

        elif risk_level == "Medium":
            st.warning("""
            You have some risk factors but also protective ones.
            You are managing but it's worth paying attention.

            **Consider:**
            - Checking in with yourself regularly
            - Strengthening your social connections
            - Small improvements to sleep or activity
            - Talking to someone if stress becomes overwhelming
            """)

        else:
            st.success("""
            Your protective factors are outweighing your risk
            factors. You seem to be coping well overall.

            **Keep doing:**
            - Whatever support systems you have — they are working
            - Your current activity and lifestyle habits
            - Being self aware like you already are
            - Checking in with yourself occasionally
            """)

    # ── REMEMBER ─────────────────────────────────────
    st.markdown("---")
    st.info("""
    💬 **Remember:** Having stress, less sleep, or hard days
    does NOT automatically mean high mental health risk.
    What matters most is — do you have support, do you still
    find meaning, and do you feel okay about your future?
    Those are the real indicators.
    """)

    # ── SAVE TO SESSION STATE ─────────────────────────
    st.session_state['individual_result'] = {
        'name': name,
        'age': age,
        'category': category,
        'score': score,
        'risk_level': risk_level,
        'sleep_hours': sleep_hours,
        'stress_level': stress_level,
        'sleep_quality': sleep_quality,
        'work_study_hours': work_study_hours,
        'physical_activity': physical_activity
    }

    st.info("💡 Go to the **Predict** page to see what the ML model predicts!")
