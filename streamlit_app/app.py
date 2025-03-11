import streamlit as st

# Set page config for a modern, immersive experience
st.set_page_config(
    page_title="JobAssist AI",
    layout="wide",
    initial_sidebar_state="collapsed",  # Sidebar hidden by default
    page_icon="🤖"
)

# Custom CSS for a polished, modern look
st.markdown("""
    <style>
    /* Full-page gradient background */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #ffffff;
    }
    /* Header styling */
    .header-text {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        margin-top: 2rem;
        animation: fadeIn 2s ease-in;
    }
    /* Subheader styling */
    .tagline {
        font-size: 1.5rem;
        text-align: center;
        color: #d1e8ff;
        margin-bottom: 3rem;
    }
    /* Feature card styling */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        transition: transform 0.3s ease, background 0.3s ease;
    }
    .feature-card:hover {
        transform: scale(1.05);
        background: rgba(255, 255, 255, 0.2);
    }
    .feature-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ffffff;
    }
    .feature-desc {
        font-size: 1rem;
        color: #d1e8ff;
    }
    /* Sidebar toggle button */
    .sidebar-toggle {
        position: fixed;
        top: 20px;
        left: 20px;
        background: #ffffff;
        color: #1e3c72;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
        z-index: 1000;
    }
    /* Animation */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar toggle button
if st.button("☰ Explore Tools", key="sidebar_toggle", help="Click to reveal tools"):
    st.session_state.sidebar_visible = not st.session_state.get("sidebar_visible", False)

# Sidebar (hidden by default, toggled via button)
if st.session_state.get("sidebar_visible", False):
    with st.sidebar:
        st.header("JobAssist Tools")
        st.write("Powered by Azure:")
        st.markdown("- [Administrative Overload](#)")
        st.markdown("- [Task Breakdown](#)")
        st.markdown("- [Knowledge Retention](#)")
        st.markdown("- [Caseload Tracking](#)")
        st.write("Select a tool from the pages to get started.")

# Main content
st.markdown('<div class="header-text">JobAssist AI</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Your Azure-Powered Companion for Supported Employment</div>', unsafe_allow_html=True)

# Interactive feature showcase
st.subheader("Empower Job Coaches with AI")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📝 Administrative Overload</div>
            <div class="feature-desc">Automate paperwork with Azure AI Language & Document Intelligence.</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📋 Task Breakdown</div>
            <div class="feature-desc">Generate personalized instructions using Azure AI.</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🧠 Knowledge Retention</div>
            <div class="feature-desc">Access a shared knowledge base via Azure Cosmos DB.</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📊 Caseload Tracking</div>
            <div class="feature-desc">Monitor progress with Azure Machine Learning insights.</div>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; font-size: 0.9rem; color: #d1e8ff;">
        Built entirely on Azure for seamless integration and scalability. <br>
        Click the top-left button to explore tools and unleash the power of AI!
    </div>
""", unsafe_allow_html=True)

# Session state initialization (for sidebar toggle persistence)
if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = False