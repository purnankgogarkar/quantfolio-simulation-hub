import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

from ui.portfolio_builder import portfolio_builder
from ui.modern_components import (
    display_header_with_animation,
    display_metric_cards,
    display_section_header,
    display_insight_box,
    display_collapsible_section,
    create_gradient_chart,
    display_portfolio_summary,
    display_stat_row,
    display_progress_bar,
    display_enhanced_insights
)

from simulations.monte_carlo import run_monte_carlo
from simulations.historical import run_historical_simulation
from simulations.bootstrap import run_bootstrap_simulation
from simulations.stress_test import run_stress_test

from utils.data_fetcher import fetch_price_data, validate_portfolio_alignment
from utils.explanations import (
    get_simulation_explanations,
    get_personalized_var_explanation,
    get_personalized_es_explanation,
    get_personalized_graph_explanation,
    get_simulation_comparison
)
from utils.styling import inject_custom_css
from utils.pdf_generator import generate_pdf_report, get_pdf_filename

# FIX: Configure page
st.set_page_config(
    page_title="Quantfolio Simulation Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FIX: Inject custom CSS
inject_custom_css()

# FIX: Display animated header
display_header_with_animation()

# FIX: Add introduction info box
display_insight_box(
    title="Welcome to Quantfolio",
    content="Use advanced simulation techniques to understand your portfolio's risk profile. Choose your stocks, run simulations, and get personalized risk insights.",
    icon="👋",
    box_type="info"
)

# ============================================
# SIDEBAR - Portfolio Management
# ============================================

st.sidebar.markdown("---")

with st.sidebar.expander("📚 Learn About Simulations", expanded=False):
    st.markdown("""
    This tool helps you understand your portfolio's risk using 4 different simulation methods.
    Each method shows you possible outcomes and helps you make informed decisions.
    
    **Choose your preferred method:**
    - **Monte Carlo** - Most comprehensive
    - **Historical** - Most realistic
    - **Bootstrap** - Balanced approach
    - **Stress Test** - Worst-case scenario
    """)

portfolio_df = portfolio_builder()

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Simulation Settings")

simulation_model = st.sidebar.selectbox(
    "Simulation Model",
    ["Monte Carlo", "Historical Simulation", "Bootstrap Simulation", "Stress Test"],
    help="Choose the simulation method that best fits your needs"
)

# FIX: Map simulation model names to dictionary keys
model_key_map = {
    "Monte Carlo": "Monte Carlo",
    "Historical Simulation": "Historical",
    "Bootstrap Simulation": "Bootstrap",
    "Stress Test": "Stress"
}

# FIX: Add simulation explanation
simulations = get_simulation_explanations()
model_key = model_key_map[simulation_model]

with st.sidebar.expander(f"ℹ️ About {simulation_model}"):
    sim_info = simulations[model_key]
    st.markdown(sim_info["title"])
    st.markdown(sim_info["what_is_it"])
    st.markdown(sim_info["how_it_works"])
    st.markdown(sim_info["why_useful"])
    st.markdown(sim_info["best_for"])

iterations = st.sidebar.slider(
    "Number of Simulations",
    1000,
    50000,
    10000,
    step=1000,
    help="More simulations = more accurate but slower"
)

confidence = st.sidebar.slider(
    "Confidence Level (%)",
    90,
    99,
    95,
    help="How confident you want to be about the VaR estimate"
)

st.sidebar.markdown("---")

run_button = st.sidebar.button(
    "🚀 Run Simulation",
    use_container_width=True,
    help="Click to run the selected simulation"
)

# ============================================
# MAIN CONTENT - Portfolio Analysis
# ============================================

if run_button and portfolio_df is not None:

    stocks = portfolio_df["Stock"].tolist()
    quantities = portfolio_df["Quantity"].values

    # Show loading state
    with st.spinner("📥 Fetching market data..."):
        try:
            data = fetch_price_data(stocks)
        except ValueError as e:
            st.error(f"❌ Error fetching data: {e}")
            st.stop()

    # FIX: Use validation function for proper alignment
    aligned_portfolio_df, valid_stocks, excluded_stocks = validate_portfolio_alignment(
        portfolio_df, 
        data.columns.tolist()
    )

    # FIX: Check if we have any valid stocks left
    if len(valid_stocks) == 0:
        st.error("❌ No valid stocks available for simulation. Please check your portfolio.")
        st.stop()

    # FIX: Update quantities array to match aligned portfolio
    quantities = aligned_portfolio_df["Quantity"].values
    stocks = aligned_portfolio_df["Stock"].tolist()
    
    # FIX: Filter data to only include valid stocks (in same order as portfolio)
    data = data[stocks]

    # Final validation
    if len(quantities) != len(data.columns):
        st.error(f"❌ Data mismatch: {len(quantities)} quantities but {len(data.columns)} stocks")
        st.stop()

    # Calculate portfolio value
    prices = aligned_portfolio_df["Price"].values
    portfolio_value = np.sum(prices * quantities)

    # Display portfolio summary with aligned data
    display_portfolio_summary(aligned_portfolio_df, portfolio_value)

    st.markdown("---")

    # Run simulation with progress indicator
    display_section_header("🔄 Running Simulation", "")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"📊 {simulation_model} with {len(stocks)} stocks and {iterations:,} iterations")
    with col2:
        st.info(f"💼 Portfolio: ₹{portfolio_value:,.0f}")

    try:
        with st.spinner(f"⏳ Running {simulation_model}..."):
            if simulation_model == "Monte Carlo":
                losses = run_monte_carlo(data, quantities, iterations)
            elif simulation_model == "Historical Simulation":
                losses = run_historical_simulation(data, quantities)
            elif simulation_model == "Bootstrap Simulation":
                losses = run_bootstrap_simulation(data, quantities, iterations)
            else:
                losses = run_stress_test(data, quantities)

        # Calculate metrics
        var = np.percentile(losses, 100 - confidence)
        es = losses[losses <= var].mean()

        st.success("✅ Simulation completed successfully!")
        
        st.markdown("---")

        # FIX: Display results with metric cards
        display_section_header("📈 Risk Analysis Results", "")
        
        display_metric_cards(var, es, confidence)

        st.markdown("---")

        # FIX: Display detailed insights
        display_section_header("🔍 Detailed Insights", "")

        col1, col2 = st.columns(2)

        with col1:
            display_stat_row(
                label="Worst Case Loss",
                value=f"₹{losses.max():,.0f}",
                icon="📉",
                color="danger"
            )
            
            display_stat_row(
                label="Best Case Gain",
                value=f"₹{abs(losses.min()):,.0f}",
                icon="📈",
                color="success"
            )

        with col2:
            max_loss_pct = (losses.max() / portfolio_value) * 100
            display_progress_bar(
                "Maximum Risk Exposure",
                max_loss_pct,
                max_value=100,
                color="danger"
            )
            
            safe_scenarios = (losses <= var).sum()
            safe_pct = (safe_scenarios / len(losses)) * 100
            display_progress_bar(
                "Safe Scenarios",
                safe_pct,
                max_value=100,
                color="success"
            )

        st.markdown("---")

        # FIX: Display chart with professional styling
        display_section_header("📊 Loss Distribution Chart", "")
        
        # Create gradient chart
        fig = create_gradient_chart(losses, var, confidence)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # FIX: Display educational explanations in collapsible sections
        display_section_header("📚 Understanding Your Results", "")

        col1, col2 = st.columns([2, 1])

        with col1:
            display_collapsible_section(
                "💰 What is Value at Risk (VaR)?",
                get_personalized_var_explanation(portfolio_value, var, confidence, losses),
                icon="💰",
                is_open=True
            )

            display_collapsible_section(
                "📊 What is Expected Shortfall (ES)?",
                get_personalized_es_explanation(portfolio_value, var, es, confidence, losses),
                icon="📊",
                is_open=False
            )

            display_collapsible_section(
                "📈 How to Read the Graph?",
                get_personalized_graph_explanation(portfolio_value, var, confidence, losses),
                icon="📈",
                is_open=False
            )

        with col2:
            display_insight_box(
                title="Pro Tips",
                content="""
                ✅ **Run all simulations** to compare results
                
                ✅ **Monitor trends** over time
                
                ✅ **Diversify** to reduce risk
                
                ✅ **Rebalance** regularly
                """,
                icon="💡",
                box_type="success"
            )

        st.markdown("---")

        # FIX: Display export options
        display_section_header("📥 Export Results", "")

        col1, col2 = st.columns(2)

        with col1:
            # PDF download button
            # FIX: Get explanations first
            var_explanation = get_personalized_var_explanation(portfolio_value, var, confidence, losses)
            es_explanation = get_personalized_es_explanation(portfolio_value, var, es, confidence, losses)
            graph_explanation = get_personalized_graph_explanation(portfolio_value, var, confidence, losses)
            
            pdf_buffer = generate_pdf_report(
                aligned_portfolio_df,
                portfolio_value,
                var,
                es,
                confidence,
                losses,
                simulation_model,
                len(stocks),
                var_explanation=var_explanation,
                es_explanation=es_explanation,
                graph_explanation=graph_explanation
            )
            
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name=get_pdf_filename(),
                mime="application/pdf",
                help="Download comprehensive simulation report as PDF"
            )

        with col2:
            # CSV export
            csv_data = pd.DataFrame({
                "Loss Scenarios": losses
            }).to_csv(index=False)
            
            st.download_button(
                label="📊 Download CSV Data",
                data=csv_data,
                file_name=f"quantfolio_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Download raw simulation data as CSV"
            )

        st.markdown("---")

        # Display enhanced insights
        display_section_header("💼 Personalized Insights", "")
        display_enhanced_insights(var, es, confidence, losses, portfolio_value)

    except Exception as e:
        st.error(f"❌ Error during simulation: {e}")
        print(f"Error details: {str(e)}")
        st.stop()

