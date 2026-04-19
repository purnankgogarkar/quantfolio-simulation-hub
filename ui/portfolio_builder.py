import streamlit as st
import pandas as pd
import yfinance as yf
from utils.stock_universe import load_stock_universe


def excel_portfolio_loader():

    file = st.sidebar.file_uploader("Upload Portfolio Excel", type=["xlsx"])

    if file:

        try:
            df = pd.read_excel(file, header=0)
        except Exception as e:
            st.sidebar.error(f"❌ Error reading Excel file: {e}")
            return None

        st.sidebar.info(f"Available columns: {list(df.columns)}")

        df.columns = df.columns.str.strip().str.lower()

        stock_col = None
        qty_col = None

        for col in df.columns:

            if any(keyword in col for keyword in ["stock", "ticker", "symbol"]):
                stock_col = col

            if any(keyword in col for keyword in ["quantity", "qty", "shares"]):
                qty_col = col

        if stock_col is None or qty_col is None:
            st.sidebar.error(f"❌ Could not find required columns")
            st.sidebar.info(f"Expected columns containing: 'Stock/Ticker/Symbol' and 'Quantity/Qty/Shares'")
            st.sidebar.warning(f"Found columns: {list(df.columns)}")
            return None

        stocks = df[stock_col].astype(str).str.upper().str.strip().tolist()

        stocks = [s if ".NS" in s or ".BO" in s else s + ".NS" for s in stocks]

        quantities = df[qty_col].values

        if "uploaded_portfolio" not in st.session_state:
            st.session_state.uploaded_portfolio = None
            st.session_state.uploaded_stocks = stocks
            st.session_state.uploaded_quantities = quantities

        st.sidebar.subheader("📋 Uploaded Portfolio Preview")
        
        preview_df = pd.DataFrame({
            "Stock": stocks,
            "Quantity": quantities
        })
        
        st.sidebar.dataframe(preview_df, use_container_width=True)

        st.sidebar.info(f"Total stocks: {len(stocks)}")

        if st.sidebar.button("✅ Fetch Prices & Verify"):
            
            st.session_state.loading = True

        if st.session_state.get("loading", False):

            with st.spinner("Fetching prices..."):

                prices = []
                valid_stocks = []
                valid_quantities = []

                for idx, s in enumerate(stocks):
                    try:

                        hist = yf.Ticker(s).history(period="5d")

                        if hist.empty:
                            price = None
                        else:
                            price = hist["Close"].iloc[-1]

                    except:
                        price = None
                    
                    if price is not None:
                        prices.append(price)
                        valid_stocks.append(s)
                        valid_quantities.append(quantities[idx])

            portfolio = pd.DataFrame({
                "Stock": valid_stocks,
                "Price": prices,
                "Quantity": valid_quantities
            })

            st.sidebar.subheader("💰 Portfolio with Current Prices")
            
            st.sidebar.dataframe(portfolio, use_container_width=True)

            if len(valid_stocks) < len(stocks):
                excluded_stocks = [s for s in stocks if s not in valid_stocks]
                st.sidebar.warning(f"⚠️ Could not fetch prices for: {', '.join(excluded_stocks)}")
                st.sidebar.info(f"Valid stocks: {len(valid_stocks)}/{len(stocks)}")

            if len(portfolio) == 0:
                st.sidebar.error("❌ No valid stocks found. Please check your portfolio.")
                st.session_state.loading = False
                return None

            st.session_state.uploaded_portfolio = portfolio

            st.sidebar.success("✅ Portfolio verified and ready for simulation!")

            st.session_state.loading = False

            return portfolio

    return None


def manual_portfolio_builder():

    universe = load_stock_universe()

    search = st.sidebar.text_input("Search Stock")

    selected = None

    if search:

        matches = universe[
            universe["Ticker"].str.contains(search.upper())
            | universe["Name"].str.contains(search, case=False)
        ].head(20)

        if len(matches) > 0:

            selected = st.sidebar.selectbox(
                "Suggestions",
                matches["Ticker"] + " — " + matches["Name"]
            )

    if selected:

        ticker = selected.split(" — ")[0]

        qty = st.sidebar.number_input(f"Quantity for {ticker}", min_value=1, value=1)

        if st.sidebar.button("Add Stock"):

            prices = []

            stocks = [ticker]

            for s in stocks:

                try:

                    hist = yf.Ticker(s).history(period="5d")

                    if hist.empty:
                        price = None
                    else:
                        price = hist["Close"].iloc[-1]
                
                except:
                    price = None

                prices.append(price)

            if "portfolio" not in st.session_state:
                st.session_state.portfolio = []

            if prices[0] is not None:
                st.session_state.portfolio.append({
                    "Stock": ticker,
                    "Price": prices[0],
                    "Quantity": qty
                })

                st.sidebar.success(f"✅ Added {ticker}")
            else:
                st.sidebar.error(f"❌ Could not fetch price for {ticker}")

    if "portfolio" in st.session_state and len(st.session_state.portfolio) > 0:

        st.sidebar.subheader("📊 Current Portfolio")
        
        df = pd.DataFrame(st.session_state.portfolio)

        st.sidebar.dataframe(df, use_container_width=True)

        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("Clear All"):
                st.session_state.portfolio = []
                st.rerun()

        with col2:
            if st.button("Finalize Portfolio"):
                st.session_state.finalized = True
                st.sidebar.success("✅ Portfolio ready for simulation!")

        if st.session_state.get("finalized", False):
            return df
        
        return df

    return None


def portfolio_builder():

    st.sidebar.header("Portfolio Builder")

    method = st.sidebar.radio(
        "Portfolio Input Method",
        ["Upload Excel", "Build Portfolio"]
    )

    if method == "Upload Excel":
        result = excel_portfolio_loader()
        
        if result is not None:
            return result
        elif st.session_state.get("uploaded_portfolio") is not None:
            return st.session_state.uploaded_portfolio

    else:
        return manual_portfolio_builder()

    return None