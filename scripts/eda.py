# eda.py
# author: Tiffany Timbers
# date: 2023-11-27

import click
import os
import altair as alt
import numpy as np
import pandas as pd

@click.command()
@click.option('--processed-training-data', type=str, help="Path to processed training data")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")

def main(processed_training_data, plot_to):
    '''Plots the densities of each feature in the processed training data
        by class and displays them as a grid of plots. Also saves the plot.'''

    scaled_cancer_train = pd.read_csv(processed_training_data)

    # melt for plotting via facets 
    cancer_train_melted = scaled_cancer_train.melt(
        id_vars=['class'],
        var_name='predictor',
        value_name='value'
    )

    # make columns names nicer for plotting
    cancer_train_melted['predictor'] = cancer_train_melted['predictor'].str.replace('_',' ')

    # exploratory data analysis - visualize predictor distributions across classes
    plot = alt.Chart(cancer_train_melted, width=150, height=100).transform_density(
        'value',
        groupby=['class', 'predictor']
    ).mark_area(opacity=0.7).encode(
        x="value:Q",
        y=alt.Y('density:Q').stack(False),
        color='class:N'
    ).facet(
        'predictor:N',
        columns=4
    ).resolve_scale(
        y='independent'
    )

    plot.save(os.path.join(plot_to, "feature_densities_by_class.png"),
              scale_factor=2.0)

if __name__ == '__main__':
    main()