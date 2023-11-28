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

## Dependencies

- [Docker](https://www.docker.com/) is a container solution 
used to manage the software dependencies for this project.
The Docker image used for this project is based on the
`quay.io/jupyter/minimal-notebook:notebook-7.0.6` image.
Additioanal dependencies are specified int the [`Dockerfile`](Dockerfile).

## Usage

#### Setup

1. [Install](https://www.docker.com/get-started/) 
and launch Docker on your computer.

2. Clone this GitHub repository.

#### Running the analysis

1. Navigate to the root of this project on your computer using the
   command line and enter the following command:

``` 
docker compose up
```

2. In the terminal, look for a URL that starts with 
`http://127.0.0.1:8888/lab?token=` 
(for an example, see the highlighted text in the terminal below). 
Copy and paste that URL into your browser.

<img src="img/jupyter-container-web-app-launch-url.png" width=400>

3. To run the analysis,
enter the following commands in the terminal in the project root:

```
# download and extract data
python scripts/download_data.py --url="https://archive.ics.uci.edu/static/public/15/breast+cancer+wisconsin+original.zip" \
   --write-to="data/raw"

# split data into train and test sets, preprocess data for eda 
# and save preprocessor
python scripts/split_n_preprocess.py --raw-data=data/raw/wdbc.data \
   --data-to=data/processed \
   --preprocessor-to=results/models \
   --seed=522

# perform eda and save plots

# train model, create visualize tuning, and save plot and model
python scripts/fit_breast_cancer_classifier.py --training-data=data/processed/cancer_train.csv \
   --preprocessor=results/models/cancer_preprocessor.pickle \
   --columns-to-drop=data/processed/columns_to_drop.csv \
   --pipeline-to=results/models \
   --plot-to=results/figures \
   --seed=523
```

#### Clean up

1. To shut down the container and clean up the resources, 
type `Cntrl` + `C` in the terminal
where you launched the container, and then type `docker compose rm`

## Developer notes

#### Adding a new dependency

1. Add the dependency to the `Dockerfile` file on a new branch.

2. Re-build the Docker image locally to ensure it builds and runs properly.

3. Push the changes to GitHub. A new Docker
   image will be built and pushed to Docker Hub automatically.
   It will be tagged with the SHA for the commit that changed the file.

4. Update the `docker-compose.yml` file on your branch to use the new
   container image (make sure to update the tag specifically).

5. Send a pull request to merge the changes into the `main` branch. 

#### Running the tests
Tests are run using the `pytest` command in the root of the project.
More details about the test suite can be found in the 
[`tests`](tests) directory.

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
