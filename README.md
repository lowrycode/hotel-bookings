# Hotel Booking Cancellations

This **Data Science** and **Machine Learning** project explores the **Hotel Booking Demand** dataset from Kaggle, with the goal of understanding booking patterns and predicting whether a reservation will be cancelled.

![Hotel Booking Demand](readme-images/hotels.jpg)

The project includes:
- **Exploratory Data Analysis (EDA):** uncovering insights into booking behaviours and factors associated with cancellations.
- **Data Visualisation:** using various plots to reveal and communicate patterns in the data.
- **Data Preprocessing & Feature Engineering:** handling missing values, encoding categorical variables and preparing the data for modelling.
- **Predictive Modelling:** building and evaluating machine learning classifiers to predict the likelihood of a booking being cancelled.
- **Dashboard Design & Deployment:** communicating findings with stakeholders and deploying a machine learning–powered tool for predicting cancellations.

You can visit the deployed dashboard <a href="https://hotel-booking-cancellations-2cb42c1135d0.herokuapp.com/" target="_blank" rel="noopener">**here**</a>.
 



# About the Dataset

The dataset is sourced from <a href="https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand/" target="_blank" rel="noopener">**Kaggle**</a> and is made available with an **Attribution 4.0 International License**.

The data is originally from the article <a href="https://www.sciencedirect.com/science/article/pii/S2352340918315191" target="_blank" rel="noopener">**Hotel Booking Demand Datasets**</a>, written by Nuno Antonio, Ana Almeida, and Luis Nunes for **Data in Brief, Volume 22** (Feb 2019). It was downloaded and cleaned by Thomas Mock and Antoine Bichat for <a href="https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-02-11" target="_blank" rel="noopener">**#TidyTuesday**</a> during the week of 11th Feb 2020. The version on Kaggle is based on this cleaned data.

The dataset contains data that was compiled from **two different hotels** in Portugal; one is a **resort hotel** and the other is a **city hotel**. Since this is **real hotel data**, all identifying information relating to the specific hotels and customers have been removed by the original authors.

The dataset contains **32 variables** with **79,330 observations of the city hotel** and **40,060 observations of the resort hotel**. Each observation represents a hotel booking, although there are many duplicated observations which likely relate to group / bulk bookings. *A justification of this assumption can be found on the first page of the deployed dashboard under the 'About the Dataset' section.*

The data focuses on bookings that were due to arrive between the **1st July 2015** and **31st August 2017**, including bookings that effectively arrived and bookings that were cancelled.


<details>
  <summary>Dataset variable details</summary>

|variable                       |description |
|:------------------------------|:-----------|
|hotel                          |'Resort Hotel' or 'City Hotel' |
|is_canceled                    |If the booking was cancelled (1) or not (0) |
|lead_time                      |Number of days between entering the booking into the PMS and the arrival date |
|arrival_date_year              |Year of arrival date |
|arrival_date_month             |Month of arrival date |
|arrival_date_week_number       |Week number of year for arrival date |
|arrival_date_day_of_month      |Day number of month for arrival date |
|stays_in_weekend_nights        |Number of weekend nights (Saturday or Sunday) the guest stayed or booked to stay at the hotel |
|stays_in_week_nights           |Number of week nights (Monday to Friday) the guest stayed or booked to stay at the hotel |
|adults                         |Number of adults |
|children                       |Number of children |
|babies                         |Number of babies |
|meal                           |Type of meal plan: <br> Undefined/SC – no meal package;<br>BB – Bed & Breakfast; <br> HB – Half board (breakfast and one other meal – usually dinner); <br> FB – Full board (breakfast, lunch and dinner) |
|country                        |Country of origin (ISO format) |
|market_segment                 |Market segment designation. In categories, the term "TA" means "Travel Agents" and "TO" means "Tour Operators" |
|distribution_channel           |Booking distribution channel. The term "TA" means "Travel Agents" and "TO" means "Tour Operators" |
|is_repeated_guest              |Value indicating if the booking name was from a repeated guest (1) or not (0) |
|previous_cancellations         |Number of previous bookings that were cancelled by the customer prior to the current booking |
|previous_bookings_not_canceled |Number of previous bookings not cancelled by the customer prior to the current booking |
|reserved_room_type             |Code of room type reserved. Code is presented instead of designation for anonymity reasons |
|assigned_room_type             |Code for the type of room assigned to the booking. Sometimes the assigned room type differs from the reserved room type due to hotel operation reasons (e.g. overbooking) or by customer request. Code is presented instead of designation for anonymity reasons |
|booking_changes                |Number of changes/amendments made to the booking from the moment the booking was entered on the PMS until the moment of check-in or cancellation|
|deposit_type                   |Indication on if the customer made a deposit to guarantee the booking:<br>No Deposit – no deposit was made;<br>Non Refund – a deposit was made in the value of the total stay cost;<br>Refundable – a deposit was made with a value under the total cost of stay. |
|agent                          |ID of the travel agency that made the booking |
|company                        |ID of the company/entity that made the booking or responsible for paying the booking. ID is presented instead of designation for anonymity reasons |
|days_in_waiting_list           |Number of days the booking was in the waiting list before it was confirmed to the customer |
|customer_type                  |Type of booking:<br>Contract - when the booking has an allotment or other type of contract associated to it;<br>Group – when the booking is associated to a group;<br>Transient – when the booking is not part of a group or contract, and is not associated to another transient booking;<br>Transient-party – when the booking is transient, but is associated to at least one other transient booking|
|adr                            |Average Daily Rate as defined by dividing the sum of all lodging transactions by the total number of staying nights |
|required_car_parking_spaces    |Number of car parking spaces required by the customer |
|total_of_special_requests      |Number of special requests made by the customer (e.g. twin bed or high floor)|
|reservation_status             |Reservation last status:<br>Canceled – booking was cancelled by the customer;<br>Check-Out – customer has checked in but already departed;<br>No-Show – customer did not check-in and did inform the hotel of the reason why |
|reservation_status_date        |Date at which the last status was set. This variable can be used in conjunction with reservation_s_tatus to understand when the booking was cancelled or when the customer checked-out of the hotel|

