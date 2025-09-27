import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_management import (
    load_deduplicated_data,
    load_all_data,
    load_correlation_matrix,
    load_room_data,
    load_lead_time_data,
    load_image,
    get_percentage_cancelled
)
from src import texts


def page_cancellations_study_body():
    # Load data - specify version in data_management.py
    df = load_deduplicated_data()
    df_all = load_all_data()
    corr_matrix = load_correlation_matrix()
    df_room = load_room_data()
    df_lead = load_lead_time_data()

    # Page Title
    st.write("## Cancellations Study Summary")

    # Intro
    st.write("This page addresses **Business Requirement 1**.")
    if st.checkbox("Show Business Requirement"):
        st.success(texts.BUSINESS_REQUIREMENT_1)

    # Contents
    if st.checkbox("Show Navigation Links", value=True):
        st.write("***Jump to...***")
        st.write(
            """
            - [a. Which variables are most associated with cancellations?](
            #correlation-analysis)
            - [b. Which countries make the most bookings, cancellations and
            percentage cancellations?](#country-analysis)
            - [c. Which travel agents make the most bookings, cancellations
            and percentage cancellations?](#travel-agent-analysis)
            - [d. What is the extent of room type reassignments and how are
            these associated with booking cancellations?](#room-analysis)
            - [e. How far in advance are bookings typically cancelled?](
            #cancellation-lead-time-analysis)
            """
        )

    # Sections addressing each business objective
    section_correlation_study(corr_matrix)
    section_countries(df, df_all)
    section_travel_agents(df, df_all)
    section_rooms(df_room)
    section_cancellation_lead_times(df_lead)


# Page Sections
def section_correlation_study(corr_matrix):
    st.html('<a name="correlation-analysis"></a>')
    st.divider()
    st.write(
        "### a. Which variables are most associated with cancellations?"
    )

    # Overview
    st.write(
        """
        A correlation analysis of the deduplicated dataset was conducted
        across different groups:
        1. Overview using **all** records.
        2. Comparison of **unique vs duplicated** records.
        3. Comparison of **City Hotel vs Resort Hotel**.

        In all cases, **no features were strongly associated with booking
        cancellations** but weak associations were found with some
        variables.
        """
    )
    st.write(
        "Overall, the following associations were observed:"
    )
    st.success(
        """
        Cancellations are **more likely** for bookings:
        - with **longer lead times**
        - made through **Online Travel Agents**
        - with a **non-refundable deposit**
        - with a **higher average daily rate**
        - booked via the **TA/TO distribution channel**
        - made by **transient customers**
        """
    )
    st.error(
        """
        Cancellations are **less likely** for bookings:
        - that require **more car parking spaces**
        - where **no deposit is required**
        - made through **Offline Travel Agents or Tour Operators**
        - including **special requests**
        """
    )
    st.write(
        """
        These findings suggest that many high-risk bookings are already being
        correctly flagged when hotels require non-refundable deposits.
        """
    )

    # Expander - all records
    with st.expander("Analysis of **all** records."):
        st.write(
            """
            The table below shows the **top 10 variables** which are
            **most strongly associated with cancelled bookings** along
            with their **Spearman Correlation Coefficients**.
            """
        )
        st.write(corr_matrix)

    # Expander - duplicated vs unique
    with st.expander("Comparing **duplicated vs unique** records."):
        st.write(
            """
            The plot below shows the Spearman correlation of each variable
            with `is_canceled`, separately for each subset.
            """
        )
        load_image("corr_unique_vs_duplicated.png")
        st.write(
            """
            Although the **strengths** of associations are often different
            in each group, the **direction** of these associations are
            nearly always the same. Therefore, it is not the case that
            correlations in one group are 'cancelling out' correlations in
            the other group.
            """
        )
        st.write(
            """
            *One notable exception is seen when considering the
            `market_segment` 'Groups' category which shows a weakly
            **positive** association with cancellation for **duplicated**
            records but a weakly **negative** association for **unique**
            records. This reflects the different nature of the bookings in
            each subset (e.g. duplicated bookings accounting for group
            bookings or bulk booking behaviours by travel agents).*
            """
        )

    # Expander - city vs hotel
    with st.expander("Comparing **City Hotel vs Resort Hotel**"):
        st.write(
            """
            The plot below shows the Spearman correlation of each variable
            with `is_canceled`, separately for each hotel.
            """
        )
        load_image("corr_city_vs_resort.png")
        st.write(
            """
            Although the **strengths** of associations are often different
            in each group, the **direction** of these associations are
            nearly always the same. Therefore, it is not the case that
            correlations in one group are 'cancelling out' correlations in
            the other group.
            """
        )
        st.write(
            """
            *The exceptions (meal types, room bookings) are very weakly
            associated with cancellation rates and not likely to be
            significant.*
            """
        )


