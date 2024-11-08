import os
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector

def create_save_preprocessor(train_data, test_data, data_to, preprocessor_to):
    cancer_preprocessor = make_column_transformer(
        (StandardScaler(), make_column_selector(dtype_include='number')),
        remainder='passthrough',
        verbose_feature_names_out=False
    )

    pickle.dump(cancer_preprocessor, open(os.path.join(preprocessor_to, "cancer_preprocessor.pickle"), "wb"))

    cancer_preprocessor.fit(train_data)
    scaled_cancer_train = cancer_preprocessor.transform(train_data)
    scaled_cancer_test = cancer_preprocessor.transform(test_data)

    scaled_cancer_train.to_csv(os.path.join(data_to, "scaled_cancer_train.csv"), index=False)
    scaled_cancer_test.to_csv(os.path.join(data_to, "scaled_cancer_test.csv"), index=False)