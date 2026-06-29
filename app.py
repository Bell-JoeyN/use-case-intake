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
    "submitted": False,
    "score": None,
    "route": None,
    "screening_outcome": None,
    "screening_reasons": [],
    "developer_raw": 0,
    "developer_pts": 0,
    "business_raw": 0,
    "business_pts": 0,
    "technical_raw": 0,
    "technical_pts": 0
}

for k, v in state_defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- UI STYLES ----------------
st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR PROGRESS ----------------
with st.sidebar:
    st.title("⚙️ Intake Progress")
    st.write("Step 1: Welcome")
    st.write("Step 2: Scope Check")
    st.write("Step 3: Intake Form")
    st.write("Step 4: Results")

    st.divider()

    if st.button("🔁 Restart Intake"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ---------------- PAGE 1 ----------------
def welcome():
    st.markdown('<div class="big-title">⚙️ Use Case Intake Portal</div>', unsafe_allow_html=True)

    st.markdown(
        """
        Welcome! This guided intake helps:
        - Check whether your use case is in scope
        - Score developer readiness
        - Score business value
        - Score technical simplicity
        - Route the request to the right path
        """
    )

    st.success("Takes ~5 minutes")

    if st.button("🚀 Start"):
        st.session_state.page = "screening"
        st.rerun()

# ---------------- SCREENING / OUT OF SCOPE ----------------
def screening_section():
    st.subheader("🔎 Section 1: Use Case Scope Check")
    st.markdown(
        "Select any statement that applies. If any out-of-scope item is selected, the request should be routed to IT."
    )

    st.markdown("### Screening Questions")

    a_constant_support = st.checkbox(
        "A. My solution requires real-time / hourly monitoring to function (constant support)."
    )
    b_many_users = st.checkbox(
        "B. My solution may reach more than 100 users through its lifetime."
    )
    c_external_facing = st.checkbox(
        "C. My solution will be external facing (for example: customer or vendor)."
    )
    d_replace_critical = st.checkbox(
        "D. My solution will replace an existing critical system / application."
    )
    e_many_non_ms_apps = st.checkbox(
        "E. My solution will touch / connect to more than 3 applications outside of Microsoft."
    )

    external_apps = st.text_area(
        "If E is selected, list the non-Microsoft applications/systems involved:",
        placeholder="Example: SAP, Salesforce, Jira, ServiceNow"
    )

    st.caption(
        "Critical system = any system where failure, downtime, or data corruption directly halts operations."
    )

    if st.button("Evaluate Scope"):
        reasons = []

        if a_constant_support:
            reasons.append("Requires real-time / hourly monitoring or constant support")
        if b_many_users:
            reasons.append("May reach more than 100 users")
        if c_external_facing:
            reasons.append("External-facing use case")
        if d_replace_critical:
            reasons.append("Replaces an existing critical system / application")
        if e_many_non_ms_apps:
            if external_apps.strip():
                reasons.append(
                    f"Connects to more than 3 non-Microsoft applications/systems: {external_apps.strip()}"
                )
            else:
                reasons.append("Connects to more than 3 non-Microsoft applications/systems")

        if reasons:
            st.session_state.screening_outcome = "out_of_scope"
            st.session_state.screening_reasons = reasons
            st.session_state.page = "results"
            st.rerun()
        else:
            st.session_state.screening_outcome = "in_scope"
            st.session_state.screening_reasons = []
            st.session_state.page = "form"
            st.rerun()

# ---------------- FORM ----------------
def intake_form():
    st.subheader("🧠 Section 2: Intake Form")

    with st.form("intake_form"):
        # ---------- USE CASE DETAILS ----------
        st.markdown("## 📝 Use Case Details")

        use_case_desc = st.text_area(
            "Describe the use case",
            placeholder="What are you trying to build, what problem does it solve, and what is the desired outcome?"
        )

        current_state = st.text_area(
            "Current mode of operation",
            placeholder="How is the process done today?"
        )

        future_state = st.text_area(
            "Future mode of operation",
            placeholder="What should the future state look like?"
        )

        st.divider()

        # ---------- DEVELOPER EXPERIENCE ----------
        st.markdown("## 👤 Citizen Developer Experience Check")

        col1, col2 = st.columns(2)

        with col1:
            q1 = st.radio(
                "Q1. General Background - Which best describes your technical background?",
                [
                    "Business User (No coding experience)",
                    "Analytical (Comfortable with Excel macros, SQL, programming basics, etc.)",
                    "Professional Developer / IT Engineering (Experienced)"
                ]
            )

            q2 = st.radio(
                "Q2. Platform Experience - Have you developed a solution in Power Platform before?",
                [
                    "No, this is my first time",
                    "Yes, simple solutions (e.g., basic flows, templates)",
                    "Yes, advanced solutions (e.g., custom connectors, complex expressions)"
                ]
            )

            q5 = st.radio(
                "Q5. How do you typically approach learning something new when there's no one immediately available to walk you through it?",
                [
                    "I actively search documentation, tutorials, or online communities and try it myself",
                    "I find a colleague who already knows it and learn from them",
                    "I wait until formal training or scheduled support becomes available",
                    "I'd rather hand it off to someone else to complete"
                ]
            )

            q6 = st.radio(
                "Q6. Have you ever taught yourself a new tool, app, or skill outside of required training — just by exploring on your own?",
                ["Yes", "No"]
            )

        with col2:
            q3 = st.multiselect(
                "Q3. Which of the following have you done in Power Platform? (Select all that apply)",
                [
                    "Used a pre-built template without modifying it",
                    "Built a basic flow (e.g., trigger an action when an item is added or a form is submitted)",
                    "Built a canvas app with multiple screens",
                    "Used premium connectors (e.g., SQL Server, Dataverse, ServiceNow)",
                    "Written complex expressions or formulas (e.g., nested conditions)",
                    "Built or used a custom connector",
                    "Integrated with an on-premises data gateway or an external API",
                    "Managed solution deployment across environments (dev/test/prod) or used Application Lifecycle Management (ALM)"
                ]
            )

            q4 = st.multiselect(
                "Q4. Do you have any of the following professional technical skills? (Select all that apply)",
                [
                    "Write code in a programming language (Python, C#, Java, JavaScript, etc.)",
                    "Write or optimize SQL queries",
                    "Build or maintain APIs",
                    "None of the above"
                ]
            )

        st.divider()

        # ---------- BUSINESS VALUE ----------
        st.markdown("## 💼 Business Value Check")

        bv_hours = st.number_input(
            "Q1. My solution will reduce manual effort by how many hours per week?",
            min_value=0,
            value=0,
            step=1
        )

        bv_cost = st.radio(
            "Q2. My solution will eliminate or reduce direct costs (e.g., vendor tools, licensing, printing, mailing)",
            [
                "No",
                "Yes (less than $10K annually)",
                "Yes (more than $10K annually)"
            ]
        )

        bv_revenue = st.radio(
            "Q3. This solution is expected to generate revenue (e.g., increased sales, faster billing)",
            [
                "No anticipated revenue impact",
                "Yes – minor or unquantified revenue impact",
                "Yes – moderate, quantifiable revenue impact",
                "Yes – significant, measurable revenue impact"
            ]
        )

        st.divider()

        # ---------- TECHNICAL COMPLEXITY / SIMPLICITY ----------
        st.markdown("## 🔧 Technical Complexity Score Questions")
        st.caption("For the Technical axis, scoring is based on simplicity — the easier the solution is, the higher the points.")

        tech_integrations = st.multiselect(
            "Q1. My solution will require integrating with systems, APIs, or connectors (select all that apply)",
            [
                "Built-in Microsoft connectors (e.g., SharePoint, Outlook, Excel, Teams, Word, PowerPoint, Power BI)",
                "Microsoft premium connectors (e.g., Dataverse, SQL, ServiceNow, Salesforce connector)",
                "External systems or APIs (e.g., SAP, Salesforce, Jira, or other systems outside Microsoft)",
                "Building or using a custom connector (to connect to an existing API not already available)",
                "A new custom API must be built to enable integration",
                "None"
            ]
        )

        tech_data = st.radio(
            "Q2. My solution will use the following type of data",
            [
                "Highly Sensitive PII (SIN, banking, passport, biometrics)",
                "Regular PII (names, DOB, home address, email)",
                "Corporate Financials / Public Data / Internal Data / similar"
            ]
        )

        tech_automation = st.radio(
            "Q3. My solution will include the following level of automation and components",
            [
                "Simple - uses a single component (e.g., one flow OR one app)",
                "Moderate - may involve multiple components (e.g., app + flow, or multiple flows)",
                "Complex - uses multiple tools or advanced architecture (e.g., Power Apps + Power Automate + AI + Dataverse)"
            ]
        )

        tech_access = st.radio(
            "Q4. My solution will be accessed by",
            [
                "Internal users only (within Bell M365 – bell.ca email accounts)",
                "External users (outside Bell M365 tenant – vendors, partners, or non-bell.ca emails)"
            ]
        )

        submitted = st.form_submit_button("Submit")

    if submitted:
        # ---------------- DEVELOPER RAW SCORE ----------------
        q1_map = {
            "Business User (No coding experience)": 0,
            "Analytical (Comfortable with Excel macros, SQL, programming basics, etc.)": 2,
            "Professional Developer / IT Engineering (Experienced)": 4
        }

        q2_map = {
            "No, this is my first time": 0,
            "Yes, simple solutions (e.g., basic flows, templates)": 2,
            "Yes, advanced solutions (e.g., custom connectors, complex expressions)": 4
        }

        q3_points = {
            "Used a pre-built template without modifying it": 0,
            "Built a basic flow (e.g., trigger an action when an item is added or a form is submitted)": 2,
            "Built a canvas app with multiple screens": 2,
            "Used premium connectors (e.g., SQL Server, Dataverse, ServiceNow)": 2,
            "Written complex expressions or formulas (e.g., nested conditions)": 2,
            "Built or used a custom connector": 4,
            "Integrated with an on-premises data gateway or an external API": 4,
            "Managed solution deployment across environments (dev/test/prod) or used Application Lifecycle Management (ALM)": 4
        }

        q4_points = {
            "Write code in a programming language (Python, C#, Java, JavaScript, etc.)": 2,
            "Write or optimize SQL queries": 2,
            "Build or maintain APIs": 2,
            "None of the above": 0
        }

        q5_map = {
            "I actively search documentation, tutorials, or online communities and try it myself": 2,
            "I find a colleague who already knows it and learn from them": 0,
            "I wait until formal training or scheduled support becomes available": 0,
            "I'd rather hand it off to someone else to complete": 0
        }

        q6_map = {
            "Yes": 2,
            "No": 0
        }

        developer_raw = q1_map[q1] + q2_map[q2] + q5_map[q5] + q6_map[q6]
        developer_raw += sum(q3_points[item] for item in q3)

        q4_clean = [item for item in q4 if item != "None of the above"]
        developer_raw += sum(q4_points[item] for item in q4_clean)

        if developer_raw >= 20:
            developer_pts = 20
        elif developer_raw >= 10:
            developer_pts = 10
        else:
            developer_pts = 0

        # ---------------- BUSINESS VALUE RAW SCORE ----------------
        if bv_hours < 5:
            hours_pts = 0
        elif 5 <= bv_hours <= 15:
            hours_pts = 5
        else:
            hours_pts = 10

        cost_map = {
            "No": 0,
            "Yes (less than $10K annually)": 5,
            "Yes (more than $10K annually)": 10
        }

        revenue_map = {
            "No anticipated revenue impact": 0,
            "Yes – minor or unquantified revenue impact": 5,
            "Yes – moderate, quantifiable revenue impact": 8,
            "Yes – significant, measurable revenue impact": 10
        }

        business_raw = hours_pts + cost_map[bv_cost] + revenue_map[bv_revenue]

        if business_raw >= 20:
            business_pts = 40
        elif business_raw >= 10:
            business_pts = 20
        else:
            business_pts = 0

        # ---------------- TECHNICAL RAW SCORE ----------------
        integration_points = {
            "Built-in Microsoft connectors (e.g., SharePoint, Outlook, Excel, Teams, Word, PowerPoint, Power BI)": 8,
            "Microsoft premium connectors (e.g., Dataverse, SQL, ServiceNow, Salesforce connector)": 4,
            "External systems or APIs (e.g., SAP, Salesforce, Jira, or other systems outside Microsoft)": 0,
            "Building or using a custom connector (to connect to an existing API not already available)": 3,
            "A new custom API must be built to enable integration": 0,
            "None": 0
        }

        if "None" in tech_integrations and len(tech_integrations) > 1:
            tech_integrations = [item for item in tech_integrations if item != "None"]

        integrations_raw = sum(integration_points[item] for item in tech_integrations)

        data_map = {
            "Highly Sensitive PII (SIN, banking, passport, biometrics)": 0,
            "Regular PII (names, DOB, home address, email)": 3,
            "Corporate Financials / Public Data / Internal Data / similar": 6
        }

        automation_map = {
            "Simple - uses a single component (e.g., one flow OR one app)": 24,
            "Moderate - may involve multiple components (e.g., app + flow, or multiple flows)": 16,
            "Complex - uses multiple tools or advanced architecture (e.g., Power Apps + Power Automate + AI + Dataverse)": 0
        }

        access_map = {
            "Internal users only (within Bell M365 – bell.ca email accounts)": 2,
            "External users (outside Bell M365 tenant – vendors, partners, or non-bell.ca emails)": 0
        }

        technical_raw = (
            integrations_raw
            + data_map[tech_data]
            + automation_map[tech_automation]
            + access_map[tech_access]
        )

        # ---------------- TECHNICAL STANDARDIZED SCORE ----------------
        uses_external_or_new_api = (
            "External systems or APIs (e.g., SAP, Salesforce, Jira, or other systems outside Microsoft)" in tech_integrations
            or "A new custom API must be built to enable integration" in tech_integrations
            or tech_automation == "Complex - uses multiple tools or advanced architecture (e.g., Power Apps + Power Automate + AI + Dataverse)"
            or tech_access == "External users (outside Bell M365 tenant – vendors, partners, or non-bell.ca emails)"
            or "Building or using a custom connector (to connect to an existing API not already available)" in tech_integrations
        )

        uses_premium_or_moderate = (
            "Microsoft premium connectors (e.g., Dataverse, SQL, ServiceNow, Salesforce connector)" in tech_integrations
            or tech_automation == "Moderate - may involve multiple components (e.g., app + flow, or multiple flows)"
        )

        built_in_only_simple = (
            (
                "Built-in Microsoft connectors (e.g., SharePoint, Outlook, Excel, Teams, Word, PowerPoint, Power BI)" in tech_integrations
                or len(tech_integrations) == 0
                or tech_integrations == ["None"]
            )
            and not uses_external_or_new_api
            and not uses_premium_or_moderate
            and tech_automation == "Simple - uses a single component (e.g., one flow OR one app)"
            and tech_access == "Internal users only (within Bell M365 – bell.ca email accounts)"
        )

        if uses_external_or_new_api:
            technical_pts = 0
        elif uses_premium_or_moderate:
            technical_pts = 20
        elif built_in_only_simple:
            technical_pts = 40
        else:
            if technical_raw >= 30:
                technical_pts = 40
            elif technical_raw >= 15:
                technical_pts = 20
            else:
                technical_pts = 0

        # ---------------- TOTAL SCORE & ROUTE ----------------
        total_score = developer_pts + business_pts + technical_pts

        if total_score >= 80:
            route = "fast_track"
        elif total_score >= 40:
            route = "standard_review"
        else:
            route = "low_priority"

        st.session_state.submitted = True
        st.session_state.developer_raw = developer_raw
        st.session_state.developer_pts = developer_pts
        st.session_state.business_raw = business_raw
        st.session_state.business_pts = business_pts
        st.session_state.technical_raw = technical_raw
        st.session_state.technical_pts = technical_pts
        st.session_state.score = total_score
        st.session_state.route = route
        st.session_state.page = "results"
        st.rerun()

# ---------------- RESULTS ----------------
def results():
    if st.session_state.get("screening_outcome") == "out_of_scope":
        st.title("⛔ Out of Scope")
        st.error("This request should be routed to IT.")
        st.markdown("### Why this is out of scope")
        for reason in st.session_state.get("screening_reasons", []):
            st.write(f"- {reason}")
        return

    st.title("📊 Results")
    st.metric("Final Score", st.session_state.score)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Developer Expertise", st.session_state.developer_pts, help=f"Raw score: {st.session_state.developer_raw}/30")
    with col2:
        st.metric("Business Value", st.session_state.business_pts, help=f"Raw score: {st.session_state.business_raw}/30")
    with col3:
        st.metric("Technical Simplicity", st.session_state.technical_pts, help=f"Raw score: {st.session_state.technical_raw}")

    st.divider()

    if st.session_state.route == "fast_track":
        st.success("🚀 FAST-TRACK APPROVED")
        st.markdown(
            """
            **Action / Queue**
            - Auto-Approve / 15-minute quick call
            - User gets an automated email to start building
            """
        )
    elif st.session_state.route == "standard_review":
        st.warning("🧾 STANDARD CoE REVIEW")
        st.markdown(
            """
            **Action / Queue**
            - Goes to backlog
            - Needs a standard 30-minute CoE technical review before approval
            """
        )
    else:
        st.error("📚 LOW PRIORITY")
        st.markdown(
            """
            **Action / Queue**
            - Auto-reply with low priority
            - Provide details for office hours and contact information
            """
        )

    st.divider()
    st.markdown("### Score Breakdown Logic")
    st.markdown(
        f"""
        - **Developer Expertise:** {st.session_state.developer_raw}/30 raw → **{st.session_state.developer_pts}** standardized points
        - **Business Value:** {st.session_state.business_raw}/30 raw → **{st.session_state.business_pts}** standardized points
        - **Technical Simplicity:** {st.session_state.technical_raw} raw → **{st.session_state.technical_pts}** standardized points
        - **Total Score:** **{st.session_state.score}/100**
        """
    )

# ---------------- ROUTER ----------------
if st.session_state.page == "welcome":
    welcome()
elif st.session_state.page == "screening":
    screening_section()
elif st.session_state.page == "form":
    intake_form()
elif st.session_state.page == "results":
    results()