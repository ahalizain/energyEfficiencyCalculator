import streamlit as st
import time
import io
import uuid

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import plotly.graph_objects as go

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ======================================================
# PAGE CONFIG  (must be the first Streamlit call)
# ======================================================
st.set_page_config(
    page_title="Energy Efficiency Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ======================================================
# CONSTANTS  (your original numbers, unchanged)
# ======================================================
ENERGY_STAR_SAVINGS = 0.30
THERMOSTAT_SAVINGS  = 0.11
WINDOWS_SAVINGS     = 0.12
MONEY_CONVERTER     = 0.1798   # dollars per kWh
TESLA_KWH_PM        = 153.33

GREEN = "#2E7D32"
BLUE  = "#1565C0"

# ======================================================
# SUPABASE (anonymous data collection) — degrades gracefully
# if secrets aren't set, so the app never crashes for users.
# ======================================================
@st.cache_resource
def get_supabase():
    try:
        from supabase import create_client
        return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_ANON_KEY"])
    except Exception:
        return None

def save_response(payload: dict):
    client = get_supabase()
    if client is None:
        return False
    try:
        client.table("survey_responses").insert(payload).execute()
        return True
    except Exception:
        return False

# ======================================================
# SESSION STATE
# ======================================================
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
for k, v in {"test_mode": False, "test_case_used": False,
             "confirm_overwrite": False, "calculated": False}.items():
    st.session_state.setdefault(k, v)

# ======================================================
# CUSTOM CSS  (the "Wix-style" coat of paint)
# Selectors targeting Streamlit internals may need small tweaks
# if Streamlit updates; the custom HTML blocks below are safe.
# ======================================================
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');

    /* Flyer palette */
    :root {
        --cream:  #FBF0DD;
        --mint:   #C9E8D2;
        --teal:   #2F8E8E;
        --blue:   #3A6FD8;
        --ink:    #2b2b2b;
    }

    /* App-wide cream background to match the flyer */
    .stApp { background: #FBF0DD; }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--ink); }
    h1, h2, h3 { font-family: 'Poppins', sans-serif; color: #2F8E8E; }
    #MainMenu, footer { visibility: hidden; }

    /* ---------- HERO (teal headline like the flyer title) ---------- */
    .hero {
        background: #FBF0DD;
        padding: 2.4rem 2rem 1.6rem 2rem;
        border-radius: 22px;
        text-align: left;
        margin-bottom: 1.4rem;
    }
    .hero h1 { font-size: 3rem; line-height:1.05; margin: 0 0 .4rem 0; color:#2F8E8E; }
    .hero p  { font-size: 1.15rem; color:#3A6FD8; font-weight:600; margin:.2rem 0; }

    /* ---------- Mint hook panel (the "Most homeowners think..." block) ---------- */
    .hook {
        background: #C9E8D2;
        padding: 1.8rem 2rem; border-radius: 18px;
        color:#3A6FD8; font-weight:600; font-size:1.1rem; line-height:1.5;
        margin-bottom: 1.4rem;
    }
    .hook strong { color:#2F8E8E; }

    /* ---------- Upgrade section ---------- */
    .upgrade h2 { color:#3A6FD8; font-size:2.2rem; margin-bottom:.6rem; }
    .upgrade .lead { color:#3A6FD8; font-weight:700; font-size:1.15rem; margin:.4rem 0; }
    .upgrade ul { color:#3A6FD8; font-weight:600; font-size:1.05rem; }
    .upgrade .tagline { color:#3A6FD8; font-weight:700; font-size:1.2rem; margin-top:.8rem; }

    /* ---------- Cards ---------- */
    .card {
        background:#fff; border:1px solid #e7ddc8; border-radius:16px;
        padding:1.4rem; text-align:center; height:100%;
        box-shadow:0 4px 16px rgba(0,0,0,.06);
    }
    .card .emoji { font-size:2.2rem; }
    .card h3 { margin:.5rem 0 .3rem 0; color:#2F8E8E; }
    .card p  { color:#555; font-size:.95rem; margin:0; }

    /* ---------- Mint "How It Works" panel ---------- */
    .howto {
        background:#C9E8D2; padding:1.6rem 2rem; border-radius:18px; margin-top:1rem;
    }
    .howto h3 { color:#2F8E8E; margin-top:0; }
    .howto ol { color:#3A6FD8; font-weight:600; font-size:1.05rem; }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 0 0; padding: 10px 20px; font-weight:600;
    }
    .stTabs [aria-selected="true"] { background:#C9E8D2 !important; color:#2F8E8E !important; }

    /* ---------- Buttons ---------- */
    div.stButton > button {
        background:#2F8E8E; color:#fff; border:none; border-radius:10px;
        padding:.6rem 1.5rem; font-weight:600;
    }
    div.stButton > button:hover { background:#256f6f; color:#fff; }
    </style>
    """, unsafe_allow_html=True)

# ======================================================
# PDF GENERATION  (kept from your original, signature unchanged)
# ======================================================
def generate_pdf(total_kwh_saved, total_money_saved, items, money_converter,
                 tesla_kwh_pm, fig_bar, fig_scatter):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    current_y = height - 50
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, current_y, "Energy Efficiency Report")
    current_y -= 40

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, current_y,
                   f"You have potential to save {total_kwh_saved:.2f} kWh and ${total_money_saved:.2f} per month!")
    current_y -= 30

    if total_kwh_saved >= tesla_kwh_pm:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.setFillColorRGB(0, 0.6, 0)
        pdf.drawString(50, current_y, "You can save enough energy monthly to charge an electric vehicle!")
        pdf.setFillColorRGB(0, 0, 0)
        current_y -= 35
    else:
        current_y -= 15

    img_bar = io.BytesIO()
    fig_bar.savefig(img_bar, format='png', dpi=100, bbox_inches='tight'); img_bar.seek(0)
    pdf.drawImage(ImageReader(img_bar), 50, current_y - 250, width=500, height=250)
    current_y -= 270

    img_sc = io.BytesIO()
    fig_scatter.savefig(img_sc, format='png', dpi=100, bbox_inches='tight'); img_sc.seek(0)
    pdf.drawImage(ImageReader(img_sc), 50, current_y - 250, width=500, height=250)

    pdf.showPage()
    current_y = height - 50
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, current_y, "Total Money & Energy Savings Per Household Replacement Type")
    current_y -= 40
    pdf.setFont("Helvetica", 12)

    templates = {
        "Bulbs": "Changing lightbulbs in your home will save {kwh:.2f} kWh, or ${money:.2f} a month!",
        "Thermostat": "Installing a learning thermostat will save {kwh:.2f} kWh, or ${money:.2f} a month!",
        "Windows": "Replacing your windows with high-efficiency ones will save {kwh:.2f} kWh, or ${money:.2f} a month!",
        "Washer": "Upgrading to an Energy Star Washer will save {kwh:.2f} kWh, or ${money:.2f} a month!",
        "Dryer": "Upgrading to an Energy Star Dryer will save {kwh:.2f} kWh, or ${money:.2f} a month!",
        "Oven/Stovetop": "Upgrading to an Energy Star Oven/Stovetop will save {kwh:.2f} kWh, or ${money:.2f} a month!",
        "Refrigerator": "Upgrading to an Energy Star Refrigerator will save {kwh:.2f} kWh, or ${money:.2f} a month!",
    }
    for name, kwh in items.items():
        if kwh > 0:
            pdf.drawString(50, current_y, "• " + templates[name].format(kwh=kwh, money=kwh * money_converter))
            current_y -= 25

    pdf.save()
    buffer.seek(0)
    return buffer

# ======================================================
# SIDEBAR — developer test-case loader (kept out of the public look)
# ======================================================
def render_sidebar():
    with st.sidebar:
        st.subheader("🧪 Developer Tools")
        pw = st.text_input("Password to load test case", type="password",
                           disabled=st.session_state.test_case_used)
        if st.button("Load Test Case", disabled=st.session_state.test_case_used):
            if pw != st.secrets.get("TEST_CASE_PASSWORD", None):
                st.error("Incorrect password.")
            else:
                st.session_state.confirm_overwrite = True

        if st.session_state.confirm_overwrite:
            st.warning("Overwrite ALL inputs with the test case?")
            if st.button("Yes, overwrite"):
                st.session_state.update({
                    "house_area": 2200, "kwh_consumption": 1100.0, "dollar_kwh_consumption": 180.0,
                    "windows_replacement": "No", "num_conv_bulb": 50, "num_led_bulb": 10,
                    "thermostat": "No", "heating": "No", "air_conditioning": "Yes", "hot_water": "No",
                    "oven_stovetop": "No", "washer": "No", "dryer": "No", "refrigerator": "No",
                    "oven_power_mode": "Average", "oven_usage_mode": "Average",
                    "washer_power_mode": "Average", "washer_usage_mode": "Average",
                    "dryer_power_mode": "Average", "dryer_usage_mode": "Average",
                    "refrigerator_power_mode": "Average", "refrigerator_usage_mode": "Average",
                    "ev": "No", "test_mode": True, "test_case_used": True,
                    "confirm_overwrite": False, "calculated": True,
                })
                st.rerun()
            if st.button("Cancel"):
                st.session_state.confirm_overwrite = False

        if st.session_state.test_mode:
            st.info("TEST MODE — inputs auto-filled.")

# ======================================================
# TAB 1 — HOME / LANDING
# ======================================================
def render_home():
    # Hero title (teal, like the flyer header)
    st.markdown("""
    <div class="hero">
        <h1>⚡ Energy Efficiency Calculator</h1>
        <p>Improve your home in 2 minutes — free, anonymous, no signup.</p>
    </div>
    """, unsafe_allow_html=True)

    # Hook panel + bulb image, side by side (mirrors flyer's top section)
    hook_col, img_col = st.columns([1.1, 1])
    with hook_col:
        st.markdown("""
        <div class="hook">
            <strong>Most homeowners think saving energy means expensive upgrades.</strong><br><br>
            It doesn't.<br><br>
            Use the Energy Efficiency Calculator to find how simple changes can deliver
            the largest savings on your monthly electricity bill.
        </div>
        """, unsafe_allow_html=True)
    with img_col:
        # Drop a bulb photo named "bulb.png" in your repo to match the flyer.
        # Falls back silently if the file isn't there.
        try:
            st.image("ledbulb.jpg", use_container_width=True)
        except Exception:
            pass

    # Upgrade Your Home section + thermostat image, side by side
    img2_col, up_col = st.columns([1, 1.4])
    with img2_col:
        try:
            st.image("smartthermostat.jpg", use_container_width=True)
        except Exception:
            pass
    with up_col:
        st.markdown("""
        <div class="upgrade">
            <h2>Upgrade Your Home</h2>
            <p class="lead">The biggest savings usually come from:</p>
            <ul>
                <li>Replacing incandescent bulbs with LEDs</li>
                <li>Using a learning smart thermostat</li>
            </ul>
            <p class="tagline">Low cost. High impact.</p>
        </div>
        """, unsafe_allow_html=True)

    # How It Works panel (mint, numbered — like the flyer)
    st.markdown("""
    <div class="howto">
        <h3>How It Works</h3>
        <ol>
            <li>Enter your home's energy details (or use smart averages)</li>
            <li>See your total potential savings in dollars &amp; kWh</li>
            <li>Focus on the upgrades that give the most savings per dollar</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.success("👉 Head to the **Survey** tab above to get started. None of your answers are tied to you — everything is anonymous.")

# ======================================================
# TAB 2 — SURVEY (3 subtabs).  Returns nothing; renders results inline.
# All three subtabs run top-to-bottom each rerun, so values created in
# "General" and "Appliances" are available when "Results" computes.
# ======================================================
def render_survey():
    gen_tab, app_tab, res_tab = st.tabs(["🏡 General Info", "🔌 Appliances", "📈 Results"])

    # ---------- GENERAL INFO ----------
    with gen_tab:
        st.header("General Information About Your Home")
        house_area = st.number_input("Square footage of the house", min_value=0, key="house_area")
        kwh_consumption = st.number_input("Average total monthly energy consumption (kWh)",
                                          min_value=0.0, key="kwh_consumption")
        dollar_kwh_consumption = st.number_input("Average total monthly energy cost ($)",
                                                 min_value=0.0, key="dollar_kwh_consumption")
        windows_replacement = st.selectbox(
            "Windows replaced with high-efficiency ones in the last 15 years?",
            ["Yes", "No"], key="windows_replacement")
        num_conv_bulb = st.number_input("Number of conventional light bulbs", min_value=0, key="num_conv_bulb")
        num_led_bulb = st.number_input("Number of LED light bulbs", min_value=0, key="num_led_bulb")
        thermostat = st.selectbox("Do you have a learning thermostat? (Nest, Ecobee, etc.)",
                                  ["Yes", "No"], key="thermostat")
        heating = st.selectbox("Does your home use electricity for heating?", ["Yes", "No"], key="heating")
        air_conditioning = st.selectbox("Does your home use electricity for air conditioning?",
                                        ["Yes", "No"], key="air_conditioning")
        hot_water = st.selectbox("Does your home use electricity for hot water?",
                                 ["Yes", "No"], key="hot_water")

    # ---------- APPLIANCES ----------
    with app_tab:
        st.header("Energy Efficient Appliances")
        st.write("Which of the following are energy efficient (ENERGY STAR)?")
        oven_stovetop = st.selectbox("Oven/Stovetop", ["Yes", "No"], key="oven_stovetop")
        washer = st.selectbox("Washer", ["Yes", "No"], key="washer")
        dryer = st.selectbox("Dryer", ["Yes", "No"], key="dryer")
        refrigerator = st.selectbox("Refrigerator", ["Yes", "No"], key="refrigerator")

        st.divider()
        st.subheader("Details for non–ENERGY STAR appliances")
        st.caption("Only the appliances you marked 'No' appear below. Pick 'Average' to use typical values.")

        # defaults so the variables always exist
        oven_watts, oven_hours = 2350.0, 25.0
        washer_watts, washer_hours = 2000.0, 24.0
        dryer_watts, dryer_hours = 2800.0, 30.0
        refrigerator_watts, refrigerator_hours = 2000.0, 24.0

        if oven_stovetop == "No":
            m = st.selectbox("Oven/Stovetop power mode", ["Actual", "Average"], key="oven_power_mode")
            oven_watts = st.number_input("Oven/Stovetop power (watts)", min_value=0.0, key="oven_watts") if m == "Actual" else 2350.0
            u = st.selectbox("Oven/Stovetop usage mode", ["Actual", "Average"], key="oven_usage_mode")
            oven_hours = st.number_input("Oven/Stovetop usage (hours/month)", min_value=0.0, key="oven_hours") if u == "Actual" else 25.0

        if washer == "No":
            m = st.selectbox("Washer power mode", ["Actual", "Average"], key="washer_power_mode")
            washer_watts = st.number_input("Washer power (watts)", min_value=0.0, key="washer_watts") if m == "Actual" else 2000.0
            u = st.selectbox("Washer usage mode", ["Actual", "Average"], key="washer_usage_mode")
            washer_hours = st.number_input("Washer usage (hours/month)", min_value=0.0, key="washer_hours") if u == "Actual" else 24.0

        if dryer == "No":
            m = st.selectbox("Dryer power mode", ["Actual", "Average"], key="dryer_power_mode")
            dryer_watts = st.number_input("Dryer power (watts)", min_value=0.0, key="dryer_watts") if m == "Actual" else 2800.0
            u = st.selectbox("Dryer usage mode", ["Actual", "Average"], key="dryer_usage_mode")
            dryer_hours = st.number_input("Dryer usage (hours/month)", min_value=0.0, key="dryer_hours") if u == "Actual" else 30.0

        if refrigerator == "No":
            m = st.selectbox("Refrigerator power mode", ["Actual", "Average"], key="refrigerator_power_mode")
            refrigerator_watts = st.number_input("Refrigerator power (watts)", min_value=0.0, key="refrigerator_watts") if m == "Actual" else 2000.0
            u = st.selectbox("Refrigerator usage mode", ["Actual", "Average"], key="refrigerator_usage_mode")
            refrigerator_hours = st.number_input("Refrigerator usage (hours/month)", min_value=0.0, key="refrigerator_hours") if u == "Actual" else 24.0

        st.divider()
        ev = st.selectbox("Do you currently own an electric vehicle?", ["Yes", "No"], key="ev")

    # ---------- RESULTS ----------
    with res_tab:
        st.header("Your Individualized Report")
        st.write("DB connected:", get_supabase() is not None)
        if st.button("⚡ Calculate My Savings"):
            bar = st.progress(0)
            for p in (25, 60, 100):
                time.sleep(0.25); bar.progress(p)
            st.session_state.calculated = True
            st.session_state.do_save = True  # write to DB once, below

        if not st.session_state.calculated:
            st.info("Fill out the **General Info** and **Appliances** subtabs, then press the button above.")
            return

        # ----- the math (identical formulas to your original) -----
        if kwh_consumption == 0:
            st.warning("Monthly kWh consumption is 0 — some savings can't be estimated.")

        bulb_savings    = num_conv_bulb * 52 * 1.6 * 30 / 1000
        thermostat_kwh  = THERMOSTAT_SAVINGS * kwh_consumption if thermostat == "No" and kwh_consumption > 0 else 0
        windows_kwh     = WINDOWS_SAVINGS * kwh_consumption if windows_replacement == "No" and kwh_consumption > 0 else 0
        washer_kwh      = (washer_watts * washer_hours / 1000 * ENERGY_STAR_SAVINGS) if washer == "No" else 0
        dryer_kwh       = (dryer_watts * dryer_hours / 1000 * ENERGY_STAR_SAVINGS) if dryer == "No" else 0
        oven_kwh        = (oven_watts * oven_hours / 1000 * ENERGY_STAR_SAVINGS) if oven_stovetop == "No" else 0
        refrigerator_kwh = (refrigerator_watts * refrigerator_hours / 1000 * ENERGY_STAR_SAVINGS) if refrigerator == "No" else 0

        items = {
            "Bulbs": bulb_savings, "Thermostat": thermostat_kwh, "Windows": windows_kwh,
            "Washer": washer_kwh, "Dryer": dryer_kwh,
            "Oven/Stovetop": oven_kwh, "Refrigerator": refrigerator_kwh,
        }
        total_kwh_saved = sum(items.values())
        total_money_saved = total_kwh_saved * MONEY_CONVERTER

        # ----- infographic metric cards -----
        m1, m2, m3 = st.columns(3)
        m1.metric("Monthly kWh Saved", f"{total_kwh_saved:.1f}")
        m2.metric("Monthly $ Saved", f"${total_money_saved:.2f}")
        m3.metric("Yearly $ Saved", f"${total_money_saved*12:.2f}")

        if total_kwh_saved >= TESLA_KWH_PM:
            st.success("🚗 You could save enough energy monthly to charge an electric vehicle!")

        if total_kwh_saved > 0:
            filtered = {k: v for k, v in items.items() if v > 0}

            # interactive Plotly chart (on-screen)
            st.subheader("Where your savings come from")
            fig = go.Figure(go.Bar(
                x=list(filtered.keys()), y=list(filtered.values()),
                marker_color=GREEN,
                hovertemplate="%{x}<br>%{y:.1f} kWh<extra></extra>"))
            fig.update_layout(yaxis_title="Monthly kWh saved", xaxis_title="",
                              plot_bgcolor="white", height=420, margin=dict(t=20))
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("See the dollar breakdown by category"):
                for name, kwh in items.items():
                    if kwh > 0:
                        st.write(f"**{name}** — {kwh:.2f} kWh → ${kwh*MONEY_CONVERTER:.2f}/month")

            # ----- matplotlib figs for the PDF (kept from your original) -----
            fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
            ax_bar.bar(list(filtered.keys()), list(filtered.values()), color=GREEN)
            ax_bar.set_xlabel("Upgrade Category"); ax_bar.set_ylabel("Monthly Savings (kWh)")
            ax_bar.set_title("Savings Breakdown (kWh)", fontweight="bold")
            ax_bar.grid(axis="y", alpha=0.3); plt.xticks(rotation=45, ha="right"); plt.tight_layout()

            fig_scatter, ax_sc = plt.subplots(figsize=(10, 6))
            sizes = [v * MONEY_CONVERTER * 100 for v in items.values()]
            colors = plt.cm.tab10(range(len(items)))
            ax_sc.scatter(range(len(items)), list(items.values()), s=sizes, c=colors,
                          alpha=0.6, edgecolors="black", linewidth=1.5)
            ax_sc.set_xticks(range(len(items))); ax_sc.set_xticklabels(list(items.keys()), rotation=45, ha="right")
            ax_sc.set_xlabel("Category"); ax_sc.set_ylabel("kWh Saved")
            ax_sc.set_title("Size represents dollar savings", fontweight="bold")
            ax_sc.grid(alpha=0.3); plt.tight_layout()

            # ----- save to Supabase ONCE per calculate press -----
            if st.session_state.get("do_save"):
                save_response({
                    "session_id": st.session_state.session_id,
                    "house_area": int(house_area),
                    "kwh_consumption": float(kwh_consumption),
                    "dollar_cost": float(dollar_kwh_consumption),
                    "total_kwh_saved": float(total_kwh_saved),
                    "total_money_saved": float(total_money_saved),
                    "bulbs_kwh": float(bulb_savings),
                    "thermostat_kwh": float(thermostat_kwh),
                    "windows_kwh": float(windows_kwh),
                    "washer_kwh": float(washer_kwh),
                    "dryer_kwh": float(dryer_kwh),
                    "oven_kwh": float(oven_kwh),
                    "refrigerator_kwh": float(refrigerator_kwh),
                    "owns_ev": ev,
                })
                st.session_state.do_save = False

            # ----- PDF download -----
            st.divider()
            pdf_file = generate_pdf(total_kwh_saved, total_money_saved, items,
                                    MONEY_CONVERTER, TESLA_KWH_PM, fig_bar, fig_scatter)
            st.download_button("📄 Download PDF Report", data=pdf_file,
                               file_name="energy_efficiency_report.pdf", mime="application/pdf")
            plt.close(fig_bar); plt.close(fig_scatter)
        else:
            st.info("No potential savings found from your answers — your home is already efficient! 🎉")

# ======================================================
# TAB 3 — CREDITS & DISCLAIMERS
# ======================================================
def render_credits():
    st.header("Credits, Sources & Disclaimers")
    st.info("🔒 All data stored is anonymous. Your responses are never tied to your name, email, or device.")
    st.write("- ENERGY STAR appliances reduce energy use by ~30% of baseline (EPA / ENERGY STAR).")
    st.link_button("ENERGY STAR Appliance Info", "https://www.energystar.gov/products/energy_choices_count")
    st.write("- Smart learning thermostats reduce total energy use ~11% (EPA estimates).")
    st.link_button("Smart Thermostat FAQ", "https://www.energystar.gov/products/heating_cooling/smart_thermostats/smart_thermostat_faq")
    st.write("- Efficient windows can cut bills ~12% (EPA typical 7–15% range).")
    st.link_button("Windows, Doors & Skylights", "https://www.energystar.gov/products/res_windows_doors_skylights")
    st.write("- Bulb savings: ~52W per conventional bulb replaced with LED.")
    st.link_button("Lighting Efficiency Article", "https://voltaelectricinc.com/blog/energy-efficient-lighting-how-to-lower-your-electricity-bill")
    st.write("- Tesla comparison: 153.33 kWh/month ≈ 1,000 miles at ~300 Wh/mile (Model 3).")
    st.link_button("Tesla Model 3 Energy Data", "https://ev-database.org/imp/car/1322/Tesla-Model-3-Performance")
    st.caption("Created March 2023. Updated regularly. Built by Zain Ahmad.")

# ======================================================
# TAB 4 — ABOUT / VIDEO GUIDE
# ======================================================
def render_about():
    st.header("About & Video Guide")
    st.write("This free tool helps anyone find practical ways to make their home more energy efficient, "
             "using public data from the EPA and ENERGY STAR.")
    st.subheader("How to fill out each question")
    st.video("https://www.youtube.com/watch?v=AxiDexkZKR0")
    st.write("Questions or feedback? Add your contact details here.")

# ======================================================
# MAIN
# ======================================================
def main():
    inject_css()
    render_sidebar()
    home, survey, credits, about = st.tabs(
        ["🏠 Home", "📋 Survey", "📄 Credits & Disclaimers", "ℹ️ About"])
    with home:    render_home()
    with survey:  render_survey()
    with credits: render_credits()
    with about:   render_about()

main()