***NOTE:*** *The American spelling of 'canceled' is used in this dataset. To ensure consistency with the original dataset and to avoid potential confusion, feature names have not been changed to the British spelling.*

</details>

# Business Scenario

Since a real-world machine learning project is driven by the business requirements of the client, a fictitious business scenario has been developed for the purposes of this project.

The scenario is as follows:
> *The client is the **owner of two hotels** in different locations in **Portugal**. Both hotels have a relatively **large proportion of bookings that are later cancelled** and this has an **impact on the operations and profitability** of the hotels. The client wants to understand **what factors contribute the most to these cancellations** and whether a cancelled booking can **be predicted**.*


# Business Requirements

## Business Requirement 1

The client wants to know the following insights from the data:
- a. Which **variables** are most associated with cancellations?
- b. Which **countries** make the most bookings, cancellations, and percentage cancellations?
- c. Which **travel agents** make the most bookings, cancellations, and percentage cancellations?
- d. What is the extent of **room type reassignments** and how are these associated with booking cancellations?
- e. **How far in advance** are bookings typically cancelled?

They also want to know whether cancellation patterns are **significantly different in the two hotels**.

## Business Requirement 2

The client wants to know whether the data supports the following hypotheses:
> **Hypothesis 1:** Local guests (especially from Portugal) tend to cancel more than guests from further afield.

> **Hypothesis 2:** Bookings where assigned room types are different from reserved room types are more likely to lead to cancellations.

> **Hypothesis 3:** Transient party customers who cancel their bookings tend to cancel closer to the arrival date than other customer types.

## Business Requirement 3

The client is interested in determining whether or not a particular booking will be cancelled and the **probability of cancellation**:
- **Goal:** Flag bookings that will actually cancel so the hotel can take proactive action (e.g. overbook, send retention offers, adjust staffing).
- **Constraint:** The hotel does not want to take action on bookings that won’t cancel (wasting effort or upsetting customers).

The model success metrics are:
- At least **80% Recall on 'Cancel'** (on train and test set)
  - *A high recall is important because missed cancellations leads to empty rooms and lost revenue.*
- At least **60% Precision on 'Cancel'** (on train and test set)
  - *A high precision is important because false alarms lead to wasted or harmful interventions.*

The client has expressed that the model should have value in predicting cancellations of:
1. **New bookings** when they are **first entered into the PMS**
2. **Existing bookings** as the **arrival date approaches**


# Mapping Business Requirements to Tasks

## **Business Requirement 1:** Data Exploration, Data Visualisation and Correlation Study

