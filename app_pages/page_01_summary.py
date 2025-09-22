import streamlit as st
from src import texts


def page_summary_body():
    # Title
    st.write("## Quick Project Summary")

    # Intro
    st.write(
        """
        This page introduces the **Key Terms and Definitions**
        and states the three **Business Requirements** for the project.
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
        """
    )

    # Link to README file
    st.write(
        """
        - For additional information, please read the
        [Project README file](https://github.com/lowrycode/hotel-bookings).
        """
    )
    st.divider()

    # Business Requirements
    st.write("### Business Requirements")
    st.write("There are 3 different business requirements.")
    st.success(texts.BUSINNESS_REQUIREMENT_1)
    st.warning(texts.BUSINNESS_REQUIREMENT_2)
    st.error(texts.BUSINNESS_REQUIREMENT_3)

    st.caption(
        """
        - **Recall on 'Cancel':** Of all the bookings that actually
        cancelled, how many were caught?
        - **Precision on 'Cancel':** Of all the bookings we predicted as
        cancelled, how many really cancelled?
        """
    )
