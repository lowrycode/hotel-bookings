import streamlit as st


def predict_cancellation(X_live, pipeline_dc_fe, pipeline_model):
    # Apply pipeline for data cleaning and feature engineering to live data
    X_live_dc_fe = pipeline_dc_fe.transform(X_live)

    # Predict cancellation
    prediction = pipeline_model.predict(X_live_dc_fe)
    prediction_proba = pipeline_model.predict_proba(X_live_dc_fe)

    # Display results
    prob = prediction_proba[0][1]*100
    if prediction == 1:
        st.error(
            "##### ⚠️ Cancellation is **likely**\n"
            f"Probability of Cancellation: **{prob.round(1)}%**"
        )
    else:
        st.success(
            "##### ✅ Cancellation is **unlikely**\n"
            f"Probability of Cancellation: **{prob.round(1)}%**"
        )

    return prediction
