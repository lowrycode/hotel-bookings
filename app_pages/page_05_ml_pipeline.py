import streamlit as st
from src import texts
from src.data_management import (
    load_ml_pipeline,
    load_cleaned_features_data,
    load_X_train_data,
    load_y_train_data,
    load_X_test_data,
    load_y_test_data,
    load_image,
)
from src.machine_learning.evaluate_clf import clf_performance


def page_ml_pipeline_body():
    # Load pipelines and data
    pipeline_dc_fe = load_ml_pipeline("pipeline_data_cleaning_feat_eng.pkl")
    pipeline_clf = load_ml_pipeline("pipeline_clf.pkl")
    cleaned_features = load_cleaned_features_data()
    X_train = load_X_train_data()
    y_train = load_y_train_data()
    X_test = load_X_test_data()
    y_test = load_y_test_data()

    # Page Title
    st.write("## Pipeline - Overview & Performance")

    # Page Intro
    st.write(
        """
        This page addresses the technical aspects relating to "
        **Business Requirement 3**.
        """
    )
    if st.checkbox("Show Business Requirement"):
        st.error(texts.BUSINESS_REQUIREMENT_3)
        st.caption(texts.METRIC_DEFINITIONS)

    # - Preprocessing Steps -
    st.divider()
    st.write("### Preprocessing Steps")

    st.write("##### Prevent Data Leakage")
    st.write(
        """
        The dataset contained many **duplicate observations** caused by
        group and bulk bookings. To **avoid data leakage**, duplicates
        were aggregated **before** splitting into training and test sets.
        A new feature, **`record_count`**, was introduced to capture the
        number of identical reservations. This feature was later found to
        have predictive power during modelling.

        Two original features (`reservation_status` and
        `reservation_status_date`) were also **removed prior to splitting**,
        as they **directly relate to the target variable** (`is_canceled`)
        and would otherwise lead to leakage.
        """
    )

    st.write("##### Tailor Model to Use Cases")
    st.write(
        """
        The client has expressed that the model should have value in
        predicting cancellations of:
        1. **New bookings** when they are **first entered into the PMS**
        2. **Existing bookings** as the **arrival date approaches**

        Therefore, to make the model valuable for both use cases, the
        following decisions were made:
        """
    )
    st.write(
        """
        ###### **Features to drop:**
        """
    )
    st.info(
        """
        - **arrival_date_year:** Future years will never have been seen
        during training so the model would struggle to generalise reliably.
        - **deposit_type:** Decisions around which type of deposit
        to require for a particular booking may later be based on the
        outcome of the model prediction.
        - **previous_cancellations** & **previous_bookings_not_canceled:**
        These values may not be known at the time when the booking is
        first entered into the PMS.
        """
    )
    st.write(
        """
        ###### **Features to Keep:**
        """
    )
    st.info(
        """
        - **booking_changes:** At the time of the booking, the value will
        default to zero but since the feature could hold valuable information
        in predicting cancellations of existing bookings, it has been retained.
        """
    )

    # - Pipelines -
    st.write("### Pipelines")
    st.write("There are 2 ML Pipelines arranged in series.")

    st.write("##### Pipeline 1: for data cleaning and feature engineering.")
    st.write(pipeline_dc_fe)

    st.write("##### Pipeline 2: for feature scaling and modelling.")
    st.write(pipeline_clf)

    # - Features -
    st.divider()
    st.write("### Features")
    st.write(
        """
        The model was trained on the following **original features**
        (+ **`record_count`**):
        """
    )
    st.write(cleaned_features.columns.to_list())
    st.info(
        """
        
        
        """
    )


    st.write(
        """
        Following processing of these original features (by the first
        pipeline), the following **transformed features** were used for
        training the classification model:
        """
    )    
    st.write(X_train.columns.to_list())

    st.write(
        """
        The plot below shows the 12 most important transformed features:
        """
    )    
    load_image('feature_importance.png')

    # - Pipeline Performance -
    st.divider()
    st.write("### Pipeline Performance")
    st.write("*The **business goals** were:*")
    st.info(
        """
        - **Recall:** At least **0.80** on 'Cancel' class
        - **Precision:** At least **0.60** on 'Cancel' class
        """
    )

    st.write("*The **ML pipeline achieved**:*")
    st.success(
        """
        - **Recall:**
          - **0.85 on train** dataset and **0.82 on test** dataset
        - **Precision:**
          - **0.62 on train** dataset and **0.60 on test** dataset
        """
    )

    # View Pipeline Evaluation on train and test set
    with st.expander("View pipeline evaluation on train and test set"):
        clf_performance(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            pipeline=pipeline_clf,
            label_map=['No Cancel', 'Cancel'],
            target_class='Cancel',
            summary_only=False
        )


