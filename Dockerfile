# Use Jupyter's minimal-notebook as base image
FROM quay.io/jupyter/minimal-notebook:notebook-7.0.6

# install necessary packages for analysis
RUN conda install -y \
    python=3.11.7 \
    altair=5.4.1 \
    pandas=1.5.3 \
    ipykernel=6.29.5  \
    scikit-learn=1.5.2 \
    requests=2.32.3 \
    notebook=7.0.8 \
    pytest=8.3.3 \
    responses=0.25.3 \
    click=8.1.7 \
    vl-convert-python=1.7.0 \
    jupyter-book=1.0.3 \
    make 
RUN pip install great-expectations==1.1.3
