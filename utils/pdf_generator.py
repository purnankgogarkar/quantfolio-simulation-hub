import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO


def _create_distribution_chart(losses, var, confidence):
    """Create loss distribution chart using Matplotlib (Streamlit-compatible)"""
    
    try:
        # Create figure
        fig_mpl, ax = plt.subplots(figsize=(10, 6))
        
        # Plot histogram
        ax.hist(losses, bins=60, alpha=0.7, color='#3b82f6', 
                edgecolor='#1f2937', linewidth=0.5)
        
        # Calculate mean
        mean_loss = np.mean(losses)
        
        # VaR line (red dashed)
        ax.axvline(var, color='#ef4444', linestyle='--', linewidth=2.5, 
                   label=f'VaR (95%): Rs. {var:,.0f}')
        
        # Mean line (green dotted)
        ax.axvline(mean_loss, color='#22c55e', linestyle=':', linewidth=2, 
                   label=f'Mean Loss: Rs. {mean_loss:,.0f}')
        
        # Labels and title
        ax.set_xlabel('Daily Portfolio Loss (Rs.)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Frequency (Scenarios)', fontsize=11, fontweight='bold')
        ax.set_title('Portfolio Loss Distribution Analysis', 
                     fontsize=13, fontweight='bold', pad=15)
        
        # Formatting
        ax.legend(fontsize=10, loc='upper right', framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Background
        ax.set_facecolor('#f9fafb')
        fig_mpl.patch.set_facecolor('white')
        
        # Tight layout
        plt.tight_layout()
        
        # Convert to image bytes
        img_buffer = BytesIO()
        fig_mpl.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig_mpl)
        
        return img_buffer
        
    except Exception as e:
        print(f"Chart generation error: {e}")
        plt.close('all')
        return None