def section_countries(df_deduplicated, df_all):
    st.html('<a name="country-analysis"></a>')
    st.divider()
    st.write(
        "### b. Which countries make the most bookings, cancellations "
        "and percentage cancellations?"
    )

    # - Total Bookings -
    st.write("#### Total Bookings:\n")
    st.write(
        """
        The largest share of bookings comes from **Portuguese guests**.
        These far exceed the number of bookings from **Great Britain** which
        ranks in second place.

        Most bookings are from **European countries**, followed by **USA**
        and **Brazil**.
        """
    )

    # Expander - pie charts
    with st.expander("Show pie charts"):
        # Duplicates counted once
        st.write(
            """
            The first pie chart shows the proportions when **duplicated
            records** are **counted once**. This gives an indication of the
            number of bookings made without giving too much weight to
            group bookings and bulk reservations. Bookings from **Portugal**
            are roughly **3 times higher** than those from **Great Britain**.
            """
        )
        plot_top_categories_pie(
            df=df_deduplicated,
            feature="country",
            top_n=10,
            title=(
                """
                Proportions of Total Bookings by Country (Duplicates counted once)
                """
            ),
            facet_col=None,
        )

        # All duplicates counted
        st.write(
            """
            The second pie chart shows the proportions when **all duplicates
            are counted**. This gives an indication of the **actual** number
            of room reservations made and a measure of the impact on hotel
            operations. Bookings from **Portugal** are roughly **4 times
            higher** than those from **Great Britain**, illustrating that most
            group/bulk bookings originate from Portugal.
            """
        )
        plot_top_categories_pie(
            df=df_all,
            feature="country",
            top_n=10,
            title=(
                """
                Proportions of Total Bookings by Country (All duplicates counted)
                """
            ),
            facet_col=None,
        )

    # - Total Cancellations -
    st.write("")  # add space
    st.write("#### Total Cancellations:\n")
    st.write(
        """
        The number of cancellations made by guests from **Portugal** is
        **much higher** than any other country. When all duplicates are
        counted, the number of cancellations even exceeds the number of
        completed bookings for Portuguese guests.
        """
    )
    st.write(
        """
        Unsurprisingly, most cancellations are from countries that also
        make the most bookings.
        """
    )
    with st.expander("Show pie charts and graphs"):
        # Duplicates counted once
        st.write(
            """
            These pie charts use the **deduplicated dataset** to show
            the proportions of total bookings, both fulfilled (left) and
            cancelled (right), for the top ten countries. This gives an
            indication of the number of cancellations made without giving
            too much weight to group bookings and bulk reservations.
            """
        )
        plot_top_categories_pie(
            df=df_deduplicated,
            feature="country",
            top_n=10,
            title=(
                """
                Cancelled vs Non-Cancelled Bookings By Country (Duplicates counted once)
                """
            ),
            facet_col="is_canceled",
        )

        # All duplicates counted
        st.write(
            """
            These pie charts use **all records (including duplicates)**
            to show the proportions of total bookings, both fulfilled (left)
            and cancelled (right), for the top ten countries. This gives an
            indication of the **actual** number of cancellations made
            and a measure of the impact on hotel operations.
            """
        )
        plot_top_categories_pie(
            df=df_all,
            feature="country",
            top_n=10,
            title=(
                """
                Cancelled vs Non-Cancelled Bookings By Country (All duplicates counted)
                """
            ),
            facet_col="is_canceled",
        )

        # Bar chart comparing
        st.write(
            """
            The chart below allows a comparison between fulfilled and
            cancelled bookings for the top ten countries, both when
            duplicates are counted once (left) and when all duplicates
            are counted (right).
            """
        )
        load_image("top_countries_by_cancellations.png")

    # - Percentage Cancellations -
    st.write("")  # add space
    st.write("#### Percentage Cancellations:\n")
    st.write(
        """
        In this analysis, only countries with a **minimum of 100 total
        bookings** were considered to avoid skewing the data.
        """
    )
    st.write(
        """
        When **all duplicate bookings** are counted, **Portuguese guests**
        have the highest cancellation rate at **58.8%**.
        However, when duplicates are **counted only once**, the cancellation
        rate for Portuguese bookings drops to **37.1%**, and seven other
        countries exceed this figure.
        """
    )
    with st.expander("Show graphs"):
        load_image("top_countries_by_percentage_cancellations.png")


