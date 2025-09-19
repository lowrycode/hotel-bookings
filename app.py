from app_pages.multipage import MultiPage

# Load pages scripts
from app_pages.page_01_summary import page_summary_body
from app_pages.page_02_cancellations_study import page_cancellations_study_body
from app_pages.page_03_project_hypothesis import page_project_hypothesis_body
from app_pages.page_04_predict_cancellations import page_predict_cancellations_body
from app_pages.page_05_ml_pipeline import page_ml_pipeline_body

# Create an instance of the app
app = MultiPage(app_name="Hotel Bookings")

# Add app pages
app.add_page("01 Quick Project Summary", page_summary_body)
app.add_page("02 Bookings and Cancellations Study", page_cancellations_study_body)
app.add_page("03 Hypotheses and Validation", page_project_hypothesis_body)
app.add_page("04 ML Predict Cancellations", page_predict_cancellations_body)
app.add_page("05 ML Pipeline - Overview & Performance", page_ml_pipeline_body)

# Run the app
app.run()