For each aspect of the business requirement, here are the key tasks:
- a. Conduct a **correlation study** (Spearman) to find out which **variables** are most associated with cancelled bookings.
- b. Analyse bookings and cancellations as they relate to the various **countries** and visualise the data using **pie charts**, **bar charts** and **maps**.
- c. Analyse bookings and cancellations as they relate to the various **travel agents** and visualise the data using **pie charts** and **bar charts**.
- d. Analyse the data relating to **room type bookings and assignments** and visualise the extent and impact of reassignments (on cancellations) using **parallel category plots** and **bar charts**.
- e. Analyse the data relating to **lead times and the timings of cancellations** and visualise the **distributions** for various groups using **histograms**, **box plots** and **kde plots**.

Each of the analyses above should also show any similarities or differences between the two hotels.

## **Business Requirement 2:** Testing and Validating Hypotheses

These closely relate to some aspects of business requirement 1.
- **Hypothesis 1:**
  - Relates to business requirement **1b**.
  - Analysis of **total cancellations** and **percentage cancellations** by country will reveal trends.
  - Summarising these findings using a **map** will help to see if there is a **relationship between proximity and cancellations**.
- **Hypothesis 2:**
  - Relates to business requirement **1d**.
  - **Creating a flag** showing if the room type was reassigned will allow comparison between the two categories.
  - This flag allows for a **correlation study** to be conducted.
- **Hypothesis 3:**
  - Relates to business requirement **1e**.
  - Using information from existing variables, we can calculate when a cancellation was made and **how many days before arrival** the cancellation was made.
  - Since different bookings have **different lead times**, it would also be beneficial to compare the **fraction of lead time that elapsed** before cancelling the booking.
  - The **distributions** of these derived variables could be compared using **histograms**, **box plots** and **kde plots**.

In addition to the above, it will often be necessary to assess the **statistical significance** of any differences observed between groups (i.e. can we reject the null hypothesis).

## **Business Requirement 3:** Binary Classification Model

Since we want to predict whether a booking will be cancelled or not, this is a binary classification task.

Key elements of the workflow include:
- Developing a data cleaning pipeline
- Developing a feature engineering pipeline
- Training various classification models and evaluating performance
- Hyperparameter optimisation
- Assessing feature importance and streamlining the pipeline
- Building the full ML pipeline ready for use in production

# ML Business Case Assessment

The following questions were asked to clarify the needs of the client and the extent to which machine learning is required to meet the business objectives.

## 1. What are the business requirements?
- **Business Requirement 1:** To understand patterns in the data, particularly as they relate to booking cancellations.
- **Business Requirement 2:** To understand whether the 3 hypotheses (stated above) are supported by the data.
- **Business Requirement 3:** To have a machine learning dashboard to accurately predict whether a future booking will be cancelled and the probability of cancellation.

## 2. Is there any business objective that can be answered with conventional data analysis?
- Yes, the first 2 objectives

## 3. Does the client need a dashboard or an API endpoint?
- Dashboard

