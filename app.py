import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import tempfile, os, base64, io

st.set_page_config(page_title="LexiTech 2.0 | Worst-Case Life Event Simulator", page_icon="LEXItech.PNG", layout="wide")

st.markdown("""
<style>
@import url('https://googleapis.com');
html, body, .stApp, p, label, h1, h2, h3, h4, li { font-family: 'Plus Jakarta Sans', sans-serif !important; color: #1A161F !important; }
.stApp { background-color: #FFFFFF; background-image: radial-gradient(#E8C5D6 0.75px, transparent 0.75px); background-size: 22px 22px; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #FDF2F7 0%, #F9E6F0 100%); border-right: 1px solid #E5B8CE; }
.mono-tag { font-family: 'JetBrains Mono', monospace !important; font-size: 11px !important; font-weight: 700 !important; letter-spacing: 0.08em; color: #B81D6F !important; text-transform: uppercase; }
.nav-bar { background: rgba(255, 255, 255, 0.94); backdrop-filter: blur(10px); border: 1.5px solid #E5B8CE; border-radius: 14px; padding: 14px 22px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 20px rgba(184, 29, 111, 0.07); }
.status-pill { background: #FDF2F7; border: 1px solid #B81D6F; border-radius: 999px; padding: 6px 14px; font-family: 'JetBrains Mono', monospace !important; font-size: 11px !important; font-weight: 700 !important; color: #B81D6F !important; }
.hero-box { background: linear-gradient(135deg, #24101C 0%, #4A1533 55%, #881652 100%); border-radius: 16px; padding: 24px 28px; margin-bottom: 20px; box-shadow: 0 10px 28px rgba(184, 29, 111, 0.16); }
.hero-box h1, .hero-box p, .hero-box span { color: #FFFFFF !important; }
.corpus-card { background: #FFFFFF; border: 1.5px solid #E5B8CE; border-top: 4px solid #B81D6F; border-radius: 14px; padding: 16px 20px; margin-bottom: 10px; box-shadow: 0 4px 14px rgba(184, 29, 111, 0.05); }
.kpi-card { background: #FDF2F7; border: 1.5px solid #E5B8CE; border-radius: 12px; padding: 14px 18px; text-align: center; }
.kpi-num { font-size: 26px !important; font-weight: 800 !important; color: #B81D6F !important; }
.stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div, .stTextArea textarea, .stTextInput input, [data-testid="stFileUploaderDropzone"] { background-color: #FDF2F7 !important; color: #1A161F !important; border: 1.5px solid #E5B8CE !important; border-radius: 10px !important; }
[data-testid="stAlert"], [data-testid="stAlertContainer"], .stSpinner > div { background-color: #FDF2F7 !important; color: #1A161F !important; border: 1.5px solid #B81D6F !important; border-radius: 10px !important; }
button, .stButton > button, .stDownloadButton > button, [data-testid="stFileUploaderDropzone"] button, [data-testid="stTextInput"] button { background: linear-gradient(135deg, #B81D6F 0%, #8E1454 100%) !important; color: #FFFFFF !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important; box-shadow: 0 4px 12px rgba(184, 29, 111, 0.22) !important; }
button *, .stButton > button *, .stDownloadButton > button *, [data-testid="stFileUploaderDropzone"] button *, [data-testid="stTextInput"] button * { color: #FFFFFF !important; }
[data-testid="stTextInput"] button svg { fill: #FFFFFF !important; }
.stTabs [data-baseweb="tab"] { background-color: #FDF2F7; border-radius: 8px 8px 0 0; padding: 8px 18px; border: 1px solid #E5B8CE; font-weight: 600; }
.stTabs [aria-selected="true"] { background: #B81D6F !important; }
.stTabs [aria-selected="true"] * { color: #FFFFFF !important; }
.lexitech-footer { background: #FDF2F7; border: 1px solid #E5B8CE; border-radius: 12px; padding: 14px 18px; text-align: center; font-size: 12.5px; margin-top: 28px; }
</style>
""", unsafe_allow_html=True)

logo_b64 = ""
if os.path.exists("LEXItech.PNG"):
    im = Image.open("LEXItech.PNG").convert("RGBA")
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    logo_b64 = base64.b64encode(buf.getvalue()).decode()