def section_travel_agents(df_deduplicated, df_all):
    st.html('<a name="travel-agent-analysis"></a>')
    st.divider()
    st.write(
        "### c. Which travel agents make the most bookings, cancellations "
        "and percentage cancellations?"
    )

    # - Total Bookings -
    st.write("#### Total Bookings:\n")
    st.write(
        """
        The largest share of reservations from individual agents are booked
        through **Agent 9**. This agent accounts for **more than twice** as
        many bookings as **Agent 240**, which ranks second.

        A **significant percentage** of bookings (~14%) are made either
        **directly** (without an agent) or through an **unspecified agent**.

        Agents **outside the top ten** still account for a **significant share
        of bookings**: **19.6%** when **duplicates are counted once**, rising
        to **26.5%** when **all duplicates** are included.
        """
    )

    # Expander - pie charts
    with st.expander("Show pie charts"):
        # Duplicates counted once
        st.write(
            """
            The first pie chart shows the proportions of bookings by agent
            when **duplicated records** are **counted once**. This gives an
            indication of the number of bookings made without giving too much
            weight to group bookings and bulk reservations.
            """
        )
        plot_top_categories_pie(
            df=df_deduplicated,
            feature="agent",
            top_n=10,
            title=(
                """
                Proportions of Total Bookings by Agent (Duplicates counted once)
                """
            ),
            facet_col=None,
        )

        # All duplicates counted
        st.write(
            """
            The second pie chart shows the proportions of bookings by agent
            when **all duplicates are counted**. This gives an indication of
            the **actual** number of room reservations made and a measure of
            the impact on hotel operations.
            """
        )
        plot_top_categories_pie(
            df=df_all,
            feature="agent",
            top_n=10,
            title=(
                """
                Proportions of Total Bookings by Agent (All duplicates counted)
                """
            ),
            facet_col=None,
        )

    # - Total Cancellations -
    st.write("")  # add space
    st.write("#### Total Cancellations:\n")
    st.write(
        """
        The **largest number of cancellations** are made by the two agents with
        the largest number of **total bookings** (agents **9** and **240**).

        The number of bookings (both cancelled and non-cancelled) **do not
        change drastically** for either of these agents when **all duplicates
        are counted** since only a **small proportion of bookings** by these
        agents are for **groups or large parties**.

        In contrast, the number of bookings (both completed and cancelled)
        shows a **significant rise** for some other agents when **all
        duplicates** are counted. This reflects a higher proportion of
        'Transient-Party' bookings. For **Agent 1**, the number of
        cancellations in this dataset **rises** to such an extent that it
        **almost equals** the number of cancellations made by **Agent 240**.
        """
    )

    # Expander pie charts and graphs
    with st.expander("Show pie charts and graphs"):
        # Duplicates counted once
        st.write(
            """
            These pie charts use the **deduplicated dataset** to show
            the proportions of total bookings, both fulfilled (left) and
            cancelled (right), for the top agents. This gives an
            indication of the number of cancellations made without giving
            too much weight to group bookings and bulk reservations.
            """
        )
        plot_top_categories_pie(
            df=df_deduplicated,
            feature="agent",
            top_n=10,
            title=(
                """
                Cancelled vs Non-Cancelled Bookings By Agent (Duplicates counted once)
                """
            ),
            facet_col="is_canceled",
        )

        # All duplicates counted
        st.write(
            """
            These pie charts use **all records (including duplicates)**
            to show the proportions of total bookings, both fulfilled (left)
            and cancelled (right), for the top agents. This gives an
            indication of the **actual** number of cancellations made
            and a measure of the impact on hotel operations.

            Notice the larger proportions for agent 1.
            """
        )
        plot_top_categories_pie(
            df=df_all,
            feature="agent",
            top_n=10,
            title=(
                """
                Cancelled vs Non-Cancelled Bookings By Agent (All duplicates counted)
                """
            ),
            facet_col="is_canceled",
        )

        # Bar chart comparing
        st.write(
            """
            The charts below allow a comparison between fulfilled and
            cancelled bookings for the top agents, both when
            duplicates are counted once (left) and when all duplicates
            are counted (right).
            """
        )
        load_image("top_agents_by_cancellations.png")

    # - Percentage Cancellations -
    st.write("")  # add space
    st.write("#### Percentage Cancellations:\n")
    st.write(
        """
        In this analysis, only agents with a **minimum of 500 total bookings**
        were considered to avoid skewing the data.
        """
    )
    st.write(
        """
        When **duplicate bookings** are **counted once**, the 3 agents with
        the **highest number of cancelled bookings** (**9**, **240** and **1**)
        also had the **highest percentage cancellations** (in the same order)
        with **similar cancellation rates** (~40%).

        When **all duplicate bookings are counted**, cancellation rates
        **jumped dramatically**. This is due to the **high cancellation rates**
        among **large party bookings**. **Agent 29** had the **highest
        percentage cancellations** with **79.9%**. Many of the agents with the
        highest percentage cancellations in this dataset made a relatively low
        number of bookings (500 to 1000). Only **Agent 1** appeared in the top
        lists for **both datasets**.
        """
    )
    with st.expander("Show graphs"):
        load_image("top_agents_by_percentage_cancellations.png")


