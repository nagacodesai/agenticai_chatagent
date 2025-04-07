import streamlit as st
from tariffagent import TariffAgent
from ui_controls import *

st.set_page_config(page_title="Trade Tariff Advisor 🌍", layout="wide")
st.title("Trade Tariff Advisor 🌍")

# Load data
agent = TariffAgent(data_source="tariff.csv")

# Chat at top
st.markdown("---")
render_chat_panel(agent)

# Controls for country selection and top N
control_col1, control_col2 = st.columns([2, 2])
with control_col1:
    selected_countries = st.multiselect("🌍 Select countries to explore:", agent.get_country_list(), default=["All Countries"])
with control_col2:
    top_n = st.radio("Show top countries", [10, 20, 50, "All"], horizontal=True)

# Filter Data
filtered_data = agent.get_data_by_country(selected_countries)
top_data = filtered_data if top_n == "All" else filtered_data.sort_values(by="TariffsCharged2USA", ascending=False).head(int(top_n))

# Summary
display_name = (
    "multiple countries" if "All Countries" in selected_countries or len(selected_countries) > 1
    else selected_countries[0]
)
render_summary(display_name)
st.markdown("<div style='margin-top: -2.5rem;'></div>", unsafe_allow_html=True)

# Charts Block
with st.container():
    render_tariff_info(agent, selected_countries)
    st.markdown("<div style='margin-top: -1rem;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        render_top_tariffs_chart(top_data)
    with col2:
        render_top_reciprocal_tariffs_chart(top_data)

    render_grouped_comparison_chart(top_data)
