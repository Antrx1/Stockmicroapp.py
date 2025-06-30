# chart.py
import streamlit as st
import pandas as pd
import plotly.express as px
from polygon import RESTClient
from datetime import datetime, timedelta

with open("apip.txt") as f:
    polygon_api_key = f.read().strip()

client = RESTClient(polygon_api_key)

def render_chart_ui():
    st.title("Financial Analysis")
    ticker = st.sidebar.text_input("Stock ticker (e.g. AAPL)", "AAPL")
    button = st.sidebar.button("Submit")

    if button:
        try:
            if 'stock_types' not in st.session_state:
                st.session_state.stock_types = client.get_ticker_types(asset_class='stocks')
            if 'exchanges' not in st.session_state:
                st.session_state.exchanges = client.get_exchanges(asset_class='stocks')

            info = client.get_ticker_details(ticker)
            st.subheader(f"{ticker} - {info.name}")

            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=30)

            history = client.list_aggs(ticker, 1, 'day', start_date, end_date, limit=50)
            chart_data = pd.DataFrame(history)
            chart_data['timestamp'] = pd.to_datetime(chart_data['timestamp'], unit='ms') 
            chart_data['date'] = chart_data['timestamp'].dt.strftime('%Y-%m-%d')

            price_chart = px.line(chart_data, x='date', y='close', width=1000, height=400, line_shape='spline')
            price_chart.update_layout(xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(price_chart)

            col1, col2, col3 = st.columns(3)

            def format_value(value):
                suffixes = ["", "K", "M", "B", "T"]
                suffix_index = 0
                while value >= 1000 and suffix_index < len(suffixes) - 1:
                    value /= 1000
                    suffix_index += 1
                return f"${value:.1f}{suffixes[suffix_index]}"

            def get_stock_type(code):
                for stock_type in st.session_state.stock_types:
                    if stock_type.code == code:
                        return stock_type.description
                return None

            def get_exchange_name(code):
                for exchange in st.session_state.exchanges:
                    if exchange.mic == code:
                        return exchange.name
                return None

            stock_info = [
                ("Stock Info", "Value"),
                ("Type", get_stock_type(info.type)),
                ("Primary Exchange", get_exchange_name(info.primary_exchange)),
                ("Listing Date", info.list_date),
                ("Market Cap", format_value(info.market_cap)),
                ("Employees", f"{info.total_employees:,}"),
                ("Website", info.homepage_url.replace("https://", ""))
            ]
            col1.dataframe(pd.DataFrame(stock_info[1:], columns=stock_info[0]), width=400, hide_index=True)

            agg = client.get_previous_close_agg(ticker)
            price_info = [
                ("Price Info", "Value"),
                ("Prev Day Close", f"${agg[0].close:.2f}"),
                ("Prev Day Open", f"${agg[0].open:.2f}"),
                ("Prev Day High", f"${agg[0].high:.2f}"),
                ("Prev Day Low", f"${agg[0].low:.2f}"),
                ("Volume", f"{agg[0].volume:,}"),
                ("VW Avg Price", f"${agg[0].vwap:.2f}")
            ]
            col2.dataframe(pd.DataFrame(price_info[1:], columns=price_info[0]), width=400, hide_index=True)

            fin = client.vx.list_stock_financials(ticker, sort='filing_date', order='desc', limit=2)
            for item in fin:
                break
            fin_metrics = [
                ("Financial Metrics", "Value"),
                ("Fiscal Period", item.fiscal_period + " " + item.fiscal_year),
                ("Total Assets", format_value(item.financials.balance_sheet.assets.value)),
                ("Total Liabilities", format_value(item.financials.balance_sheet.liabilities.value)),
                ("Revenues", format_value(item.financials.income_statement.revenues.value)),
                ("Net Cash Flow", format_value(item.financials.cash_flow_statement.net_cash_flow.value)),
                ("Basic EPS", f"${item.financials.income_statement.basic_earnings_per_share.value}")
            ]
            col3.dataframe(pd.DataFrame(fin_metrics[1:], columns=fin_metrics[0]), width=400, hide_index=True)

        except Exception as e:
            st.error(f"Error: {e}")

