import streamlit as st
import plotly.express as px
import pandas as pd
import joblib
import sqlite3
import base64
import hashlib

from disease_info import disease_details
from chatbot import ask_health_question
from pdf_generator import generate_report

st.set_page_config(
    page_title="MediScan AI",
    page_icon="🏥",
    layout="wide"
)
def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()
conn = sqlite3.connect(
    "mediscan.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (

id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,

patient_name TEXT,

age INTEGER,

gender TEXT,

disease TEXT,

confidence TEXT,

severity TEXT

)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()

model = joblib.load("model.pkl")
if not st.session_state.get("logged_in", False):

    st.markdown("""
    <style>

    .login-container{
        max-width:600px;
        margin:auto;
        padding-top:30px;
    }

    .login-title{
        font-size:55px;
        font-weight:700;
        color:#2F3241;
        margin-bottom:5px;
    }

    .login-subtitle{
        font-size:20px;
        color:#8B8E9B;
        margin-bottom:30px;
    }

    .welcome-text{
        font-size:65px;
        font-weight:700;
        color:#2F3241;
        margin-bottom:30px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="login-container">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-title">MediScan AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subtitle">Secure Healthcare Dashboard</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(
        ["Login", "Register"]
    )

    # ---------------- LOGIN ----------------

    with tab1:

        st.markdown(
            '<div class="welcome-text">Welcome Back</div>',
            unsafe_allow_html=True
        )

        username = st.text_input(
            "Email Address",
            placeholder="Enter Gmail Address"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter Password"
        )

        col1, col2 = st.columns([1,1])

        with col1:
            remember = st.checkbox(
                "Remember for 30 days"
            )

        with col2:
            st.markdown(
                "<div style='text-align:right;padding-top:8px;'>Forgot Password?</div>",
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "Sign In",
            use_container_width=True
        ):

            hashed_password = hashlib.sha256(
                password.encode()
            ).hexdigest()

            cursor.execute(
                """
                SELECT * FROM users
                WHERE username=? AND password=?
                """,
                (
                    username.strip(),
                    hashed_password
                )
            )

            user = cursor.fetchone()

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "Invalid Email or Password"
                )

    # ---------------- REGISTER ----------------

    with tab2:

        st.markdown(
            '<div class="welcome-text">Register</div>',
            unsafe_allow_html=True
        )

        new_user = st.text_input(
            "Gmail Address"
        )

        new_pass = st.text_input(
            "Password",
            type="password",
            key="reg_pass"
        )

        confirm_pass = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not new_user.endswith("@gmail.com"):

                st.error(
                    "Email must end with @gmail.com"
                )

            elif new_pass != confirm_pass:

                st.error(
                    "Passwords do not match"
                )

            else:

                try:

                    hashed_password = hashlib.sha256(
                        new_pass.encode()
                    ).hexdigest()

                    cursor.execute(
                        """
                        INSERT INTO users
                        (
                            username,
                            password
                        )
                        VALUES (?,?)
                        """,
                        (
                            new_user.strip(),
                            hashed_password
                        )
                    )

                    conn.commit()

                    st.success(
                        "Account Created Successfully"
                    )

                except:

                    st.error(
                        "Email Already Exists"
                    )

    st.stop()
if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "confidence" not in st.session_state:
    st.session_state.confidence = None

if "severity" not in st.session_state:
    st.session_state.severity = None

if "history" not in st.session_state:
    st.session_state.history = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""
st.markdown("""
<style>

.stApp {
    background-color: #F4F9FF;
}

h1 {
    color: #0A66FF;
}

[data-testid="stMetric"] {

    background: rgba(
        255,
        255,
        255,
        0.9
    );

    padding:20px;

    border-radius:18px;

    box-shadow:
    0 8px 20px rgba(
        0,
        0,
        0,
        0.1
    );
}



.stButton > button {
    background: linear-gradient(
        90deg,
        #0A66FF,
        #4DA6FF
    );

    color:white;
    border:none;
    border-radius:15px;
    height:55px;
    font-size:18px;
    font-weight:bold;
}



/* Sidebar Styling */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0A66FF,
        #003B99
    );
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0A66FF,
        #003B99
    );
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div {
    color: white;
}
            
</style>
""", unsafe_allow_html=True)

st.sidebar.image(
    "assets/logo.png",
    width=150
)
if st.session_state.logged_in:
    st.sidebar.success(
        f"Welcome {st.session_state.username}"
    )
st.sidebar.markdown("""
# 🏥 MediScan AI

