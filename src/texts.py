BUSINNESS_REQUIREMENT_1 = """
##### **Business Requirement 1:**
The client wants to know the following **insights** from the data:
- a. Which **variables** are most associated with cancellations?
- b. Which **countries** make the most bookings, cancellations, and percentage
cancellations?
- c. Which **travel agents** make the most bookings, cancellations, and
percentage cancellations?
- d. What is the extent of **room type reassignments** and how are these
associated with booking cancellations?
- e. **How far in advanced** are bookings typically cancelled?
They also want to know whether cancellation patterns are **significantly
different in the two hotels**.
"""

BUSINNESS_REQUIREMENT_2 = """
##### **Business Requirement 2:**
The client wants to know whether the data supports the following
**hypotheses**:
- **H1:** Local guests (especially from Portugal) tend to cancel
more than guests from further afield.
- **H2:** Bookings where assigned room types are different from
reserved room types are more likely to lead to cancellations.
- **H3:** Transient party customers who cancel their bookings tend
to cancel closer to the arrival date than other customer types.
"""

BUSINNESS_REQUIREMENT_3 = """
##### **Business Requirement 3:**
The client is interested in determining whether or not a particular
booking will be cancelled.
- **Goal:** Flag bookings that will actually cancel so the hotel can
take proactive action (e.g. overbook, send retention offers, adjust
staffing).
- **Constraint:** The hotel does not want to take action on bookings
that won't cancel (wasting effort or upsetting customers).

The model success metrics are:
- At least **80% Recall on 'Cancel'** (on train and test set)
  - *A high recall is important because missed cancellations leads
to empty rooms and lost revenue.*
- At least **60% Precision on 'Cancel'** (on train and test set)
  - *A high precision is important because false alarms lead to
wasted or harmful interventions.*
"""
