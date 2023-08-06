from scipy.sparse import csr_matrix
from sklearn.base import BaseEstimator, TransformerMixin


class NullVariableTransformer(BaseEstimator, TransformerMixin):
    # Null data transformer

    def __init__(self, subject, user, rating_variable):
        self.subject = subject
        self.user = user
        self.rating_variable = rating_variable

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        # so that we do not over-write the original dataframe
        X = X.copy()
        X = X.drop_duplicates([self.user, self.subject])
        X = X.dropna(axis=0, subset=self.subject)

        return X


class AddVariableTransformer(BaseEstimator, TransformerMixin):
    # add additional data for data limit transformer

    def __init__(self, subject, user, rating_variable, new_feature):
        self.subject = subject
        self.user = user
        self.rating_variable = rating_variable
        self.new_feature = new_feature

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        # so that we do not over-write the original dataframe
        X = X.copy()

        X_additional = (
            X.groupby(by=[self.subject])[self.rating_variable]
            .count()
            .reset_index()
            .rename(columns={self.rating_variable: self.new_feature})[[self.subject, self.new_feature]]
        )

        X_last = X.merge(X_additional, left_on=self.subject, right_on=self.subject, how="left")

        return X_last


class RestrictVariablesTransformer(BaseEstimator, TransformerMixin):
    # limit data according to threshold data transformer

    def __init__(self, location, popularity_threshold, new_feature, specific_location):
        self.location = location
        self.popularity_threshold = popularity_threshold
        self.new_feature = new_feature
        self.specific_location = specific_location

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        # so that we do not over-write the original dataframe
        X = X.copy()
        X = X[X[self.new_feature] >= self.popularity_threshold]
        X = X[X[self.location].str.contains(self.specific_location)]
        return X


class PrepareVariablesTransformer(BaseEstimator, TransformerMixin):
    # prepare data for knn transformer

    def __init__(self, subject, user, rating_variable):
        self.subject = subject
        self.user = user
        self.rating_variable = rating_variable
        self.X_pivot = None

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        # so that we do not over-write the original dataframe
        X = X.copy()
        self.X_pivot = X.pivot(index=self.subject, columns=self.user, values=self.rating_variable).fillna(0)
        X_matrix = csr_matrix(self.X_pivot.values)
        return X_matrix

    def get_prepared_data(self):
        return self.X_pivot
