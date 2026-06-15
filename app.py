import streamlit as st
import anthropic
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Healthcare AI Contact Center Intelligence Hub",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background-color: #0A0F1E; }
    .stApp { background-color: #0A0F1E; }

    .hero-banner {
        background: linear-gradient(135deg, #1B3A6B 0%, #0D7680 100%);
        padding: 32px 40px;
        border-radius: 16px;
        margin-bottom: 28px;
        border: 1px solid rgba(13,118,128,0.3);
    }
    .hero-banner h1 {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 700;
        margin: 0 0 8px 0;
    }
    .hero-banner p {
        color: rgba(255,255,255,0.75);
        font-size: 14px;
        margin: 0;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        color: #FFD700;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 12px;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }

    .metric-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        height: 100%;
    }
    .metric-card .value {
        font-size: 32px;
        font-weight: 700;
        margin: 8px 0 4px 0;
    }
    .metric-card .label {
        font-size: 12px;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card .delta {
        font-size: 12px;
        margin-top: 4px;
    }
    .metric-red { color: #EF4444; }
    .metric-amber { color: #F59E0B; }
    .metric-green { color: #10B981; }
    .metric-teal { color: #0D7680; }

    .section-header {
        font-size: 20px;
        font-weight: 700;
        color: #FFFFFF;
        margin: 24px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #0D7680;
    }

    .intent-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 12px;
    }
    .intent-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #6B7280;
        margin-bottom: 4px;
    }
    .intent-value {
        font-size: 15px;
        font-weight: 600;
        color: #FFFFFF;
    }

    .risk-pill {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .risk-low { background: #065F46; color: #6EE7B7; }
    .risk-medium { background: #78350F; color: #FDE68A; }
    .risk-high { background: #7F1D1D; color: #FCA5A5; }
    .risk-critical { background: #6B21A8; color: #E9D5FF; }

    .score-bar-container {
        background: #1F2937;
        border-radius: 8px;
        height: 8px;
        overflow: hidden;
        margin-top: 6px;
    }
    .score-bar-fill {
        height: 100%;
        border-radius: 8px;
        transition: width 0.5s ease;
    }

    .ai-response {
        background: linear-gradient(135deg, #0D1F3C, #0A2540);
        border: 1px solid #0D7680;
        border-radius: 12px;
        padding: 24px;
        margin-top: 16px;
    }
    .ai-response-header {
        font-size: 12px;
        font-weight: 600;
        color: #0D7680;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 12px;
    }

    .handoff-block {
        background: #111827;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 16px;
        margin-top: 12px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #9CA3AF;
        line-height: 1.8;
    }

    .disclaimer {
        background: #1F1010;
        border: 1px solid #7F1D1D;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 11px;
        color: #FCA5A5;
        margin-top: 24px;
    }

    .sidebar-logo {
        font-size: 18px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .sidebar-sub {
        font-size: 11px;
        color: #6B7280;
        margin-bottom: 20px;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stSlider"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stTextInput"] label {
        color: #D1D5DB !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    div[data-testid="stMarkdownContainer"] p {
        color: #D1D5DB;
    }

    .stTabs [data-baseweb="tab-list"] {
        background-color: #111827;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #6B7280;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 500;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1B3A6B !important;
        color: #FFFFFF !important;
    }

    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #0D7680, #1B3A6B);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        padding: 10px 24px;
        width: 100%;
    }
    div[data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, #0A9AA6, #1E3F7A);
        transform: translateY(-1px);
    }

    .kpi-table-header {
        background: #1B3A6B;
        color: white;
        font-weight: 600;
        font-size: 13px;
        padding: 10px 12px;
        border-radius: 6px 6px 0 0;
    }

    footer { display: none; }
    #MainMenu { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Synthetic KPI Data ────────────────────────────────────────
KPI_DATA = pd.DataFrame({
    "Week": ["Week 1\n(Jun 2–6)", "Week 2\n(Jun 9–13)", "Week 3\n(Jun 16–20)", "Week 4\n(Jun 23–27)"],
    "Week_Label": ["Week 1", "Week 2", "Week 3", "Week 4"],
    "Total_Calls": [1624, 1812, 1538, 1741],
    "ASA_Min": [4.2, 5.8, 3.9, 4.7],
    "AHT_Min": [8.6, 9.1, 8.2, 8.8],
    "Abandonment_Pct": [19.4, 23.7, 17.1, 21.3],
    "FCR_Pct": [61.2, 58.4, 64.7, 60.1],
    "Callback_Vol": [187, 241, 163, 209],
    "Escalation_Pct": [14.8, 17.2, 13.1, 15.6],
    "Repeat_Call_Pct": [31.5, 34.8, 28.9, 33.2],
    "Agent_Avail_Pct": [78.3, 71.6, 81.4, 76.8],
})

BENCHMARKS = {
    "ASA_Min": 2.0, "Abandonment_Pct": 10.0, "FCR_Pct": 77.0,
    "Escalation_Pct": 10.0, "Repeat_Call_Pct": 15.0, "Agent_Avail_Pct": 85.0
}

# ── Intent library for ARIA ───────────────────────────────────
INTENTS = {
    "Password Reset": {"risk": "LOW", "route": "Self-Service / Tier-1 IT", "emoji": "🔑"},
    "Application Access Issue": {"risk": "MEDIUM", "route": "IT Access Management Queue", "emoji": "💻"},
    "Device Issue": {"risk": "LOW", "route": "IT Hardware Support Queue", "emoji": "🖥️"},
    "Callback Request": {"risk": "LOW", "route": "Callback Queue", "emoji": "📞"},
    "Telecom Issue": {"risk": "LOW", "route": "Telecom Support Queue", "emoji": "📡"},
    "General IT Support": {"risk": "MEDIUM", "route": "Tier-1 General IT Queue", "emoji": "🛠️"},
    "Urgent Escalation": {"risk": "HIGH", "route": "Immediate Human Agent + Supervisor", "emoji": "🚨"},
    "EHR Access Issue": {"risk": "HIGH", "route": "Clinical Systems + IT Security", "emoji": "🏥"},
}

RISK_COLORS = {"LOW": "risk-low", "MEDIUM": "risk-medium", "HIGH": "risk-high", "CRITICAL": "risk-critical"}

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🏥 Healthcare AI Portfolio</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">James D. McClain, MBA</div>', unsafe_allow_html=True)
    st.divider()

    st.markdown("**Navigation**")
    page = st.radio(
        "Select Module",
        ["📊 KPI Dashboard", "🤖 ARIA Intent Simulator", "🎯 AI Readiness Scorer", "📈 Performance Analyzer"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("**API Configuration**")
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")

    if api_key:
        st.success("✅ API Key connected")
    else:
        st.warning("⚠️ API key not configured")

    st.divider()
    st.markdown("""
    <div style="font-size:11px;color:#4B5563;line-height:1.6">
    <strong style="color:#6B7280">Portfolio Demo</strong><br>
    Synthetic data only.<br>
    No PHI included.<br><br>
    <strong style="color:#6B7280">James D. McClain, MBA</strong><br>
    Healthcare IT Leader<br>
    AI Contact Center Modernization
    </div>
    """, unsafe_allow_html=True)

# ── Hero banner ───────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">⚕ Synthetic Portfolio Demo — No PHI Included</div>
    <h1>Healthcare AI Contact Center Intelligence Hub</h1>
    <p>AI-powered KPI analysis, virtual agent simulation, readiness scoring, and performance insights — built to demonstrate AI/CX Solutions Architect methodology.</p>
    <p style="font-size:12px;color:rgba(255,255,255,0.5);margin-top:8px">James D. McClain, MBA — Healthcare IT Leader | AI Contact Center Modernization | Responsible AI Governance</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 1 — KPI DASHBOARD
# ════════════════════════════════════════════════════════════════
if page == "📊 KPI Dashboard":
    st.markdown('<div class="section-header">📊 4-Week KPI Performance Dashboard</div>', unsafe_allow_html=True)

    # Summary metric cards
    avg_abandon = KPI_DATA["Abandonment_Pct"].mean()
    avg_asa = KPI_DATA["ASA_Min"].mean()
    avg_fcr = KPI_DATA["FCR_Pct"].mean()
    avg_repeat = KPI_DATA["Repeat_Call_Pct"].mean()
    avg_avail = KPI_DATA["Agent_Avail_Pct"].mean()
    total_calls = KPI_DATA["Total_Calls"].sum()

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    metrics = [
        (col1, f"{total_calls:,}", "Total Calls (4 Wks)", "metric-teal", "↑ 12% Week 2 surge"),
        (col2, f"{avg_asa:.1f} min", "Avg Speed to Answer", "metric-red", f"⚠ Benchmark: 2.0 min"),
        (col3, f"{avg_abandon:.1f}%", "Avg Abandonment Rate", "metric-red", f"⚠ Benchmark: ≤10%"),
        (col4, f"{avg_fcr:.1f}%", "Avg First Call Res.", "metric-amber", f"⚠ Benchmark: 75–80%"),
        (col5, f"{avg_repeat:.1f}%", "Avg Repeat Call Rate", "metric-red", f"⚠ Benchmark: ≤15%"),
        (col6, f"{avg_avail:.1f}%", "Avg Agent Availability", "metric-amber", f"⚠ Benchmark: ≥85%"),
    ]
    for col, value, label, color_class, delta in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">{label}</div>
                <div class="value {color_class}">{value}</div>
                <div class="delta" style="color:#6B7280">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row 1
    col_l, col_r = st.columns(2)

    with col_l:
        fig1 = go.Figure()
        colors = ["#1B3A6B", "#EF4444", "#10B981", "#F59E0B"]
        fig1.add_trace(go.Bar(
            x=KPI_DATA["Week_Label"], y=KPI_DATA["Total_Calls"],
            marker_color=colors, text=KPI_DATA["Total_Calls"],
            textposition="outside", textfont=dict(color="white", size=12)
        ))
        fig1.add_hline(y=1700, line_dash="dash", line_color="#0D7680",
                      annotation_text="Capacity Target", annotation_font_color="#0D7680")
        fig1.update_layout(
            title=dict(text="Weekly Call Volume", font=dict(color="white", size=14)),
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            font=dict(color="#9CA3AF"), height=300,
            xaxis=dict(gridcolor="#1F2937"), yaxis=dict(gridcolor="#1F2937"),
            showlegend=False, margin=dict(t=40, b=20, l=20, r=20)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_r:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=KPI_DATA["Week_Label"], y=KPI_DATA["Abandonment_Pct"],
            name="Abandonment %", line=dict(color="#EF4444", width=3),
            mode="lines+markers+text", text=KPI_DATA["Abandonment_Pct"].apply(lambda x: f"{x}%"),
            textposition="top center", textfont=dict(color="#EF4444")
        ))
        fig2.add_trace(go.Scatter(
            x=KPI_DATA["Week_Label"], y=KPI_DATA["FCR_Pct"],
            name="FCR %", line=dict(color="#10B981", width=3),
            mode="lines+markers+text", text=KPI_DATA["FCR_Pct"].apply(lambda x: f"{x}%"),
            textposition="bottom center", textfont=dict(color="#10B981")
        ))
        fig2.add_hline(y=10, line_dash="dash", line_color="#EF4444",
                      annotation_text="Abandon Target ≤10%", annotation_font_color="#EF4444")
        fig2.add_hline(y=77, line_dash="dash", line_color="#10B981",
                      annotation_text="FCR Target 77%", annotation_font_color="#10B981")
        fig2.update_layout(
            title=dict(text="Abandonment Rate vs. First Call Resolution", font=dict(color="white", size=14)),
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            font=dict(color="#9CA3AF"), height=300,
            xaxis=dict(gridcolor="#1F2937"), yaxis=dict(gridcolor="#1F2937"),
            legend=dict(bgcolor="#111827", font=dict(color="white")),
            margin=dict(t=40, b=20, l=20, r=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Charts row 2
    col_l2, col_r2 = st.columns(2)

    with col_l2:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=KPI_DATA["Week_Label"], y=KPI_DATA["Agent_Avail_Pct"],
            name="Agent Availability %", line=dict(color="#0D7680", width=3),
            mode="lines+markers", fill="tozeroy", fillcolor="rgba(13,118,128,0.1)"
        ))
        fig3.add_trace(go.Scatter(
            x=KPI_DATA["Week_Label"], y=KPI_DATA["Repeat_Call_Pct"],
            name="Repeat Call Rate %", line=dict(color="#F59E0B", width=3),
            mode="lines+markers"
        ))
        fig3.add_hline(y=85, line_dash="dash", line_color="#0D7680",
                      annotation_text="Avail Target 85%", annotation_font_color="#0D7680")
        fig3.update_layout(
            title=dict(text="Agent Availability vs. Repeat Call Rate", font=dict(color="white", size=14)),
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            font=dict(color="#9CA3AF"), height=300,
            xaxis=dict(gridcolor="#1F2937"), yaxis=dict(gridcolor="#1F2937"),
            legend=dict(bgcolor="#111827", font=dict(color="white")),
            margin=dict(t=40, b=20, l=20, r=20)
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_r2:
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=KPI_DATA["Week_Label"], y=KPI_DATA["Callback_Vol"],
            name="Callback Volume", marker_color="#1B3A6B",
            text=KPI_DATA["Callback_Vol"], textposition="outside",
            textfont=dict(color="white")
        ))
        fig4.add_trace(go.Scatter(
            x=KPI_DATA["Week_Label"], y=KPI_DATA["Abandonment_Pct"] * 8,
            name="Abandonment (scaled)", line=dict(color="#EF4444", width=2, dash="dot"),
            mode="lines+markers", yaxis="y2"
        ))
        fig4.update_layout(
            title=dict(text="Callback Volume vs. Abandonment Rate", font=dict(color="white", size=14)),
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            font=dict(color="#9CA3AF"), height=300,
            xaxis=dict(gridcolor="#1F2937"),
            yaxis=dict(gridcolor="#1F2937", title="Callback Volume"),
            yaxis2=dict(overlaying="y", side="right", title="Abandon % (scaled)", showgrid=False),
            legend=dict(bgcolor="#111827", font=dict(color="white")),
            margin=dict(t=40, b=20, l=20, r=20)
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Week 2 callout
    st.markdown("""
    <div style="background:#1F0A0A;border:1px solid #7F1D1D;border-radius:10px;padding:16px 20px;margin-top:8px">
        <div style="color:#EF4444;font-weight:700;font-size:14px;margin-bottom:6px">⚠️ Week 2 Crisis Event — Root Cause Flag</div>
        <div style="color:#FCA5A5;font-size:13px;line-height:1.7">
        System upgrade Sunday night caused EHR access failures Tuesday AM. Call volume spiked to 1,812 (+12%). 
        ASA reached 5.8 min. Abandonment hit 23.7%. Agent availability dropped to 71.6%. 
        Callback volume peaked at 241. <strong>This single event demonstrates the operational fragility of a manual-only contact center — zero surge buffer, no virtual agent, no automated callback recovery.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
    ⚠️ SYNTHETIC DATA ONLY — All figures are illustrative. No protected health information included. Portfolio demonstration by JDMC Services LLC.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 2 — ARIA INTENT SIMULATOR
# ════════════════════════════════════════════════════════════════
elif page == "🤖 ARIA Intent Simulator":
    st.markdown('<div class="section-header">🤖 ARIA — AI Virtual Agent Intent Simulator</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#111827;border:1px solid #1F2937;border-radius:10px;padding:16px 20px;margin-bottom:20px">
        <div style="color:#0D7680;font-weight:600;font-size:13px;margin-bottom:6px">How This Works</div>
        <div style="color:#9CA3AF;font-size:13px;line-height:1.7">
        Type any caller phrase below — exactly as a caller would say it. ARIA will classify the intent, 
        assess risk, determine routing, and generate a structured agent handoff summary using the Claude AI model. 
        This simulates the ARIA virtual agent workflow from the AI Virtual Agent specification document.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_examples = st.columns([2, 1])

    with col_input:
        caller_phrase = st.text_area(
            "Enter caller phrase",
            placeholder="e.g. I can't log into the EHR system and I have patients waiting...",
            height=100,
            help="Type what the caller says when they first contact the contact center"
        )

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            run_aria = st.button("🤖 Run ARIA Analysis", use_container_width=True)
        with col_b2:
            clear = st.button("🗑️ Clear", use_container_width=True)

    with col_examples:
        st.markdown('<div style="color:#6B7280;font-size:12px;font-weight:600;margin-bottom:8px">EXAMPLE PHRASES</div>', unsafe_allow_html=True)
        examples = [
            "My password expired and I can't log in",
            "I don't have access to the medication dispensing app",
            "My laptop won't turn on",
            "Can someone call me back later today?",
            "The phones on the 3rd floor aren't working",
            "I'm not sure who to call about this",
            "This is urgent — the EHR is down and patients are waiting",
        ]
        for ex in examples:
            if st.button(f"→ {ex[:45]}...' " if len(ex) > 45 else f"→ {ex}", key=ex, use_container_width=True):
                caller_phrase = ex
                run_aria = True

    if run_aria and caller_phrase:
        if not api_key:
            st.error("⚠️ Please enter your Anthropic API key in the sidebar to enable AI analysis.")
        else:
            with st.spinner("ARIA is analyzing the caller intent..."):
                try:
                    client = anthropic.Anthropic(api_key=api_key)

                    system_prompt = """You are ARIA — an AI Virtual Agent for a healthcare IT contact center. 
You analyze caller phrases and produce structured triage output.

You must respond ONLY with a valid JSON object in this exact format:
{
  "intent": "one of: Password Reset, Application Access Issue, Device Issue, Callback Request, Telecom Issue, General IT Support, Urgent Escalation, EHR Access Issue",
  "confidence": "percentage as integer 0-100",
  "risk_level": "one of: LOW, MEDIUM, HIGH, CRITICAL",
  "routing": "specific queue or team name",
  "urgency": "one of: Routine, Elevated, High, Critical",
  "key_details_collected": ["list", "of", "key", "details", "from", "the", "phrase"],
  "clarifying_questions": ["question 1 ARIA would ask", "question 2 if needed"],
  "handoff_summary": "2-3 sentence structured summary for the human agent",
  "recommended_action": "specific next step for the agent",
  "ai_use_case_opportunity": "which AI/CX use case from the assessment would prevent or handle this call",
  "phi_flag": false
}

CRITICAL RULES:
- Never collect or reference PHI, patient names, MRNs, or clinical data
- If the caller mentions patient safety or clinical emergency, set risk_level to CRITICAL and urgency to Critical
- Keep handoff_summary factual and structured — no patient clinical details
- phi_flag must be true only if the caller phrase contains actual PHI (then do not process further)"""

                    response = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1000,
                        system=system_prompt,
                        messages=[{"role": "user", "content": f"Caller phrase: {caller_phrase}"}]
                    )

                    raw = response.content[0].text.strip()
                    # Robust JSON extraction
                    if "```json" in raw:
                        raw = raw.split("```json")[1].split("```")[0].strip()
                    elif "```" in raw:
                        raw = raw.split("```")[1].split("```")[0].strip()
                    start = raw.find("{")
                    end = raw.rfind("}") + 1
                    if start != -1 and end > start:
                        raw = raw[start:end]
                    # Clean problematic characters
                    raw = raw.replace("’", "'").replace("‘", "'")
                    raw = raw.replace("“", '"').replace("”", '"')
                    raw = raw.replace("–", "-").replace("—", "-")

                    result = json.loads(raw)

                    # Display results
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="section-header" style="font-size:16px">ARIA Analysis Results</div>', unsafe_allow_html=True)

                    # Top row metrics
                    r1, r2, r3, r4 = st.columns(4)
                    with r1:
                        intent_info = INTENTS.get(result.get("intent", ""), {"emoji": "❓"})
                        st.markdown(f"""
                        <div class="intent-card">
                            <div class="intent-label">Classified Intent</div>
                            <div class="intent-value">{intent_info.get('emoji','')} {result.get('intent','Unknown')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with r2:
                        risk = result.get("risk_level", "MEDIUM")
                        risk_class = RISK_COLORS.get(risk, "risk-medium")
                        st.markdown(f"""
                        <div class="intent-card">
                            <div class="intent-label">Risk Level</div>
                            <div class="intent-value"><span class="risk-pill {risk_class}">{risk}</span></div>
                        </div>
                        """, unsafe_allow_html=True)
                    with r3:
                        conf = result.get("confidence", 0)
                        conf_color = "#10B981" if conf >= 85 else "#F59E0B" if conf >= 70 else "#EF4444"
                        st.markdown(f"""
                        <div class="intent-card">
                            <div class="intent-label">NLU Confidence</div>
                            <div class="intent-value" style="color:{conf_color}">{conf}%</div>
                            <div class="score-bar-container"><div class="score-bar-fill" style="width:{conf}%;background:{conf_color}"></div></div>
                        </div>
                        """, unsafe_allow_html=True)
                    with r4:
                        urg = result.get("urgency", "Routine")
                        urg_color = "#EF4444" if urg in ["Critical","High"] else "#F59E0B" if urg == "Elevated" else "#10B981"
                        st.markdown(f"""
                        <div class="intent-card">
                            <div class="intent-label">Urgency</div>
                            <div class="intent-value" style="color:{urg_color}">{urg}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    col_left, col_right = st.columns(2)

                    with col_left:
                        st.markdown(f"""
                        <div class="ai-response">
                            <div class="ai-response-header">🗺️ Routing Decision</div>
                            <div style="color:#FFFFFF;font-size:15px;font-weight:600;margin-bottom:12px">{result.get('routing','—')}</div>
                            <div class="ai-response-header" style="margin-top:16px">📋 Key Details Collected</div>
                            {''.join([f'<div style="color:#D1D5DB;font-size:13px;padding:3px 0">• {d}</div>' for d in result.get('key_details_collected',[])])}
                            <div class="ai-response-header" style="margin-top:16px">❓ ARIA Clarifying Questions</div>
                            {''.join([f'<div style="color:#0D7680;font-size:13px;padding:3px 0">→ {q}</div>' for q in result.get('clarifying_questions',[])])}
                        </div>
                        """, unsafe_allow_html=True)

                    with col_right:
                        st.markdown(f"""
                        <div class="ai-response">
                            <div class="ai-response-header">📄 Agent Handoff Summary</div>
                            <div class="handoff-block">
INTERACTION ID: ARIA-{hash(caller_phrase) % 99999:05d}<br>
TIMESTAMP: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} ET<br>
INTENT: {result.get('intent','—')}<br>
RISK: {result.get('risk_level','—')} | URGENCY: {result.get('urgency','—')}<br>
ROUTING: {result.get('routing','—')}<br>
PHI COLLECTED: {'⚠️ FLAG REVIEW' if result.get('phi_flag') else 'NONE — COMPLIANT'}<br>
<br>
SUMMARY:<br>{result.get('handoff_summary','—')}<br>
<br>
RECOMMENDED ACTION:<br>{result.get('recommended_action','—')}
                            </div>
                            <div class="ai-response-header" style="margin-top:16px">💡 AI/CX Opportunity</div>
                            <div style="color:#0D7680;font-size:13px;line-height:1.6">{result.get('ai_use_case_opportunity','—')}</div>
                        </div>
                        """, unsafe_allow_html=True)

                except json.JSONDecodeError:
                    st.error("ARIA returned an unexpected response format. Please try again.")
                except Exception as e:
                    st.error(f"API Error: {str(e)}")

    st.markdown("""
    <div class="disclaimer">
    ⚠️ SYNTHETIC DEMO — ARIA does not collect PHI. This simulation demonstrates methodology only. No real patient or employee data is processed.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 3 — AI READINESS SCORER
# ════════════════════════════════════════════════════════════════
elif page == "🎯 AI Readiness Scorer":
    st.markdown('<div class="section-header">🎯 AI Contact Center Readiness Scorer</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#111827;border:1px solid #1F2937;border-radius:10px;padding:16px 20px;margin-bottom:20px">
        <div style="color:#0D7680;font-weight:600;font-size:13px;margin-bottom:6px">How This Works</div>
        <div style="color:#9CA3AF;font-size:13px;line-height:1.7">
        Answer 10 questions about your contact center environment. The scorer evaluates readiness across 
        6 domains and recommends the right AI use case to pilot first — based on the methodology in the 
        AI Contact Center Readiness Assessment.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("readiness_form"):
        st.markdown('<div style="color:#FFFFFF;font-size:15px;font-weight:600;margin-bottom:16px">Contact Center Profile</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            q1 = st.selectbox("1. Do you have structured call data or analytics available?",
                ["No data infrastructure", "Basic call logs only", "Some structured reporting", "Full analytics platform"])
            q2 = st.selectbox("2. How would you describe your current IVR?",
                ["No IVR", "Basic DTMF (press 1, press 2)", "Some automation", "Modern NLU-based IVR"])
            q3 = st.selectbox("3. What is your current abandonment rate?",
                [">25% (Critical)", "15–25% (High)", "10–15% (Elevated)", "<10% (Acceptable)"])
            q4 = st.selectbox("4. Do agents have access to a centralized knowledge base?",
                ["No KB at all", "Printed/informal references", "Basic digital KB", "Structured AI-searchable KB"])
            q5 = st.selectbox("5. Do you have automated callback capability?",
                ["No callback system", "Manual callbacks only", "Basic callback queue", "Intelligent callback with timing"])

        with col2:
            q6 = st.selectbox("6. How mature is your HIPAA/compliance governance?",
                ["No formal governance", "Basic HIPAA policies", "Documented framework", "AI governance framework in place"])
            q7 = st.selectbox("7. How integrated are your telephony, EHR, and ITSM systems?",
                ["No integration — silos", "Manual data sharing", "Some API connectivity", "Full integrated data layer"])
            q8 = st.selectbox("8. How receptive is leadership to AI investment?",
                ["No awareness", "Curious but skeptical", "Supportive with conditions", "Fully committed"])
            q9 = st.selectbox("9. What is your first-call resolution rate?",
                ["<55% (Critical)", "55–65% (Poor)", "65–75% (Fair)", ">75% (Good)"])
            q10 = st.selectbox("10. Have you run any AI pilots or proofs of concept before?",
                ["No AI experience", "Evaluated vendors only", "One completed pilot", "Multiple AI deployments"])

        submitted = st.form_submit_button("🎯 Calculate My Readiness Score", use_container_width=True)

    if submitted:
        # Score mapping
        score_map = {0: 1, 1: 2, 2: 3, 3: 4}
        scores = {
            "Data Readiness": score_map[["No data infrastructure","Basic call logs only","Some structured reporting","Full analytics platform"].index(q1)],
            "Process Maturity": score_map[["No IVR","Basic DTMF (press 1, press 2)","Some automation","Modern NLU-based IVR"].index(q2)],
            "Integration Readiness": score_map[["No integration — silos","Manual data sharing","Some API connectivity","Full integrated data layer"].index(q7)],
            "Governance Readiness": score_map[["No formal governance","Basic HIPAA policies","Documented framework","AI governance framework in place"].index(q6)],
            "Operational Readiness": score_map[["No awareness","Curious but skeptical","Supportive with conditions","Fully committed"].index(q8)],
            "AI Adoption Readiness": score_map[["No AI experience","Evaluated vendors only","One completed pilot","Multiple AI deployments"].index(q10)],
        }

        # Abandonment and FCR bonus scoring
        abandon_bonus = [0,0,1,2][["<10% (Acceptable)","10–15% (Elevated)","15–25% (High)",">25% (Critical)"].index(q3)]
        fcr_gap = [3,2,1,0][["<55% (Critical)","55–65% (Poor)","65–75% (Fair)",">75% (Good)"].index(q9)]

        overall = sum(scores.values()) / len(scores)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header" style="font-size:16px">Your Readiness Score</div>', unsafe_allow_html=True)

        # Overall score
        verdict_color = "#EF4444" if overall < 2.5 else "#F59E0B" if overall < 3.5 else "#10B981"
        verdict_text = "NOT READY — Remediation Required" if overall < 2 else "CONDITIONALLY READY — Structured PoV Recommended" if overall < 3.5 else "READY — Proceed to AI Deployment"

        st.markdown(f"""
        <div style="background:#111827;border:2px solid {verdict_color};border-radius:12px;padding:24px;text-align:center;margin-bottom:20px">
            <div style="font-size:48px;font-weight:700;color:{verdict_color}">{overall:.1f} / 5.0</div>
            <div style="font-size:14px;font-weight:600;color:{verdict_color};margin-top:8px">{verdict_text}</div>
        </div>
        """, unsafe_allow_html=True)

        # Domain scores
        domain_cols = st.columns(3)
        domain_colors = {"Data Readiness": "#EF4444", "Process Maturity": "#F59E0B",
                        "Integration Readiness": "#EF4444", "Governance Readiness": "#0D7680",
                        "Operational Readiness": "#10B981", "AI Adoption Readiness": "#1B3A6B"}

        for idx, (domain, score) in enumerate(scores.items()):
            col = domain_cols[idx % 3]
            color = "#EF4444" if score <= 2 else "#F59E0B" if score == 3 else "#10B981"
            with col:
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:12px">
                    <div class="label">{domain}</div>
                    <div class="value" style="color:{color};font-size:28px">{score} / 5</div>
                    <div class="score-bar-container">
                        <div class="score-bar-fill" style="width:{score/5*100}%;background:{color}"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Recommendation
        min_domain = min(scores, key=scores.get)
        if overall < 2.5:
            rec_use_case = "Agent Assist (Lowest Risk Entry Point)"
            rec_reason = f"Your {min_domain} score of {scores[min_domain]}/5 is a critical gate. Start with Agent Assist — it requires minimal integration and builds trust before any patient-facing AI."
        elif overall < 3.5:
            rec_use_case = "Agent Assist + AI Call Summaries (Recommended PoV)"
            rec_reason = "You have foundational readiness. A 60-90 day Agent Assist PoV with AI Call Summaries will deliver measurable ROI while building the data quality needed for Phase 2."
        else:
            rec_use_case = "Virtual Agent Triage (ARIA) — You Are Ready"
            rec_reason = "Strong readiness across all domains. You can proceed directly to virtual agent deployment with proper governance controls."

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0D1F3C,#0A2540);border:1px solid #0D7680;border-radius:12px;padding:24px;margin-top:16px">
            <div style="color:#0D7680;font-weight:700;font-size:14px;margin-bottom:8px">🎯 RECOMMENDED FIRST AI USE CASE</div>
            <div style="color:#FFFFFF;font-size:18px;font-weight:700;margin-bottom:12px">{rec_use_case}</div>
            <div style="color:#9CA3AF;font-size:13px;line-height:1.7">{rec_reason}</div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 4 — PERFORMANCE ANALYZER
# ════════════════════════════════════════════════════════════════
elif page == "📈 Performance Analyzer":
    st.markdown('<div class="section-header">📈 AI-Powered Performance Analyzer</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#111827;border:1px solid #1F2937;border-radius:10px;padding:16px 20px;margin-bottom:20px">
        <div style="color:#0D7680;font-weight:600;font-size:13px;margin-bottom:6px">How This Works</div>
        <div style="color:#9CA3AF;font-size:13px;line-height:1.7">
        Select your worst-performing KPI and enter your current value. Claude AI will generate a root-cause hypothesis, 
        AI/CX remediation recommendation, and ROI estimate — applying the analysis framework from the Performance Analysis document.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_in, col_out = st.columns([1, 1])

    with col_in:
        kpi_choice = st.selectbox("Select your most urgent KPI problem", [
            "Abandonment Rate",
            "Average Speed to Answer",
            "First Call Resolution",
            "Repeat Call Rate",
            "Agent Availability",
            "Escalation Rate",
            "After-Call Work Time",
            "Callback Volume",
        ])

        kpi_value = st.text_input(
            f"Your current {kpi_choice} value",
            placeholder="e.g. 22% or 5.5 min"
        )

        environment = st.selectbox("Contact center environment", [
            "Healthcare — Internal IT Support",
            "Healthcare — Patient Access",
            "Healthcare — Clinical Operations",
            "Healthcare — Revenue Cycle",
        ])

        weekly_calls = st.slider("Approximate weekly call volume", 500, 5000, 1700, 100)

        analyze = st.button("📈 Generate AI Analysis", use_container_width=True)

    with col_out:
        if analyze and kpi_value:
            if not api_key:
                st.error("⚠️ Please enter your Anthropic API key in the sidebar.")
            else:
                with st.spinner("Analyzing performance data..."):
                    try:
                        client = anthropic.Anthropic(api_key=api_key)

                        prompt = f"""You are a senior AI/CX Solutions Architect analyzing contact center performance for a healthcare environment.

KPI Problem: {kpi_choice}
Current Value: {kpi_value}
Environment: {environment}
Weekly Call Volume: {weekly_calls:,} calls

CRITICAL: Respond ONLY with a valid JSON object. Use only standard ASCII characters. No smart quotes, no em-dashes, no special unicode. Use straight apostrophes only inside string values if needed. No markdown, no code blocks, just raw JSON:
{{
  "benchmark": "industry benchmark for this KPI",
  "gap_assessment": "one sentence on how far from benchmark",
  "severity": "one of: CRITICAL, HIGH, MEDIUM, LOW",
  "top_root_causes": ["cause 1", "cause 2", "cause 3"],
  "primary_ai_recommendation": "specific AI/CX use case name",
  "why_this_use_case": "2 sentences explaining the fit",
  "expected_improvement": "specific projected improvement with numbers",
  "estimated_annual_value": "dollar range based on volume",
  "implementation_timeline": "how long to see results",
  "governance_consideration": "key responsible AI control for this use case",
  "next_step": "single most important action to take this week"
}}"""

                        response = client.messages.create(
                            model="claude-sonnet-4-6",
                            max_tokens=800,
                            messages=[{"role": "user", "content": prompt}]
                        )

                        raw = response.content[0].text.strip()
                        # Robust JSON extraction
                        if "```json" in raw:
                            raw = raw.split("```json")[1].split("```")[0].strip()
                        elif "```" in raw:
                            raw = raw.split("```")[1].split("```")[0].strip()
                        # Find JSON object boundaries
                        start = raw.find("{")
                        end = raw.rfind("}") + 1
                        if start != -1 and end > start:
                            raw = raw[start:end]
                        # Clean problematic characters
                        raw = raw.replace("’", "'").replace("‘", "'")
                        raw = raw.replace("“", '"').replace("”", '"')
                        raw = raw.replace("–", "-").replace("—", "-")

                        r = json.loads(raw)

                        sev = r.get("severity", "HIGH")
                        sev_color = {"CRITICAL":"#EF4444","HIGH":"#F59E0B","MEDIUM":"#0D7680","LOW":"#10B981"}.get(sev,"#F59E0B")

                        # Dashboard header
                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,#1B3A6B,#0D7680);border-radius:12px;padding:16px 20px;margin-bottom:16px">
                            <div style="color:rgba(255,255,255,0.7);font-size:11px;text-transform:uppercase;letter-spacing:0.8px">Analysis Results</div>
                            <div style="color:#FFFFFF;font-size:20px;font-weight:700;margin-top:4px">{kpi_choice}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Top metric row
                        m1, m2, m3 = st.columns(3)
                        with m1:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="label">Industry Benchmark</div>
                                <div class="value metric-green" style="font-size:22px">{r.get('benchmark','—')}</div>
                            </div>""", unsafe_allow_html=True)
                        with m2:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="label">Severity Rating</div>
                                <div class="value" style="font-size:22px;color:{sev_color}">{sev}</div>
                            </div>""", unsafe_allow_html=True)
                        with m3:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="label">Timeline to Results</div>
                                <div class="value metric-teal" style="font-size:18px">{r.get('implementation_timeline','—')}</div>
                            </div>""", unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)

                        # Gap assessment
                        st.markdown(f"""
                        <div style="background:#111827;border-left:4px solid {sev_color};border-radius:0 8px 8px 0;padding:12px 16px;margin-bottom:16px">
                            <div style="color:#6B7280;font-size:11px;text-transform:uppercase;margin-bottom:4px">Gap Assessment</div>
                            <div style="color:#D1D5DB;font-size:13px">{r.get('gap_assessment','—')}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Two columns — root causes + recommendation
                        rc1, rc2 = st.columns(2)
                        with rc1:
                            st.markdown('<div style="color:#0D7680;font-size:12px;font-weight:700;text-transform:uppercase;margin-bottom:8px">🔍 Root Causes</div>', unsafe_allow_html=True)
                            for c in r.get('top_root_causes', []):
                                st.markdown(f"""
                                <div style="background:#111827;border:1px solid #1F2937;border-radius:8px;padding:10px 14px;margin-bottom:6px;color:#D1D5DB;font-size:13px">
                                    ▸ {c}
                                </div>""", unsafe_allow_html=True)

                        with rc2:
                            st.markdown('<div style="color:#0D7680;font-size:12px;font-weight:700;text-transform:uppercase;margin-bottom:8px">💡 AI Recommendation</div>', unsafe_allow_html=True)
                            st.markdown(f"""
                            <div style="background:#0D1F3C;border:1px solid #0D7680;border-radius:8px;padding:14px;margin-bottom:8px">
                                <div style="color:#FFFFFF;font-size:14px;font-weight:700;margin-bottom:6px">{r.get('primary_ai_recommendation','—')}</div>
                                <div style="color:#9CA3AF;font-size:12px;line-height:1.6">{r.get('why_this_use_case','—')}</div>
                            </div>""", unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)

                        # Value row
                        v1, v2 = st.columns(2)
                        with v1:
                            st.markdown(f"""
                            <div style="background:#064E3B;border:1px solid #10B981;border-radius:10px;padding:16px;text-align:center">
                                <div style="color:#6EE7B7;font-size:11px;text-transform:uppercase;margin-bottom:6px">Expected Improvement</div>
                                <div style="color:#FFFFFF;font-size:15px;font-weight:700">{r.get('expected_improvement','—')}</div>
                            </div>""", unsafe_allow_html=True)
                        with v2:
                            st.markdown(f"""
                            <div style="background:#064E3B;border:1px solid #10B981;border-radius:10px;padding:16px;text-align:center">
                                <div style="color:#6EE7B7;font-size:11px;text-transform:uppercase;margin-bottom:6px">Est. Annual Value</div>
                                <div style="color:#FFFFFF;font-size:15px;font-weight:700">{r.get('estimated_annual_value','—')}</div>
                            </div>""", unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)

                        # Next step + governance
                        st.markdown(f"""
                        <div style="background:#0A2540;border:1px solid #0D7680;border-radius:10px;padding:16px;margin-bottom:10px">
                            <div style="color:#0D7680;font-size:11px;font-weight:700;text-transform:uppercase;margin-bottom:6px">⚡ Next Step This Week</div>
                            <div style="color:#FFFFFF;font-size:13px;font-weight:600">{r.get('next_step','—')}</div>
                        </div>
                        <div style="background:#111827;border:1px solid #1F2937;border-radius:10px;padding:16px">
                            <div style="color:#6B7280;font-size:11px;font-weight:700;text-transform:uppercase;margin-bottom:6px">🛡️ Governance Consideration</div>
                            <div style="color:#9CA3AF;font-size:13px">{r.get('governance_consideration','—')}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Analysis error: {str(e)}")
        else:
            st.markdown("""
            <div style="background:#111827;border:1px dashed #374151;border-radius:12px;padding:40px;text-align:center;height:400px;display:flex;align-items:center;justify-content:center">
                <div>
                    <div style="font-size:40px;margin-bottom:16px">📈</div>
                    <div style="color:#4B5563;font-size:14px">Select a KPI, enter your current value,<br>and click Generate AI Analysis</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
    ⚠️ AI-generated analysis is for demonstration purposes only. All recommendations should be validated by qualified professionals before implementation.
    </div>
    """, unsafe_allow_html=True)

# ── Bottom CTA ────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background:linear-gradient(135deg,#1B3A6B,#0D7680);border-radius:12px;padding:24px;text-align:center;margin-top:20px">
    <div style="color:#FFFFFF;font-size:16px;font-weight:700;margin-bottom:8px">Ready to assess your organization's AI contact center readiness?</div>
    <div style="color:rgba(255,255,255,0.75);font-size:13px;margin-bottom:16px">James D. McClain, MBA | Healthcare IT Leader | AI Contact Center Modernization | Responsible AI Governance</div>
    <a href="https://www.linkedin.com/in/jamesdmcclain" target="_blank" style="background:rgba(255,255,255,0.15);color:#FFFFFF;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:600;font-size:13px;border:1px solid rgba(255,255,255,0.3)">
        Connect on LinkedIn →
    </a>
</div>
""", unsafe_allow_html=True)