### AI-Powered Healthcare Assistant

---
""")

st.sidebar.markdown("""
### 📊 Dashboard

**Supported Diseases:** 12

**Prediction Model:** Random Forest

**Version:** 2.0
""")


st.sidebar.markdown("""
---

### 🚀 Quick Stats

🩺 Diseases Supported: 12

📄 PDF Reports: Enabled

📊 Visual Analytics: Enabled

🤖 AI Assistant: Enabled

⚡ Version: 2.0

---

### 🩺 Medical Notice

This application is intended for
educational purposes only and does
not replace professional medical advice.

---

### 👩‍💻 Developer

**Shreya Chaudhary**

""")
if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False

    st.session_state.username = ""

    st.rerun()
logo_base64 = get_base64_image("assets/logo.png")
st.markdown(f"""
<div style="
background: linear-gradient(90deg,#1E64F0,#5AA4F2);
padding:40px;
border-radius:25px;
color:white;
text-align:center;
margin-bottom:20px;
">

<div style="
display:flex;
justify-content:center;
align-items:center;
gap:25px;
">

<img src="data:image/png;base64,{logo_base64}"
width="150"
style="margin-right:20px;">
<div>
<h1 style="
margin:0;
font-size:60px;
font-weight:700;
color:white;
">
MediScan AI
</h1>

<p style="
font-size:22px;
margin-top:15px;
color:white;
text-align:center;
">
AI-Powered Disease Prediction & Healthcare Assistant
</p>

</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Diseases Supported",
        "12"
    )

with col2:
    st.metric(
        "Prediction Engine",
        "Random Forest"
    )

with col3:
    st.metric(
        "Version",
        "2.0"
    )

