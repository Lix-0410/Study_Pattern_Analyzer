# 📘 Smart Study Pattern Analyzer  
### Performance Prediction & Burnout Risk Detection using Machine Learning

---

## 🔍 Overview

The **Smart Study Pattern Analyzer** is a machine learning–based application that analyzes **daily study behavior** to predict **academic performance** and assess **burnout risk**.

The project focuses on study habits, cognitive load, and mental well-being, making it applicable to **learners across any field of study**.

The system provides:

- 📊 Performance predictions  
- 🔥 Burnout risk detection (Low → Very High)  
- 📈 Confidence-aware outputs  
- 🧠 Actionable, habit-based recommendations  
- 🖥️ An interactive Streamlit-based user interface  

This project emphasizes **realistic ML system behavior**, not just model accuracy.

---

## 🎯 Objectives

- Predict expected **performance score (0–100)**  
- Detect **early signs of burnout**  
- Quantify model confidence at inference time  
- Recommend **healthy, practical study adjustments**  
- Demonstrate an **end-to-end ML pipeline**, from data generation to deployment  

---

## 🧠 Machine Learning Pipeline

### 1️⃣ Data Generation

- Synthetic yet **realistic daily study logs**
- Includes controlled **edge cases**, such as:
  - Cramming sessions  
  - Sleep deprivation  
  - Excessive screen exposure  
- Designed to reduce data leakage and prevent trivial correlations  

> ⚠️ Note: The dataset is synthetic and intended for learning, experimentation, and system design.

---

### 2️⃣ Feature Engineering

Raw behavioral inputs are transformed into meaningful signals:

- **Focus Score** – study efficiency relative to breaks  
- **Fatigue Index** – imbalance between study hours and sleep  
- **Effective Study Cap** – prevents overstudying from being rewarded  
- **Revision Intensity** – revision activity indicator  
- **Cognitive Load** – difficulty × study hours  
- **Productivity Index** – composite behavioral metric  

Feature design prioritizes **interpretability and alignment with human intuition**.

---

## 📊 Models Used

### 🔹 Performance Prediction

- **Task:** Regression  
- **Model:** Gradient Boosting Regressor  

**Why this model?**
- Handles non-linear relationships well  
- Strong performance on tabular behavioral data  
- Smaller model size compared to Random Forest  
- Suitable for deployment  

**Performance Metrics:**
- MAE ≈ **4–5**  
- R² ≈ **0.83–0.86**

The model predicts expected performance based on **daily study patterns**, not raw effort alone.

---

### 🔹 Burnout Risk Detection

- **Task:** Binary Classification  
- **Model:** Random Forest Classifier (class-balanced)  

**Key Metrics:**
- Burnout Recall ≈ **90%**  
- F1-score ≈ **0.88**

The model prioritizes **early burnout detection**.  
Inference-time logic combines model probability with calibrated rule-based scoring to ensure intuitive behavior in extreme cases.

---

## 🖥️ Interactive Web Application

The Streamlit-based application allows users to:

- Enter daily study parameters using **hours and minutes**
- View predicted performance scores
- See burnout risk probability with confidence indicators
- Receive **context-aware recommendations**
- Safely handle extreme inputs (e.g., low sleep + high workload)

The UI is designed to match how users naturally think about time and effort.

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Data & ML:** NumPy, Pandas, Scikit-learn  
- **Visualization:** Matplotlib  
- **Deployment:** Streamlit  
- **Model Persistence:** Joblib  

---



