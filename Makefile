all: report/_build/html/index.html

# download and extract data
data/raw/wdbc.data : scripts/download_data.py
	python scripts/download_data.py \
		--url="https://archive.ics.uci.edu/static/public/15/breast+cancer+wisconsin+original.zip" \
		--write-to=data/raw

# split data into train and test sets, preprocess data for eda 
# and save preprocessor
results/models/cancer_preprocessor.pickle data/processed/cancer_train.csv data/processed/cancer_test.csv data/processed/scaled_cancer_train.csv data/processed/scaled_cancer_train.csv : scripts/split_n_preprocess.py data/raw/wdbc.data
	python scripts/split_n_preprocess.py \
		--raw-data=data/raw/wdbc.data \
		--data-to=data/processed \
		--preprocessor-to=results/models \
		--seed=522

# perform eda and save plots
results/figures/feature_densities_by_class.png : scripts/eda.py data/processed/scaled_cancer_train.csv
	python scripts/eda.py \
		--processed-training-data=data/processed/scaled_cancer_train.csv \
		--plot-to=results/figures

# train model, create visualize tuning, and save plot and model
results/models/cancer_pipeline.pickle results/figures/cancer_choose_k.png : scripts/fit_breast_cancer_classifier.py \
data/processed/cancer_train.csv \
results/models/cancer_preprocessor.pickle \
data/processed/columns_to_drop.csv
	python scripts/fit_breast_cancer_classifier.py \
		--training-data=data/processed/cancer_train.csv \
		--preprocessor=results/models/cancer_preprocessor.pickle \
		--columns-to-drop=data/processed/columns_to_drop.csv \
		--pipeline-to=results/models \
		--plot-to=results/figures \
		--seed=523

# evaluate model on test data and save results
results/tables/test_scores.csv results/tables/confusion_matrix.csv : scripts/evaluate_breast_cancer_predictor.py \
data/processed/cancer_test.csv \
results/models/cancer_pipeline.pickle
	python scripts/evaluate_breast_cancer_predictor.py \
		--scaled-test-data=data/processed/cancer_test.csv \
		--pipeline-from=results/models/cancer_pipeline.pickle \
		--results-to=results/tables \
		--seed=524

# build HTML report and copy build to docs folder
report/_build/html/index.html : report/breast_cancer_predictor_report.ipynb \
report/references.bib \
report/_toc.yml \
report/_config.yml \
results/models/cancer_pipeline.pickle \
results/figures/feature_densities_by_class.png \
results/figures/feature_densities_by_class.png \
results/tables/test_scores.csv \
results/tables/confusion_matrix.csv
	jupyter-book build report
	cp -r report/_build/html/* docs
	if [ ! -f ".nojekyll" ]; then touch docs/.nojekyll; fi

# clean up analysis
clean :
	rm -rf data/raw/*
	rm -r results/models/cancer_preprocessor.pickle \
		data/processed/cancer_train.csv \
		data/processed/cancer_test.csv \
		data/processed/scaled_cancer_train.csv \
		data/processed/scaled_cancer_test.csv \
	rm -f results/models/cancer_preprocessor.pickle \
		data/processed/cancer_train.csv \
		data/processed/cancer_test.csv \
		data/processed/scaled_cancer_train.csv \
		data/processed/scaled_cancer_train.csv
	rm -f results/figures/feature_densities_by_class.png
	rm -f results/models/cancer_pipeline.pickle \
		results/figures/cancer_choose_k.png
	rm -f results/tables/test_scores.csv \
		results/tables/confusion_matrix.csv
	rm -rf report/_build \
		docs/*