st.markdown("""
<div style="
background:white;
padding:25px;
border-radius:20px;
box-shadow:0px 4px 15px rgba(0,0,0,0.08);
margin-bottom:20px;
">

<h2>👋 Welcome to MediScan AI</h2>

<p style="font-size:18px;">
Analyze symptoms, predict possible diseases,
check severity levels, receive precautions,
and generate medical reports using AI.
</p>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 👤 Patient Information")

col1, col2 = st.columns(2)

with col1:

    patient_name = st.text_input(
        "Patient Name"
    )
    uploaded_photo = st.file_uploader(
        "📸 Upload Patient Photo",
        type=["jpg", "jpeg", "png"]
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=25
    )

with col2:

    gender = st.selectbox(
        "Gender",
        [
            "Male",
            "Female",
            "Other"
        ]
    )

    blood_group = st.selectbox(
        "Blood Group",
        [
            "A+",
            "A-",
            "B+",
            "B-",
            "AB+",
            "AB-",
            "O+",
            "O-"
        ]
    )

st.markdown("### 📏 Health Metrics")

col1, col2 = st.columns(2)

with col1:

    height = st.number_input(
        "Height (cm)",
        min_value=50,
        max_value=250,
        value=170
    )

with col2:

    weight = st.number_input(
        "Weight (kg)",
        min_value=10,
        max_value=300,
        value=70
    )

bmi = round(
    weight / ((height / 100) ** 2),
    1
)

if bmi < 18.5:
    bmi_status = "Underweight"

elif bmi < 25:
    bmi_status = "Normal"

elif bmi < 30:
    bmi_status = "Overweight"

else:
    bmi_status = "Obese"

st.metric(
    "🏥 BMI Score",
    bmi,
    bmi_status
)
if uploaded_photo:

    st.image(
        uploaded_photo,
        width=180,
        caption="Patient Photo"
    )
st.markdown("## 📋 Patient Summary")

photo_col, summary_col1, summary_col2 = st.columns([1,2,2])
with photo_col:

    if uploaded_photo:

        st.image(
            uploaded_photo,
            width=150
        )
with summary_col1:
    st.write(f"**👤 Name:** {patient_name}")
    st.write(f"**🎂 Age:** {age}")
    st.write(f"**⚧ Gender:** {gender}")

with summary_col2:
    st.write(f"**🩸 Blood Group:** {blood_group}")
    st.write(f"**📏 Height:** {height} cm")
    st.write(f"**⚖ Weight:** {weight} kg")

st.info(
    f"🏥 BMI: {bmi} ({bmi_status})"
)

st.markdown("## 🩺 Health Risk Analysis")
risk_score = 0

# Age Risk
if age >= 60:
    risk_score += 30

elif age >= 40:
    risk_score += 15

# BMI Risk
if bmi >= 30:
    risk_score += 30

elif bmi >= 25:
    risk_score += 15

if risk_score < 20:
    risk_level = "Low"

elif risk_score < 50:
    risk_level = "Medium"

else:
    risk_level = "High"

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Risk Score",
        f"{risk_score}/100"
    )

with col2:
    st.metric(
        "Risk Level",
        risk_level
    )

if risk_level == "High":
    st.error(
        "🚨 High Health Risk"
    )

elif risk_level == "Medium":
    st.warning(
        "⚠️ Moderate Health Risk"
    )

else:
    st.success(
        "✅ Low Health Risk"
    )

st.markdown("""
### 🩺 Select Symptoms

Choose all symptoms you are currently experiencing.
""")
col1, col2 = st.columns(2)

with col1:
    fever = st.checkbox("🤒 Fever")
    headache = st.checkbox("🤕 Headache")
    sore_throat = st.checkbox("😷 Sore Throat")
    nausea = st.checkbox("🤢 Nausea")

with col2:
    cough = st.checkbox("😮‍💨 Cough")
    fatigue = st.checkbox("😴 Fatigue")
    body_pain = st.checkbox("🦴 Body Pain")

predict_clicked = st.button(
    "Predict Disease"
)

if predict_clicked:

    input_data = pd.DataFrame([[
        int(fever),
        int(cough),
        int(headache),
        int(fatigue),
        int(sore_throat),
        int(body_pain),
        int(nausea)
    ]], columns=[
        "fever",
        "cough",
        "headache",
        "fatigue",
        "sore_throat",
        "body_pain",
        "nausea"
    ])

    prediction = model.predict(input_data)[0]
    
    confidence = max(
        model.predict_proba(input_data)[0]
    )

    info = disease_details[prediction]
    severity = info["severity"]

    st.session_state.history.append({
        "Patient": patient_name,
        "Age": age,
        "Gender": gender,
        "Disease": prediction,
        "Confidence": f"{confidence:.0%}",
        "Severity": severity
    })

    cursor.execute(
        """
        INSERT INTO predictions
        (
           username,
           patient_name,
           age,
           gender,
           disease,
           confidence,
           severity
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
           st.session_state.username,
           patient_name,
           age,
           gender,
           prediction,
           f"{confidence:.0%}",
           severity
        )
    )
    conn.commit()

    st.markdown("## 📊 Prediction Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🩺 Disease",
            prediction
        )
    with col2:
        st.metric(
            "🎯 Confidence",
            f"{confidence:.0%}"
        )
    with col3:
        st.metric(
            "⚠️ Severity",
            severity
        )
    
    st.metric(
    "Prediction Confidence",
    f"{confidence:.0%}"
    )

    probabilities = model.predict_proba(
        input_data
    )[0]
    
    fig = px.bar(
        x=model.classes_,
        y=probabilities,
        title="Disease Probability"
    )
    
    st.plotly_chart(
        fig,
         width="stretch"
    )
    
    if severity == "High":
        st.error(
            "🚨 High Risk Case - Medical Consultation Recommended"
   
        )
    elif severity == "Medium":
        st.warning(
             "⚠️ Moderate Risk - Monitor Symptoms Carefully"
        )
    
    else:
        st.success(
            "✅ Low Risk - Follow Precautions"
        )

    st.subheader("🛡 Recommended Precautions")
    
    for p in info["precautions"]:
        st.write("✅", p)

    st.subheader("👨‍⚕️ Recommended Specialist")
    st.write(info["doctor"])
    
    st.divider()

    st.subheader("📋 Disease Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(
            f"""
            
    Overview
    
    {info['overview']}
    """
        )
        st.success(
            f"""
    Recovery Time
    
    {info['recovery']}
    """
         )
    with col2:
        st.warning(
            f"""
    Common Causes
    
    {info['causes']}
    """
        )
        
        st.info(
            f"""
    Recommended Specialist
    {info['doctor']}
    """
        )

    report_file = generate_report(
        patient_name,
        age,
        gender,
        blood_group,
        height,
        weight,
        bmi,
        risk_level,
        prediction,
        f"{confidence:.0%}",
        severity,
        info["precautions"],
        info["doctor"]
    )
    
    with open(report_file, "rb") as file:
        st.download_button(
            label="📄 Download Medical Report",
            data=file,
            file_name="MediScan_Report.pdf",
            mime="application/pdf"
        )