def section_rooms(df_room):
    st.html('<a name="room-analysis"></a>')
    st.divider()
    st.write(
        "### d. What is the extent of room type reassignments and how "
        "are these associated with booking cancellations?"
    )

    # - Total Bookings -
    st.write("#### Overview of Room Types:\n")
    st.write(
        """
        This analysis used the **deduplicated dataset**. The data shows that
        **most guests** get assigned the **same room type** as they reserved.

        **Room type A** was the **most commonly reserved and assigned room
        type** in **both hotels**.
        - In the **city hotel**, this room type constituted **over half of all
        reservations** and the vast majority of guests were also **assigned
        this room type**.
        - In the **resort hotel**, a much greater proportion of bookings which
        **reserved room type A** were **assigned a different room type**
        (approximately one third).

        **Room type D** was the **second most commonly reserved and assigned
        room type** in **both hotels**. It also had the **highest number** of
        bookings that were **reassigned from a different room type**.
        """
    )

    # Expander - pie charts
    with st.expander("Show parallel category plots"):
        st.write(
            """
            The **parallel categories plots** below show the proportions of
            reserved and assigned room types, coloured by the assigned
            room type. They also show the extent of room type reassignments.
            """
        )

        # Both hotels
        plot_room_parallel_categegories(
            df=df_room,
            dimensions=['reserved_room_type', 'assigned_room_type'],
            colour_by='reserved_room_type',
            title='Both Hotels'
        )

        # City Hotel
        plot_room_parallel_categegories(
            df=df_room.query("hotel == 'City Hotel'"),
            dimensions=['reserved_room_type', 'assigned_room_type'],
            colour_by='reserved_room_type',
            title='City Hotel'
        )

        # Resort Hotel
        plot_room_parallel_categegories(
            df=df_room.query("hotel == 'Resort Hotel'"),
            dimensions=['reserved_room_type', 'assigned_room_type'],
            colour_by='reserved_room_type',
            title='Resort Hotel'
        )

    # - Percentage Cancellations By Room Type -
    st.write("")  # add space
    st.write("#### Percentage Cancellations By Room Type:\n")
    st.write(
        """
        This analysis used the **deduplicated dataset**.

        When considering rooms which have a **minimum of 50 total bookings**:
        - **City Hotel:** room type **F** had **marginally higher cancellation
        rates** than other room types, both for 'assigned' and 'reserved'
        categories
        - **Resort Hotel:** room types **H** and **G** had **marginally higher
        cancellation rates** than other room types, both for 'assigned' and
        'reserved' categories
        """
    )

    # Expander graphs
    with st.expander("Show graphs"):
        st.write(
            """
            The bars charts below show the percentage cancellations by room
            type, both reserved (left) and assigned (right), for each
            hotel.
            """
        )
        st.write("For the **City Hotel:**")
        load_image("city_percentage_cancellations_by_room.png")

        st.write("For the **Resort Hotel:**")
        load_image("resort_percentage_cancellations_by_room.png")

    # - Percentage Cancellations by Room Type Reassignment -
    st.write("")  # add space
    st.write("#### Percentage Cancellations by Room Type Reassignment:\n")
    st.write(
        """
        Analysing the **deduplicated dataset** shows that roughly **15%** of
        all bookings involve a **room type reassignment**. The figure is
        slightly **lower for the city hotel (11.4%)** and **higher for the
        resort hotel (20.4%)**.

        Bookings **involving room type reassignments** have **much lower**
        percentage cancellation rates (**4.7%** overall) than bookings
        **not involving reassignment** (**32.8%** overall).

        When specific room type reassignments are analysed (e.g.
        reserved A but assigned D), **all of the reassignment categories** with
        more than 50 instances have **very low percentage cancellations**.
        """
    )

    with st.expander("Show graphs and table"):
        # Stacked bar charts
        st.write(
            """
            The percentage of bookings involving room type reassignments are:
            - **City Hotel:** 11.4%
            - **Resort Hotel:** 20.4%
            """
        )
        st.write(
            """
            The bar charts below allow a comparison of cancellation rates for
            bookings involving (and not involving) room types reassignments.
            """
        )
        load_image("room_type_reassignment_by_hotel.png")

        # Dataframe
        st.write(
            """
            The table below shows the percentage cancellations for the top 20
            room type reassignments:
            """
        )
        percent_cancelled_room_changes = get_percentage_cancelled(
            df=df_room.query("is_reassigned == True"),
            feature="reserved_to_assigned",
            target="is_canceled",
            min_total_bookings=0
        )
        st.write(percent_cancelled_room_changes.head(20))