## 4. What does the client consider as a successful project outcome?
- A running dashboard which
  - summarises the patterns found in the data (Business Requirement 1)
  - illustrates how the data supports (or doesn't support) the three hypotheses (Business Requirement 2)
  - includes a cancellation predictor where live data (new or existing bookings) can be used as an input to make accurate real-time predictions as to whether a booking will be cancelled

## 5. Can you break down the project into Epics and User Stories?
- Yes - according to the ML lifecycle steps:
  - Information gathering and data collection
  - EDA, data visualisation, cleaning and preparation
  - Model training, evaluation and optimisation
  - Dashboard planning, design and development
  - Dashboard deployment and release

## 6. Ethical or Privacy concerns?
- The client removed identifying information about the hotels and individual customers from the dataset

*(In a real-world case, the client would probably provide the data under a non-disclosure agreement and the project would not be hosted in a public repository)*

## 7. Does the data suggest a particular model?
- Classifier for predicting 'Cancel' or 'No Cancel'

## 8. What are the model's inputs and intended outputs?
- **Inputs:** live booking information
- **Outputs:** predict 'Cancellation is likely' or 'Cancellation is unlikely' with a percentage probability of cancellation

## 9. What are the criteria for the performance goal of the predictions?
- **Recall:** 80% on 'Cancel'
- **Precision:** 60% on 'Cancel'

## 10. How will the client benefit?
- Gain insights into booking data, especially as it relates to cancellations
- Be able to accurately predict future cancellations so can make informed decisions to minimise losses


# Dashboard Design Plan

## Page 1: Quick project summary
- Background Information (business context)
- About the Dataset
- Key Terms & Definitions
- Business Requirements

## Page 2: Bookings and Cancellations Study
- Intro with business requirement 1 and navigation links
- Sections for analysis of each question

## Page 3: Hypotheses and Validation
- Intro with business requirement 2 and navigation links
- Sections for analysis of each hypothesis

## Page 4: ML Predict Cancellations
- Intro with business requirement 3 and instructions for using Cancellation Predictor
- Cancellation Predictor
  - Widgets and 'Run predictive analysis' button
  - Prediction outcome (displayed immediately below button)

## Page 5: ML Pipeline - Overview & Performance
- Intro with business requirement 3
- Preprocessing steps
- Pipelines
  - data cleaning and feature engineering
  - feature scaling and modelling
- Features
  - Original features used to train model
  - Transformed features used to train model
  - Feature importance plot
- Pipeline performance
  - Summary of recall and precision scores
  - Drilldown analysis


# Unfixed Bugs

There are no known bugs remaining.

***NOTE:*** *Some Jupyter notebooks **purposely** raise an error when a versioned outputs folder already exists. This is not a bug. It is intended to ensure that the notebook **doesn't run any subsequent cells** without the user first checking that they want to proceed and prevents accidentally overwriting historic files.*


# Deployment with Heroku

The App live link is: https://hotel-booking-cancellations-2cb42c1135d0.herokuapp.com/ 

Before deploying, set the Python version in a `.python-version` file to a [Heroku-24](https://devcenter.heroku.com/articles/python-support#supported-runtimes) stack currently supported version. *This project used python version 3.12.*

The `Procfile` and `setup.sh` files are required for Heroku deployment. They tell Heroku how to run the Streamlit app and ensure the environment is set up correctly.

The project can be deployed to Heroku using the following steps.
1. Log in to Heroku and create an App
2. At the Deploy tab, select GitHub as the deployment method.
3. Select your repository name and click Search. Once it is found, click Connect.
4. Select the branch you want to deploy, then click Deploy Branch.
5. The deployment process should happen smoothly if all deployment files are fully functional. Click on the button Open App on the top of the page to access your App.
6. If the slug size is too large then add large files not required for the app to the .slugignore file.

***NOTE:*** *Only the packages required for the streamlit dashboard should be included in the requirements.txt file or the maximum slug size will be exceeded.*


# Main Data Analysis and Machine Learning Libraries

The following packages were used in **production**:
- **feature_engine 1.9.3**
  - for feature engineering and preprocessing pipelines
- **joblib 1.5.1**
  - for saving and loading the fitted pipelines
- **numpy 2.1.3**
  - for fast numerical computing and array operations
- **pandas 2.3.2**
  - for data manipulation and analysis with DataFrames
- **plotly 6.3.0**
  - for creating interactive plots and visualisations
- **scikit-learn 1.7.1**
  - for machine learning models and evaluation tools
- **streamlit 1.49.1**
  - for building the dashboard

These additional packages were used in **development**:
- **kaggle 1.7.4.5**
  - for retrieving dataset via Kaggle API
- **imbalanced-learn 0.14.0**
  - for handling target imbalance with SMOTE
- **matplotlib 3.10.0**
  - for creating data visualisations
- **pingouin 0.5.5**
  - for statistical testing
- **seaborn 0.13.2**
  - for data visualisation (built on matplotlib)
- **statsmodels 0.14.5**
  - for statistical modeling and hypothesis testing
- **xgboost 3.0.5**
  - for XGBClassifier algorithm
- **ydata-profiling 4.16.1**
  - for exploratory data analysis and profiling report

These packages were required to run the notebooks locally on a **windows machine**:
- pywin32 311
- pywinpty 3.0.0


# Additional Notes

The project was developed locally on a windows machine and then checked for cross-platform compatibility using a GitHub Codespace.

When running notebook 6 (`06_classification_model.ipynb`), the classification model gave better results when trained on the windows machine than in the GitHub codespace. This is presumably due to the way that various python packages are implemented in the different operating systems. The dashboard uses the model that was trained locally on the windows machine.


# Credits 

This project reuses and adapts certain functions from the Code Institute *Churnometer* walkthrough project. Appropriate acknowledgements are included in the notebooks where these functions appear.

The images at the top of this README were generated using the [Deep AI Image Generator](https://deepai.org/machine-learning-model/text2img).
 

# Acknowledgements

This project was developed as part of the **Full Stack Developer Course** at <a href="https://codeinstitute.net/" target="_blank" rel="noopener">**Code Institute**</a> and was submitted as my fifth and final portfolio project. I would like to thank my mentor <a href="https://www.linkedin.com/in/precious-ijege-908a00168/" target="_blank" rel="noopener">**Precious Ijege**</a> for his encouragement and advice throughout the course.