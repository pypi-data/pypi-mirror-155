import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# This class transforms the experience column into a numerical value.
class TransformExperienceColumn(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_ = X.copy()
        X_['Experience'] = X_['Experience'].str.replace(',', '.').astype(float)
        return X_

# This class is used to extract individual technologies from the technologies column.
class CreateIndividualTechnologyColumns(BaseEstimator, TransformerMixin):
    def __init__(self, technologies):
        self.technologies = np.array(technologies)
    
    def set_individual_technology(self, row):
        row_technologies = np.array(list(filter(None, row['Technologies'].lower().strip().split('/'))))
        individual_technologies = np.isin(self.technologies, row_technologies).astype(int)
        return np.concatenate((row, individual_technologies))
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_ = X.copy()
        transformed_X = X_.apply(
            self.set_individual_technology,
            axis=1,
            result_type='expand'
        )
        transformed_X.columns = [*X_.columns, *self.technologies.tolist()]
        return transformed_X

# This class is used to extract predictors from the dataframe.
class DropNotSelectedColumns(BaseEstimator, TransformerMixin):
    def __init__(self, selected_features):
        self.selected_features = selected_features
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_ = X.copy()
        result = X_[self.selected_features]
        return result