def section_cancellation_lead_times(df_lead):
    st.html('<a name="cancellation-lead-time-analysis"></a>')
    st.divider()
    st.write(
        "### e. How far in advance are bookings typically cancelled?"
    )

    # - Lead Times -
    st.write("#### Overview of Lead Times:\n")
    st.write(
        """
        This analysis used the **deduplicated dataset** to analyse the
        distribution of lead times for different groups.

        **No significant differences** were found when **comparing the two
        hotels**. However, **significant differences** were found across
        **other groups**:
        """
    )
    st.info(
        """
        - **Reservation Status:**
          - Lead times tend to be **larger for cancelled bookings**, although
        guests who do not inform the hotels beforehand (the 'No-Show'
        category) tend to have smaller lead times.
        """
    )
    st.info(
        """
        - **Duplicated bookings:**
          - Lead times tend to be **larger for duplicated bookings** than
        single / unique bookings.
        """
    )
    st.info(
        """
        - **Distribution Channel:**
          - Lead times tend to be **larger for bookings made by travel agents /
        tour operators**.
        """
    )
    st.info(
        """
        - **Market Segment:**
          - Lead times tend to be **larger for group bookings and offline
          travel agents / tour operators**.
        """
    )
    st.info(
        """
        - **Customer Type:**
          - Lead times tend to be **larger for transient party and contract
        customers**.
        """
    )

    # Expander - pie charts
    with st.expander("View distribution plots"):
        st.write(
            """
            The plots below summarise the distribution of lead time for
            different groups.
            """
        )

        # By Hotel
        st.write("##### By Hotel")
        load_image("lead_time_by_hotel.png")
        st.write(
            """
            Similar distributions are observed for each hotel.
            """
        )

        # By Reservation Status
        st.write("##### By Reservation Status")
        load_image("lead_time_by_reservation_status.png")
        st.write(
            """
            Lead times tend to be **larger for cancelled bookings**, although
            guests who do not inform the hotels beforehand (the 'No-Show'
            category) tend to have smaller lead times.
            """
        )

        # Unique vs Duplicate Records
        st.write("##### Unique vs Duplicate Records")
        load_image("lead_time_by_is_duplicate.png")
        st.write(
            """
            **Duplicated bookings** have a **higher median lead time** and
            show a **less pronounced spike in very short lead times** compared
            to single / unique bookings.
            """
        )

        # By Distribution Channel
        st.write("##### By Distribution Channel")
        load_image("lead_time_by_distribution_channel.png")
        st.write(
            """
            Lead times tend to be **larger for bookings made by travel agents
            / tour operators**.
            """
        )

        # By Market Segment
        st.write("##### By Market Segment")
        load_image("lead_time_by_market_segment.png")
        st.write(
            """
            Lead times tend to be **larger for group bookings and offline
            travel agents / tour operators**.
            """
        )

        # By Customer Type
        st.write("##### By Customer Type")
        load_image("lead_time_by_customer_type.png")
        st.write(
            """
            Lead times tend to be **larger for transient party and contract
            customers**.
            """
        )

    # - Fraction of Lead Time Elapsed Before Cancellations -
    st.write("")  # add space
    st.write("#### Fraction of Lead Time Elapsed Before Cancellations:\n")
    st.write(
        """
        This analysis examined **cancelled bookings** using the **deduplicated
        dataset**. However, it **excluded** records for:
        - guests who **did not inform the hotel** of the cancellation (i.e.
        **No-shows**)
        - bookings made and cancelled **on the date they were due to arrive**

        Since bookings have different lead times, a fairer comparison is to
        analyse the **fraction of lead time elapsed before cancellation**.
        This information has been calculated and stored as
        **`frac_lead_time_before_cancel`**:
        - A value **close to zero** means the cancellation was made
        **immediately after the booking was made**
        - A value **close to one** means the cancellation was made
        **immediately before the arrival date**

        Bookings are found to be **cancelled at all stages** between booking
        and arrival dates but tend to **cluster slightly at the two
        extremes**. The overall distributions are **similar for both hotels**
        with a slightly **higher proportion of cancellations shortly after
        booking**.

        Some groups tend to **cancel later** , most notably
        **complementary bookings** and **transient-party bookings**.

        Cancellation patterns seem to be largely random, although specific
        patterns were found in the cancellation timings for **agent 1**.
        These patterns suggest that this agent is making **regular bulk
        bookings** which are later cancelled after designated time periods.
        """
    )

    # Expander - pie charts
    with st.expander("View overall distributions"):
        st.write(
            """
            The histogram below summarises when bookings tend to cancel as
            a fraction of the lead time elapsed.
            """
        )
        load_image("frac_lead_time_before_cancel_distribution.png")
        st.write(
            """
            Here is the same data represented as an empirical cumulative
            distribution function (ECDF) plot.
            """
        )
        load_image("frac_lead_time_before_cancel_ecdf.png")
        st.write(
            """
            When considering all bookings that eventually cancel, **60% have
            cancelled** before getting **40% into the lead time**.

            ***NOTE:*** *This does not mean that 60% of **all bookings** will
            cancel at this stage - the data is considering **cancelled
            bookings** only.*
            """
        )

    with st.expander("View distributions by groups"):
        st.write(
            """
            The plots below summarise when bookings tend to cancel as
            a fraction of the lead time elapsed for different groups.
            """
        )

        # Unique vs Duplicate Records
        st.write("##### Unique vs Duplicate Records")
        load_image("frac_lead_time_by_is_duplicate.png")
        st.write(
            """
            Similar distributions are observed for each group.
            """
        )

        # By Distribution Channel
        st.write("##### By Distribution Channel")
        load_image("frac_lead_time_by_distribution_channel.png")
        st.write(
            """
            Compared to bookings that come through travel agents and tour
            operators, **direct** and **corporate bookings** are **less likely
            to cancel immediately after booking** and **more likely to cancel
            close to the arrival date**.
            """
        )

        # By Market Segment
        st.write("##### By Market Segment")
        load_image("frac_lead_time_by_market_segment.png")
        st.write(
            """
            Compared to bookings that come through travel agents and tour
            operators:
            - **Complementary bookings** tend to cancel **close to arrival**.
            - **Corporate bookings** also show a slight bias towards
            **last-minute cancellations** although there is a **also an early
            spike** in cancellations.

            ***CAUTION:*** *It should be noted that both `Complementary` and
            `Corporate` are minority categories and that these conclusions are
            based on a relatively small number of records (40 and 412
            respectively).*
            """
        )

        # By Customer Type
        st.write("##### By Customer Type")
        load_image("frac_lead_time_by_customer_type.png")
        st.write(
            """
            Compared to other customer groups, **Transient-Party bookings**
            tend to cancel **closer to arrival** with a **significant spike**
            in cancellations **near the arrival date**.
            """
        )

    with st.expander("View patterns for agent 1"):
        st.write(
            """
            The plot below shows the **cancellation patterns** for agent 1.

            The horizontal bands are indicative of **bulk booking behaviour**
            since all bookings within these bands are:
            - **group bookings** of the **same size**
            - booked for the **same hotel** (city)
            - booked on the **same date**
            - booked **far in advance** (>250 days)
            - **cancelled** after a **specific number of days** after booking
            - sharing the **same customer type**
            """
        )
        plot_agent_1_cancellations(df_lead)


