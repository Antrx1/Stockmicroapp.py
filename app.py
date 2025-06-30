import streamlit as st
st.set_page_config(layout="wide", page_title="Market Dashboard")

import finnhub
import time
import chart
import trending

DEFAULT_SYMBOLS = ['SPY', 'QQQ', 'BINANCE:BTCUSDT']
REFRESH_INTERVAL = 10

@st.cache_resource
def get_client():
    with open("api.txt") as f:
        return finnhub.Client(api_key=f.read().strip())

def get_quote(client, symbol):
    data = client.quote(symbol)
    return {
        'symbol': symbol,
        'current': data['c'],
        'change': data['d'],
        'percent': data['dp']
    }

def build_card_html(symbol, quote):
    color = "#00FF00" if quote["change"] >= 0 else "#FF4B4B"
    return f"""
    <div style='
        background-color:#111111;
        color:{color};
        padding:1.5em;
        border-radius:10px;
        width:250px;
        height:150px;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        box-shadow: 0 0 5px #444;
    '>
        <div style='font-size:22px; font-family:monospace; font-weight:bold; color:white'>{symbol}</div>
        <div style='font-size:28px; margin-top:5px'>{quote["current"]:.2f}</div>
        <div style='font-size:16px; margin-top:5px'>netChng: {quote["change"]:+.2f}</div>
    </div>
    """

def show_trending_panel():
    st.markdown("<pre style='font-family:monospace; font-size:18px;'>Most Mentioned Tickers (ApeWisdom)</pre>", unsafe_allow_html=True)
    data = trending.get_api_data()
    if not data:
        st.markdown("<pre style='font-family:monospace;'>No data available.</pre>", unsafe_allow_html=True)
        return

    st.markdown("<pre style='font-family:monospace;'>Rank  Ticker     Name</pre>", unsafe_allow_html=True)
    st.markdown("<pre style='font-family:monospace;'>----------------------------------------------</pre>", unsafe_allow_html=True)
    for item in data[:15]:
        st.markdown(f"<pre style='font-family:monospace; font-size:14px;'>{item['rank']:<5}  {item['ticker']:<10}  {item['name']}</pre>", unsafe_allow_html=True)

def show_dashboard():
    client = get_client()

    if "symbols" not in st.session_state:
        st.session_state.symbols = DEFAULT_SYMBOLS.copy()

    col_main, col_trending = st.columns([3, 1])

    with col_main:
        st.markdown("<pre style='font-size:20px; font-family:monospace;'>Live Watchlist</pre>", unsafe_allow_html=True)
        with st.form("symbol_form"):
            cols = st.columns(len(st.session_state.symbols))
            new_symbols = []
            for i, col in enumerate(cols):
                with col:
                    symbol = col.text_input(f"Symbol {i+1}", value=st.session_state.symbols[i], key=f"input_{i}")
                    new_symbols.append(symbol.strip().upper())
            submitted = st.form_submit_button("Update Symbols")
            if submitted:
                st.session_state.symbols = new_symbols

        card_cols = st.columns(len(st.session_state.symbols))
        for col, symbol in zip(card_cols, st.session_state.symbols):
            try:
                quote = get_quote(client, symbol)
                col.markdown(build_card_html(symbol, quote), unsafe_allow_html=True)
            except:
                col.error(f"Failed: {symbol}")

    with col_trending:
        show_trending_panel()

def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ["Dashboard", "Chart & Financials"])

    if choice == "Dashboard":
        show_dashboard()
    elif choice == "Chart & Financials":
        chart.render_chart_ui()

if __name__ == "__main__":
    main()

