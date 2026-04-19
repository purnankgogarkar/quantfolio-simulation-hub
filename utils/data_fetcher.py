import yfinance as yf
import pandas as pd
import streamlit as st


def fetch_price_data(stocks):
    """
    Fetch historical price data for stocks with intelligent NaN handling.
    
    Args:
        stocks: List of stock tickers
        
    Returns:
        DataFrame with cleaned price data
        
    Raises:
        ValueError: If insufficient data available
    """
    
    try:
        # Download data for all stocks
        data = yf.download(stocks, period="1y", progress=False)["Close"]
        
        # Handle single stock case (returns Series instead of DataFrame)
        if isinstance(data, pd.Series):
            data = data.to_frame(name=stocks[0])
        
        # Store original stock count
        original_stocks = set(data.columns)
        
        # Step 1: Remove completely empty columns (100% NaN)
        data = data.dropna(axis=1, how='all')
        
        # Step 2: Forward fill then backward fill for missing values (handles gaps in trading)
        data = data.fillna(method='ffill').fillna(method='bfill')
        
        # Step 3: Remove rows with ANY NaN (across all stocks)
        data = data.dropna(axis=0, how='any')
        
        # Step 4: Identify excluded stocks
        remaining_stocks = set(data.columns)
        excluded_stocks = original_stocks - remaining_stocks
        
        # Step 5: Validate data quality
        if data.shape[0] < 50:
            raise ValueError(f"Not enough historical data for simulation. Only {data.shape[0]} trading days available.")
        
        if len(remaining_stocks) == 0:
            raise ValueError("No valid stock data could be fetched. Please check stock tickers.")
        
        # Step 6: Warn if stocks were excluded
        if excluded_stocks:
            warning_msg = f"⚠️ Warning: Could not fetch sufficient data for {len(excluded_stocks)} stock(s): {', '.join(sorted(excluded_stocks))}"
            st.warning(warning_msg)
            print(f"Excluded stocks: {excluded_stocks}")
        
        # Log successful fetch
        print(f"Successfully fetched data for {len(remaining_stocks)} stocks: {sorted(remaining_stocks)}")
        print(f"Data shape: {data.shape[0]} trading days × {len(remaining_stocks)} stocks")
        
        return data
    
    except Exception as e:
        error_msg = f"Error fetching price data: {str(e)}"
        st.error(error_msg)
        raise ValueError(error_msg)


def validate_portfolio_alignment(portfolio_df, downloaded_stocks):
    """
    Validate that portfolio stocks match downloaded data and handle mismatches.
    
    Args:
        portfolio_df: Portfolio DataFrame with stocks
        downloaded_stocks: List of stocks in downloaded data
        
    Returns:
        Tuple of (aligned_portfolio_df, valid_stocks, excluded_stocks)
    """
    
    portfolio_stocks = set(portfolio_df["Stock"].values)
    downloaded_set = set(downloaded_stocks)
    
    # Find matches and mismatches
    valid_stocks = portfolio_stocks & downloaded_set
    excluded_stocks = portfolio_stocks - downloaded_set
    
    # Filter portfolio to only include valid stocks
    aligned_df = portfolio_df[portfolio_df["Stock"].isin(valid_stocks)].copy()
    
    # Warn user about excluded stocks
    if excluded_stocks:
        warning_msg = f"⚠️ Excluding {len(excluded_stocks)} stock(s) due to insufficient data: {', '.join(sorted(excluded_stocks))}"
        st.warning(warning_msg)
    
    return aligned_df, list(valid_stocks), list(excluded_stocks)