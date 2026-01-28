"""
Theme Module for Hiring Bias Intelligence Engine

Dark glassmorphism theme with smooth animations and modern styling.
"""

def get_theme_css():
    """
    Get the complete CSS for the dark glassmorphism theme.
    
    Returns:
    --------
    str
        CSS styles as a string
    """
    return """
    <style>
    /* ===== RESET & BASE STYLES ===== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Remove default Streamlit padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 100%;
    }
    
    /* Dark background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1438 50%, #24243e 100%);
        color: #e0e0e0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== GLASSMORPHISM CARDS ===== */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease-in-out;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(138, 102, 255, 0.3);
        border: 1px solid rgba(138, 102, 255, 0.3);
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: linear-gradient(135deg, rgba(138, 102, 255, 0.1) 0%, rgba(102, 126, 234, 0.1) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(138, 102, 255, 0.2);
        transition: all 0.3s ease;
        animation: slideInUp 0.5s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(138, 102, 255, 0.4);
        border-color: rgba(138, 102, 255, 0.5);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #b0b0b0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 2px 10px rgba(138, 102, 255, 0.3);
    }
    
    h1 {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: fadeIn 0.8s ease;
    }
    
    h2 {
        font-size: 1.8rem;
    }
    
    h3 {
        font-size: 1.4rem;
    }
    
    p, div, span {
        color: #e0e0e0;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(138, 102, 255, 0.4);
        cursor: pointer;
        min-height: 44px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(138, 102, 255, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* ===== INPUTS & SELECTS ===== */
    .stSelectbox, .stTextInput, .stNumberInput {
        color: #e0e0e0;
    }
    
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: #e0e0e0;
        padding: 0.75rem;
        min-height: 44px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover,
    .stTextInput > div > div > input:hover,
    .stNumberInput > div > div > input:hover {
        border-color: rgba(138, 102, 255, 0.5);
        box-shadow: 0 0 10px rgba(138, 102, 255, 0.2);
    }
    
    /* ===== SIDEBAR ===== */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 12, 41, 0.95) 0%, rgba(36, 36, 62, 0.95) 100%);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .element-container {
        animation: fadeIn 0.5s ease;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #b0b0b0;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        min-height: 44px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(138, 102, 255, 0.1);
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(138, 102, 255, 0.4);
    }
    
    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #ffffff;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: rgba(138, 102, 255, 0.1);
        border-color: rgba(138, 102, 255, 0.3);
    }
    
    /* ===== DATAFRAMES ===== */
    .dataframe {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        overflow: hidden;
    }
    
    .dataframe th {
        background-color: rgba(138, 102, 255, 0.2);
        color: #ffffff;
        font-weight: 600;
        padding: 0.75rem;
    }
    
    .dataframe td {
        background-color: rgba(255, 255, 255, 0.02);
        color: #e0e0e0;
        padding: 0.75rem;
    }
    
    .dataframe tr:hover td {
        background-color: rgba(138, 102, 255, 0.1);
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    /* ===== RESPONSIVE - MOBILE FIRST ===== */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .glass-card {
            padding: 1rem;
            border-radius: 15px;
        }
        
        h1 {
            font-size: 1.8rem;
        }
        
        h2 {
            font-size: 1.4rem;
        }
        
        h3 {
            font-size: 1.2rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .stButton > button {
            width: 100%;
            padding: 0.875rem 1rem;
        }
        
        /* Reduce animations on mobile for performance */
        .glass-card:hover {
            transform: none;
        }
        
        .metric-card:hover {
            transform: scale(1.01);
        }
    }
    
    @media (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            padding: 2rem;
        }
        
        h1 {
            font-size: 2.2rem;
        }
    }
    
    @media (min-width: 1025px) {
        .main .block-container {
            padding: 3rem;
        }
    }
    
    /* ===== PLOTLY CHARTS ===== */
    .js-plotly-plot {
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* ===== LOADING SPINNER ===== */
    .stSpinner > div {
        border-color: #667eea !important;
        border-right-color: transparent !important;
    }
    
    /* ===== SUCCESS/ERROR/WARNING MESSAGES ===== */
    .stSuccess, .stError, .stWarning, .stInfo {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border-left: 4px solid;
        padding: 1rem;
        animation: slideInLeft 0.5s ease;
    }
    
    .stSuccess {
        border-left-color: #10b981;
    }
    
    .stError {
        border-left-color: #ef4444;
    }
    
    .stWarning {
        border-left-color: #f59e0b;
    }
    
    .stInfo {
        border-left-color: #3b82f6;
    }
    
    /* ===== CUSTOM CLASSES ===== */
    .fade-in {
        animation: fadeIn 0.6s ease-in-out;
    }
    
    .slide-in-up {
        animation: slideInUp 0.5s ease;
    }
    
    .slide-in-left {
        animation: slideInLeft 0.5s ease;
    }
    
    .glow {
        box-shadow: 0 0 20px rgba(138, 102, 255, 0.5);
    }
    
    /* ===== TOUCH TARGETS (Mobile-friendly) ===== */
    @media (max-width: 768px) {
        a, button, input, select, textarea {
            min-height: 44px;
            min-width: 44px;
        }
    }
    </style>
    """


def apply_theme():
    """Apply the theme to the Streamlit app."""
    import streamlit as st
    st.markdown(get_theme_css(), unsafe_allow_html=True)


if __name__ == "__main__":
    print("Theme CSS generated successfully!")
    print(f"Total CSS length: {len(get_theme_css())} characters")
