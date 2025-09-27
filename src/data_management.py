import streamlit as st
import pandas as pd
import joblib

# Define the version used (so use files from the correct outputs directory)
VERSION = "v1"


# Functions for loading data
@st.cache_data
def load_all_data(version=VERSION):
    return load_cleaned_data('cleaned_all_records.csv', version)


@st.cache_data
def load_deduplicated_data(version=VERSION):
    return load_cleaned_data('cleaned_deduplicated.csv', version)


@st.cache_data
def load_correlation_matrix(version=VERSION):
    df = pd.read_csv(
        f"outputs/{version}/datasets/cleaned/correlation_matrix.csv",
        index_col=0)
    return df


@st.cache_data
def load_cleaned_features_data(version=VERSION):
    return load_cleaned_data('cleaned_features.csv', version)


@st.cache_data
def load_lead_time_data(version=VERSION):
    return load_cleaned_data('lead_times.csv', version)


@st.cache_data
def load_percentage_cancellations_by_country_data(version=VERSION):
    return load_cleaned_data(
        'percentage_cancellations_by_country_deduplicated.csv', version)


@st.cache_data
def load_room_data(version=VERSION):
    return load_cleaned_data('rooms.csv', version)


# Helper function for loading cleaned datasets
@st.cache_data
def load_cleaned_data(filename, version):
    df = pd.read_csv(f"outputs/{version}/datasets/cleaned/{filename}")
    return df


# Functions for loading images
def load_image(filename, version=VERSION):
    filepath = f"outputs/{version}/images/{filename}"
    st.image(filepath)


# Function for loading pipelines
def load_ml_pipeline(filename, version=VERSION):
    filepath = f"outputs/{version}/ml_pipelines/{filename}"
    return joblib.load(filename=filepath)


# Helper functions
def get_percentage_cancelled(df, feature, target, min_total_bookings=0):
    """
    Calculate total bookings and percentage cancellations for each group of a
    specified feature. Optionally apply a minimum bookings threshold, and
    return a dataframe summarizing results sorted by cancellation percentage.

    This function assumes `target` is the column `is_canceled` with boolean
    categories (True = cancelled, False = not cancelled).
    """

    # Get counts
    counts = (
        df.groupby([feature, target], observed=False)
        .size().reset_index(name="count"))
    counts = (
        counts.pivot(index=feature, columns=target, values="count").fillna(0))
    counts.columns.name = None

    # Add total bookings and % cancelled
    summary = counts.copy()
    summary["Total Bookings"] = summary.sum(axis=1).astype("int")
    summary["% Cancelled"] = round(
        summary[True] / summary["Total Bookings"] * 100, 1)

    # Filter for relevant columns
    summary = summary[["Total Bookings", "% Cancelled"]]

    # Filter out countries with total bookings below a threshold
    condition = summary["Total Bookings"] >= min_total_bookings
    summary = summary[condition]

    # Sort and display
    summary.sort_values("% Cancelled", ascending=False, inplace=True)
    return summary
