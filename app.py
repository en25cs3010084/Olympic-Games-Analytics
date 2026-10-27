import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Olympic Performance Analysis", page_icon="🏅", layout="wide")
ROOT = Path(__file__).parent
DATA = ROOT / "data"
medals = pd.read_csv(DATA / "country_medals.csv")
sports = pd.read_csv(DATA / "sport_events_demo.csv")

st.title("🏅 Global Olympic Sports Performance Analysis")
st.caption("Interactive exploratory dashboard • selected countries and Olympic editions")
st.warning("Dataset note: country medal figures are a selected-country sample, not the complete official medal table. Sport event counts are demonstration estimates; verify official sources before publication.")

years = sorted(medals["Year"].unique())
selected_years = st.sidebar.multiselect("Olympic year", years, default=years)
country_options = sorted(medals["Country"].unique())
selected_countries = st.sidebar.multiselect("Countries", country_options, default=country_options)
metric = st.sidebar.selectbox("Metric", ["Total", "Gold", "Silver", "Bronze"], index=0)

filtered = medals[medals["Year"].isin(selected_years) & medals["Country"].isin(selected_countries)]
if filtered.empty:
    st.info("Choose at least one year and one country.")
    st.stop()

a,b,c,d = st.columns(4)
a.metric("Countries in selection", filtered["Country"].nunique())
b.metric("Olympic editions", filtered["Year"].nunique())
c.metric(f"{metric} medals (sample)", int(filtered[metric].sum()))
d.metric("Highest selected result", int(filtered[metric].max()))

left, right = st.columns(2)
with left:
    st.subheader(f"{metric} medals by country and year")
    chart_df = filtered.groupby(["Year","Country"], as_index=False)[metric].sum()
    fig = px.bar(chart_df, x="Country", y=metric, color="Year", barmode="group", title=f"{metric} medal comparison")
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Medal composition")
    comp = filtered.groupby("Country", as_index=False)[["Gold","Silver","Bronze"]].sum()
    comp = comp.sort_values("Gold", ascending=False).head(15)
    long_comp = comp.melt(id_vars="Country", var_name="Medal", value_name="Count")
    fig2 = px.bar(long_comp, x="Country", y="Count", color="Medal", barmode="stack", title="Gold, silver and bronze medals")
    fig2.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Performance trend")
trend = filtered.groupby(["Year","Country"], as_index=False)[["Gold","Silver","Bronze","Total"]].sum()
fig3 = px.line(trend, x="Year", y=metric, color="Country", markers=True, title=f"{metric} medals across selected editions")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Sports programme (demonstration dataset)")
sport_years = st.multiselect("Sport programme year", sorted(sports["Year"].unique()), default=sorted(sports["Year"].unique()))
sf = sports[sports["Year"].isin(sport_years)]
fig4 = px.bar(sf, x="Sport", y="Medal_Events", color="Year", barmode="group", title="Estimated medal events by sport")
fig4.update_layout(xaxis_tickangle=-35)
st.plotly_chart(fig4, use_container_width=True)
with st.expander("View filtered medal data"):
    st.dataframe(filtered.sort_values(["Year", metric], ascending=[True, False]), use_container_width=True)
st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"), "filtered_olympic_medals.csv", "text/csv")
st.markdown("---")
st.caption("Created for academic demonstration. Always cite and validate the original data source in the final submission.")
