import streamlit as st
from src import texts
from src.data_management import load_deduplicated_data


def page_summary_body():
    # Load data - specify version in data_management.py
    df = load_deduplicated_data()

    # Title
    st.write("## Quick Project Summary")

    # Intro
    st.write(
        """
        This page gives some background information for the project,
        introduces the dataset, defines some key terms and states the
        three business requirements.
        """
    )
    # Link to README file
    st.write(
        """
        - For full details about the project, please read the
        [Project README](https://github.com/lowrycode/hotel-bookings) file.
        """
    )

    # Background Information
    st.divider()
    st.write("### Background Information")
    st.write("The business context is as follows:")
    st.info(
        """
        The client is the **owner of two hotels** in different locations in
        **Portugal**. Both hotels have a relatively **large proportion of
        bookings that are later cancelled** and this has an **impact on the
        operations and profitability** of the hotels. The client wants to
        understand **what factors contribute the most to these
        cancellations** and whether a cancelled booking can **be predicted**.
        """
    )

    # About the Dataset
    st.divider()
    st.write("### About the Dataset")
    st.write(
        """
        The dataset was provided by the client.

        It contains **32 variables** with **79,330 observations of the
        city hotel** and **40,060 observations of the resort hotel**.
        Each observation represents a hotel booking.

        Many **duplicated records** exist (due to group and bulk bookings).
        To avoid skewing the data towards these larger bookings, many
        aspects of the analysis were based on a **cleaned version** of
        the data where **duplicate records** were **aggregated** and
        **counted**.
        """
    )

    # Inspect Data
    with st.expander("Inspect the deduplicated dataset"):
        st.write(
            f"""
            The deduplicated dataset contains **{df.shape[0]:,} individual
            records** and has **{df.shape[1]} variables**. The two
            additional variables are found in the far right columns:
            - **`record_count`**: shows the aggregate count for each record
            - **`is_duplicate`:** distinguishes duplicated records from
            truly unique records
            """
        )
        st.write(
            """
            The first 5 records in the deduplicated dataset (in descending
            "order by `record_count`) are shown below:
            """
        )
        st.write(df.head(5))

    # Project Terms
    st.divider()
    st.write("### Key Terms and Definitions")
    st.info(
        """
        - **Lead Time:** Number of days between the booking date and the
        arrival date.
        - **Average Daily Rate:** Average revenue earned per night per room,
        calculated as total revenue divided by nights stayed.
        - **No-show:** A guest who booked but did not arrive and didn't
        cancel.
        - **Property Management System (PMS):** The software used
        by hotels to manage reservations, guest services, billing and daily
        operations.
        """
    )

    # Business Requirements
    st.divider()
    st.write("### Business Requirements")
    st.write("There are three business requirements.")
    st.success(texts.BUSINESS_REQUIREMENT_1)
    st.warning(texts.BUSINESS_REQUIREMENT_2)
    st.error(texts.BUSINESS_REQUIREMENT_3)
    st.caption(texts.METRIC_DEFINITIONS)

