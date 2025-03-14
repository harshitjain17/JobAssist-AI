import streamlit as st

def inject_custom_css():
    st.markdown(
        """
        <style>

        # Hide Streamlit's default header, footer, and sidebar toggle
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        # remove default sidebar 
        stSidebarNavItems { display: none; }
        [data-testid="stSidebarNavItems"] {
            display: none;
        }
        
        # Fixed header
        .fixed-header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #ffffff;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            padding: 10px 15px;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .header-title {
            font-size: 22px;
            text-align: center;
        }

        # Content Padding 
        .content {
            padding-top: 100px;  /* Make room for header */
            margin-left: 250px;   /* Space for sidebar */
            padding-bottom: 40px;
        }

        # Fixed footer
        .fixed-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f1f1f1;
            padding: 5px 0;
            text-align: center;
            font-size: 12px;
            color: gray;
            z-index: 1000;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

def render_header():
    st.markdown(
        """
        <div class="fixed-header">
            <h2 class="header-title">Job Assist AI</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Add content to the sidebar
    with st.sidebar:
        st.page_link("app.py", label="Home")
        st.page_link("pages/1_Document Processor.py", label="Document Processor")
        st.page_link("pages/2_task_breakdown.py", label="Task Breakdown")
        st.page_link("pages/3_knowledge_retention.py", label="Knowledge Retention")
        st.page_link("pages/4_caseload_tracking.py", label="Caseload Tracking")

def render_footer():
    st.markdown(
        """
        <hr>
        <div class="fixed-footer">
            Powered by Azure | JobAssistAI &copy; 2025. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True
    )

def with_layout(content_func):
    inject_custom_css()  # Inject CSS for fixed positioning
    render_header()      # Render header
    st.markdown('<div class="content">', unsafe_allow_html=True)  # Start content div
    content_func()       # Call page-specific content
    st.markdown('</div>', unsafe_allow_html=True)  # End content div
    render_footer()      # Render footer