import streamlit as st
import numpy as np
import plotly.graph_objects as go


def display_header_with_animation():
    """Display animated header"""
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown("📊", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <h1 style='margin: 0;'>Quantfolio Simulation Hub</h1>
        <p style='color: #6b7280; font-size: 1.1rem; margin: 5px 0 0 0;'>Advanced Portfolio Risk Analysis</p>
        """, unsafe_allow_html=True)


def display_info_card(title, value, icon, color="primary", metric_type="neutral"):
    """Display an animated info card"""
    
    color_map = {
        "primary": ("#0066cc", "#dbeafe"),
        "success": ("#10b981", "#dcfce7"),
        "danger": ("#ef4444", "#fee2e2"),
        "warning": ("#f59e0b", "#fef3c7"),
        "info": ("#3b82f6", "#dbeafe")
    }
    
    bg_color, light_bg = color_map.get(color, color_map["primary"])
    
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, {bg_color} 0%, rgba(0,0,0,0.1) 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: slideUp 0.5s ease-out;
    '>
        <div style='color: white; font-size: 2.5rem; margin-bottom: 10px;'>{icon}</div>
        <div style='color: rgba(255,255,255,0.9); font-size: 0.9rem; margin-bottom: 8px;'>{title}</div>
        <div style='color: white; font-size: 1.8rem; font-weight: bold;'>{value}</div>
    </div>
    """, unsafe_allow_html=True)


