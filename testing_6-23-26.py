import streamlit as st

# ---------------- CONSTANTS ----------------
MAX_USERS_IN_SCOPE = 50

SCORE_THRESHOLDS = {
    "fast_track": 80,
    "standard": 40,
}

STEPS = ["welcome", "screening", "form", "results"]
STEP_LABELS = {
    "welcome": "Welcome",
    "screening": "Screening",
    "form": "Intake Form",
    "results": "Results",
}

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Use Case Intake",
    page_icon="⚙️",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
state_defaults = {
    "page": "welcome",          # one of STEPS
    "screening_passed": False,  # True -> goes to full intake form
    "screening_outcome": None,  # "out_of_scope" | "low_complexity" | "needs_intake" | None
    "screening_reasons": [],
    "complexity_flags": 0,
    "submitted": False,
    "score": None,
    "score_breakdown": {}
}

for k, v in state_defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- UI STYLES ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
.big-title {
    font-size: 42px;
    font-weight: 700;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f8f9fa;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR PROGRESS ----------------
with st.sidebar:
    st.title("⚙️ Intake Progress")

    current_step = st.session_state.page
    current_index = STEPS.index(current_step) if current_step in STEPS else 0

    for i, step in enumerate(STEPS):
        label = STEP_LABELS[step]
        if i < current_index:
            st.write(f"✅ {label}")
        elif i == current_index:
            st.markdown(f"**👉 {label}**")
        else:
            st.write(f"▫️ {label}")

    st.divider()
    if st.button("🔄 Restart"):
        for k, v in state_defaults.items():
            st.session_state[k] = v
        st.rerun()

# ---------------- PAGE 1 ----------------
def welcome():
    st.markdown('<div class="big-title">⚙️ Use Case Intake Portal</div>', unsafe_allow_html=True)

    st.markdown("""
    Welcome! This guided intake helps:
    - Evaluate your idea  
    - Score business value  
    - Route to correct team  
    - Fast-track high-impact solutions  
    """)

    st.success("Takes ~5 minutes")

    if st.button("🚀 Start"):
        st.session_state.page = "screening"
        st.rerun()

# ---------------- SCREENING ----------------
def screening_section():
    st.subheader("🔎 Step 1: Smart Screening & Complexity Check")

    st.markdown("Answer a few questions to determine if your use case is in scope and how it should be routed.")

    # ---------------- HARD STOPS ----------------
    st.markdown("### 🔴 Critical Checks")

    col1, col2 = st.columns(2)

    with col1:
        constant_support = st.checkbox("Requires **24/7 or real-time support**")
        critical_app = st.checkbox("Customer-facing or **highly critical application**")
        replaces_system = st.checkbox("Replaces a **core system (e.g., SAP)**")

    with col2:
        users = st.number_input("Number of users", min_value=1, value=10)
        multi_team = st.checkbox("Impacts **2 or more teams**")

    st.markdown("### 📋 Additional Critical Evaluation")

    impact_critical = st.selectbox(
        "Business impact if unavailable 4+ hours",
        ["Minimal", "Moderate disruption", "Revenue loss / customer impact / compliance breach"]
    )

    systems_touched = st.text_area(
        "Applications/systems involved (e.g., SAP, IBMS, SharePoint)"
    )

    data_combination = st.selectbox(
        "Data complexity",
        ["Single source & clean", "Multiple sources / some transformation", "Multiple sources / messy"]
    )

    rules_documentation = st.selectbox(
    "Business rules clarity",
    ["Well documented, few exceptions", "Some gaps/exceptions", "Poorly documented with many exceptions"])


    # ---------------- COMPLEXITY FLAGS ----------------
    st.markdown("### 🟡 Complexity Indicators")

    col3, col4 = st.columns(2)

    with col3:
        external_data = st.checkbox("Shares data with **external parties**")
        core_systems = st.checkbox("Connects to **core business systems** (SAP, etc.)")
        multi_systems = st.checkbox("Touches **multiple systems/apps**")

    with col4:
        data_complexity = st.selectbox(
            "Data quality",
            ["Clean & standardized", "Some transformation needed", "Messy / multiple sources"]
        )

        rules_complexity = st.selectbox(
            "Business rules",
            ["Simple / well documented", "Some exceptions", "Complex / undocumented"]
        )

    # ---------------- SUBMIT ----------------
    if st.button("Evaluate Screening"):

        # HARD STOP LOGIC
        out = False
        reasons = []

        if constant_support:
            out = True
            reasons.append("Requires 24/7 support")

        if users > MAX_USERS_IN_SCOPE:
            out = True
            reasons.append(f"More than {MAX_USERS_IN_SCOPE} users")

        if critical_app:
            out = True
            reasons.append("Critical/customer-facing system")

        if replaces_system:
            out = True
            reasons.append("Replacing core enterprise system")

        if out:
            st.session_state.screening_outcome = "out_of_scope"
            st.session_state.screening_reasons = reasons
            st.session_state.screening_passed = False
            st.session_state.page = "results"
            st.rerun()

        # NEW HARD STOPS

        if impact_critical == "Revenue loss / customer impact / compliance breach":
            out = True
            reasons.append("High business impact if unavailable")

        if data_combination == "Multiple sources / messy":
            out = True
            reasons.append("High data complexity (multiple messy sources)")

        if rules_documentation == "Poorly documented with many exceptions":
            out = True
            reasons.append("Unclear and complex business rules")

        # Optional (more strict): systems complexity trigger
        if systems_touched and len(systems_touched.split(",")) >= 3:
            out = True
            reasons.append("Touches multiple complex systems")
        if out:
            st.session_state.screening_outcome = "out_of_scope"
            st.session_state.screening_reasons = reasons
            st.session_state.screening_passed = False
            st.session_state.page = "results"
            st.rerun()

        # ---------------- COMPLEXITY SCORING ----------------
        complexity_flags = 0

        if multi_team:
            complexity_flags += 1
        if external_data:
            complexity_flags += 1
        if core_systems:
            complexity_flags += 1
        if multi_systems:
            complexity_flags += 1
        if data_complexity != "Clean & standardized":
            complexity_flags += 1
        if rules_complexity != "Simple / well documented":
            complexity_flags += 1

        # ---------------- ROUTING ----------------
        if complexity_flags == 0:
            st.session_state.screening_outcome = "low_complexity"
            st.session_state.screening_passed = False
            st.session_state.page = "results"
            st.rerun()

        else:
            st.session_state.screening_outcome = "needs_intake"
            st.session_state.complexity_flags = complexity_flags
            st.session_state.screening_passed = True
            st.session_state.page = "form"
            st.rerun()

# ---------------- FORM ----------------
def intake_form():
    st.subheader("🧠 Experience & Use Case")

    with st.form("intake"):

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 👤 Experience")

            q1 = st.selectbox("Background", [
                "Business User",
                "Analytical",
                "Developer"
            ])

            q2 = st.selectbox("Platform Experience", [
                "None",
                "Basic",
                "Advanced"
            ])

            q5 = st.selectbox("Learning Style", [
                "Self-learner",
                "Ask others",
                "Wait training"
            ])

            q6 = st.radio("Self-taught before?", ["Yes", "No"])

        with col2:
            st.markdown("### ⚙️ Skills")

            q3 = st.multiselect("Power Platform Skills", [
                "Basic flow",
                "Canvas app",
                "Premium connectors",
                "Complex expressions",
                "Custom connector",
                "API / Gateway",
                "ALM"
            ])

            q4 = st.multiselect("Technical Skills", [
                "Coding",
                "SQL",
                "APIs"
            ])

        st.divider()

        # -------------------------------------------------
        # 💼 EXPANDED BUSINESS VALUE (PROD VERSION)
        # -------------------------------------------------

        st.markdown("## 💼 Business Value & Impact")

        # ---------- TIME SAVINGS ----------
        with st.expander("⏱️ Time & Labor Savings", expanded=True):

            time = st.select_slider(
                "1. Manual hours spent per week",
                ["0-2", "2-5", "5-10", "10-20", "20+"]
            )

            role = st.selectbox(
                "2. Primary role performing this task",
                ["Frontline", "Analyst", "Manager", "Executive", "Multiple roles"]
            )

        # ---------- COST SAVINGS ----------
        with st.expander("💰 Hard Cost Savings"):

            cost = st.radio(
                "1. Does this eliminate external costs?",
                ["No", "Yes"],
                horizontal=True
            )

            cost_value = st.select_slider(
                "2. Estimated annual savings",
                ["< $2k", "$2k - $10k", "> $10k"],
                disabled=(cost == "No")
            )

        # ---------- RISK ----------
        with st.expander("⚠️ Risk Reduction & Compliance"):

            risk = st.radio(
                "1. Does this address compliance / audit / high error risk?",
                ["No", "Yes"],
                horizontal=True
            )

            risk_desc = st.text_area(
                "2. Describe the risk being mitigated",
                placeholder="e.g., Removes manual entry errors causing compliance issues",
                disabled=(risk == "No")
            )

        # ---------- EXPERIENCE ----------
        with st.expander("🚀 Employee / Customer Experience"):

            sla = st.radio(
                "1. Improves SLA or turnaround time?",
                ["No", "Yes"],
                horizontal=True
            )

            sla_detail = st.text_area(
                "2. Current vs future turnaround time",
                placeholder="e.g., 3 days → 2 hours",
                disabled=(sla == "No")
            )

        # ---------- REVENUE ----------
        with st.expander("📈 Revenue Impact"):

            revenue = st.radio(
                "1. Impacts revenue / billing / churn?",
                ["No", "Yes"],
                horizontal=True
            )

            revenue_detail = st.text_area(
                "2. Estimated financial or volume impact",
                placeholder="Describe impact",
                disabled=(revenue == "No")
            )

        st.markdown("### 🔧 Technical Needs")

        premium = st.checkbox("Premium connectors needed?")
        premium_list = []
        premium_other = ""

        if premium:
            premium_list = st.multiselect(
                "Select premium connectors",
                [
                    "SQL Server",
                    "Dataverse",
                    "Salesforce",
                    "ServiceNow",
                    "Azure DevOps",
                    "SAP",
                    "Oracle",
                    "IBM DB2",
                    "Other"
                ]
            )

            if "Other" in premium_list:
                premium_other = st.text_input("Specify other premium connector(s)")


        custom = st.checkbox("Custom connectors / API needed?")
        custom_list = []
        custom_other = ""

        if custom:
            custom_list = st.multiselect(
                "Select custom/API types",
                [
                    "Internal API",
                    "External Vendor API",
                    "Azure Function",
                    "On-prem gateway",
                    "Other"
                ]
            )

            if "Other" in custom_list:
                custom_other = st.text_input("Specify other custom/API details")
            st.markdown("### 🔐 Licensing")

            premium_license = st.radio(
                "Do you need a Power Platform Premium license?",
                ["No", "Yes"]
            )

            premium_license_users = st.number_input(
                "How many users will need a premium license?",
                min_value=0,
                step=1
            )


        submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.submitted = True

        # -------- SCORING --------
        score = 0

        q1_map = {"Business User": 0, "Analytical": 2, "Developer": 4}
        q2_map = {"None": 0, "Basic": 2, "Advanced": 4}

        score_dev = q1_map[q1] + q2_map[q2]

        score_dev += 2 if q5 == "Self-learner" else 0
        score_dev += 2 if q6 == "Yes" else 0

        score_dev += len(q3) * 2
        score_dev += len(q4) * 2

        # bracket
        if score_dev >= 20:
            dev_pts = 20
        elif score_dev >= 10:
            dev_pts = 10
        else:
            dev_pts = 0

        # ---------------- BUSINESS VALUE SCORING ----------------

        is_high_impact = (
            time in ["10-20", "20+"] or
            (cost == "Yes" and cost_value == "> $10k") or
            risk == "Yes" or
            revenue == "Yes"
        )

        is_medium_impact = (
            time == "5-10" or
            (cost == "Yes" and cost_value == "$2k - $10k") or
            sla == "Yes"
        )

        if is_high_impact:
            value_pts = 40
        elif is_medium_impact:
            value_pts = 20
        else:
            value_pts = 0

        # technical simplicity
        if custom:
            tech_pts = 0
        elif premium:
            tech_pts = 20
        else:
            tech_pts = 40

        total = dev_pts + value_pts + tech_pts
        st.session_state.score = total
        st.session_state.score_breakdown = {
            "Experience": (dev_pts, 20),
            "Business Value": (value_pts, 40),
            "Technical Simplicity": (tech_pts, 40),
        }
        st.session_state.page = "results"
        st.rerun()

# ---------------- RESULTS ----------------
def results():
    st.title("📊 Results")

    outcome = st.session_state.screening_outcome

    if outcome == "out_of_scope":
        st.error("⛔ OUT OF SCOPE → Route to IT")
        for r in st.session_state.screening_reasons:
            st.write(f"- {r}")
        return

    if outcome == "low_complexity":
        st.success("✅ LOW COMPLEXITY")
        st.info("👉 You can proceed directly in your BU environment. No further intake needed.")
        return

    score = st.session_state.score
    if score is None:
        st.warning("No score available yet — please complete the intake form first.")
        return

    st.metric("Final Score", score)

    breakdown = st.session_state.score_breakdown
    if breakdown:
        cols = st.columns(len(breakdown))
        for col, (label, (pts, max_pts)) in zip(cols, breakdown.items()):
            col.metric(label, f"{pts}/{max_pts}")

    if score >= SCORE_THRESHOLDS["fast_track"]:
        st.success("🚀 FAST TRACK\n15-min review + start build")
    elif score >= SCORE_THRESHOLDS["standard"]:
        st.warning("🧾 Standard Review\nAdded to backlog")
    else:
        st.error("📚 Training Required")

# ---------------- ROUTER ----------------
if st.session_state.page == "welcome":
    welcome()

elif st.session_state.page == "screening":
    screening_section()

elif st.session_state.page == "form":
    intake_form()

elif st.session_state.page == "results":
    results()