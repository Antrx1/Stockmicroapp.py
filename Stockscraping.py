import requests
import time
import streamlit as st

API_URL = "https://apewisdom.io/api/v1.0/filter/all"

def get_api_data():
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            st.error(f"Error: Received status code {response.status_code}")
    except requests.exceptions.Timeout:
        st.error("Error: The request timed out.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
    return []

def display_top_tickers(data):
    if not data:
        st.write("No data available.")
        return

    # Header
    st.markdown("<pre style='font-family:monospace; font-size:20px;'>Top 15 Trending Tickers</pre>", unsafe_allow_html=True)
    st.markdown("<pre style='font-family:monospace; font-size:14px;'>Rank  Ticker     Name</pre>", unsafe_allow_html=True)
    st.markdown("<pre style='font-family:monospace;'>----------------------------------------------</pre>", unsafe_allow_html=True)

    # Display top 15
    for item in data[:15]:
        st.markdown(
            f"<pre style='font-family:monospace; font-size:14px;'>{item['rank']:<5}  {item['ticker']:<10}  {item['name']}</pre>",
            unsafe_allow_html=True
        )

def app():
    st.set_page_config(page_title="ApeWisdom Trending Tickers")
    st.markdown("<pre style='font-family:monospace; font-size:26px;'>Trending Tickers Dashboard</pre>", unsafe_allow_html=True)
    st.markdown("Live feed of the most mentioned tickers on social platforms (source: ApeWisdom.io)")

    while True:
        data = get_api_data()
        display_top_tickers(data)
        st.markdown("<pre style='font-family:monospace;'>Refreshing in 1 hour...</pre>", unsafe_allow_html=True)
        time.sleep(3600)
        st.rerun()

if __name__ == "__main__":
    app()

