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
consistency_score = min(study_hours,6)          
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

def sanitize_inputs(user):
    return {
        "study_hours": min(max(user["study_hours"], 0.5), 10),
        "sleep_hours": min(max(user["sleep_hours"], 1), 10),
        "screen_time": min(max(user["screen_time"], 0), 12),
        "break_count": min(max(user["break_count"], 0), 10),
        "mood_score": min(max(user["mood_score"], 1), 5)
    }

def compute_raw_burnout_score(user):
    sleep_penalty = min(7 - user["sleep_hours"], 5)
    study_penalty = min(user["study_hours"], 8)
    screen_penalty = min(user["screen_time"], 8)
    break_penalty = min(user["break_count"], 6)
    mood_penalty = 5 - user["mood_score"]

    return (
        0.6 * sleep_penalty +
        0.4 * study_penalty +
        0.3 * screen_penalty +
        0.3 * break_penalty +
        0.5 * mood_penalty
    )

def burnout_advice(burnout_level, user):
    advice = []

    
    advice.append(f"🔥 Burnout Level: {burnout_level}")

    
    if burnout_level == "Low":
        advice.append("✅ Your burnout risk is low today.")

        if user["sleep_hours"] < 7:
            advice.append("🛌 Getting a bit more sleep could further improve focus.")

        if user["screen_time"] > 6:
            advice.append("📵 Slightly reducing screen time may help maintain energy.")

        advice.append("👍 Keep maintaining a healthy balance.")

   
    elif burnout_level == "Moderate":
        advice.append("🟡 You may be starting to feel some mental or physical strain.")

        if user["sleep_hours"] < 6:
            advice.append("😴 Your sleep is on the lower side. Prioritizing rest can help.")

        if user["study_hours"] > 6:
            advice.append("📖 Consider slightly reducing study hours or improving breaks.")

        if user["screen_time"] > 6:
            advice.append("📵 Reducing screen time at night may improve recovery.")

        advice.append("🔍 Small adjustments now can prevent burnout later.")

    
    else:
        advice.append("🚨 High burnout risk detected.")

        if user["sleep_hours"] < 5:
            advice.append("😴 Severe sleep deprivation detected.")

        if user["study_hours"] > 8:
            advice.append("📚 Very high workload detected.")

        advice.append("🧠 Strongly recommend taking rest or reducing workload.")

    return advice



if st.button("🔍 Analyze My Study Pattern"):
    # Performance prediction
    perf_pred = perf_model.predict(df_input)[0]

    # Burnout probability
    burnout_prob = burnout_model.predict_proba(df_input)[0][1]
    burnout_prob = min(max(burnout_prob, 0.05), 0.95)

    # Burnout score
    clean_user = sanitize_inputs(input_data)
    raw_score = compute_raw_burnout_score(clean_user)

    # Burnout level
    if raw_score >= 7.5:
        burnout_level = "Very High"
    elif raw_score >= 5.5:
        burnout_level = "High"
    elif raw_score >= 3.5:
        burnout_level = "Moderate"
    else:
        burnout_level = "Low"


    st.subheader("📊 Results")

    st.metric("Predicted Performance Score", f"{perf_pred:.1f} / 100")
    st.metric("Burnout Risk Probability", f"{burnout_prob * 100:.1f}%")
    st.metric("Burnout Score", f"{raw_score:.2f}")

    st.subheader("🧠 Recommendations")
    for tip in burnout_advice(burnout_level, input_data):
        st.write("•", tip)
