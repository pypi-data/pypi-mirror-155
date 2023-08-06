from feature_engine.selection import DropFeatures
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline

from bookRecommender import config
from bookRecommender.processing import features

book_pipe = Pipeline(
    [
        ("drop_features", DropFeatures(features_to_drop=config.model_config.features_to_drop)),
        (
            "null_variable",
            features.NullVariableTransformer(
                config.model_config.subject, config.model_config.user, config.model_config.rating_variable
            ),
        ),
        (
            "add_variable",
            features.AddVariableTransformer(
                config.model_config.subject,
                config.model_config.user,
                config.model_config.rating_variable,
                config.model_config.new_feature,
            ),
        ),
        (
            "restrict_variable",
            features.RestrictVariablesTransformer(
                config.model_config.location,
                config.model_config.popularity_threshold,
                config.model_config.new_feature,
                config.model_config.specific_location,
            ),
        ),
        (
            "prepare",
            features.PrepareVariablesTransformer(
                config.model_config.subject, config.model_config.user, config.model_config.rating_variable
            ),
        ),
        ("knn", NearestNeighbors(metric=config.model_config.knn_metric, algorithm=config.model_config.knn_algorithm)),
    ]
)
