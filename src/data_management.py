import streamlit as st
import pandas as pd

# Define the version used (so use files from the correct outputs directory)
VERSION = 'v1'


# Functions for loading data
@st.cache_data
def load_deduplicated_data(version=VERSION):
    df = pd.read_csv(
        f"outputs/{version}/datasets/cleaned/cleaned_deduplicated.csv"
    )
    return df


@st.cache_data
def load_all_data(version=VERSION):
    df = pd.read_csv(
        f"outputs/{version}/datasets/cleaned/cleaned_all_records.csv"
    )
    return df


@st.cache_data
def load_correlation_matrix(version=VERSION):
    df = pd.read_csv(
        f"outputs/{version}/datasets/cleaned/correlation_matrix.csv",
        index_col=0
    )
    return df


@st.cache_data
def load_room_data(version=VERSION):
    df = pd.read_csv(
        f"outputs/{version}/datasets/cleaned/rooms.csv"
    )
    return df


@st.cache_data
def load_lead_time_data(version=VERSION):
    df = pd.read_csv(
        f"outputs/{version}/datasets/cleaned/lead_times.csv"
    )
    return df


# Functions for loading images
def load_image(filename, version=VERSION):
    filepath = f"outputs/{version}/images/{filename}"
    st.image(filepath)
