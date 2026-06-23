import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Use Case Intake",
    page_icon="⚙️",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
state_defaults = {
    "page": "welcome",
    "screening_passed": False,
    "submitted": False,
    "score": None
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

    st.write("Step 1: Welcome")
    st.write("Step 2: Screening")
    st.write("Step 3: Intake Form")
    st.write("Step 4: Results")

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
        st.session_state.page = "form"
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

    # ---------------- AI CONTEXT ----------------
    st.markdown("### 🧠 Impact & Context")

    impact = st.selectbox(
        "Impact if solution is down for 4+ hours",
        ["Minimal", "Moderate disruption", "Revenue / compliance impact"]
    )

    systems_list = st.text_area("List systems involved (SAP, SharePoint, etc.)")

    # ---------------- SUBMIT ----------------
    if st.button("Evaluate Screening"):

        # HARD STOP LOGIC
        out = False
        reasons = []

        if constant_support:
            out = True
            reasons.append("Requires 24/7 support")

        if users > 50:
            out = True
            reasons.append("More than 50 users")

        if critical_app:
            out = True
            reasons.append("Critical/customer-facing system")

        if replaces_system:
            out = True
            reasons.append("Replacing core enterprise system")

        if out:
            st.error("⛔ OUT OF SCOPE → Route to IT")
            for r in reasons:
                st.write(f"- {r}")

            st.session_state.screening_passed = False
            return

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
        if impact == "Revenue / compliance impact":
            complexity_flags += 1

        # ---------------- ROUTING ----------------
        if complexity_flags == 0:
            st.success("✅ LOW COMPLEXITY")
            st.info("👉 You can proceed directly in your BU environment.")
            st.session_state.screening_passed = False  # skip full intake if desired

        else:
            st.success("✅ PROCEED TO INTAKE FORM")
            st.warning(f"⚙️ Complexity Flags Detected: {complexity_flags}")
            st.session_state.screening_passed = True

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
        # ---------- LICENSING ----------
        with st.expander("💳 Licensing", expanded=False):

            lic_required = st.radio(
                "Does this require premium licensing?",
                ["Not sure", "No", "Yes"],
                horizontal=True
            )

            lic_users = st.number_input(
                "Number of users needing licenses",
                min_value=1,
                value=1
            )

        st.markdown("### 🔧 Technical Needs")

        premium = st.checkbox("Premium connectors needed?")
        custom = st.checkbox("Custom connectors/API needed?")

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

# ---------------- RESULTS ----------------
def results():
    score = st.session_state.score

    st.title("📊 Results")
    st.metric("Final Score", score)

    # FAST TRACK (from PDF logic)
    if score >= 80:
        st.success("🚀 FAST TRACK\n15-min review + start build")
    elif score >= 40:
        st.warning("🧾 Standard Review\nAdded to backlog")
    else:
        st.error("📚 Training Required")

# ---------------- ROUTER ----------------
if st.session_state.page == "welcome":
    welcome()

elif st.session_state.page == "form":
    screening_section()

    if st.session_state.screening_passed:
        intake_form()

    if st.session_state.submitted:
        results()