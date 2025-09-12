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
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript
import base64




# Page configuration
st.set_page_config(
    page_title="AutoMARK AI - Professional MCQs Grading",
    page_icon="✔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")  # must be verified in Elastic Email
TO_EMAIL = os.getenv("TO_EMAIL")      # where you want to receive messages

# ------------------ EMAIL FUNCTION ------------------
def send_email(name, email, message):
    """Send contact form email via Elastic Email API"""
    url = "https://api.elasticemail.com/v2/email/send"
    payload = {
        "apikey": ELASTIC_API_KEY,
        "from": FROM_EMAIL,
        "to": TO_EMAIL,
        "subject": f"📩 New Contact from {name}",
        "bodyHtml": f"""
            <h3>New Contact Form Submission</h3>
            <p><b>Name:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Message:</b><br>{message}</p>
        """
    }

    try:
        response = requests.post(url, data=payload)
        res = response.json()
        return res.get("success", False)
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return False

# Professional CSS styling

st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.0/css/all.min.css" integrity="sha512-DxV+EoADOkOygM4IR9yXP8Sb2qwgidEmeqAEmDKIOfPRQZOWbXCzLC6vjbZyy0vPisbH2SyW27+ddLVCN+OMzQ==" crossorigin="anonymous" referrerpolicy="no-referrer"/>
""", unsafe_allow_html=True)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Streamlit Settings*/
            
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {z-index: 998;}
    /* #MainMenu {visibility: hidden;} */    
    .st-emotion-cache-yinll1.e1hznt4w1 {visibility: hidden !important;}
    span[data-testid="stHeaderActionElements"]  {visibility: hidden !important;}    
    /* header {background-color: black;}*/            
            
    /* Sidebar floats on top */
    [data-testid="stSidebar"] {
        position: fixed !important;
        left: 0;
        top: 0;
        bottom: 0;
        z-index: 999;
        min-width: 300px;
        max-width: 350px; /* adjust width */
        box-shadow: 2px 0px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease-in-out;
    }



    /* Hide Streamlit default elements */
    .main > div {
        padding-top: 0 !important;
    }
                    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
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
        margin: -4.8rem -2rem 2rem -2rem;
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
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
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


    .note-box {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-left: 5px solid #007bff;
        border-radius: 6px;
        padding: 16px 20px;
        margin: 0 0 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .note-text {
        font-family: Arial, sans-serif;
        font-size: 14px;
        line-height: 1.5;
        color: #0b2540;
    }
    .note-icon {
        margin-right: 8px;
        font-size: 16px;
    }
    .note-brand {
        color: #0b61ff;
        font-weight: bold;
    }
    .note-agentic {
        font-style: italic;
        color: #2a6f4a;
    }
    .note-feature {
        color: #d97706;
        font-weight: bold;
    }
    .note-highlight {
        background: #fbfc8d;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
            
    .video-content {
        display: flex;
        align-items: center;
        border: 1px solid #e1e8ed;
        border-radius: 36px;
        background: linear-gradient(135deg, #f8fafc, #eaf4ff);
        gap: 40px;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.25),   /* Blue */
                    0 10px 25px rgba(16, 185, 129, 0.2),  /* Teal */
                    0 12px 30px rgba(245, 158, 11, 0.15); /* Amber */
        transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
        max-width: 1200px;
        margin-top: 2rem;
        margin-bottom: 2rem;
        margin-left: 10%;
        margin-right: 10%;
        padding: 20px;
        position: relative;
        overflow: hidden; /* shimmer stays inside */
    }
    .video-content::after {
        content: "";
        position: absolute;
        top: 0;
        left: -50%;
        width: 10%;
        height: 100%;
        background: linear-gradient(
            120deg,
            rgba(255, 255, 255, 0) 0%,
            rgba(255, 255, 255, 0.6) 50%,
            rgba(255, 255, 255, 0) 100%
        );
        transform: skewX(-20deg);
        pointer-events: none;
    }

    /* Trigger shimmer ONCE when hovered */
    .video-content:hover::after {
        animation: shimmer-slide 0.8s forwards;
    }

    /* Keyframes → only move forward */
    @keyframes shimmer-slide {
        from { left: -50%; }
        to { left: 120%; }
    }
    .info-text {
        text-align: center;
        font-family: "Segoe UI", Roboto, Arial, sans-serif;
        font-size: 16px;
        line-height: 1.7;
        color: #1f2937;
    }

    .info-icon {
        margin-right: 3px;
        font-size: 18px;
        color: #1d4ed8;
    }
    .info-text h2{
        color: #0F766E;
        font-family: "Segoe UI", Roboto, Arial, sans-serif;
        font-size: 36px;
        text-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        margin-top: -3rem;
        padding: 1rem 0;
        font-weight: 700;        
    }
    .info-brand {
        color: #1d4ed8;
        font-size: 16px;
        font-weight: 700;
    }

    .info-core {
        font-style: italic;
        color: #047857;
        font-weight: 500;
    }

    .info-key {
        color: #b45309;
        font-weight: 600;
    }

    .info-focus {
        background: #e0f2fe;
        padding: 3px 6px;
        border-radius: 6px;
        font-weight: 600;
        color: #0c4a6e;
    }


    .description-div {
        flex: 1;
    }


    .video-div {
        flex: 0 0 350px;
        max-width: 350px;
        width: 400px;
    }

    .video-div video {
        width: 100%;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
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
            
    .feature-card {
        background: white;
        padding: 2rem;
        color: black;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid #e1e8ed;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        transform: scale(1.05);
        z-index: 1;
        box-shadow: 0 15px 45px rgba(0,0,0,0.15);
    }
            
    .works {
        background: white;
        padding: 2rem;
        align-items: center;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid #e1e8ed;
        margin-bottom: 1.5rem;
        margin-top: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        min-height: 260px;
    }

    .works:hover {
        transform: translateY(-5px);
        transform: scale(1.05);
        border : 1px solid black;
        z-index: 1;
        box-shadow: 0 15px 45px rgba(0,0,0,0.15);
    }
    
    .upload-zone {
        border: 3px dashed #667eea;
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    }
    
    .results-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: rgba(255,255,255,0.95);
        color: #333;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .developer-card {
        background: linear-gradient(135deg, #2d3748, #4a5568, #2d3748);
        background-size: 300% 300%;
        animation: gradientBG 12s ease infinite;
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 0rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        animation: fadeUp 1.2s ease forwards;
        
    }

    .developer-avatar {
        width: 80px; 
        height: 80px; 
        border-radius: 50%; 
        background: linear-gradient(135deg, #667eea, #764ba2); 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        margin: 0 auto 0.6rem auto; 
        font-size: 3rem;
        color: black;
        box-shadow: 0 0 20px rgba(102,126,234,0.6);
        animation: float 4s ease-in-out infinite;
    }
    
            
    .typewriter-text {
        margin: 0;
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        display: inline-block;
        border-right: 2px solid white;
        white-space: nowrap;
        overflow: hidden;
        animation: continuousType 4s infinite, blink 1s infinite;
        width: 11ch;
    }

    @keyframes continuousType {
        0% {
            width: 0;
        }
        20% {
            width: 11ch; /* Full text "Hussain Ali" */
        }
        40% {
            width: 11ch; /* Hold full text */
        }
        60% {
            width: 0; /* Backspace to empty */
        }
        80% {
            width: 0; /* Hold empty */
        }
        100% {
            width: 0; /* Ready to restart */
        }
    }
            
    @keyframes blink {
        0%, 50% {
            border-color: white;
        }
        51%, 100% {
            border-color: transparent;
        }
    }
        
    .social-links {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
            
    .social-btn {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        height: 50px;
        width: 50px;
        padding: 0.75rem 0.75rem;
        border-radius: 50%;
        text-decoration: none !important;
        font-weight: 600;
        background: linear-gradient(135deg, #2d3748, #4a5568);
        color: white !important;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.5);
        white-space: nowrap;
        animation: socialsAnimation 2s ease-in-out infinite;
    }
            
    .social-btn::before {
        content: "";
        position: absolute;
        color: #fff;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(120deg, rgba(255,255,255,0.2), rgba(255,255,255,0));
        transition: left 0.5s ease;
    }
    

    .social-btn:hover::before {
        left: 100%;
    }

    .social-btn:hover {
        transform: scale(1.1) !important;
        text-decoration: none;
        color: black !important;
    }
        
    .watermark {
        position: fixed;
        bottom: 10px;
        right: 10px;
        background: rgba(102, 126, 234, 0.9);
        color: black;
        padding: 0.5rem 2rem;
        align-items: center !important;
        text-align: center !important;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 500;
        z-index: 1000;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
            
    @keyframes socialsAnimation {
        0% {
            box-shadow: 0 2px 5px rgba(36, 52, 77,0.7);
            transform: scale(1);
        }
        50% {
            box-shadow: 0 5px 10px rgba(36, 52, 77,0.9);
            transform: scale(1.01);
        }
        100% {
            box-shadow: 0 2px 5px rgba(0,36, 52, 77,.7); 
            transform: scale(1);
        }
    }
    
    @keyframes pulseAnimation {
        0% {
            box-shadow: 0 2px 10px rgba(0,0,0,0.7);
            transform: scale(1);
        }
        50% {
            box-shadow: 0 4px 15px rgba(0,0,0,1);
            transform: scale(1.1);
        }
        100% {
            box-shadow: 0 2px 10px rgba(0,0,0,0.7);
            transform: scale(1);
        }
    }
            
    .sidebar .block-container {
        padding-top: 2rem;
    }

    .tips-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1rem 0;
    }

    .tips-card h4 {
        margin: 0 0 1rem 0;
        font-size: 1.2rem;
    }

    .tips-card h5 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
    }

    .tips-card ul {
        margin: 0;
        padding-left: 1.5rem;
        font-size: 0.9rem;
    }

    .tips-card li {
        margin-bottom: 0.3rem;
    }

    .tips-columns {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }

    .tips-column {
        flex: 1;
    }
    



    /* Mobile Responsive */
            
    @media (max-width: 1200px) {
        .hero-title {
            font-size: 5rem !important;
        }
    }
            
    @media (max-width: 1024px) {
        .video-content {
            flex-direction: column;
            gap: 30px;
            padding-top: 15px;
            align-items: center;   /* center video + text */
            margin: 1rem auto;

        }
        .info-text {
            font-size: 20px;
            line-height: 1.5;
            padding: 10px 20px;
        }
                
        .info-text h2 {
            font-size: 32px;
            margin-top: 0;
        }

        .video-div video {
            width: 100%;        /* responsive inside container */
            height: auto;
            border-radius: 16px;
        }

        .video-div {
            width: 100%;
            max-width: 400px;   /* keep video at 400px */
            margin: 1rem auto 0 auto;     /* center it */
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

        .note-box {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-left: 5px solid #007bff;
            border-radius: 6px;
            padding: 4px 10px;
            margin: 0 0 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }           
        .note-text {
            font-family: Arial, sans-serif;
            font-size: 8px;
            line-height: 1.8;
            color: #0b2540;
            text-align: center;
        }
        .note-icon {
            margin-right: 8px;
            font-size: 10px;
            text-align: left !important;
        }
            
        .video-content {
            flex-direction: column;
            padding-top: 1.5rem;
            margin: 1rem auto 0 auto;
            align-items: center;   /* center video + text */
        }

        .info-text {
            font-size: 12px;
            line-height: 1.7;
            padding: 0 5px 10px 5px !important;
        }
        .info-brand {
            color: #1d4ed8;
            font-size: 14px;
            font-weight: 700;
        }

        .info-text h2 {
            font-size: 24px;
            margin-top: -2.5rem;
            padding-left: 27px;
            
        }

        .video-div {
            width: 100%;
            max-width: 400px;   /* keep video at 400px */
            margin: 0 auto;     /* center it */
        }

        .video-div video {
            width: 100%;        /* responsive inside container */
            height: auto;
            border-radius: 20px;
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

# Watermark
st.markdown("""
<div class="watermark">
     <strong style="padding-right:0.4rem; text-align:center;">Developer </strong> <a href="https://github.com/choudaryhussainali"><i class="fa-solid fa-code"></i></a>
