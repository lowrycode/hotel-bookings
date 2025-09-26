import streamlit as st
import pandas as pd
from src import texts
from src.data_management import load_ml_pipeline, load_deduplicated_data
from src.machine_learning.predictive_analysis_ui import predict_cancellation


def page_predict_cancellations_body():
    # Load pipelines and data
    pipeline_dc_fe = load_ml_pipeline("pipeline_data_cleaning_feat_eng.pkl")
    pipeline_clf = load_ml_pipeline("pipeline_clf.pkl")

    # Page Title
    st.write("## Predict Cancellations")

    # Page Intro
    st.write("This page addresses **Business Requirement 3**.")
    if st.checkbox("Show Business Requirement"):
        st.error(texts.BUSINESS_REQUIREMENT_3)
        st.caption(texts.METRIC_DEFINITIONS)

    # Instructions
    st.divider()
    # st.write("##### INSTRUCTIONS:")
    st.info(
        """
        *To **make a prediction**, enter the details below and press the
        **Run Predictive Analysis** button.*
        """
    )

    # Get live data from input panel
    X_live = DrawInputsWidgets()

    # Predict on live data
    if st.button("Run Predictive Analysis"):
        predict_cancellation(X_live, pipeline_dc_fe, pipeline_clf)
        st.divider()


def DrawInputsWidgets():
    """
    Draws input widgets for entering values for the most important features
    and returns a dataframe including these values.
    """
    # load dataset
    df = load_deduplicated_data()

    # Create input widgets for 12 features
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)
    col10, col11, col12 = st.columns(3)

    # create an empty DataFrame, which will be the live data
    X_live = pd.DataFrame([], index=[0])

    # Draw widgets for each feature in original_best_features (from notebook 6)
    with col1:
        feature = "country"
        st_widget = st.selectbox(label=feature, options=df[feature].unique())
    X_live[feature] = st_widget

    with col2:
        feature = "lead_time"
        st_widget = st.number_input(
            label=feature,
            min_value=0,
            max_value=df[feature].max(),
            value=0
        )
    X_live[feature] = st_widget

    with col3:
        feature = "total_of_special_requests"
        st_widget = st.number_input(
            label=feature,
            min_value=0,
            max_value=df[feature].max(),
            value=0
        )
    X_live[feature] = st_widget

    with col4:
        feature = "agent"
        st_widget = st.selectbox(label=feature, options=df[feature].unique())
    X_live[feature] = st_widget

    with col5:
        feature = "required_car_parking_spaces"
        st_widget = st.number_input(
            label=feature, min_value=0, max_value=df[feature].max(), value=0
        )
    X_live[feature] = st_widget

    with col6:
        feature = "customer_type"
        st_widget = st.selectbox(label=feature, options=df[feature].unique())
    X_live[feature] = st_widget

    with col7:
        feature = "stays_in_weekend_nights"
        st_widget = st.number_input(
            label=feature,
            min_value=0,
            max_value=df[feature].max(),
            value=0,
        )
    X_live[feature] = st_widget

    with col8:
        feature = "stays_in_week_nights"
        st_widget = st.number_input(
            label=feature,
            min_value=0,
            max_value=df[feature].max(),
            value=0,
        )
    X_live[feature] = st_widget

    with col9:
        feature = "booking_changes"
        st_widget = st.number_input(
            label=feature, min_value=0, max_value=df[feature].max(), value=0
        )
    X_live[feature] = st_widget

    with col10:
        feature = "record_count"
        st_widget = st.number_input(
            label=feature, min_value=1, max_value=df[feature].max(), value=1
        )
    X_live[feature] = st_widget

    with col11:
        feature = "arrival_date_week_number"
        st_widget = st.number_input(
            label=feature, min_value=1, max_value=df[feature].max(), value=1
        )
    X_live[feature] = st_widget

    with col12:
        feature = "adr"
        st_widget = st.number_input(
            label=feature,
            min_value=0.0,
            max_value=df[feature].max(),
            value=df[feature].median(),
        )
    X_live[feature] = st_widget

    return X_live
