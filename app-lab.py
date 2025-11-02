import streamlit as st
import pandas as pd

st.set_page_config(page_title="California Housing Data (1990)", layout="wide")

def load_data():
    df = pd.read_csv("housing.csv")
    df = df.dropna(subset=["latitude", "longitude", "median_house_value", "median_income", "ocean_proximity"])
    return df

df = load_data()

st.title("California Housing Data (1990) by Liu Yimeng")
st.caption("See more filters in the sidebar:")

st.subheader("Filter by Median House Price")
price_range = st.slider(
    label="Minimal Median House Price",
    min_value=0,
    max_value=500001,
    value=200000,
    step=1000
)

with st.sidebar:
    st.header("Other Filter Options")
    
    location_types = st.multiselect(
        label="Choose the location type",
        options=["NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"],
        default=["NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"]
    )
    
    income_level = st.radio(
        label="Select Income Level",
        options=["Low", "Medium", "High"],
        index=1
    )

filtered_df = df[(df["median_house_value"] >= price_range) & 
                 (df["ocean_proximity"].isin(location_types))]

if income_level == "Low (≤2.5)":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_level == "Medium (>2.5 & <4.5)":
    filtered_df = filtered_df[(filtered_df["median_income"] > 2.5) & 
                             (filtered_df["median_income"] < 4.5)]
else:
    filtered_df = filtered_df[filtered_df["median_income"] > 4.5]

st.subheader("Housing Data Map")
st.map(
    data=filtered_df[["latitude", "longitude", "median_house_value"]],
    zoom=5
)

with st.expander("View Filtered Data (Sample)"):
    st.dataframe(filtered_df.head(10))