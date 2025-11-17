def show_landing_page():
    """Display the landing page for region selection"""
    
    # Apply the landing page CSS
    st.markdown(HUB_CSS, unsafe_allow_html=True)
    
    # Hide Streamlit's default elements
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
    
    # Render the header and gradient background
    st.markdown("""
    <div class="landing-container">
        <div class="mesh-gradient"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Title and subtitle using Streamlit native components
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem; position: relative; z-index: 10;">
        <h1 style="font-size: 3.5rem; font-weight: 200; color: #ffffff; margin-bottom: 1rem;">
            Workforce <strong style="font-weight: 600; background: linear-gradient(135deg, #c8d9e5 0%, #567c8d 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Analytics</strong>
        </h1>
        <p style="font-size: 1.2rem; color: #8b9db3; margin-bottom: 0.5rem;">
            Comprehensive labor cost insights and workforce metrics
        </p>
        <p style="font-size: 0.95rem; color: #6b7d93;">
            Select your region to access the dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for the region cards
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        with st.container():
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <svg width="70" height="70" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="8" y="12" width="48" height="8" rx="2" fill="#567c8d" opacity="0.8"/>
                    <rect x="8" y="22" width="48" height="8" rx="2" fill="#567c8d" opacity="0.6"/>
                    <rect x="8" y="32" width="48" height="8" rx="2" fill="#567c8d" opacity="0.4"/>
                    <rect x="8" y="42" width="48" height="8" rx="2" fill="#567c8d" opacity="0.3"/>
                    <circle cx="52" cy="16" r="3" fill="#c8d9e5"/>
                    <circle cx="52" cy="26" r="3" fill="#c8d9e5"/>
                    <circle cx="52" cy="36" r="3" fill="#c8d9e5"/>
                </svg>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<h3 style='color: #ffffff; font-size: 2rem; margin-bottom: 1rem;'>United States</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #8b9db3; margin-bottom: 1.5rem;'>US labor cost analysis with compensation and productivity metrics</p>", unsafe_allow_html=True)
            st.markdown("""
            <ul style='color: #6b7d93; list-style: none; padding-left: 0;'>
                <li style='margin-bottom: 0.5rem;'>▹ US compensation benchmarks</li>
                <li style='margin-bottom: 0.5rem;'>▹ State-level cost analysis</li>
                <li style='margin-bottom: 0.5rem;'>▹ Overtime tracking</li>
            </ul>
            """, unsafe_allow_html=True)
            
            if st.button("View US Dashboard →", key="us_btn", use_container_width=True, type="primary"):
                st.session_state.page = 'dashboard'
                st.session_state.region = 'US'
                st.rerun()
    
    with col2:
        with st.container():
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <svg width="70" height="70" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="8" y="8" width="48" height="48" rx="4" stroke="#567c8d" stroke-width="2" fill="none" opacity="0.3"/>
                    <path d="M16 40 L24 32 L32 36 L48 20" stroke="#c8d9e5" stroke-width="2.5" stroke-linecap="round"/>
                    <circle cx="16" cy="40" r="2.5" fill="#567c8d"/>
                    <circle cx="24" cy="32" r="2.5" fill="#567c8d"/>
                    <circle cx="32" cy="36" r="2.5" fill="#567c8d"/>
                    <circle cx="48" cy="20" r="2.5" fill="#567c8d"/>
                </svg>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<h3 style='color: #ffffff; font-size: 2rem; margin-bottom: 1rem;'>European Union</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #8b9db3; margin-bottom: 1.5rem;'>EU labor cost analysis with multi-country comparisons</p>", unsafe_allow_html=True)
            st.markdown("""
            <ul style='color: #6b7d93; list-style: none; padding-left: 0;'>
                <li style='margin-bottom: 0.5rem;'>▹ EU compensation standards</li>
                <li style='margin-bottom: 0.5rem;'>▹ Multi-country analysis</li>
                <li style='margin-bottom: 0.5rem;'>▹ Regional workforce metrics</li>
            </ul>
            """, unsafe_allow_html=True)
            
            if st.button("View EU Dashboard →", key="eu_btn", use_container_width=True, type="primary"):
                st.session_state.page = 'dashboard'
                st.session_state.region = 'EU'
                st.rerun()