if st.session_state.prediction is not None and not predict_clicked:

    st.subheader("Previous Prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Disease",
            st.session_state.prediction
        )

    with col2:
        st.metric(
            "Confidence",
            f"{st.session_state.confidence:.0%}"
        )

    with col3:
        st.metric(
            "Severity",
            st.session_state.severity
        )

    st.subheader("Precautions")

    for p in st.session_state.info["precautions"]:
        st.write("✅", p)

    st.subheader("Recommended Doctor")

    st.write(
        st.session_state.info["doctor"]
    )
    

st.divider()
st.subheader("🤖 AI Health Assistant")
if "ai_answer" not in st.session_state:
    st.session_state.ai_answer = ""

with st.form("health_form"):

    question = st.text_input(
        "Ask a health question"
    )

    submitted = st.form_submit_button(
        "Ask AI"
    )

if submitted and question:
    with st.spinner("🤖 MediScan AI is analyzing your health question..."):
        st.session_state.ai_answer = (
            ask_health_question(question)
        )

if st.session_state.ai_answer:

    st.markdown(
        "### 🩺 AI Health Response"
    )

    st.write(
        st.session_state.ai_answer
    )
st.divider()

st.subheader("📜 Prediction History")

if len(st.session_state.history) > 0:

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

else:

    st.info(
        "No predictions made yet."
    )
st.divider()

st.subheader("📊 Analytics Dashboard")

if len(st.session_state.history) > 0:

    total_predictions = len(
        st.session_state.history
    )

    disease_counts = {}

    for item in st.session_state.history:

        disease = item["Disease"]

        if disease not in disease_counts:
            disease_counts[disease] = 0

        disease_counts[disease] += 1

    most_predicted = max(
        disease_counts,
        key=disease_counts.get
    )
    high_risk_cases = 0
    confidence_sum = 0

    for item in st.session_state.history:
        if item["Severity"] == "High":
            high_risk_cases += 1
        confidence_sum += int(
            item["Confidence"].replace(
                "%",
                ""
            )
        )
    avg_confidence = round(
        confidence_sum /
        total_predictions
    )
    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Predictions",
            total_predictions
        )

    with col2:

        st.metric(
            "Most Predicted",
            most_predicted
        )
       
    with col3:
        st.metric(
            "High Risk Cases",
            high_risk_cases
        )
    with col4:
        st.metric(
            "Avg Confidence",
            f"{avg_confidence}%"
        )
st.divider()

st.subheader("📈 Disease Statistics")
disease_stats = {}

for item in st.session_state.history:

    disease = item["Disease"]

    if disease not in disease_stats:
        disease_stats[disease] = 0

    disease_stats[disease] += 1
    if disease_stats:
        stats_df = pd.DataFrame(
            {
                "Disease": list(
                    disease_stats.keys()
                ),
                "Count": list(
                    disease_stats.values()
                )
            }
        )
        
        fig = px.bar(
            stats_df,
            x="Disease",
            y="Count",
            title="Disease Prediction Frequency"
        )
        
        st.plotly_chart(
            fig,
            use_container_width=True
        )
st.divider()

st.subheader("🗄 Database Records")
search_name = st.text_input(
    "🔍 Search Patient"
)
if search_name:

    cursor.execute(
        """
        SELECT
        patient_name,
        age,
        gender,
        disease,
        confidence,
        severity
        FROM predictions
        WHERE patient_name LIKE ?
        ORDER BY id DESC
        """,
        (f"%{search_name}%",)
    )

else:

    cursor.execute(
        """
        SELECT
        patient_name,
        age,
        gender,
        disease,
        confidence,
        severity
        FROM predictions
        ORDER BY id DESC
        """
    )

records = cursor.fetchall()
if records:

    db_df = pd.DataFrame(
        records,
        columns=[
            "Patient",
            "Age",
            "Gender",
            "Disease",
            "Confidence",
            "Severity"
        ]
    )

    st.dataframe(
        db_df,
        use_container_width=True
    )

else:

    st.info(
        "No records found."
    )


st.caption(
    "© 2026 MediScan AI | Built by Shreya Chaudhary"
)
