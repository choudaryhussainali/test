import streamlit as st

st.set_page_config(
    page_title="AutoMARK AI - Professional MCQs Grading",
    page_icon="✔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Hide Streamlit default elements */
    .main > div {
        padding-top: 0 !important;
    }
    header[data-testid="stHeader"] {
        background: white;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background-color: black;}
    /* Global Styles */
    .main {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Hero Container */
    .hero-container {
        position: relative;
        min-height: 80vh;
        background: #0a0a0a;
        overflow: hidden;
        display: flex;
        top: 0;
        align-items: center;
        justify-content: center;
        border-radius: 60px !important;
        margin: -2.5rem -2rem 2rem -2rem;
        padding: 0
    }
    
    /* Animated Background */
    .hero-bg {
        position: absolute;
        top: -50%;
        width: 150%;
        height: 150%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(14, 165, 233, 0.4) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(99, 102, 241, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(236, 72, 153, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 70% 60%, rgba(168, 85, 247, 0.3) 0%, transparent 50%);
        animation: gradientShift 20s ease-in-out infinite;
    }
    @keyframes gradientShift {
        0%, 100% {
            transform: rotate(0deg) scale(1);
        }
        25% {
            transform: rotate(90deg) scale(1.1);
        }
        50% {
            transform: rotate(180deg) scale(1);
        }
        75% {
            transform: rotate(270deg) scale(1.1);
        }
    }

    .hero-content {
        position: relative;
        z-index: 10;
        text-align: center;
        max-width: 1200px;
        padding: 2rem;
        color: white;
    }

    .hero-title {
        font-size: clamp(2.5rem, 8vw, 5rem);
        font-weight: 700;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #fff 0%, rgba(168, 85, 247, 1) 50%, rgba(14, 165, 233, 1) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 3s ease-in-out infinite;
        background-size: 200% 200%;
    }

    .hero-subtitle {
        font-size: clamp(0.5rem, 3vw, 1rem);
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 2rem;
        margin-top: 2rem;
        line-height: 1.6;
    }

    @keyframes shimmer {
        0%, 100% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
    }



    /* Mobile Responsive */
    @media (max-width: 768px) {
        .hero-container {
            padding: 1rem;
            min-height: 70vh;
            max-width: 95vw;
            margin-right: 1.5vw;
            margin-left: 1.5vw;
        }
    
    @media (max-width: 480px) {
        .stats-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Sidebar Compatibility */

    
    /* Scrolldown Indicator */
    .scroll-indicator {
        position: absolute;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        animation: bounce 2s infinite;
    }
    
    .scroll-arrow {
        width: 30px;
        height: 30px;
        border: 2px solid rgba(255, 255, 255, 0.5);
        border-top: none;
        border-right: none;
        transform: rotate(-45deg);
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateX(-50%) translateY(0); }
        40% { transform: translateX(-50%) translateY(-10px); }
        60% { transform: translateX(-50%) translateY(-5px); }
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application with professional hero section"""
    
    st.sidebar.title("🚀 AutoMARK AI")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Navigation**")
    
    # Professional Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-bg"></div>
        <div class="hero-content">
            <h1 class="hero-title">AutoMARK</h1>
            <h2 style = "font-size: clamp(1rem, 3vw, 1.5rem); margin-bottom: 2rem;">| Revolutionize Your Assessment Process |</h2>
        </div>
    """, unsafe_allow_html=True)




if __name__ == "__main__":
    main()
