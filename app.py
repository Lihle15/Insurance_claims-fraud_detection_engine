import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Claims Triage & Fraud Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .title-text {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle-text {
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_trained_model():
    np.random.seed(42)
    n_samples = 1200

    data = {
        'claim_amount': np.random.randint(5000, 350000, size=n_samples),
        'months_as_customer': np.random.randint(1, 120, size=n_samples),
        'previous_claims': np.random.randint(0, 5, size=n_samples),
        'police_report_filed': np.random.choice([0, 1], size=n_samples, p=[0.4, 0.6]),
    }

    df = pd.DataFrame(data)
    df['is_fraud'] = (
        (df['claim_amount'] > 180000) & (df['months_as_customer'] < 14) & (df['previous_claims'] >= 2)
    ).astype(int)

    X = df[['claim_amount', 'months_as_customer', 'previous_claims', 'police_report_filed']]
    y = df['is_fraud']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=120, random_state=42)
    clf.fit(X_train, y_train)
    return clf

model = load_trained_model()

if 'claims_queue' not in st.session_state:
    st.session_state['claims_queue'] = [
        {"Claim ID": "CLM-9042", "Policyholder": "S. Dlamini", "Amount (ZAR)": "R 125,000", "Tenure": "6 mos", "Risk Category": "High Risk (Flagged)", "Triage Action": "SIU Review"},
        {"Claim ID": "CLM-9043", "Policyholder": "M. Naidoo", "Amount (ZAR)": "R 18,500", "Tenure": "36 mos", "Risk Category": "Low Risk (Passed)", "Triage Action": "Auto-Approve"},
        {"Claim ID": "CLM-9044", "Policyholder": "K. van der Merwe", "Amount (ZAR)": "R 310,000", "Tenure": "2 mos", "Risk Category": "High Risk (Flagged)", "Triage Action": "SIU Review"}
    ]

with st.sidebar:
    st.markdown("### System Controls")
    preset = st.radio("Load Test Scenario", ["Custom Input", "High Risk / Suspicious Claim", "Low Risk / Fast-Track Claim"])
    
    if preset == "High Risk / Suspicious Claim":
        default_amount, default_tenure, default_claims, default_police = 245000, 3, 4, 1
    elif preset == "Low Risk / Fast-Track Claim":
        default_amount, default_tenure, default_claims, default_police = 18000, 48, 0, 0
    else:
        default_amount, default_tenure, default_claims, default_police = 75000, 24, 1, 0

    st.divider()
    st.caption("AI Model: RandomForestClassifier v1.2")

st.markdown('<p class="title-text">Automated Claims Triage & Fraud Detection Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Real-time risk scoring, anomaly detection, and automated routing for insurance policy claims.</p>', unsafe_allow_html=True)

col_input, col_analytics = st.columns([1, 1.3], gap="medium")

with col_input:
    st.markdown("### Claim Input Parameters")
    policyholder_name = st.text_input("Policyholder Name", value="T. Khumalo")
    claim_amount = st.number_input("Claim Amount (ZAR)", min_value=1000, max_value=1000000, value=default_amount, step=5000)
    months_as_customer = st.number_input("Customer Tenure (Months)", min_value=1, max_value=300, value=default_tenure, step=1)
    previous_claims = st.number_input("Previous Claims History", min_value=0, max_value=20, value=default_claims, step=1)
    
    police_report_option = st.selectbox("Police Report Filed", options=["Yes", "No"], index=default_police)
    police_report_filed = 1 if police_report_option == "Yes" else 0
    
    st.markdown("<br>", unsafe_allow_html=True)
    run_assessment = st.button("Run AI Risk Assessment", type="primary", use_container_width=True)

input_data = np.array([[claim_amount, months_as_customer, previous_claims, police_report_filed]])
prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0][1]

if run_assessment:
    new_id = f"CLM-{np.random.randint(9050, 9999)}"
    risk_label = "High Risk (Flagged)" if (prediction == 1 or probability > 0.5) else "Low Risk (Passed)"
    action_label = "SIU Review" if prediction == 1 or probability > 0.5 else "Auto-Approve"
    
    new_entry = {
        "Claim ID": new_id,
        "Policyholder": policyholder_name,
        "Amount (ZAR)": f"R {claim_amount:,.0f}",
        "Tenure": f"{months_as_customer} mos",
        "Risk Category": risk_label,
        "Triage Action": action_label
    }
    st.session_state['claims_queue'].insert(0, new_entry)

with col_analytics:
    st.markdown("### Real-Time Risk Analytics")
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = probability * 100,
        number = {'suffix': "%", 'font': {'size': 32}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "#ef4444" if probability > 0.5 else "#22c55e"},
            'bgcolor': "rgba(128, 128, 128, 0.1)",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(34, 197, 94, 0.15)'},
                {'range': [30, 70], 'color': 'rgba(234, 179, 8, 0.15)'},
                {'range': [70, 100], 'color': 'rgba(239, 68, 68, 0.15)'}
            ],
        }
    ))
    fig.update_layout(height=210, margin=dict(l=20, r=20, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    
    if run_assessment:
        if prediction == 1 or probability > 0.5:
            st.error(f"**HIGH RISK ANOMALY DETECTED** (Risk Index: {probability:.1%})")
            st.markdown("**Action Required:** Route to Special Investigations Unit (SIU) for manual review.")
        else:
            st.success(f"**LOW RISK CLAIM** (Risk Index: {probability:.1%})")
            st.markdown("**Action Required:** Fast-track for automated payout processing.")
    else:
        st.info("Adjust parameters on the left and click **Run AI Risk Assessment** to evaluate.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Risk Factor Breakdown & Claim Insights")
fcol1, fcol2, fcol3 = st.columns(3)

with fcol1:
    ratio = claim_amount / max(months_as_customer, 1)
    st.metric(label="Claim-to-Tenure Ratio", value=f"R{ratio:,.0f}/mo")

with fcol2:
    report_status = "Verified" if police_report_filed == 1 else "Missing"
    st.metric(label="Police Verification", value=report_status)

with fcol3:
    history_level = "High Risk" if previous_claims >= 3 else ("Moderate" if previous_claims >= 1 else "Clean")
    st.metric(label="Historical Claim Density", value=history_level)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Active Claims Queue (Dynamic Batch Triage)")
st.caption("This queue updates in real-time as new claims are evaluated and routed through the AI model.")

queue_df = pd.DataFrame(st.session_state['claims_queue'])
st.dataframe(queue_df, use_container_width=True, hide_index=True)