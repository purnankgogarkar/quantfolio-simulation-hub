def get_custom_css():
    """Returns custom CSS for modern finance app styling with proper light/dark mode support"""
    
    css = """
    <style>
    /* Global Styles */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main container animations */
    .main {
        animation: fadeIn 0.6s ease-in;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Metric cards with hover effect */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        animation: slideUp 0.5s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Success card */
    .success-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    /* Danger card */
    .danger-card {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    /* Warning card */
    .warning-card {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    /* Info card */
    .info-card {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    }
    
    /* Expandable sections */
    .streamlit-expanderHeader {
        background-color: #f3f4f6;
        border-radius: 8px;
        transition: all 0.3s ease;
        border-left: 4px solid #0066cc;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #e5e7eb;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Dark mode expandable sections */
    @media (prefers-color-scheme: dark) {
        .streamlit-expanderHeader {
            background-color: #374151;
            border-left-color: #60a5fa;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #4b5563;
        }
    }
    
    /* Buttons with modern style */
    .stButton > button {
        border-radius: 8px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: none;
        padding: 10px 20px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #0066cc;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
    }
    
    /* Dark mode input fields */
    @media (prefers-color-scheme: dark) {
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            border-color: #4b5563;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #60a5fa;
            box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
        }
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 8px;
        animation: slideIn 0.4s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Charts */
    .plotly-graph-div {
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);
    }
    
    /* Data tables */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Dividers */
    hr {
        border: none;
        border-top: 2px solid #e5e7eb;
        margin: 30px 0;
    }
    
    @media (prefers-color-scheme: dark) {
        hr {
            border-top-color: #4b5563;
        }
    }
    
    /* Custom headers */
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    h2 {
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 24px;
    }
    
    h3 {
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    /* Loading spinner */
    .spinner {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Icon animations */
    .icon-bounce {
        animation: bounce 0.6s ease-in-out;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Pulse animation for alerts */
    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    </style>
    """
    
    return css


def inject_custom_css():
    """Inject custom CSS into Streamlit app"""
    import streamlit as st
    st.markdown(get_custom_css(), unsafe_allow_html=True)