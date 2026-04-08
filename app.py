import streamlit as st
import plotly.graph_objects as go
from engine import StockEngine

# 1. Setup & API Key
# Get your free key at: https://www.alphavantage.co/support/#api-key
API_KEY = "YOUR_API_KEY_HERE" 
engine = StockEngine(API_KEY)

st.set_page_config(page_title="Pro Stock Dashboard", layout="wide")

# 2. Sidebar Navigation
st.sidebar.header("Dashboard Controls")
ticker = st.sidebar.text_input("Stock Ticker", value="AAPL").upper()
run_query = st.sidebar.button("Update Dashboard")

# 3. Main Dashboard Logic
if run_query or ticker:
    with st.spinner(f'Fetching data for {ticker}...'):
        overview = engine.get_company_overview(ticker)
        prices = engine.get_daily_prices(ticker)
        news = engine.get_stock_news(ticker)

    if prices is not None and 'Name' in overview:
        # Header Section
        st.title(f"{overview['Name']} ({ticker})")
        st.caption(f"{overview['Exchange']} | {overview['Sector']} | {overview['Industry']}")

        # Row 1: Key Performance Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Market Cap", f"${int(overview['MarketCapitalization']):,}")
        m2.metric("P/E Ratio", overview['PERatio'])
        m3.metric("52W High", f"${overview['52WeekHigh']}")
        m4.metric("Dividend Yield", f"{overview['DividendYield']}%")

        # Row 2: Interactive Price Chart
        st.subheader("Price Action (Last 100 Days)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=prices.index, y=prices['close'], 
                                 fill='tozeroy', name='Close Price',
                                 line=dict(color='#00d1b2', width=2)))
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

        # Row 3: News Feed & Company Bio
        col_bio, col_news = st.columns([1, 2])
        
        with col_bio:
            st.subheader("About")
            st.write(overview['Description'][:600] + "...")
        
        with col_news:
            st.subheader("Latest Market News")
            if news:
                for article in news:
                    sentiment = article.get('overall_sentiment_label', 'Neutral')
                    sent_color = "green" if "Bullish" in sentiment else "red" if "Bearish" in sentiment else "gray"
                    
                    st.markdown(f"**[{article['title']}]({article['url']})**")
                    st.markdown(f":{sent_color}[Sentiment: {sentiment}] | Source: {article['source']}")
                    st.divider()
            else:
                st.info("No recent news found.")
    else:
        st.error("Error: Could not retrieve data. You may have hit the 25-request daily limit.")