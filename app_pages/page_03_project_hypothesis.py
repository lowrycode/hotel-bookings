import streamlit as st
import plotly.express as px
from src.data_management import (
    load_room_data,
    load_percentage_cancellations_by_country_data,
    load_image,
    get_percentage_cancelled
)
from src import texts


def page_project_hypothesis_body():
    # Load data - specify version in data_management.py
    df_country = load_percentage_cancellations_by_country_data()
    df_room = load_room_data()

    # Page Title
    st.write("## Hypotheses and Validation")

    # Page Intro
    st.write("This page addresses **Business Requirement 2**.")
    if st.checkbox("Show Business Requirement"):
        st.warning(texts.BUSINESS_REQUIREMENT_2)

    # Contents
    if st.checkbox("Show Navigation Links", value=True):
        st.write("***Jump to...***")
        st.write(
            """
            - [Hypothesis 1](#section-hypothesis-1)
            - [Hypothesis 2](#section-hypothesis-2)
            - [Hypothesis 3](#section-hypothesis-3)
            """
        )

    # Sections addressing each business objective
    section_hypothesis_1(df_country)
    section_hypothesis_2(df_room)
    section_hypothesis_3()


# Page Sections
def section_hypothesis_1(df_country):
    st.html('<a name="section-hypothesis-1"></a>')
    st.divider()
    st.write("### Hypothesis 1")
    st.write(
        """
        The hypothesis states:
        - ***"Local guests (especially from Portugal) tend to cancel more than
        guests from further afield."***
        """
    )
    st.warning(
        """
        This hypothesis is **supported to some extent**.
        """
    )

    # - Evidence -
    st.write("")
    st.write("##### Evidence:")
    st.success(
        """
        The following evidence **supports the hypothesis**:
        - For the **resort hotel**, **Portugal** ranks as the country with
        the **highest percentage cancellations**.
        - When **all duplicate reservations are counted**, **Portugal** has
        the **highest percentage cancellations overall** (for both hotels).
        """
    )
    st.error(
        """
        However, the data **does not support the hypothesis** in the following
        ways:
        - When **duplicate reservations are counted once**, Portuguese guests
        are **not the most likely to cancel** for the **City hotel**, although
        they **remain among the top 10 countries** with the highest
        cancellation rates.
        - Many of the countries with the **highest cancellation rates** are
        for guests from countries that are **very far away** (such as
        **China**, **Russia**, **South Korea** and **Colombia**).
        """
    )

    # - Analysis -
    # Top Countries for Percentage Cancellations
    with st.expander("View analysis overview"):
        # Disclaimer
        st.write(
            """
            *In this analysis, only countries with a **minimum of 100 total
            bookings** were considered to avoid skewing the data.*
            """
        )

        # Duplicates counted once vs all duplicates counted
        st.write(
            """
            The bar charts show two perspectives:
            - **With duplicates included (right chart):**
              - Portugal ranks as the country with the **highest percentage
            of cancellations**.
              - This **supports** the hypothesis.
            - **With duplicates counted only once (left chart):**
              - Portugal falls to **8th place** in percentage cancellations.
              - This **weakens** the hypothesis.
            """
        )
        load_image("top_countries_by_percentage_cancellations.png")

        # Map view
        st.write(
            """
            The map shows the **percentage cancellations** for each country
            when **duplicates are counted once:**
              - There is **not a clear relationship** between **proximity** to
              the hotels (in Portugal) and the **percentage cancellations**.
              - This **weakens** the hypothesis.
            """
        )
        plot_cancellations_map(df_country)

    # Top Countries for Percentage Cancellations by hotel
    with st.expander("View analysis by hotel"):
        # Disclaimer
        st.write(
            """
            *In this analysis, only countries with a **minimum of 100 total
            bookings** were considered to avoid skewing the data.*
            """
        )

        # Duplicates counted once
        st.write(
            """
            The bar charts below show the countries with the **highest
            percentage of cancellations** for each hotel when **duplicates are
            counted once**.
              - Although Portugal ranks in **1st place** for the **resort
              hotel**, it falls to **4th place** for the **city hotel**.
              - This evidence **weakens the hypothesis**.
            """
        )
        load_image("top_countries_for_percentage_cancellations_by_hotel_deduplicated.png")

        # All duplicates counted
        st.write(
            """
            These bar charts show the countries with the **highest percentage
            of cancellations** for each hotel when **all duplicates are
            counted**.
              - Portugal ranks in **1st place** for **both hotels**.
              - This evidence **strengthens the hypothesis**.
            """
        )
        load_image("top_countries_for_percentage_cancellations_by_hotel_all.png")

    # - Overall -
    st.write("")
    st.write("##### Overall:")
    st.write(
        """
        There is **not a linear relationship** between **distance
        from Portugal** and **cancellations rates** but Portugal ranks as the
        country with the **highest percentage of cancellations** when **all
        duplicated bookings** are counted.
        """
    )