else:
    if portfolio_df is None:
        display_insight_box(
            title="Get Started",
            content="👈 **Step 1:** Build or upload your portfolio from the sidebar\n\n👈 **Step 2:** Configure simulation settings\n\n👈 **Step 3:** Click 'Run Simulation' to see your risk analysis",
            icon="🚀",
            box_type="info"
        )

st.markdown("---")

# FIX: Add comparison and glossary
with st.expander("🔍 Compare All Simulation Methods"):
    st.markdown(get_simulation_comparison())

with st.expander("📚 Financial Terms Glossary"):
    glossary = """
    **Portfolio**: All your investments combined
    
    **Volatility**: How much a stock's price jumps up and down
    
    **Risk**: The chance of losing money
    
    **Distribution**: How outcomes are spread (concentrated vs scattered)
    
    **Confidence Level**: How sure you want to be (95% means 95% certainty)
    
    **Scenario**: A possible outcome or simulation run
    
    **Historical Data**: Actual price movements from the past
    
    **Correlation**: How two stocks move together (or apart)
    
    **Tail Risk**: The risk of extreme, unexpected losses
    
    **Stress Test**: Testing portfolio under worst-case conditions
    
    **Value at Risk (VaR)**: Maximum expected loss at a given confidence level
    
    **Expected Shortfall**: Average loss in worst-case scenarios
    """
    st.markdown(glossary)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 0.9rem; padding: 20px;'>
    <p>💼 Quantfolio Simulation Hub | Advanced Portfolio Risk Analysis</p>
    <p>⚠️ Disclaimer: This tool is for educational and analytical purposes. Past performance doesn't guarantee future results.</p>
</div>
""", unsafe_allow_html=True)