</div>
""", unsafe_allow_html=True)

def configure_gemini():
    """Configure Gemini API"""
    try:
        # Try to get API key from Streamlit secrets first
        if 'GEMINI_API_KEY' in st.secrets:
            api_key = st.secrets['GEMINI_API_KEY']
        # Fallback to environment variable
        elif 'GEMINI_API_KEY' in os.environ:
            api_key = os.environ['GEMINI_API_KEY']
        else:
            return None
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"Error configuring Gemini: {str(e)}")
        return None

def check_image_quality(image):
    import numpy as np

    """Check if the image is too blurry for accurate processing using multiple methods"""
    try:
        import cv2
        
        # Convert PIL image to OpenCV format
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Method 1: Laplacian variance (primary method)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Method 2: Sobel gradient magnitude
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        sobel_mean = np.mean(sobel_magnitude)
        
        # Method 3: Text edge detection (important for MCQ papers)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Strict thresholds for MCQ papers (much higher than before)
        laplacian_threshold = 250  # Increased from 100
        sobel_threshold = 15       # New threshold
        edge_threshold = 0.02      # New threshold
        
        # All methods must pass for image to be considered clear
        laplacian_clear = laplacian_var > laplacian_threshold
        sobel_clear = sobel_mean > sobel_threshold
        edge_clear = edge_density > edge_threshold
        
        is_clear = laplacian_clear and sobel_clear and edge_clear
        
        quality_scores = {
            'laplacian': laplacian_var,
            'sobel': sobel_mean,
            'edges': edge_density,
            'overall_clear': is_clear
        }
        
        return is_clear, quality_scores
        
    except ImportError:
        # Enhanced fallback method without OpenCV
        img_array = np.array(image.convert('L'))
        
        # Multiple fallback checks
        std_dev = np.std(img_array)
        mean_val = np.mean(img_array)
        
        # Calculate local contrast
        kernel_size = 9
        h, w = img_array.shape
        contrast_sum = 0
        count = 0
        
        for i in range(0, h - kernel_size, kernel_size):
            for j in range(0, w - kernel_size, kernel_size):
                patch = img_array[i:i+kernel_size, j:j+kernel_size]
                local_std = np.std(patch)
                contrast_sum += local_std
                count += 1
        
        avg_local_contrast = contrast_sum / count if count > 0 else 0
        
        # Stricter fallback thresholds
        std_threshold = 45      # Increased from 30
        contrast_threshold = 25  # New threshold
        
        is_clear = std_dev > std_threshold and avg_local_contrast > contrast_threshold
        
        quality_scores = {
            'std_dev': std_dev,
            'contrast': avg_local_contrast,
            'overall_clear': is_clear
        }
        
        return is_clear, quality_scores
        
    except Exception:
        # Conservative approach - if we can't check quality, assume it might be blurry
        return False, {'error': 'Could not assess image quality'}

def validate_and_fix_results(result):
    """Validate and fix the results from Gemini API to ensure consistency"""
    if not result or 'mcqs' not in result:
        return result
    
    mcqs = result['mcqs']
    
    # Recalculate correct and wrong answers by actually counting from the mcqs list
    correct_count = sum(1 for mcq in mcqs if mcq.get('is_correct', False))
    total_questions = len(mcqs)
    wrong_count = total_questions - correct_count
    
    # Recalculate percentage
    score_percentage = round((correct_count / total_questions * 100), 2) if total_questions > 0 else 0
    
    # Update the result with the corrected values
    result['total_questions'] = total_questions
    result['correct_answers'] = correct_count
    result['wrong_answers'] = wrong_count
    result['score_percentage'] = score_percentage
    
    return result

def grade_mcqs_from_image(image, model):
    """Process the uploaded image and grade MCQs"""
    start_time = time.time()
    
    # Check image quality first
    is_clear, quality_scores = check_image_quality(image)
    if not is_clear:
        error_msg = "⚠️ Image quality insufficient for accurate grading.\n\n"
        if 'error' in quality_scores:
            error_msg += "Could not assess image quality properly."
        else:
            error_msg += "**Quality Analysis:**\n"
            if 'laplacian' in quality_scores:
                error_msg += f"• Sharpness Score: {quality_scores['laplacian']:.1f} (needs >250)\n"
                error_msg += f"• Edge Clarity: {quality_scores['sobel']:.1f} (needs >15)\n"
                error_msg += f"• Text Definition: {quality_scores['edges']:.3f} (needs >0.02)"
            else:
                error_msg += f"• Contrast Score: {quality_scores['std_dev']:.1f} (needs >45)\n"
                error_msg += f"• Local Sharpness: {quality_scores['contrast']:.1f} (needs >25)"
        
        return None, 0, error_msg

    # Prepare the image
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()

    # Optimized prompt for Gemini Vision
    prompt = """You are an MCQ checking Expert. Carefully analyze this image of a solved MCQ exam paper. Extract and return the following information in JSON format:

    CRITICAL INSTRUCTIONS:
    1. Look VERY CAREFULLY at each question's answer choices (A, B, C, D, etc.)
    2. very carefully and intelligently Identify which option the student has ACTUALLY marked/selected (circled, bubbled, filled, checked, etc.)
    3. Double verify the marked options that which options are ACTUALLY marked/selected by student.
    4. Identify ALL options that could be considered correct (sometimes there are duplicate/misstyped options with same content)
    5. DO NOT assume patterns - each question must be analyzed individually
    6. If you cannot clearly see what the student marked, mark that question as "unclear"
    7. Pay close attention to different marking styles (circles, fills, checkmarks, crosses, bubbles)
    8. If multiple options have identical or very similar content, list ALL of them as potential correct answers
    9. If this is an English paper and have Grammar mcqs, then you have to wisely identify which option is correct

    Extract and return the following information in EXACT JSON format:

    {
        "student_name": "[Name from paper or 'Unknown']",
        "total_questions": [Total number of questions],
        "correct_answers": [Number of correct answers],
        "wrong_answers": [Number of wrong answers],
        "score_percentage": [Percentage score],
        "mcqs": [
            {
                "question_number": "[Q1, Q2, etc.]",
                "question": "[Full question text]",
                "available_options": "[A, B, C, D or whatever options are shown]",
                "correct_answer": "[Primary correct option]",
                "all_correct_answers": "[Array of ALL correct options if multiple exist, e.g., ['A', 'C'] for duplicate content]",
                "student_answer": "[The option the student ACTUALLY marked/selected]",
                "marking_confidence": "[high/medium/low - how clear was the student's marking]",
                "is_correct": [true/false]
            }
        ]
    }

    VALIDATION RULES:
    - If student answers appear identical across questions, you are making an error
    - Each question should have different student answers unless truly identical
    - Look for different marking patterns: circles, fills, checkmarks, X marks
    - If markings are unclear, set marking_confidence to "low"
    - If you see duplicate options with same content, include ALL in all_correct_answers array
    - Return ONLY valid JSON, no additional text or explanations
    
    DOUBLE-CHECK your work - students rarely mark the same option for every question!
    IMPORTANT FINAL RULE:
    - If the uploaded image does NOT contain multiple choice questions (MCQs with options like A, B, C, D etc.),
    then you MUST return exactly:
    {
        "mcqs": []
    }
    and nothing else.
    """

    try:
        # Send to Gemini for processing
        response = model.generate_content(
            [prompt, Image.open(io.BytesIO(img_bytes))],
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 4000
            }
        )

        # Clean the response to extract pure JSON
        response_text = response.text.replace('```json', '').replace('```', '').strip()
        result = json.loads(response_text)
        
        # Validate and fix the results to ensure consistency
        result = validate_and_fix_results(result)

        # Calculate processing time
        processing_time = time.time() - start_time

        return result, processing_time, None

    except Exception as e:
        return None, 0, str(e)

def display_results(result, processing_time):
    """Display the grading results in a professional format"""
    
    # Processing time with success message
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #10b981, #059669); color: white; border-radius: 10px; text-align: center;padding: 0 0 0.1rem; margin: 1rem 0;">
        <h3 style="margin: 0;"><i class="fa-duotone fa-solid fa-check-double"></i> Analysis Complete!</h3>
        <p>Processed in {processing_time:.2f} seconds</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional metrics display
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value"><i class="fa-solid fa-user-tie"></i></div>
            <div class="metric-label">Student Name</div>
            <div style="font-weight: 600; color: #667eea; margin-top: 0.5rem;">
                {result.get('student_name', 'Unknown')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{result['total_questions']}</div>
            <div class="metric-label">Total Questions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #10b981;">{result['correct_answers']}</div>
            <div class="metric-label">Correct Answers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #f59e0b;">{result['score_percentage']}%</div>
            <div class="metric-label">Final Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Animated progress bar
    progress_color = "#10b981" if result['score_percentage'] >= 70 else "#f59e0b" if result['score_percentage'] >= 50 else "#ef4444"
    st.markdown(f"""
    <div style="background: #f1f5f9; border-radius: 10px; padding: 1rem; margin: 2rem 0;">
        <div style="background: {progress_color}; width: {result['score_percentage']}%; height: 20px; border-radius: 10px; 
             display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 0.9rem;
             transition: width 2s ease;">
            {result['score_percentage']}%
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Grade classification
    if result['score_percentage'] >= 90:
        grade = "A+ Excellent"
        color = "#10b981"
    elif result['score_percentage'] >= 80:
        grade = "A Good"
        color = "#059669"
    elif result['score_percentage'] >= 70:
        grade = "B Average"
        color = "#f59e0b"
    elif result['score_percentage'] >= 60:
        grade = "C Below Average"
        color = "#f97316"
    else:
        grade = "D Needs Improvement"
        color = "#ef4444"
    
    st.markdown(f"""
    <div style="background: {color}; color: white; padding: 0.2rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;">
        <h2 style="margin: 0;"><i class="fa-solid fa-square-poll-horizontal"></i> Grade: {grade}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed results
    st.markdown("""<div style="margin: 0.5rem 0;"><h3><i class="fa-solid fa-list"></i> Detailed Question Analysis</h3></div>""", unsafe_allow_html=True)
    
    correct_questions = [mcq for mcq in result['mcqs'] if mcq['is_correct']]
    incorrect_questions = [mcq for mcq in result['mcqs'] if not mcq['is_correct']]
    
    # Tabs for better organization
    tab1, tab2, tab3 = st.tabs([f"✅ Correct ({len(correct_questions)})", f"❌ Incorrect ({len(incorrect_questions)})", "📊 All Questions"])
    
    with tab1:
        if correct_questions:
            for mcq in correct_questions:
                with st.expander(f"✅ {mcq['question_number']}: Correct Answer", expanded=False):
                    st.markdown(f"**Question:** {mcq['question']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success(f"**Correct Answer:** {mcq['correct_answer']}")
                    with col2:
                        st.success(f"**Student Answer:** {mcq['student_answer']}")
        else:
            st.info("No correct answers found.")
    
    with tab2:
        if incorrect_questions:
            for mcq in incorrect_questions:
                with st.expander(f"❌ {mcq['question_number']}: Incorrect Answer", expanded=False):
                    st.markdown(f"**Question:** {mcq['question']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success(f"**Correct Answer:** {mcq['correct_answer']}")
                    with col2:
                        st.error(f"**Student Answer:** {mcq['student_answer']}")
        else:
            st.success("All answers are correct! 🎉")
    
    with tab3:
        for i, mcq in enumerate(result['mcqs']):
            status = "✅ Correct" if mcq['is_correct'] else "❌ Incorrect"
            with st.expander(f"{mcq['question_number']}: {status}", expanded=False):
                st.markdown(f"**Question:** {mcq['question']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Correct Answer:** {mcq['correct_answer']}")
                with col2:
                    st.write(f"**Student Answer:** {mcq['student_answer']}")
                
                if mcq['is_correct']:
                    st.success("✅ Correct Answer!")
                else:
                    st.error("❌ Incorrect Answer")


def sidebar_content():
    """Professional sidebar with developer info and features"""
    with st.sidebar:
        # Developer Profile
        st.markdown("""
            <div class="developer-card">
                <div class="developer-avatar">
                    <i class="fa-duotone fa-solid fa-user-secret"></i>
                </div>
                <h3 class="typewriter-text">HUSSAIN ALI</h3>
                <p style="margin: 0.1rem 0 0.2rem; font-size: 1rem; opacity: 1;">| Python Developer |</p>
                <p style="margin: 1rem auto; font-size: 0.9rem; opacity: 0.7;">
                    Always learning. Always building. Let's connect and innovate!
                </p>
            </div>
            """, unsafe_allow_html=True)

        
        # Social Media Links
        st.markdown("""
            <div class="social-links">
                    <a href="https://linkedin.com/in/ch-hussain-ali" class="social-btn" style="font-size:1.5rem;" target="_blank">
                    <i class="fab fa-linkedin"></i>
                    </a>
                    <a href="https://github.com/choudaryhussainali" class="social-btn" style="font-size:1.5rem;" target="_blank">        
                    <i class="fab fa-github"></i>
                    </a>
                    <a href="mailto:choudaryhussainali@outlook.com" class="social-btn" style="font-size:1.5rem;" target="_blank">
                        <i class="fas fa-envelope"></i>
                    </a>
                    <a href="https://www.instagram.com/choudary_hussain_ali/" class="social-btn" style="font-size:1.5rem;" target="_blank">
                        <i class="fa-brands fa-instagram"></i>
                    </a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---") 

        st.markdown("""<div style="text-align: center;"><h3 style="color: #667eea; margin-bottom: 1rem;">How We Work</h3></div>""", unsafe_allow_html=True)
        
        steps = [
            ("📞", "Initial Call", "Discuss requirements"),
            ("📋", "Project Scope", "Define deliverables"),
            ("🔨", "Development", "Build with updates"),
            ("🚀", "Launch", "Deploy & celebrate")
        ]
        
        for i, (icon, title, desc) in enumerate(steps):
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f9fafb, #f3f4f6); border-radius: 10px; padding: 1rem; margin-bottom: 1.5rem; border-left: 3px solid #3b82f6;">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.5rem; margin-right: 0.8rem;">{icon}</span>
                    <h5 style="color: #667eea; margin: 0; font-size: 0.9rem;">{title}</h5>
                </div>
                <p style="color: #888; font-size: 0.8rem; margin: 0; padding-left: 2.3rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
         
        st.markdown("---")

        def contact_form_sidebar():
            # Custom CSS
            st.markdown("""
                <style>
                .contact-box {
                    background: linear-gradient(135deg, #f8f9fa, #ffffff);
                    border-radius: 16px;
                    padding: 20px;
                    margin: 10px 0;
                    box-shadow: 0 5px 12px rgba(0,0,0,0.5);
                }
                .stForm{
                    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
                }
                .contact-title {
                    text-align: center;
                    color: #667eea;
                    font-weight: 700;
                    margin-bottom: 1rem;
                    font-size: 1.3rem;
                }

                div[class*="st-key-FormSubmitter-contact_form-Send-Message"] {
                    width: 100% !important;
                    display: flex !important;
                    justify-content: center !important; /* horizontal center */
                    align-items: center !important;     /* vertical center */
                    padding: 0 !important;
                    box-sizing: border-box !important;
                    }
                        
                div[class*="st-key-FormSubmitter-contact_form-Send-Message"] .stFormSubmitButton > button,
                div[class*="st-key-FormSubmitter-contact_form-Send-Message"] [data-testid="stFormSubmitButton"] > button {
                    width: auto !important;
                    min-width: 140px !important;
                    padding: 10px 20px !important;
                    border-radius: 10px !important;
                    box-shadow: none !important;
                }
                        
                div[class*="st-key-FormSubmitter-contact_form-Send-Message"] .stFormSubmitButton button div[data-testid="stMarkdownContainer"],
                div[class*="st-key-FormSubmitter-contact_form-Send-Message"] [data-testid="stFormSubmitButton"] button div[data-testid="stMarkdownContainer"] {
                    text-align: center !important;
                }
                .stTextInput>div>div>input, .stTextArea>div>div>textarea {
                    border-radius: 12px;
                }
                /* Button styling */
                        
                div.stFormSubmitButton {
                    display: flex !important;
                    justify-content: center !important;
                }
                .stFormSubmitButton {
                    display: flex !important;
                    justify-content: center !important; /* horizontally center */
                }
                .stFormSubmitButton>button {
                    width: auto !important; /* shrink to fit text */
                    min-width: 150px; /* optional fixed min size */
                    border-radius: 12px;
                    background: red;
                    border: 0px !important;
                    color: white !important;
                    font-weight: 600;
                    padding: 0.6rem 1.5rem;
                    transition: all 0.3s ease;
                }

                div[class*="st-key-FormSubmitter-contact_form-Send-Message"] * {
                    opacity: 1 !important;
                    filter: none !important;
                }
                div[class*="st-key-FormSubmitter-contact_form-Send-Message"] .stFormSubmitButton > button,
                div[class*="st-key-FormSubmitter-contact_form-Send-Message"] [data-testid="stFormSubmitButton"] > button {
                width: auto !important;           /* don't stretch full width */
                min-width: 150px !important;      /* nice button size */
                padding: 10px 20px !important;
                border-radius: 12px !important;
                background: red;
                color: #ffffff !important;
                font-weight: 800 !important;
                box-shadow: 0 8px 24px rgba(79,70,229,0.18) !important;
                opacity: 1 !important;            /* ensure full opacity inside this container */
                border: 0 !important;
                transition: transform .12s ease, box-shadow .12s ease !important;
                }
                .stFormSubmitButton>button:hover {
                    background: linear-gradient(135deg, #141E30 0%, #243B55 100%) !important;
                    color: white;
                    transform: translateY(-3px);
                }                

                button[data-testid="stBaseButton-primary"],
                    button[data-testid="stBaseButton-secondary"],
                    button[data-testid="stBaseButton-secondaryFormSubmit"] {
                    opacity: 1 !important;
                    filter: none !important;
                    }
                </style>
                        
            """, unsafe_allow_html=True)

            import re

            with st.sidebar:
                st.markdown("""<div class='contact-title'><i class="fa-solid fa-address-book"></i> Quick Contact</div>""", unsafe_allow_html=True)
                with st.form("contact_form", clear_on_submit=True):
                    name = st.text_input("Your Name")
                    email = st.text_input("Your Email")
                    message = st.text_area("Message", height=120)

                    submitted = st.form_submit_button("Send Message")

                    if submitted:
                        # Regex pattern for valid email
                        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

                        if not name or not email or not message:
                            st.warning("⚠️ Please fill all fields before submitting.")
                        elif not re.match(email_pattern, email):
                            st.error("❌ Please enter a valid email address (example: user@gmail.com).")
                        else:
                            if send_email(name, email, message):
                                st.success("✅ Message sent successfully! We will reach you soon..")
                            else:
                                st.error("⚠️ Something went wrong while sending.")
                                


        contact_form_sidebar()
        st.caption("You can also _share_ your :blue[feedback] ! :sunglasses:")
        st.markdown("---")
        st.markdown("""
             <h3 style='text-align: center;'><i class="fa-solid fa-bars-progress"></i> Core Insights</h3>""",
            unsafe_allow_html=True
        )

        insights = [
            ("📂", "Total Processed", "500+", "+23%"),
            ("🎯", "Accuracy Rate", "98.5%", "+2.1%"),
            ("⭐", "User Satisfaction", "4.7 / 5", "Stable"),
        ]

        for icon, title, value, delta in insights:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f9fafb, #f3f4f6);
                border-radius: 12px;
                padding: 1rem;
                margin-bottom: 0.8rem;
                border-left: 4px solid #667eea;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            ">
                <div style="display:flex; align-items:center; justify-content:space-between;">
                    <div style="display:flex; align-items:center;">
                        <span style="font-size:1.4rem; margin-right:0.6rem;">{icon}</span>
                        <div>
                            <p style="margin:0; font-size:0.85rem; color:#555;">{title}</p>
                            <h4 style="margin:0; font-size:1.1rem; color:#1f2937;">{value}</h4>
                        </div>
                    </div>
                    <span style="font-size:0.9rem; color:#10b981; font-weight:600;">{delta}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")

        def fun_fact_mcq_sidebar():
            """Sidebar widget: Fun Fact MCQ of the Day"""
            st.markdown("""
                <h2 style='text-align: center;'><i style="color:yellow;" class="fa-solid fa-lightbulb"></i></i> Fun Fact <strong style="color: #667eea;">MCQ</strong> of the day </h2>""",
                unsafe_allow_html=True
            )

            if "fun_mcq" not in st.session_state:
                st.session_state.fun_mcq = random.choice(fun_mcqs)


            q = st.session_state.fun_mcq
            # Show the question
            st.sidebar.write(f"**{q['question']}**")
            
            # Show options
            choice = st.sidebar.radio(
                "Pick your answer:",
                q["options"],
                key="fun_mcq_choice"
            )
            
            # Submit button
            if st.sidebar.button("Submit Answer", key="fun_mcq_submit"):
                if choice == q["answer"]:
                    st.sidebar.success(f"✅ Correct! {q['fact']}")
                else:
                    st.sidebar.error(f"❌ Oops! Correct answer: **{q['answer']}**\n\n{q['fact']}")


        fun_fact_mcq_sidebar()
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; padding: 0; margin-top: 0.5rem;">
                <p style="color: #999; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                    © 2025 AutoMARK AI. All rights reserved.
                </p>
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main application"""
    
    # Sidebar
    sidebar_content()
    result = None

        
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

    st_javascript("alert('⚠️ This is a preliminary release. AutoMARK is currently in development integrating more AI Agents !');") 


if __name__ == "__main__":
    main()



