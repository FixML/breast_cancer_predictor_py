# Breast Cancer Predictor

  - author: Tiffany Timbers, Melissa Lee & Joel Ostblom

Demo of a data analysis project for DSCI 522 (Data Science workflows); a
course in the Master of Data Science program at the University of
British Columbia.

## About

Here we attempt to build a classification model using the k-nearest 
neighbours algorithm which can use breast cancer tumour image 
measurements to predict whether a newly discovered breast cancer tumour 
is benign (i.e., is not harmful and does not require treatment) or 
malignant (i.e., is harmful and requires treatment intervention). 
Our final classifier performed fairly well on an unseen test data set, 
with Fbeta score, where beta = 2, of 0.98 
and an overall accuracy calculated to be 0.96. On the 171 test data cases, 
it correctly predicted 168. 
It incorrectly predicted 3 cases, 
however these were false positives - predicting that a tumour is malignant 
when in fact it is benign. 
These kind of incorrect predictions could cause the patient 
to undergo unnecessary treatment, 
and as such we recommend further research to improve the model 
before it is ready to be put into production in the clinic.


The data set that was used in this project is of digitized breast cancer
image features created by Dr. William H. Wolberg, W. Nick Street, and
Olvi L. Mangasarian at the University of Wisconsin, Madison (Street,
Wolberg, and Mangasarian 1993). It was sourced from the UCI Machine
Learning Repository (Dua and Graff 2017) and can be found
[here](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+\(Diagnostic\)),
specifically [this
file](http://mlr.cs.umass.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data).
Each row in the data set represents summary statistics from measurements
of an image of a tumour sample, including the diagnosis (benign or
malignant) and several other measurements (e.g., nucleus texture,
perimeter, area, etc.). Diagnosis for each image was conducted by
physicians.

## Report

The final report can be found
[here](https://ttimbers.github.io/breast_cancer_predictor_py/src/breast_cancer_predictor_report.html).

## Usage

First time running the project,
run the following from the root of this repository:

``` bash
conda env create --file environment.yml
```

To run the analysis,
run the following from the root of this repository:

``` bash
jupyter lab 
```

Open `src/breast_cancer_predict_report.ipynb` in Jupyter Lab
and under Switch/Select Kernel choose 
"Python [conda env:breast_cancer_predictor]".

Next, under the "Kernel" menu click "Restart Kernel and Run All Cells...".

## Dependencies

- `conda` (version 23.9.0 or higher)
- `nb_conda_kernels` (version 2.3.1 or higher)
- Python and packages listed in [`environment.yml`](environment.yml)

## License

The Breast Cancer Predictor report contained herein are licensed under the
[Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
See [the license file](LICENSE.md) for more information. . If
re-using/re-mixing please provide attribution and link to this webpage.
The software code contained within this repository is licensed under the
MIT license. See [the license file](LICENSE.md) for more information.

## References

<div id="refs" class="references hanging-indent">

<div id="ref-Dua2019">

Dua, Dheeru, and Casey Graff. 2017. “UCI Machine Learning Repository.”
University of California, Irvine, School of Information; Computer
Sciences. <http://archive.ics.uci.edu/ml>.

</div>

<div id="ref-Streetetal">

Street, W. Nick, W. H. Wolberg, and O. L. Mangasarian. 1993. “Nuclear
feature extraction for breast tumor diagnosis.” In *Biomedical Image
Processing and Biomedical Visualization*, edited by Raj S. Acharya and
Dmitry B. Goldgof, 1905:861–70. International Society for Optics;
Photonics; SPIE. <https://doi.org/10.1117/12.148698>.

</div>

</div>
