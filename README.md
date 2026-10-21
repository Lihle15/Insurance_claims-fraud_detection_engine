# AI Insurance Claims Triage & Fraud Detection Engine

An enterprise-ready, real-time risk scoring and automated claim triage dashboard built with **Python**, **Streamlit**, **Scikit-Learn**, and **Plotly**. Localized for South African Rand (ZAR) operational contexts.

---

## 📌 Executive Summary & Problem Statement

### Problem Statement
Traditional insurance claims processing heavily relies on manual review workflows. This reliance introduces significant operational bottlenecks, slow claim turnaround times, and high administrative overhead. Crucially, manual triage struggles to efficiently identify fraudulent or anomalous claims amidst high transaction volumes, resulting in substantial financial leakages for insurance providers.

### The Solution
The **Automated Claims Triage & Fraud Detection Engine** introduces an AI-driven real-time risk assessment pipeline. Powered by a **Random Forest Classification model**, the system dynamically scores incoming policy claims based on risk indicators—such as claim-to-tenure ratios, historical claim frequency, and police report verification status—to automatically route legitimate low-risk claims for fast-track payout while flagging high-risk anomalies for Special Investigations Unit (SIU) forensic review.

---

## 🚀 Key Features

* **Real-Time Risk Scoring Gauge**: Interactive Plotly radial gauge visualising predicted anomaly risk percentages dynamically on input.
* **Dynamic Active Claims Queue**: Real-time batch triage table managed via Streamlit session state that appends newly evaluated policyholders with dynamic claim IDs and routing actions.
* **Custom Policyholder Inputs**: Real-time evaluation allowing custom policyholder names, claim amounts in ZAR, customer tenure, claim history, and police report verification status.
* **Interactive Scenario Presets**: Sidebar controls for instant loading of pre-configured **High Risk / Suspicious** and **Low Risk / Fast-Track** test scenarios.
* **Key Risk Drivers & Insights**: Dynamic metric cards computing Claim-to-Tenure ratio (`ZAR/month`), Police Verification status, and Historical Claim Density.
* **Theme-Adaptive Glassmorphism UI**: High-contrast, executive-grade interface compatible with dark and light Streamlit themes.

---

## 📸 Interface Preview

![Dashboard Overview]<img width="1881" height="957" alt="dashboard_overview (2)" src="https://github.com/user-attachments/assets/de38ed39-af1c-486e-a278-bda726d68358" />
*Real-time risk analytics gauge, claim input parameters, and risk breakdown metrics.*

![Active Claims Queue]<img width="1892" height="915" alt="claims_queue" src="https://github.com/user-attachments/assets/887a16d6-eaa2-487a-b4e6-d9fc0100292b" />
*Dynamic live claims queue tracking evaluated policyholders and automated triage actions.*


---

## 🛠️ Tech Stack & Dependencies

* **Language**: Python 3.10+
* **Frontend Framework**: Streamlit
* **Machine Learning**: Scikit-Learn (`RandomForestClassifier`), NumPy, Pandas
* **Data Visualization**: Plotly (`graph_objects`)

---

## ⚡ Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Insurance_Fraud_AI.git
cd Insurance_Fraud_AI
```

### 2. Install Dependencies
```bash
pip install streamlit numpy pandas scikit-learn plotly
```

### 3. Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` to view the running dashboard.
Live link: https://insurance-claims-fraud-detection-engine.onrender.com

---

## 📊 Machine Learning Model Architecture

The predictive engine uses an ensemble **RandomForestClassifier** (120 estimators) trained on synthetic general insurance policy data:

| Feature Variable | Data Type | Operational Description |
| :--- | :--- | :--- |
| **Claim Amount (ZAR)** | Numeric (Continuous) | Financial value requested for reimbursement (R1,000 – R1,000,000) |
| **Customer Tenure** | Numeric (Integer) | Policyholder account duration in months |
| **Previous Claims History** | Numeric (Integer) | Count of historical claims previously submitted |
| **Police Report Status** | Binary (`Yes` / `No`) | Official police verification flag |

---

## 📑 Project Documentation

Full technical architecture documentation, system specifications, and compliance guidelines are available in the project repository:
* 📄 [`claims_triage_documentation.docx`][Automated_Claims_Triage_._Fraud_Detection.pdf](https://github.com/user-attachments/files/33770014/Automated_Claims_Triage_._Fraud_Detection.pdf)

---

## 🔐 Enterprise Compliance & Best Practices

* **Human-in-the-Loop Triage**: High-risk anomaly flags serve as decision-support indicators for SIU forensic investigators rather than automated claim rejections.
* **Model Explainability**: Calculated key driver metrics expose risk factors (e.g., high claim-to-tenure ratio) to support auditability.