LOGO_SVG = f"""
<div style="display:flex;align-items:center;gap:16px;">
  <div style="background:linear-gradient(135deg,#FDF2F7 0%,#FFFFFF 100%);border:2px solid #E5B8CE;border-radius:18px;padding:8px;box-shadow:0 6px 18px rgba(184,29,111,0.16);display:flex;align-items:center;justify-content:center;">
    <img src="data:image/png;base64,{logo_b64}" style="width:86px;height:86px;object-fit:contain;image-rendering:high-quality;" />
  </div>
  <div>
    <div style="font-weight:800;font-size:26px;letter-spacing:-0.02em;line-height:1.1;">LEXI<span style="color:#B81D6F;">TECH</span></div>
    <div class="mono-tag" style="font-size:12px !important;margin-top:3px;">LEGAL &amp; TAX AI STUDIO</div>
  </div>
</div>
"""

with st.sidebar:
    st.markdown(LOGO_SVG, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="mono-tag">01 // AUTHENTICATION</div>', unsafe_allow_html=True)
    api_key = st.text_input("Gemini API Key", type="password", placeholder="Paste AI Studio Key...")
    st.markdown("---")
    st.markdown('<div class="mono-tag">02 // CRISIS SANDBOX</div>', unsafe_allow_html=True)
    use_sample = st.checkbox("🌪️ Load Built-In Trap Contract", value=False)
    st.caption("Stress-tests a Commercial Lease & Employment Offer against sudden emergencies.")
    st.markdown("---")
    st.caption("Architected by **Heidi Seckman**")
st.markdown(f"""
<div class="nav-bar">
  {LOGO_SVG}
  <div class="status-pill">● MODULE 03 // ADVERSARIAL CRISIS SIMULATOR</div>
</div>
<div class="hero-box">
  <span style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.1em;opacity:0.85;">WORST-CASE LIFE EVENT STRESS-TESTING</span>
  <h1 style="margin:4px 0 8px 0;font-size:30px;">Life Event Contract Simulator</h1>
  <p style="margin:0;font-size:15px;opacity:0.92;">Simulate sudden job loss, medical emergencies, business partner default, or force majeure against any contract to uncover hidden financial traps and draft pre-signing escape clauses.</p>
</div>
""", unsafe_allow_html=True)

SAMPLE_TRAP_CONTRACT = """COMMERCIAL STUDIO LEASE & EXECUTIVE EMPLOYMENT AGREEMENT (EXCERPT)
Section 3.1 (Rent Acceleration & Personal Guarantee): Tenant signs a 36-month lease at $3,800/month ($136,800 total) backed by an unconditional Personal Guarantee. If Tenant defaults for any reason—including illness, business closure, or loss of income—100% of remaining rent accelerates immediately plus 18% annual interest and Landlord's attorney fees. No subletting or early termination is permitted.
Section 6.4 (Relocation & Non-Compete): Employee agrees not to work within 50 miles in any related field for 24 months even if terminated without cause or laid off due to company restructuring. Signing bonus of $10,000 must be repaid in full within 15 days if employment ends before 24 months for any reason.
Section 9.2 (Force Majeure): Unforeseen emergencies, public health orders, or building damage do not excuse or pause Tenant's monthly payment obligations."""

if not use_sample:
    st.markdown('<div class="corpus-card"><div class="mono-tag">STEP 01 // UPLOAD TARGET CONTRACT</div><h4 style="margin:4px 0;">Agreement to Stress-Test</h4><p style="margin:0;font-size:13.5px;">Residential/commercial lease, job offer, LLC operating agreement, loan note, or service contract.</p></div>', unsafe_allow_html=True)
    contract_pdf = st.file_uploader("Upload Contract PDF", type="pdf", key="sim_doc")
else:
    st.info("🌪️ Crisis Sandbox Active: Stress-testing a 36-Month Personal-Guarantee Lease & Employment Agreement.")
    with st.expander("🔍 Inspect Active Sample Contract"):
        st.text_area("Sample Contract Text", SAMPLE_TRAP_CONTRACT, height=165, disabled=True)

c1, c2 = st.columns((1, 1))
with c1:
    scenarios = st.multiselect(
        "Select Worst-Case Life Events to Simulate:",
        (
            "Sudden Job Loss / Involuntary Layoff",
            "Severe Medical Emergency / Temporary Disability",
            "Business Partner Ghosting, Insolvency, or Default",
            "Divorce / Household Separation & Relocation",
            "Natural Disaster / Fire / Force Majeure Shutdown"
        ),
        default=("Sudden Job Loss / Involuntary Layoff", "Severe Medical Emergency / Temporary Disability")
    )
with c2:
    user_role = st.text_input("Your Role & Specific Worry (Optional):", placeholder="e.g., I am the Tenant/Employee—calculate my exact dollar exposure...")

SYSTEM_INSTRUCTIONS = """You are LexiTech 2.0 (Module 03), an adversarial legal-financial crisis simulator. Stress-test the attached contract against the user's selected worst-case life events. Anchor every finding strictly to exact sections and page numbers in the document. Output three exact Markdown sections:
## SECTION 1: CRISIS IMPACT & EXPOSURE MATRIX
Markdown table: | Severity | Life Event Trigger | Contract Clause & Citation | Financial & Legal Fallout |
## SECTION 2: PRE-SIGNING PROTECTION CLAUSES
For each trap show: **Vulnerable Clause**, **LexiTech Escape-Hatch Redline** (hardship cap, cure period, or termination trigger), and **Why This Protects You**.
## SECTION 3: EMERGENCY SURVIVAL ACTION PLAN
Step-by-step tactical checklist if this emergency strikes after signing."""

if st.button("🌪️ Run Worst-Case Crisis Simulation"):
    if not api_key:
        st.warning("Paste your Gemini API Key in the left sidebar to activate the simulator.")
    elif not use_sample and not contract_pdf:
        st.warning("Upload a contract PDF—or toggle 'Load Built-In Trap Contract' in the sidebar.")
    elif not scenarios:
        st.warning("Select at least one worst-case life event scenario to simulate.")
    else:
        with st.spinner("Running adversarial life-event stress test..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"Simulated Scenarios: {', '.join(scenarios)}\nUser Role & Context: {user_role or 'Signing party seeking maximum downside protection.'}"
                if use_sample:
                    payload = (f"CONTRACT:\n{SAMPLE_TRAP_CONTRACT}\n\n{prompt}",)
                    src = "Sample_Trap_Contract"
                else:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(contract_pdf.read())
                        p = tmp.name
                    f_up = client.files.upload(file=p)
                    os.remove(p)
                    payload = ("CONTRACT DOCUMENT:", f_up, prompt)
                    src = contract_pdf.name

                models = tuple(m.name.replace("models/", "") for m in client.models.list() if "gemini" in m.name and "flash" in m.name)
                for m_name in models:
                    try:
                        res = client.models.generate_content(model=m_name, contents=list(payload), config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTIONS))
                        st.session_state["sim_rep"], st.session_state["sim_mod"], st.session_state["sim_src"], st.session_state["sim_cnt"] = res.text, m_name, src, len(scenarios)
                        break
                    except Exception:
                        continue
            except Exception as e:
                st.error(f"Error: {e}")

if "sim_rep" in st.session_state:
    txt = st.session_state["sim_rep"]
    high_hits = txt.upper().count("HIGH") + txt.upper().count("CRITICAL")
    k1, k2, k3 = st.columns(3)
    k1.markdown(f'<div class="kpi-card"><div class="mono-tag">SCENARIOS TESTED</div><div class="kpi-num">{st.session_state["sim_cnt"]}</div><div>Stress Vectors</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-card"><div class="mono-tag">SEVERE TRAPS CAUGHT</div><div class="kpi-num">{max(high_hits, 1)}</div><div>Downside Flags</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-card"><div class="mono-tag">ACTIVE ENGINE</div><div class="kpi-num" style="font-size:18px !important;padding-top:6px;">{st.session_state["sim_mod"]}</div><div>Closed-Book Audit</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    s1, _, rest = txt.partition("## SECTION 2:")
    s2, _, s3 = rest.partition("## SECTION 3:")
    t1, t2, t3 = st.tabs(("🚨 Crisis Exposure Matrix", "🛡️ Pre-Signing Escape Clauses", "📋 Survival Checklist & Export"))
    t1.markdown(s1)
    t2.markdown("## SECTION 2:" + s2 if rest else txt)
    t3.markdown("## SECTION 3:" + s3 if s3 else txt)
    t3.download_button("📥 Export Crisis Simulation Report (.txt)", data=txt, file_name=f"LexiTech2_CrisisSim_{st.session_state['sim_src']}.txt", mime="text/plain")

st.markdown('<div class="lexitech-footer"><strong>© 2026 LexiTech by Heidi Seckman. All Rights Reserved.</strong><br>Proprietary software, interface design, and branding—unauthorized copying, cloning, or commercial redistribution is prohibited. For educational and research assistance only; not legal or financial advice.</div>', unsafe_allow_html=True)
