import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def show_distribution_chart(losses, var):
    """Display loss distribution chart using matplotlib"""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(losses, bins=50, alpha=0.7, color='#667eea', edgecolor='black')
    ax.axvline(var, color='red', linestyle="--", linewidth=2, label=f"VaR: ₹{var:,.0f}")
    
    ax.set_title("Loss Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Portfolio Loss (₹)", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    plt.close(fig)