def section_hypothesis_2(df_room):
    st.html('<a name="section-hypothesis-2"></a>')
    st.divider()
    st.write("### Hypothesis 2")
    st.write(
        """
        The hypothesis states:
        - ***"Bookings where assigned room types are different from reserved
        room types are more likely to lead to cancellations."***
        """
    )
    st.error(
        """
        This hypothesis is **not supported**. In fact, the opposite is
        found to be the case.
        """
    )

    # - Evidence -
    st.write("")
    st.write("##### Evidence:")
    st.write(
        """
        The data shows a **statistically significant association** between
        room type reassignments and **lower cancellation rates**.
        """
    )

    # - Analysis -
    with st.expander("View analysis"):
        st.write(
            """
            *This analysis used the **deduplicated dataset**.*
            """
        )

        # Percentage Cancellations by Room Type Reassignment
        st.write("##### Percentage Cancellations by Room Type Reassignment")
        st.write(
            """
            Percentage cancellations are much lower for bookings with
            reassigned room types.
            """
        )
        percent_cancelled = get_percentage_cancelled(
            df_room,
            "is_reassigned",
            "is_canceled",
            min_total_bookings=0
        )
        percent_cancelled.index.name = ""
        percent_cancelled.index = percent_cancelled.index.map(
            {True: "Reassigned", False: "Not Reassigned"}
        )
        st.write(percent_cancelled)

        # Analysis by Hotel
        st.write("##### Analysis by Hotel")
        st.write(
            """
            The bar charts below allow a comparison of cancellation rates for
            bookings involving (and not involving) room types reassignments
            for each hotel.
            """
        )
        load_image("room_type_reassignment_by_hotel.png")

        # Correlation Analysis
        st.write("##### Correlation Analysis")
        st.write(
            """
            A **correlation analysis** reveals that there is a **negative
            association** between **room type reassignment** and
            **cancellation rates**, indicating that bookings with a room
            type reassignment are **less likely to be cancelled**.

            A **chi-square test of independence** confirms that this
            association is **statistically significant**. The strength of
            the association is considered to be **weak** with a **Cramér's
            V of 0.22**.
            """
        )

    # - Overall -
    st.write("")
    st.write("##### Overall:")
    st.write(
        """
        Bookings with room type reassignments have much **lower cancellation
        rates**.

        While this may suggests that offering guests a different room type
        can help secure bookings, the effect **may be influenced by other
        factors** such as the nature of the reassignment (e.g. upgrades)
        and guest characteristics (e.g. guests with flexible preferences).

        **Further analysis controlling for these factors would be needed**
        in order to confirm whether reassignment itself directly reduces
        cancellations.
        """
    )