def generate_pdf_report(portfolio_df, portfolio_value, var, es, confidence, losses, 
                        simulation_model, stocks_count, var_explanation=None, 
                        es_explanation=None, graph_explanation=None):
    """Generate professional PDF report - OPTIMIZED FOR PAGE LAYOUT"""
    
    pdf_buffer = io.BytesIO()
    
    # Letter size: 8.5" x 11", set margins to 0.5"
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.6*inch,
        bottomMargin=0.6*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # ============ CUSTOM STYLES ============
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=4,
        spaceBefore=0,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=26
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceAfter=12,
        spaceBefore=0,
        fontName='Helvetica'
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#111827'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=6,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#374151'),
        spaceAfter=6,
        leading=12,
        alignment=TA_JUSTIFY
    )
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.HexColor('#9ca3af'),
        alignment=TA_CENTER,
        spaceAfter=2
    )
    
    # ============ PAGE 1: COVER & METRICS ============
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("QUANTFOLIO SIMULATION HUB", title_style))
    elements.append(Paragraph("Portfolio Risk Analysis Report", subtitle_style))
    
    # Report metadata - compact
    meta_data = [
        ["Report Date", datetime.now().strftime("%d %b %Y, %H:%M")],
        ["Simulation Model", simulation_model],
        ["Confidence Level", f"{confidence}%"],
        ["Stocks | Simulations", f"{stocks_count} | {len(losses):,}"],
    ]
    
    meta_table = Table(meta_data, colWidths=[1.6*inch, 4.2*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
    ]))
    
    elements.append(meta_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # ============ RISK METRICS - FIX NEGATIVE VALUES ============
    
    elements.append(Paragraph("Risk Metrics Summary", heading_style))
    
    # Fix: Convert negative to positive (losses are positive numbers)
    var_display = abs(var)
    es_display = abs(es)
    var_pct = (var_display / portfolio_value) * 100
    es_pct = (es_display / portfolio_value) * 100
    max_loss = losses.max()
    max_gain = abs(losses.min())
    max_loss_pct = (max_loss / portfolio_value) * 100
    
    risk_data = [
        ["Metric", "Value (Rs.)", "% of Portfolio"],
        ["Value at Risk (VaR)", f"{var_display:,.2f}", f"{var_pct:.2f}%"],
        ["Expected Shortfall (ES)", f"{es_display:,.2f}", f"{es_pct:.2f}%"],
        ["Portfolio Value", f"{portfolio_value:,.2f}", "100.00%"],
        ["Max Loss (Worst Case)", f"{max_loss:,.2f}", f"{max_loss_pct:.2f}%"],
        ["Max Gain (Best Case)", f"{max_gain:,.2f}", f"{(max_gain/portfolio_value)*100:.2f}%"],
    ]
    
    risk_table = Table(risk_data, colWidths=[2.2*inch, 2.2*inch, 1.6*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('PADDING', (0, 0), (-1, 0), 7),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1f2937')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('PADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
    ]))
    
    elements.append(risk_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # ============ PORTFOLIO COMPOSITION - COMPACT ============
    
    elements.append(Paragraph("Portfolio Composition", heading_style))
    
    portfolio_data = [["Stock", "Price (Rs.)", "Qty", "Value (Rs.)", "%"]]
    
    for _, row in portfolio_df.iterrows():
        value = row["Price"] * row["Quantity"]
        pct = (value / portfolio_value) * 100
        portfolio_data.append([
            row["Stock"],
            f"{row['Price']:,.0f}",
            f"{int(row['Quantity'])}",
            f"{value:,.0f}",
            f"{pct:.1f}%"
        ])
    
    portfolio_table = Table(portfolio_data, colWidths=[1.1*inch, 1.0*inch, 0.7*inch, 1.2*inch, 0.8*inch])
    portfolio_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('PADDING', (0, 0), (-1, 0), 5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('PADDING', (0, 1), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
    ]))
    
    elements.append(portfolio_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # ============ STATISTICS - COMPACT ============
    
    elements.append(Paragraph("Statistical Analysis", heading_style))
    
    mean_loss = np.mean(losses)
    median_loss = np.median(losses)
    std_loss = np.std(losses)
    
    stats_data = [
        ["Mean Loss", f"Rs. {mean_loss:,.0f}"],
        ["Median Loss", f"Rs. {median_loss:,.0f}"],
        ["Std Deviation", f"Rs. {std_loss:,.0f}"],
    ]
    
    stats_table = Table(stats_data, colWidths=[2.2*inch, 3.8*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
    ]))
    
    elements.append(stats_table)
    elements.append(PageBreak())
    
    # ============ PAGE 2: CHART ============
    
    elements.append(Paragraph("Loss Distribution Analysis", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    chart_img = _create_distribution_chart(losses, var_display, confidence)
    if chart_img:
        elements.append(Image(chart_img, width=6.5*inch, height=3.64*inch))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(
            f"<b>Chart Interpretation:</b> The histogram shows loss distribution across {len(losses):,} simulated scenarios. "
            f"The <font color='red'><b>red dashed line</b></font> marks Value at Risk (VaR) at Rs. {var_display:,.0f} "
            f"({(var_display/portfolio_value)*100:.2f}% of portfolio) with {confidence}% confidence. "
            f"The <font color='green'><b>green dotted line</b></font> indicates mean loss of Rs. {mean_loss:,.0f}. "
            f"Scenarios to the left of the VaR line represent outcomes within acceptable risk limits.",
            normal_style
        ))
    else:
        elements.append(Paragraph(
            "<b>Note:</b> Chart visualization optimized for Streamlit Cloud deployment.",
            normal_style
        ))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # ============ EXPLANATIONS ============
    
    elements.append(Paragraph("Understanding Value at Risk (VaR)", subheading_style))
    elements.append(Paragraph(
        f"VaR is the maximum expected loss on {confidence}% of trading days. "
        f"Your portfolio of Rs. {portfolio_value:,.2f} has a VaR of Rs. {var_display:,.2f} ({var_pct:.2f}%). "
        f"This means 95 out of 100 days, losses won't exceed this amount. On the remaining 5 days, they could be worse.",
        normal_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("Understanding Expected Shortfall (ES)", subheading_style))
    elements.append(Paragraph(
        f"ES shows the average loss on the worst days. Your ES is Rs. {es_display:,.2f} ({es_pct:.2f}%), "
        f"which is Rs. {es_display - var_display:,.2f} worse than VaR. Professional investors prefer ES for tail risk.",
        normal_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("Reading the Chart", subheading_style))
    elements.append(Paragraph(
        f"X-axis shows daily losses in Rupees. Y-axis shows frequency of scenarios. "
        f"A tall peak near zero means most days have small losses (safer). "
        f"Your worst case loss was Rs. {max_loss:,.2f} ({max_loss_pct:.2f}% of portfolio).",
        normal_style
    ))
    
    elements.append(PageBreak())
    
    # ============ PAGE 3: RECOMMENDATIONS ============
    
    elements.append(Paragraph("Key Insights & Recommendations", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    safe_scenarios = (losses <= var_display).sum()
    safe_pct = (safe_scenarios / len(losses)) * 100
    
    elements.append(Paragraph("<b>Risk Assessment:</b>", subheading_style))
    elements.append(Paragraph(
        f"• Daily risk: {var_pct:.2f}% at {confidence}% confidence<br/>"
        f"• Safe scenarios: {safe_pct:.1f}%<br/>"
        f"• Maximum loss: {max_loss_pct:.2f}% of portfolio<br/>"
        f"• Emergency fund needed: Rs. {max_loss:,.0f}",
        normal_style
    ))
    
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Action Items:</b>", subheading_style))
    elements.append(Paragraph(
        f"• Monitor against VaR threshold: Rs. {var_display:,.0f}<br/>"
        f"• Maintain emergency liquidity: Rs. {max_loss:,.0f}<br/>"
        f"• Rebalance quarterly<br/>"
        f"• Review diversification regularly<br/>"
        f"• Test portfolio changes using simulations",
        normal_style
    ))
    
    elements.append(Spacer(1, 0.15*inch))
    
    # Disclaimer
    elements.append(Paragraph(
        "<b>⚠️ DISCLAIMER:</b> Educational purposes only. Past performance ≠ future results. "
        "Consult a financial advisor before investment decisions. "
        "The tool creators are not liable for financial losses.",
        footer_style
    ))
    
    # Build PDF
    doc.build(elements)
    pdf_buffer.seek(0)
    
    return pdf_buffer


def get_pdf_filename():
    """Generate PDF filename with timestamp"""
    return f"Quantfolio_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"