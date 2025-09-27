import streamlit as st
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd


def target_class_summary(
    X_train, y_train, X_test, y_test, pipeline, label_map, target_class
):
    """
    Generate a summary of precision, recall and F1-score for a specific target
    class on both training and test datasets.
    """

    # Model performance on training dataset
    y = y_train
    prediction = pipeline.predict(X_train)

    train_report = classification_report(
        y, prediction, target_names=label_map, output_dict=True
    )
    train_precision = train_report[target_class]["precision"]
    train_recall = train_report[target_class]["recall"]
    train_f1 = train_report[target_class]["f1-score"]

    # Model performance on testing dataset
    y = y_test
    prediction = pipeline.predict(X_test)

    test_report = classification_report(
        y, prediction, target_names=label_map, output_dict=True
    )
    test_precision = test_report[target_class]["precision"]
    test_recall = test_report[target_class]["recall"]
    test_f1 = test_report[target_class]["f1-score"]

    results = {
        "Dataset": ["Train", "Test"],
        "Precision": [
            f"{train_precision:.2f}",
            f"{test_precision:.2f} ({(test_precision - train_precision):.2f})",
        ],
        "Recall": [
            f"{train_recall:.2f}",
            f"{test_recall:.2f} ({(test_recall - train_recall):.2f})",
        ],
        "F1-Score": [
            f"{train_f1:.2f}", f"{test_f1:.2f} ({(test_f1 - train_f1):.2f})"
        ],
    }

    overview = pd.DataFrame(results).set_index("Dataset")
    overview.index.name = None
    st.write(overview)


def confusion_matrix_and_report(X, y, pipeline, label_map):
    """
    Write a confusion matrix and classification report for predictions on the
    given dataset.
    """
    prediction = pipeline.predict(X)

    st.write("---  Confusion Matrix  ---")
    cm = confusion_matrix(y_true=y, y_pred=prediction)
    st.write(
        pd.DataFrame(
            cm,
            index=["Actual " + sub for sub in label_map],
            columns=["Predicted " + sub for sub in label_map],
        )
    )
    st.write("\n")

    st.write("---  Classification Report  ---")
    st.code(classification_report(y, prediction, target_names=label_map), "\n")


def clf_performance(
    X_train,
    y_train,
    X_test,
    y_test,
    pipeline,
    label_map,
    target_class=None,
    summary_only=False,
):
    """
    Evaluate classification performance on train and test datasets,
    with optional focus on a specific target class.
    """

    # Show Summary
    if target_class:
        st.write(f'#### Summary on "{target_class}" class ####')
        target_class_summary(
            X_train, y_train, X_test, y_test, pipeline, label_map, target_class
        )

    else:
        st.write("No target class specified\n")

    # Show Drilldown
    if not summary_only:
        st.write("#### Train Set #### \n")
        confusion_matrix_and_report(X_train, y_train, pipeline, label_map)

        st.write("#### Test Set ####\n")
        confusion_matrix_and_report(X_test, y_test, pipeline, label_map)
