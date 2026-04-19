import streamlit as st

def display_risk_cards(var, es, confidence=95):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Value at Risk (VaR)",
            f"₹{var:,.2f}",
            help=f"At {confidence}% confidence: Maximum expected loss"
        )
    
    with col2:
        st.metric(
            "Expected Shortfall (ES)",
            f"₹{es:,.2f}",
            help="Average loss in worst case scenarios"
        )
    
    with col3:
        st.metric(
            "Confidence Level",
            f"{confidence}%",
            help="How certain we are about the VaR estimate"
        )