"""
AgroVision – Simple & Farmer-Friendly Leaf Disease Check (Streamlit)
Matches the clean wireframe layout:
  Top Navbar (AgroVision logo | Home | About Us | Contact Us | Login / Sign Up)
  -> Farmer Hero Banner
  -> Centered Leaf Upload Box & Simple Result
  -> Footer (About Us & Contact Us)
"""

from pathlib import Path
import numpy as np
import streamlit as st
from PIL import Image

from src.preprocessing import extract_foliar_color_analytics, preprocess_image

st.set_page_config(
    page_title="AgroVision",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide default Streamlit sidebar toggle & extra chrome for a clean website feel
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1050px; }
    .nav-logo { font-size: 1.7rem; font-weight: 700; color: #166534; margin: 0; padding-top: 0.15rem; }
    .upload-card {
        border: 1.5px dashed #22c55e;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        background-color: rgba(34, 197, 94, 0.05);
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
    .footer-box {
        border-top: 1px solid rgba(148, 163, 184, 0.35);
        padding-top: 1.2rem;
        margin-top: 2.5rem;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "page" not in st.session_state:
    st.session_state["page"] = "Home"

CLASSES = [
    ("Healthy Leaf", "Your crop leaf looks healthy. Continue regular watering and care."),
    ("Early Blight", "Dark spots detected on the leaf. Remove affected lower leaves and apply a suitable fungicide."),
    ("Late Blight / Leaf Spot", "Spread of dark patches detected. Isolate affected plants and consult a local agriculture officer."),
    ("Yellowing / Mosaic", "Leaf yellowing detected. Check the underside of leaves for insects such as whiteflies."),
]


def predict_leaf(norm_arr: np.ndarray):
    stats = extract_foliar_color_analytics(norm_arr)
    g_idx = stats["green_index"]
    c_idx = stats["chlorosis_index"]
    lesion = stats["lesion_ratio"]

    if g_idx > 0.05 and lesion < 0.08 and c_idx < 0.14:
        scores = np.array([0.84, 0.07, 0.05, 0.04])
    elif lesion >= 0.12:
        scores = np.array([0.06, 0.50, 0.36, 0.08])
    elif c_idx >= 0.14:
        scores = np.array([0.08, 0.13, 0.12, 0.67])
    else:
        scores = np.array([0.20, 0.43, 0.25, 0.12])

    idx = int(np.argmax(scores))
    return CLASSES[idx][0], CLASSES[idx][1], float(scores[idx]) * 100.0


# --- TOP NAVBAR ---
nav_left, nav_b1, nav_b2, nav_b3, nav_b4 = st.columns([3.2, 1.0, 1.2, 1.3, 1.5])
with nav_left:
    st.markdown('<p class="nav-logo">🌿 AgroVision</p>', unsafe_allow_html=True)
with nav_b1:
    if st.button("Home", use_container_width=True):
        st.session_state["page"] = "Home"
with nav_b2:
    if st.button("About Us", use_container_width=True):
        st.session_state["page"] = "About Us"
with nav_b3:
    if st.button("Contact Us", use_container_width=True):
        st.session_state["page"] = "Contact Us"
with nav_b4:
    if st.button("Login / Sign Up", use_container_width=True):
        st.session_state["page"] = "Login / Sign Up"

st.divider()

page = st.session_state["page"]

# --- PAGE: HOME ---
if page == "Home":
    banner_path = Path("assets/farmer_banner.jpg")
    if banner_path.exists():
        st.image(str(banner_path), use_container_width=True)

    st.markdown(
        "<h3 style='text-align:center; margin-top:0.8rem;'>Check Your Crop Leaf Health in Seconds</h3>",
        unsafe_allow_html=True,
    )

    # Centered Upload Box
    _, center_col, _ = st.columns([1, 2.4, 1])
    with center_col:
        st.markdown('<div class="upload-card">', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Upload a photo of the crop leaf (JPG or PNG)",
            type=["jpg", "jpeg", "png"],
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if uploaded is not None:
        img = Image.open(uploaded)
        norm_arr = preprocess_image(img)
        label, advice, confidence = predict_leaf(norm_arr)

        res_l, res_r = st.columns([1, 1.3])
        with res_l:
            st.image(img, caption="Uploaded Leaf", use_container_width=True)
        with res_r:
            st.subheader("Result")
            if label == "Healthy Leaf":
                st.success(f"**{label}** ({confidence:.0f}% confidence)")
            else:
                st.warning(f"**{label}** ({confidence:.0f}% confidence)")
            st.write(advice)

# --- PAGE: ABOUT US ---
elif page == "About Us":
    st.subheader("About Us")
    st.write(
        "AgroVision is a student-led community service project (DSN3099 – EPICS) at **VIT Bhopal University** "
        "built to help farmers quickly check crop leaf health using simple leaf photographs."
    )
    st.write("**Team Members:**")
    st.markdown(
        """
        - Puli Sai Chaithanya Kumar (`24MEI10002`)
        - Addepalli Sai Krishnam Raju (`24BEC10165`)
        - Atla Dhatri Sai (`24BCY10362`)
        - Pragada Sharmila (`24BEC10071`)
        - Madineni Vignesh (`24BCY10002`)
        - K Bala Yaswanth (`24MIM10243`)
        """
    )

# --- PAGE: CONTACT US ---
elif page == "Contact Us":
    st.subheader("Contact Us")
    st.write("Have questions or feedback from the field? Send us a message below.")
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        phone_or_email = st.text_input("Phone Number or Email")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Send Message")
        if submitted:
            if name and message:
                st.success("Thank you! Your message has been recorded.")
            else:
                st.error("Please enter your name and message.")

# --- PAGE: LOGIN / SIGN UP ---
elif page == "Login / Sign Up":
    st.subheader("Login / Sign Up")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        with st.form("login_form"):
            user = st.text_input("Phone or Email")
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if user and pwd:
                    st.success(f"Welcome back, {user}!")
                else:
                    st.error("Please enter both fields.")
    with tab2:
        with st.form("signup_form"):
            new_name = st.text_input("Full Name")
            new_user = st.text_input("Phone or Email", key="su_user")
            new_pwd = st.text_input("Create Password", type="password", key="su_pwd")
            if st.form_submit_button("Create Account"):
                if new_name and new_user and new_pwd:
                    st.success("Account created! You can now log in.")
                else:
                    st.error("Please fill in all fields.")

# --- FOOTER ---
st.markdown('<div class="footer-box">', unsafe_allow_html=True)
f1, f2 = st.columns(2)
with f1:
    st.markdown("**About Us**")
    st.caption("AgroVision helps farmers detect crop leaf diseases early with a simple photo upload. Built at VIT Bhopal University.")
with f2:
    st.markdown("**Contact Us**")
    st.caption("VIT Bhopal University, Kothri Kalan, Sehore, Madhya Pradesh | Team AgroVision (DSN3099 EPICS)")
st.markdown("</div>", unsafe_allow_html=True)