# Plotting functions
def plot_top_categories_pie(df, feature, top_n, title, facet_col=None):
    """
    Create a pie chart showing the distribution of the top N categories for a
    given feature, grouping all other categories into "Other". Optionally
    split the chart into facets by another column.
    """

    # Prevent changes to original dataframe
    df = df.copy()

    # Group countries not in top ten as 'Other'
    top_n_items = df[feature].value_counts().head(top_n).index.to_list()
    df["grouped_feature"] = (
        df[feature].astype(str).where(df[feature].isin(top_n_items), "Other")
    )

    # Count values again for the grouped column
    if facet_col:
        grouped_counts = df.groupby(["grouped_feature", facet_col]).size().reset_index()
        grouped_counts.columns = [feature, facet_col, "count"]
    else:
        grouped_counts = df.groupby(["grouped_feature"]).size().reset_index()
        grouped_counts.columns = [feature, "count"]

    # Plot pie chart
    fig = px.pie(
        grouped_counts,
        names=feature,
        values="count",
        color=feature,
        color_discrete_sequence=px.colors.qualitative.Set3,
        title=title,
        facet_col=facet_col,
    )
    # Render in streamlit
    st.plotly_chart(fig)


def plot_total_cancellations_map(df):
    is_cancelled = df["is_canceled"] == 0
    counts = df[is_cancelled]["country"].value_counts().reset_index(name="count")
    counts.columns = ["Country", "Total Cancellations"]

    # Create choropleth
    fig = px.choropleth(
        counts,
        locations="Country",
        color="Total Cancellations",
        hover_name="Country",
        hover_data={"Total Cancellations": True, "Country": False},
        color_continuous_scale="Viridis",
        title="Total Cancellations by Country (duplicates counted once)",
        width=1200,
        height=700,
    )

    # Render in streamlit
    st.plotly_chart(fig)


