# fit_breast_cancer_classifier.py
# author: Tiffany Timbers
# date: 2023-11-27

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn import set_config
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector


@click.command()
@click.option('--training-data', type=str, help="Path to training data")
@click.option('--preprocessor', type=str, help="Path to preprocessor object")
@click.option('--columns-to-drop', type=str, help="Optional: columns to drop")
@click.option('--pipeline-to', type=str, help="Path to directory where the pipeline object will be written to")
@click.option('--plot-to', type=int, help="Path to directory where the plot will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)

def main(training_data, preprocessor, columns_to_drop, pipeline_to, plot_to, seed):
    '''Fits a breast cancer classifier to the training data 
    and saves the pipeline object.'''
    np.random.seed(seed)
    set_config(transform_output="pandas")

    # read in data & preprocessor
    cancer_train = pd.read_csv(training_data)
    pickle.load(open(preprocessor, "rb"))

    if columns_to_drop:
        to_drop = pd.read_csv(columns_to_drop).['feats_to_drop'].tolist()
        cancer_train = cancer_train.drop(columns=to_drop)

    # tune model (here, find K for k-nn using 30 fold cv)
    knn = KNeighborsClassifier()
    cancer_tune_pipe = make_pipeline(cancer_preprocessor, knn)

    parameter_grid = {
        "kneighborsclassifier__n_neighbors": range(1, 100, 3),
    }

    cv = 30
    cancer_tune_grid = GridSearchCV(
        estimator=cancer_tune_pipe,
        param_grid=parameter_grid,
        cv=cv,
        scoring=make_scorer(fbeta_score, pos_label='Malignant', beta=2)
    )

    cancer_fit = cancer_tune_grid.fit(
        cancer_train.drop(columns=["class"]),
        cancer_train["class"]
    )

    pickle.dump(cancer_fit, open(os.path.join(pipeline_to, "cancer_pipeline.pickle"), "wb"))

    accuracies_grid = pd.DataFrame(cancer_fit.cv_results_)

    accuracies_grid = (
        accuracies_grid[[
            "param_kneighborsclassifier__n_neighbors",
            "mean_test_score",
            "std_test_score"
        ]]
        .assign(
            sem_test_score=accuracies_grid["std_test_score"] / cv**(1/2),
            # `lambda` allows access to the chained dataframe so that we can use the newly created `sem_test_score` column 
            sem_test_score_lower=lambda df: df["mean_test_score"] - (df["sem_test_score"]/2),
            sem_test_score_upper=lambda df: df["mean_test_score"] + (df["sem_test_score"]/2)
        )
        .rename(columns={"param_kneighborsclassifier__n_neighbors": "n_neighbors"})
        .drop(columns=["std_test_score"])
    )

    line_n_point = alt.Chart(accuracies_grid, width=600).mark_line(color="black").encode(
        x=alt.X("n_neighbors").title("Neighbors"),
        y=alt.Y("mean_test_score")
            .scale(zero=False) 
            .title("F2 score (beta = 2)")
    )

    error_bar = alt.Chart(accuracies_grid).mark_errorbar().encode(
        alt.Y("sem_test_score_upper:Q").scale(zero=False).title("F2 score (beta = 2)"),
        alt.Y2("sem_test_score_lower:Q"),
        alt.X("n_neighbors:Q").title("Neighbors")
    )

    plot = line_n_point + line_n_point.mark_circle(color='black') + error_bar
    plot.save(os.path.join(plot_to, "cancer_choose_k.png"))

if __name__ == '__main__':
    main()