def section_hypothesis_3():
    st.html('<a name="section-hypothesis-3"></a>')
    st.divider()
    st.write("### Hypothesis 3")
    st.write(
        """
        The hypothesis states:
        - ***"Transient party customers who cancel their bookings tend to
        cancel closer to the arrival date than other customer types."***
        """
    )
    st.success(
        """
        This hypothesis **is supported** by the data.
        """
    )

    # - Evidence - Days before arrival -
    st.write("")
    st.write("##### Evidence:")
    st.write(
        """
        When considering the **absolute timings** of cancellations for
        bookings that were made **before the arrival date**:
        """
    )
    st.success(
        """
        - **Transient-Party** customers tend to cancel **closer to the arrival
        date** than other customer types
        - Statistical tests confirm that these differences are significant.
        - **Transient-Party** customers cancel a median of **19 days before
        arrival**, compared with **26 days for Contract**, **36 days for
        Group** and **43 days for Transient** customers.
        """
    )

    # - Analysis -
    with st.expander(
        "View analysis for number of days before arrival that "
        "cancellations were made"
    ):
        st.write(
            """
            *This analysis used the **deduplicated dataset**.*
            """
        )

        # Distributions
        st.write("##### Comparing Distributions")
        st.write(
            """
            When considering the raw number of days before arrival that
            bookings were cancelled:
            - **Transient-Party bookings** tend to cancel **closer to
            arrival** than other customer types.
            - **Mann-Whitney U tests** confirm that the differences in
            distributions are **statistically significant**.
            """
        )
        load_image("cancel_days_before_arrival_by_customer_type.png")

        # Medians
        st.write("##### Comparing Medians")
        st.write(
            """
            When considering the median values:
            - **Transient-Party** customers cancel **19 days before arrival**
            on average.
            - This is lower than other customer types: **26.5 days for
            Contract**, **36 days for Group** and **43 days for Transient**.
            """
        )

    # - Evidence - Fraction of lead time elapsed -
    st.write("")
    st.write(
        """
        When considering the **fraction of lead time elapsed** before
        cancellations for bookings that were made **before the arrival date**:
        """
    )
    st.success(
        """
        - **Transient-Party** customers **cancel proportionally later** than
        other customer types.
        - Statistical tests confirm that these differences are significant.
        - Their median fraction of elapsed lead time before cancellation is
        **0.75**, compared with **0.40 for Contract**, **0.24 for Transient**
        and **0.20 for Group** customers.
        - Moreover, the distribution shows a **marked spike in cancellations
        close to arrival** among **Transient-Party** customers, which is not
        observed for other customer types.
        """
    )

    # - Analysis -
    with st.expander(
        "View analysis for fraction of lead time elapsed before "
        "cancellations were made"
    ):
        st.write(
            """
            *This analysis used the **deduplicated dataset**.*
            """
        )

        # Distributions
        st.write("##### Comparing Distributions")
        st.write(
            """
            Compared to other customer groups:
            - **Transient-Party bookings** tend to cancel **closer to
            arrival** with a **significant spike** in cancellations
            **near the arrival date**.
            - **Mann-Whitney U tests** confirm that the differences in
            distributions are **statistically significant**.
            """
        )
        load_image("frac_lead_time_by_customer_type.png")

        # Medians
        st.write("##### Comparing Medians")
        st.write(
            """
            When considering the median values for **fraction of lead time
            elapsed before cancellation**:
            - **Transient-Party** customers have a median value of **0.75**
            - This is significantly higher than any other customer type:
            **0.40 for Contract**, **0.24 for Transient** and **0.20 for
            Group**.
            """
        )

    # - Evidence - No Shows and Same-Day bookings -
    st.write("")
    st.write(
        """
        **NOTE:** The analysis above **excluded No-shows and
        same-day bookings**. A separate analysis for this group reveals that:
        """
    )
    st.error(
        """
        - **Transient-Party** customers make up only a **small minority** of
        the cancellations.
        - Most of the cancellations for this group are attributed to
        **Transient** customers.
        """
    )

    # - Analysis -
    with st.expander("View analysis for No-shows and same day bookings"):
        st.write(
            """
            *This analysis used the **deduplicated dataset** to examine
            **no-shows**, as well as reservations that were both **booked and
            cancelled on the arrival date**.*
            """
        )
        st.info(
            """
            These categories were **not included** in the main analysis
            because:
            - No-shows **never formally cancelled** their booking.
            - Same-day bookings have a **lead time of zero**, so cannot be
            analysed using fraction of lead time elapsed.
            - They both constitute a **small percentage of the total records**
            in the dataset: **6.8% for same-day bookings** and **1.1% for
            No-shows**.
            """
        )

        st.write(
            """
            In both cases, the **majority of bookings** were made by
            **Transient** customers, while **Transient-Party** customers
            accounted for a **smaller proportion**.
            """
        )
        load_image("customer_types_same_day_vs_no_shows.png")

    # - Overall -
    st.write("")
    st.write("##### Overall:")
    st.write(
        """
        These findings suggest that bookings by **Transient-Party** customers
        present a **higher risk to operations and revenue** when compared with
        other customer types since the later cancellations mean less time to
        reallocate the rooms. Hotels may need to **adapt cancellation
        policies**, **refine overbooking strategies** and **strengthen
        pre-arrival engagement** with this type of customer.
        """
    )


def plot_cancellations_map(df_country):
    # Create choropleth
    fig = px.choropleth(
        df_country,
        locations='country',
        color='% Cancelled',
        hover_name='country',
        hover_data={'country': False, '% Cancelled': True},
        color_continuous_scale='Viridis',
        title=(
            "Percentage Cancellations by Country "
            "(minimum reservations=100, duplicates counted once)"
        ),
        width=800,
        height=500
    )

    # Render in streamlit
    st.plotly_chart(fig)
