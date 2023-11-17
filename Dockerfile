FROM quay.io/jupyter/minimal-notebook:notebook-7.0.6

COPY environment.yml .
RUN mamba env update --file environment.yml
