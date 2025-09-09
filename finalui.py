import streamlit as st
from PIL import Image
import io
import time
import json
import os
import requests
import numpy as np
import google.generativeai as genai
import random
from fun_mcqs import fun_mcqs
import os
from dotenv import load_dotenv

st.set_page_config(
    page_title="AutoMARK AI - Professional MCQs Grading",
    page_icon="✔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Streamlit Settings*/
            
    footer {visibility: hidden;}
    /*header[data-testid="stHeader"] {background: white;}*/
    /* #MainMenu {visibility: hidden;} */    
    .st-emotion-cache-yinll1.e1hznt4w1 {visibility: hidden !important;}
    span[data-testid="stHeaderActionElements"]  {visibility: hidden !important;}    
    /* header {background-color: black;}*/            


    /* Hide Streamlit default elements */
    .main > div {
        padding-top: 0 !important;
    }
                    
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
        margin: -3rem -2rem 2rem -2rem;
        padding: 0
    }
    
    /* Animated Background */
    .hero-bg {
        position: absolute;
        top: -50%;
        width: 160%;
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
        font-size: 6rem !important; /* Increased base size */
        font-weight: 700 !important;
        margin-bottom: 1.5rem;
        padding: 5px 5px 5px 40px !important;
        background: linear-gradient(135deg, #fff 0%, rgba(168, 85, 247, 1) 50%, rgba(14, 165, 233, 1) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 3s ease-in-out infinite;
        background-size: 200% 200%;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);

    }
    .hero-slogan {
        font-size: 33px !important;
        padding-left: 35px !important;
        margin-bottom: 1rem !important;
        font-family: BlinkMacSystemFont !important;
        font-weight: 700;
        background-size: 300% auto;
        animation: luxuryWord 6s ease-in-out infinite;
    }

    /* Smooth bounce + float */
    @keyframes luxuryWord {
        0%, 100% {
            transform: scale(1) translateY(0);
            opacity: 1;
        }
        25% {
            transform: scale(1.03) translateY(-6px);
            opacity: 0.95;
        }
        50% {
            transform: scale(0.98) translateY(4px);
            opacity: 0.9;
        }
        75% {
            transform: scale(1.02) translateY(-3px);
            opacity: 1;
        }
    }

    .hero-subtitle {
        font-size: 15px !important;
        color: #E0E0E0;
        opacity: 0.8;
        margin-bottom: 2rem;
        margin-top: 0rem !important;
        line-height: 1.6;
    }
            
    .cta-button {
        display: inline-block;
        padding: 1rem 2.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        color: white !important;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(168, 85, 247, 0.8));
        border: none;
        border-radius: 50px;
        cursor: pointer;
        z-index: 99999;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        text-decoration: none !important;
    }

    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(168, 85, 247, 0.4);
    }

    .cta-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }

    .cta-button:hover::before {
        left: 100%;
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
            
    @media (max-width: 1200px) {
        .hero-title {
            font-size: 5rem !important;
        }
    }
            
    @media (max-width: 768px) {
            
        .hero-content {
            padding: 2rem 0.1rem;

        }
        .hero-container {
            padding: 1rem;
            min-height: 50vh;
            max-width: 95vw;
            margin-right: 1.5vw;
            margin-left: 1.5vw;
        }
        .hero-title {
            font-size: 2.5rem !important;
            padding-left: 25px !important;
        }
        .hero-slogan{
            font-size: 12px !important;
            font-weight: 400 !important;
            padding-left: 25px !important;
            font-family: BlinkMacSystemFont !important;
            background-size: 300% auto;
            animation: luxuryWordmb 6s ease-in-out infinite !important;
        }
        
        @keyframes luxuryWordmb {
            0%, 100% {
                transform: scale(1.17) translateY(0);
                opacity: 1;
            }
            25% {
                transform: scale(1.20) translateY(-2px);
                opacity: 0.95;
            }
            50% {
                transform: scale(1.16) translateY(1px);
                opacity: 0.9;
            }
            75% {
                transform: scale(1.19) translateY(-0.5px);
                opacity: 1;
            }
        }

        .hero-bg {
            position: absolute;
            top: -30%;
            width: 110%;
            height: 150%;
        }
        .hero-subtitle{
            font-family: 'Inter', sans-serif !important;    
            font-size: 12px !important;
            margin-bottom: 1.5rem;
        }
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
            <h2 class="hero-slogan"> Revolutionize Your Assessment Process ✨</h2>
            <p class="hero-subtitle">Transform your grading process with cutting-edge AI technology. Fast, Accurate and Reliable Automated MCQs evaluation.</p>
            <a href="#" class="cta-button">AI Powered</a>
        </div>
    </div>
    """, unsafe_allow_html=True)




if __name__ == "__main__":
    main()
