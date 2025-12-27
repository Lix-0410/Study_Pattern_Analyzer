import streamlit as st
import pandas as pd
import joblib

perf_model = joblib.load("models/performance_model.pkl")
burnout_model = joblib.load("models/burnout_model.pkl")

st.header("🧑‍🎓 Your Study Details")

# ⏱️ STUDY TIME (Hours + Minutes)

st.subheader("⏱️ Study Duration")

col1, col2 = st.columns(2)
with col1:
    study_hours_h = st.number_input(
        "Study hours",
        min_value=0,
        max_value=10,
        step=1,
        value=4
    )

with col2:
    study_minutes = st.number_input(
        "Study minutes (10-minute steps)",
        min_value=0,
        max_value=50,
        step=10,
        value=0
    )

study_hours = study_hours_h + study_minutes / 60
st.caption(f"📌 Total study time: **{study_hours_h}h {study_minutes}m**")

# 😴 SLEEP TIME (Hours + Minutes)

st.subheader("😴 Sleep Duration")

col1, col2 = st.columns(2)
with col1:
    sleep_hours_h = st.number_input(
        "Sleep hours",
        min_value=1,
        max_value=10,
        step=1,
        value=7
    )

with col2:
    sleep_minutes = st.number_input(
        "Sleep minutes (10-minute steps)",
        min_value=0,
        max_value=50,
        step=10,
        value=0
    )

sleep_hours = sleep_hours_h + sleep_minutes / 60
st.caption(f"🛌 Total sleep: **{sleep_hours_h}h {sleep_minutes}m**")

# ☕ BREAKS

st.subheader("☕ Breaks")

break_count = st.number_input(
    "Number of breaks",
    min_value=0,
    max_value=10,
    step=1,
    value=3
)

avg_break_duration = st.number_input(
    "Average break duration (minutes)",
    min_value=5,
    max_value=40,
    step=5,
    value=10
)

# 📱 SCREEN TIME (Hours + Minutes)

st.subheader("📱 Screen Time")

col1, col2 = st.columns(2)
with col1:
    screen_hours = st.number_input(
        "Screen hours",
        min_value=0,
        max_value=12,
        step=1,
        value=4
    )

with col2:
    screen_minutes = st.number_input(
        "Screen minutes (10-minute steps)",
        min_value=0,
        max_value=50,
        step=10,
        value=0
    )

screen_time = screen_hours + screen_minutes / 60
st.caption(f"📱 Total screen time: **{screen_hours}h {screen_minutes}m**")

# 📚 STUDY DIFFICULTY

st.subheader("📚 Study Difficulty")

difficulty_level = st.number_input(
    "Difficulty (1 = Easy, 5 = Very Hard)",
    min_value=1,
    max_value=5,
    step=1,
    value=3
)

# 🔁 REVISION

st.subheader("🔁 Revision")

revision_done = st.radio(
    "Did you revise today?",
    [1, 0],
    format_func=lambda x: "Yes" if x == 1 else "No",
    horizontal=True
)

# 🙂 MOOD

st.subheader("🙂 Mental State")

mood_score = st.number_input(
    "Mood (1 = Very stressed, 5 = Highly motivated)",
    min_value=1,
    max_value=5,
    step=1,
    value=3
)

# 📝 DAILY SUMMARY

st.markdown("### 📝 Daily Summary")

st.write(
    f"""
    • **Study:** {study_hours_h}h {study_minutes}m  
    • **Sleep:** {sleep_hours_h}h {sleep_minutes}m  
    • **Breaks:** {break_count} (avg {avg_break_duration} min)  
    • **Screen Time:** {screen_hours}h {screen_minutes}m  
    • **Difficulty:** {difficulty_level}/5  
    • **Revision:** {"Yes" if revision_done else "No"}  
    • **Mood:** {mood_score}/5  
    """
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
    sleep_penalty = max(0, 7 - user["sleep_hours"])
    study_penalty = max(0, user["study_hours"] - 3)
    screen_penalty = max(0, user["screen_time"] - 3)
    break_penalty = max(0, user["break_count"] - 2)
    mood_penalty = max(0, 4 - user["mood_score"])

    burnout = (
        0.7 * sleep_penalty +
        0.4 * study_penalty +
        0.3 * screen_penalty +
        0.3 * break_penalty +
        0.5 * mood_penalty
    )

    return round(burnout, 2)

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
    elif raw_score >= 5:
        burnout_level = "High"
    elif raw_score >= 2.5:
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




