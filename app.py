import streamlit as st
import pandas as pd
import joblib

perf_model = joblib.load("models/performance_model.pkl")
burnout_model = joblib.load("models/burnout_model.pkl")

st.set_page_config(
    page_title="Smart Study Pattern Analyzer",
    layout="centered"
)

st.title("📘 Smart Study Pattern Analyzer")
st.write(
    "Enter your study details to predict performance "
    "and assess burnout risk."
)

st.header("🧑‍🎓 Your Study Details")

study_hours = st.slider("Study hours per day", 0.5, 10.0, 4.0)
sleep_hours = st.slider("Sleep hours", 1.0, 10.0, 7.0)
break_count = st.slider("Number of breaks", 1, 10, 3)
avg_break_duration = st.slider("Average break duration (minutes)", 5, 40, 10)
screen_time = st.slider("Screen time (hours)", 1.0, 12.0, 4.0)

difficulty_level = st.slider(
    "Difficulty of what you're studying (1 = Easy, 5 = Very Hard)",
    1, 5, 3
)

revision_done = st.selectbox(
    "Did you revise today?",
    [0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

mood_score = st.slider(
    "Your mental state today (1 = Very stressed, 5 = Highly motivated)",
    1, 5, 3
)

focus_score = study_hours / (break_count + 1)
fatigue_index = study_hours / sleep_hours
consistency_score = study_hours          
revision_intensity = revision_done

cognitive_load = difficulty_level * study_hours

productivity_index = (
    0.35 * focus_score +
    0.30 * consistency_score +
    0.20 * revision_intensity -
    0.15 * fatigue_index
)

input_data = {
    "difficulty_level": difficulty_level,
    "study_hours": study_hours,
    "break_count": break_count,
    "avg_break_duration": avg_break_duration,
    "sleep_hours": sleep_hours,
    "screen_time": screen_time,
    "revision_done": revision_done,
    "mood_score": mood_score,
    "focus_score": focus_score,
    "fatigue_index": fatigue_index,
    "consistency_score": consistency_score,
    "revision_intensity": revision_intensity,
    "cognitive_load": cognitive_load,
    "productivity_index": productivity_index
}

df_input = pd.DataFrame([input_data])

def burnout_advice(burnout_prob, user):
    advice = []

    if burnout_prob >= 0.75:
        advice.append("⚠️ Very high burnout risk detected.")

        if user["sleep_hours"] < 6:
            advice.append("Increase sleep to at least 7 hours.")

        if user["study_hours"] > 6:
            advice.append("Reduce daily study hours temporarily.")

        if user["screen_time"] > 6:
            advice.append("Limit screen exposure, especially at night.")

        advice.append("Take a rest or light study day this week.")

    elif burnout_prob >= 0.4:
        advice.append("⚠️ Moderate burnout risk.")
        advice.append("Maintain balance and monitor fatigue levels.")

    else:
        advice.append("✅ Low burnout risk. Keep your current routine.")

    return advice

if st.button("🔍 Analyze My Study Pattern"):
    perf_pred = perf_model.predict(df_input)[0]
    burnout_prob = burnout_model.predict_proba(df_input)[0][1]

    st.subheader("📊 Results")
    st.metric("Predicted Performance Score", f"{perf_pred:.1f} / 100")
    st.metric("Burnout Risk Probability", f"{burnout_prob * 100:.1f}%")

    st.subheader("🧠 Recommendations")
    for tip in burnout_advice(burnout_prob, input_data):
        st.write("•", tip)
