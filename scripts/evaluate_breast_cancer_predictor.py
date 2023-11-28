# evaluate_breast_cancer_classifier.py
# author: Tiffany Timbers
# date: 2023-11-27

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn import set_config
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import fbeta_score, make_scorer

@click.command()
@click.option('--scaled-test-data', type=str, help="Path to scaled test data")
@click.option('--columns-to-drop', type=str, help="Optional: columns to drop")
@click.option('--pipeline-from', type=str, help="Path to directory where the fit pipeline object lives")
@click.option('--results-to', type=str, help="Path to directory where the plot will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)

def main(scaled_test_data, columns_to_drop, pipeline_from, results_to, seed):
    '''Evaluates the breast cancer classifier on the test data 
    and saves the evaluation results.'''
    np.random.seed(seed)
    set_config(transform_output="pandas")

    # read in data & cancer_fit (pipeline object)
    cancer_test = pd.read_csv(scaled_test_data)
    if columns_to_drop:
        to_drop = pd.read_csv(columns_to_drop).feats_to_drop.tolist()
        cancer_test = cancer_test.drop(columns=to_drop)
    with open(pipeline_from, 'rb') as f:
        cancer_fit = pickle.load(f)

    # Compute accuracy
    accuracy = cancer_fit.score(
        cancer_test.drop(columns=["class"]),
        cancer_test["class"]
    )

    # Compute F2 score (beta = 2)
    cancer_preds = cancer_test.assign(
        predicted=cancer_fit.predict(cancer_test)
    )
    f2_beta_2_score = fbeta_score(
        cancer_preds['class'],
        cancer_preds['predicted'],
        beta=2,
        pos_label='Malignant'
    )

    test_scores = pd.DataFrame({'accuracy': [accuracy], 'F2 score (beta = 2)': [f2_beta_2_score]})
    test_scores.to_csv(os.path.join(results_to, "test_scores.csv"), index=False)

    confusion_matrix = pd.crosstab(
        cancer_preds["class"],
        cancer_preds["predicted"],
    )
    confusion_matrix.to_csv(os.path.join(results_to, "confusion_matrix.csv"), index=False)

if __name__ == '__main__':
    main()