def display_metric_cards(var, es, confidence):
    """Display three metric cards in a row with animations"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        display_info_card(
            title="Value at Risk (VaR)",
            value=f"₹{var:,.0f}",
            icon="📉",
            color="danger"
        )
    
    with col2:
        display_info_card(
            title="Expected Shortfall (ES)",
            value=f"₹{es:,.0f}",
            icon="⚠️",
            color="warning"
        )
    
    with col3:
        display_info_card(
            title="Confidence Level",
            value=f"{confidence}%",
            icon="🎯",
            color="success"
        )


def display_stat_row(label, value, icon, color="primary"):
    """Display a stat row with icon"""
    
    color_map = {
        "primary": "#0066cc",
        "success": "#10b981",
        "danger": "#ef4444",
        "warning": "#f59e0b",
    }
    
    color_code = color_map.get(color, color_map["primary"])
    
    st.markdown(f"""
    <div style='
        display: flex;
        align-items: center;
        padding: 12px;
        background: #f9fafb;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 4px solid {color_code};
    '>
        <div style='font-size: 1.5rem; margin-right: 15px;'>{icon}</div>
        <div style='flex: 1;'>
            <div style='color: #6b7280; font-size: 0.9rem;'>{label}</div>
            <div style='color: {color_code}; font-size: 1.3rem; font-weight: 600;'>{value}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_insight_box(title, content, icon="💡", box_type="info"):
    """Display an insight/tip box"""
    
    type_map = {
        "info": ("#3b82f6", "#dbeafe"),
        "success": ("#10b981", "#dcfce7"),
        "warning": ("#f59e0b", "#fef3c7"),
        "danger": ("#ef4444", "#fee2e2"),
    }
    
    color, bg_color = type_map.get(box_type, type_map["info"])
    
    st.markdown(f"""
    <div style='
        background-color: {bg_color};
        border-left: 4px solid {color};
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        animation: slideIn 0.4s ease-out;
    '>
        <div style='color: {color}; font-weight: 600; margin-bottom: 8px;'>
            {icon} {title}
        </div>
        <div style='color: {color}; font-size: 0.95rem; line-height: 1.6;'>
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_section_header(title, icon=""):
    """Display a modern section header"""
    
    st.markdown(f"""
    <div style='
        margin-top: 30px;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 3px solid #e5e7eb;
    '>
        <h2 style='margin: 0; display: inline-block;'>
            {icon} {title}
        </h2>
    </div>
    """, unsafe_allow_html=True)


def display_progress_bar(title, value, max_value=100, color="primary"):
    """Display an animated progress bar"""
    
    percentage = (value / max_value) * 100
    
    color_map = {
        "primary": "#0066cc",
        "success": "#10b981",
        "danger": "#ef4444",
        "warning": "#f59e0b",
    }
    
    color_code = color_map.get(color, color_map["primary"])
    
    st.markdown(f"""
    <div>
        <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
            <span style='font-weight: 600;'>{title}</span>
            <span style='color: {color_code}; font-weight: 600;'>{percentage:.1f}%</span>
        </div>
        <div style='
            background-color: #e5e7eb;
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
        '>
            <div style='
                background: linear-gradient(90deg, {color_code} 0%, {color_code} 100%);
                height: 100%;
                width: {percentage}%;
                animation: fillWidth 1s ease-out forwards;
            '></div>
        </div>
    </div>
    <style>
        @keyframes fillWidth {{
            from {{
                width: 0%;
            }}
            to {{
                width: {percentage}%;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)


def display_collapsible_section(title, content, icon="", is_open=False):
    """Display a modern collapsible section"""
    
    with st.expander(f"{icon} {title}", expanded=is_open):
        st.markdown(content)


def create_gradient_chart(losses, var, confidence):
    """Create an enhanced distribution chart with gradient"""
    
    # Calculate statistics
    mean_loss = np.mean(losses)
    median_loss = np.median(losses)
    
    # Create histogram
    fig = go.Figure()
    
    # Add histogram
    fig.add_trace(go.Histogram(
        x=losses,
        nbinsx=50,
        name='Loss Distribution',
        marker=dict(
            color='rgba(102, 126, 234, 0.7)',
            line=dict(
                color='rgba(102, 126, 234, 1)',
                width=1.5
            )
        ),
        hovertemplate='<b>Loss Range</b><br>₹%{x:,.0f}<br><b>Frequency</b>: %{y}<extra></extra>'
    ))
    
    # Add VaR line
    fig.add_vline(
        x=var,
        line_dash="dash",
        line_color="red",
        line_width=3,
        name=f'VaR ({confidence}%)',
        annotation_text=f"VaR<br>₹{var:,.0f}",
        annotation_position="top right",
        annotation=dict(
            bgcolor="rgba(239, 68, 68, 0.9)",
            bordercolor="red",
            font=dict(color="white", size=12)
        )
    )
    
    # Add Mean line
    fig.add_vline(
        x=mean_loss,
        line_dash="dot",
        line_color="green",
        line_width=2,
        name='Mean Loss',
        annotation_text=f"Mean<br>₹{mean_loss:,.0f}",
        annotation_position="top left",
        annotation=dict(
            bgcolor="rgba(16, 185, 129, 0.9)",
            bordercolor="green",
            font=dict(color="white", size=12)
        )
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="<b>Portfolio Loss Distribution Analysis</b>",
            font=dict(size=20)
        ),
        xaxis_title="Portfolio Loss (₹)",
        yaxis_title="Number of Scenarios",
        hovermode='x unified',
        template='plotly_white',
        showlegend=True,
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
        font=dict(family="Arial, sans-serif", size=12),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e5e7eb',
            showline=True,
            linewidth=2,
            linecolor='#d1d5db',
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e5e7eb',
            showline=True,
            linewidth=2,
            linecolor='#d1d5db',
        )
    )
    
    return fig


def display_portfolio_summary(portfolio_df, portfolio_value):
    """Display portfolio summary with animations"""
    
    display_section_header("📊 Portfolio Summary", "")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        display_info_card(
            title="Total Portfolio Value",
            value=f"₹{portfolio_value:,.0f}",
            icon="💰",
            color="success"
        )
    
    with col2:
        display_info_card(
            title="Number of Stocks",
            value=str(len(portfolio_df)),
            icon="📈",
            color="primary"
        )
    
    with col3:
        total_quantity = portfolio_df["Quantity"].sum()
        display_info_card(
            title="Total Shares",
            value=f"{int(total_quantity):,}",
            icon="📦",
            color="info"
        )
    
    # Display portfolio breakdown
    st.markdown("**Portfolio Composition:**")
    portfolio_df_display = portfolio_df.copy()
    portfolio_df_display["Value"] = portfolio_df_display["Price"] * portfolio_df_display["Quantity"]
    portfolio_df_display["% of Portfolio"] = (portfolio_df_display["Value"] / portfolio_value) * 100
    
    # Format for display
    display_cols = portfolio_df_display[["Stock", "Price", "Quantity", "Value", "% of Portfolio"]].copy()
    display_cols["Price"] = display_cols["Price"].apply(lambda x: f"₹{x:,.2f}")
    display_cols["Value"] = display_cols["Value"].apply(lambda x: f"₹{x:,.2f}")
    display_cols["% of Portfolio"] = display_cols["% of Portfolio"].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(display_cols, use_container_width=True, hide_index=True)


def display_enhanced_insights(var, es, confidence, losses, portfolio_value):
    """Display enhanced Pro Tips and insights section"""
    
    # Calculate metrics
    var_pct = (var / portfolio_value) * 100
    es_pct = (es / portfolio_value) * 100
    max_loss_pct = (losses.max() / portfolio_value) * 100
    safe_scenarios = (losses <= var).sum()
    safe_pct = (safe_scenarios / len(losses)) * 100
    risky_scenarios = len(losses) - safe_scenarios
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 20px;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        '>
            <div style='font-size: 1.3rem; font-weight: bold; margin-bottom: 15px;'>
                💡 Smart Recommendations
            </div>
            <div style='line-height: 1.8; font-size: 0.95rem;'>
                <div style='margin-bottom: 10px;'>
                    <span style='color: #fbbf24;'>📊</span> 
                    <b>Risk Level:</b> Your portfolio has <b>{var_pct:.1f}%</b> daily risk exposure
                </div>
                <div style='margin-bottom: 10px;'>
                    <span style='color: #34d399;'>✅</span> 
                    <b>Safe Days:</b> <b>{safe_pct:.1f}%</b> of scenarios are within safe zone
                </div>
                <div style='margin-bottom: 10px;'>
                    <span style='color: #f87171;'>⚠️</span> 
                    <b>Risky Days:</b> <b>{risky_scenarios}</b> out of <b>{len(losses)}</b> scenarios exceed VaR
                </div>
                <div style='margin-bottom: 10px;'>
                    <span style='color: #60a5fa;'>🎯</span> 
                    <b>Worst Case:</b> Potential loss of <b>{max_loss_pct:.1f}%</b> of portfolio
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border-radius: 12px;
            padding: 20px;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        '>
            <div style='font-size: 1.3rem; font-weight: bold; margin-bottom: 15px;'>
                🎯 Action Items
            </div>
            <div style='line-height: 1.8; font-size: 0.95rem;'>
                <div style='margin-bottom: 8px;'>
                    1️⃣ Review portfolio daily for losses above ₹{var:,.0f}
                </div>
                <div style='margin-bottom: 8px;'>
                    2️⃣ Prepare emergency fund for worst-case loss of ₹{losses.max():,.0f}
                </div>
                <div style='margin-bottom: 8px;'>
                    3️⃣ Rebalance quarterly or after major market moves
                </div>
                <div style='margin-bottom: 8px;'>
                    4️⃣ Consider hedging strategies for risky positions
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            border-radius: 12px;
            padding: 20px;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            height: 100%;
        '>
            <div style='font-size: 1.3rem; font-weight: bold; margin-bottom: 15px;'>
                ⚡ Quick Stats
            </div>
            <div style='line-height: 2; font-size: 1rem;'>
                <div style='display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.2); padding: 8px 0;'>
                    <span>Average Loss:</span>
                    <span style='font-weight: bold;'>₹{np.mean(losses):,.0f}</span>
                </div>
                <div style='display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.2); padding: 8px 0;'>
                    <span>Median Loss:</span>
                    <span style='font-weight: bold;'>₹{np.median(losses):,.0f}</span>
                </div>
                <div style='display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.2); padding: 8px 0;'>
                    <span>Std Deviation:</span>
                    <span style='font-weight: bold;'>₹{np.std(losses):,.0f}</span>
                </div>
                <div style='display: flex; justify-content: space-between; padding: 8px 0;'>
                    <span>Simulations:</span>
                    <span style='font-weight: bold;'>{len(losses)}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)