def plot_room_parallel_categegories(df, dimensions, colour_by, title):
    # Encode colour_by category as int (for using with colour scale)
    data = df.copy()
    data['colour_by_encoded'], uniques = pd.factorize(data[colour_by])

    # Generate plot
    fig = px.parallel_categories(
        data,
        dimensions=dimensions,
        color='colour_by_encoded',
        color_continuous_scale=px.colors.qualitative.Set1,
    )

    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        margin=dict(l=50, r=50, t=80, b=50),
        coloraxis_showscale=False
    )

    # Render in streamlit
    st.plotly_chart(fig)


def plot_agent_1_cancellations(df_lead):
    fig = px.scatter(
        data_frame=df_lead.query("agent == '1'"),
        x="lead_time",
        y="cancel_days_after_booking",
        color="customer_type",
        hover_data=[
            "agent",
            "hotel",
            "market_segment",
            "customer_type",
            "record_count",
            "booking_date",
            "arrival_date"
        ],
        opacity=0.5,
        size="record_count",
        size_max=10
    )

    # Optional: adjust size
    fig.update_layout(
        width=1200,
        height=600,
        title=(
            "Lead Time vs Days After Booking That Cancellation Was Made "
            "for Agent 1 (size=record_count)"
        )
    )

    # Render in streamlit
    st.plotly_chart(fig)
