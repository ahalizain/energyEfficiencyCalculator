import streamlit as st

# This file is the OLD Streamlit deployment's entry point.
# Keep your full calculator running separately on Railway.
APP_URL = "https://energyefficiencyforall.up.railway.app"

st.set_page_config(
    page_title="We've Moved | Energy Efficiency for All",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --cream: #FBF0DD;
        --mint: #C9E8D2;
        --teal: #2F8E8E;
        --blue: #3A6FD8;
        --ink: #2b2b2b;
    }

    .stApp {
        background: var(--cream);
        color: var(--ink);
        font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        max-width: 900px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    .eyebrow {
        display: inline-block;
        background: var(--mint);
        color: var(--teal);
        border-radius: 999px;
        padding: .45rem .9rem;
        font: 800 .82rem 'Inter', sans-serif;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: 1.15rem;
    }

    .hero {
        text-align: center;
        padding: 2.4rem 1.8rem 1.7rem;
        background: rgba(255,255,255,.58);
        border: 1px solid #eadfc9;
        border-radius: 26px;
        box-shadow: 0 12px 34px rgba(43,43,43,.06);
    }

    .bolt {
        font-size: 3rem;
        line-height: 1;
        margin-bottom: .8rem;
    }

    .hero h1 {
        color: var(--teal);
        font: 900 clamp(2.15rem, 6vw, 3.7rem)/1.04 'Montserrat', sans-serif;
        letter-spacing: -.055em;
        margin: 0 0 .9rem;
    }

    .hero p {
        color: var(--blue);
        font: 700 clamp(1.05rem, 2.5vw, 1.35rem)/1.5 'Inter', sans-serif;
        max-width: 620px;
        margin: 0 auto;
    }

    .notice {
        margin: 1.25rem 0;
        padding: 1.45rem 1.6rem;
        background: var(--mint);
        border-radius: 20px;
        color: var(--blue);
        font: 600 1.03rem/1.65 'Inter', sans-serif;
        text-align: center;
    }

    .notice strong {
        color: var(--teal);
        font-weight: 800;
    }

    .features {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: .9rem;
        margin: 1.1rem 0 1.25rem;
    }

    .feature {
        background: #fff;
        border: 1px solid #e7ddc8;
        border-radius: 17px;
        padding: 1.15rem .9rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,.045);
    }

    .feature .icon {
        font-size: 1.8rem;
        margin-bottom: .35rem;
    }

    .feature h3 {
        color: var(--teal);
        font: 800 1rem 'Montserrat', sans-serif;
        margin: .2rem 0 .35rem;
    }

    .feature p {
        color: #555;
        font: 500 .88rem/1.45 'Inter', sans-serif;
        margin: 0;
    }

    .destination {
        text-align: center;
        color: var(--ink);
        font: 600 .9rem 'Inter', sans-serif;
        margin: .6rem 0 .2rem;
    }

    .url {
        color: var(--teal);
        font-weight: 800;
        overflow-wrap: anywhere;
    }

    .footer-note {
        text-align: center;
        color: #6b665d;
        font: 500 .82rem/1.5 'Inter', sans-serif;
        margin-top: 1.6rem;
    }

    @media (max-width: 640px) {
        .features { grid-template-columns: 1fr; }
        .hero { padding: 2rem 1.1rem 1.5rem; }
        .notice { padding: 1.2rem; }
    }

    div.stButton > button, div.stLinkButton > a {
        background: var(--teal) !important;
        color: #fff !important;
        border: 0 !important;
        border-radius: 12px !important;
        padding: .85rem 1.3rem !important;
        font: 800 1.05rem 'Inter', sans-serif !important;
        min-height: 3.25rem;
        box-shadow: 0 7px 16px rgba(47,142,142,.2);
        transition: transform .15s ease, background .15s ease;
    }

    div.stLinkButton > a:hover {
        background: #256f6f !important;
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">A quick update</div>
        <div class="bolt">⚡</div>
        <h1>We've moved!</h1>
        <p>Energy Efficiency for All has a new home — with the same mission
        to help you save energy, lower your bills, and make smarter upgrades.</p>
    </section>

    <section class="notice">
        <strong>You're in the right place.</strong><br>
        We've upgraded our hosting so the calculator is easier to access.
        Your energy-saving journey can continue at our new address.
    </section>

    <section class="features">
        <div class="feature">
            <div class="icon">🏡</div>
            <h3>Know your home</h3>
            <p>Enter your household energy details.</p>
        </div>
        <div class="feature">
            <div class="icon">📊</div>
            <h3>Find your savings</h3>
            <p>Explore potential monthly energy and cost savings.</p>
        </div>
        <div class="feature">
            <div class="icon">🌱</div>
            <h3>Make an impact</h3>
            <p>Discover practical ways to use less energy.</p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.link_button(
    "⚡  Open the Energy Efficiency Calculator",
    APP_URL,
    type="primary",
    use_container_width=True,
)

st.markdown(
    f"""
    <div class="destination">
        New address: <span class="url">{APP_URL}</span>
    </div>
    <div class="footer-note">
        Thanks for visiting Energy Efficiency for All.<br>
        Created by Zain Ali Ahmad.
    </div>
    """,
    unsafe_allow_html=True,
)
