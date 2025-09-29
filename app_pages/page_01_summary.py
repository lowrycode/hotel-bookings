import streamlit as st
from src import texts
from src.data_management import load_deduplicated_data, load_image


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

    # Analysis of Duplicated Records
    with st.expander("View analysis of duplicated records"):
        st.write(
            """
            *Since the dataset contains a large number of duplicates, it
            is important for the purposes of this project to understand
            the **nature of these duplicate records**. In a real-world
            scenario, a **discussion would be had** with the client to gain
            an understanding of the **hotel administrative workflows** and
            whether record IDs (which were previously removed to protect
            anonymity) **confirm that these duplicates cannot be attributed
            to errors in collating the data**. Since this is not possible,
            an analysis of the duplicates has been conducted.*
            """
        )
        st.write("#### Interpreting Duplicate Records")
        st.write(
            """
            Nearly all of the duplicate records have **less than 30 exact
            duplicates** with the **vast majority having between 1 and 5
            duplicates**. It is not implausible that a small number of
            **independent** reservations could have identical information,
            especially if the hotels are large and bookings were made in
            response to advertised special offers. However, it is **highly
            unlikely** that **more than 5 *independent* bookings** should have
            exactly the same information.

            The analysis below suggests that records with high numbers
            of duplicates can most likely be explained by the **booking
            behaviours of travel agents**. It is highly likely that
            these bookings were made by travel agents to **secure
            availability** and then **later cancelled** if not needed.

            The following analysis explains the evidence in support of
            this conclusion.
            """
        )

        st.write("##### Analysis of Top Ten Duplicated Records")
        st.write(
            """
            The top ten records with the most number of duplicates are shown
            below:
            """
        )
        st.write(df.head(10))
        st.write(
            """
            The following similarities are observed:
            - same hotel (City)
            - all were cancelled
            - short stays (1 to 3 nights) predominantly mid-week
            - no children or babies
            - same meal type (BB)
            - all booked through travel agents or corporate organisations
            - none are repeated guests
            - same reserved and assigned room type (A)
            - no booking changes
            - non refundable deposits
            - three from the same agent (37)
            - no special requests

            These are most likely all **group bookings or bulk reservations**
            where each room is recorded as a **separate record** and the rooms
            were later **cancelled in bulk**. This theory is supported by the
            fact that all of the records above have
            **deposit_type='Non Refund'** - this is a **minority class** in
            the context of the whole dataset and suggests that the hotel may
            already be **expecting these bookings to be cancelled**.

            ***NOTE:*** *Only half of these records have been assigned as
            'Groups' under **`market_segment`** with others preferring to
            label them as Offline bookings from travel agents. Perhaps the
            offline bookings were also group bookings or perhaps they
            represent travel agents making bulk reservations to secure the
            rooms.*
            """
        )

        st.write(
            """
            ##### Analysis by Grouping Duplicates by record_count
            """
        )
        st.write(
            """
            Certain **patterns emerge** when records are **categorised**
            according to the **number of duplicates**. It is **highly
            unlikely** that these patterns would be observed if duplicate
            records were the result of **random data collation errors**.
            """
        )
        st.write(
            """
            In analysing the **market segments** for each category, 'Groups'
            and 'Offline TA/TO' become more prominant in the larger duplicate
            categories which supports the theory that duplicate records are
            largely group bookings by travel agents.
            """
        )
        load_image("market_segments_by_dup_category.png")
        st.write(
            """
            The **cancellation rate increases** with the level of duplication.
            This also suggests that the duplicates are **not random
            errors in the data collation process** but likely relate to
            **real booking behaviour and administrative workflows**.
            """
        )
        load_image("cancellations_by_dup_category.png")

        st.write("##### Overall Conclusion")
        st.write(
            """
            Some of the duplicates **may still be the result of errors** when
            collating the data. However, the evidence above suggests that these
            duplicates should be **understood to be group or bulk bookings**,
            and **this is assumed** for the rest of the analysis that follows.
            """
        )

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
