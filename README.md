# 📘 Smart Study Pattern Analyzer  
### Performance Prediction & Burnout Risk Detection using Machine Learning

---

## 🔍 Overview

The **Smart Study Pattern Analyzer** is a machine learning–based application that analyzes daily study behavior to **predict academic performance** and **detect burnout risk**.

It focuses on *study behavior, cognitive load, and mental well-being*, making it applicable to **any learner, any field of study**.

The system provides:
- Performance predictions
- Burnout risk detection
- Confidence-aware outputs
- Actionable study recommendations
- An interactive Streamlit-based user interface

---

## 🎯 Objectives

- Predict expected **performance score (0–100)**
- Detect **burnout risk** early
- Quantify **model confidence**
- Recommend **healthy study adjustments**
- Demonstrate an end-to-end ML pipeline

---

## 🧠 Machine Learning Pipeline

### 1️⃣ Data Generation
- Synthetic yet **realistic daily study logs**
- Includes rare edge cases:
  - Cramming
  - Sleep deprivation
  - Excessive screen time
- Designed to avoid data leakage and overfitting

### 2️⃣ Feature Engineering
Raw behavioral data is transformed into meaningful signals:

- **Focus Score** – study quality vs distractions  
- **Fatigue Index** – study–sleep imbalance  
- **Consistency Score** – 7-day rolling average  
- **Revision Intensity** – weekly revision frequency  
- **Cognitive Load** – difficulty × study hours  
- **Productivity Index** – composite behavioral metric  

---

## 📊 Models Used

### 🔹 Performance Prediction
- **Task:** Regression  
- **Model:** **Gradient Boosting Regressor**
- **Reason for choice:**
  - Handles non-linear relationships well
  - Strong performance on tabular data
  - Significantly smaller model size than Random Forest
  - Easier deployment

**Performance:**
- MAE ≈ **4–5**
- R² ≈ **0.83–0.86**
Predicts academic performance based on behavioral patterns.

---

### 🔹 Burnout Risk Detection
- **Type:** Binary Classification  
- **Model:** Random Forest Classifier (class-balanced)

**Key Metrics:**
- Burnout Recall ≈ **90%**
- F1-score ≈ **0.88**

Designed to **prioritize early burnout detection**.

---

## 🖥️ Interactive Web App

Built using **Streamlit**, the app allows users to:
- Enter daily study parameters
- View predicted performance score
- See burnout risk probability with confidence
- Receive appropriate recommendations

---

## 🛠️ Tech Stack

- **Python**
- **NumPy, Pandas**
- **Matplotlib**
- **Scikit-learn**
- **Streamlit**
- **Joblib**

---
